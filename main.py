import streamlit as st
import cv2
import pyrebase
import time
import pandas as pd
import numpy as np
from ultralytics import YOLO
from datetime import datetime
import tempfile

# --- 1. FIREBASE CONFIG ---
firebase_config = {
    "apiKey": "AIzaSyA5hCM4d72S7VCPRNB4pDRBARsUPvNL2lo",
    "authDomain": "trafficcongestionproject.firebaseapp.com",
    "databaseURL": "https://trafficcongestionproject-default-rtdb.firebaseio.com",
    "projectId": "trafficcongestionproject",
    "storageBucket": "trafficcongestionproject.firebasestorage.app",
    "messagingSenderId": "974827440611",
    "appId": "1:974827440611:web:9d9505fac76b32c6fc38d6"
}
firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

# --- 2. THE INTELLIGENT CONTROLLER (Pre-emptive + Budgeting) ---
class DhakaTrafficBrain:
    def __init__(self):
        self.min_green = 15
        self.max_green = 60
        self.current_phase = "ROAD_A"
        self.allocated_time = 20
        self.start_time = time.time()
        self.needs_recalculation = True
        self.emergency_override = False

    def calculate_budget(self, density):
        # Intelligent Formula: Base + Proportion of Max
        return self.min_green + int((density / 100) * (self.max_green - self.min_green))

    def get_status(self, density, emergency):
        elapsed = time.time() - self.start_time
        
        # Immediate Switch for Emergency Vehicles
        if emergency and self.current_phase != "ROAD_A":
            self.emergency_override = True
            return self.trigger_switch("🚑 EMERGENCY PRE-EMPTION")

        if self.needs_recalculation:
            self.allocated_time = self.calculate_budget(density)
            self.needs_recalculation = False
            
        remaining = max(0, self.allocated_time - int(elapsed))

        if remaining <= 0:
            return self.trigger_switch("⏰ BUDGET EXPIRED")
        
        return self.current_phase, remaining

    def trigger_switch(self, reason):
        self.current_phase = "ROAD_B" if self.current_phase == "ROAD_A" else "ROAD_A"
        self.start_time = time.time()
        self.needs_recalculation = True
        st.toast(f"🔄 Signal Switch: {reason}")
        return self.current_phase, 0

# --- 3. PROCESSING ENGINE ---
def run_fog_node(video_path):
    model = YOLO(r'D:\finalyearproject\runs\detect\runs\train\fog_traffic_model\weights\best.pt')
    brain = DhakaTrafficBrain()
    cap = cv2.VideoCapture(video_path)
    
    # UI Layout: Main Video | Sidebar Stats
    col_vid, col_stats = st.columns([2, 1])
    frame_window = col_vid.empty()
    stats_window = col_stats.empty()
    
    # Persistent Session Data
    if 'history' not in st.session_state:
        st.session_state.history = pd.DataFrame(columns=["Time", "Density", "Phase", "Objects"])
    
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break

        frame_count += 1
        if frame_count % 3 != 0: continue

        results = model(frame, conf=0.28, verbose=False)
        labels = [results[0].names[int(c)] for c in results[0].boxes.cls.tolist()]
        
        # Advanced Object Analytics
        obj_counts = pd.Series(labels).value_counts().to_dict()
        emergency = any(x in ["ambulance", "fire truck"] for x in labels)
        
        # Weighted Scoring (Buses carry more weight in Dhaka)
        score = sum(15 if x in ["bus", "truck"] else 5 for x in labels)
        density = min(score, 100)
        
        active_lane, time_left = brain.get_status(density, emergency)
        
        # Cloud Sync
        timestamp = datetime.now().strftime("%H:%M:%S")
        payload = {"lane": active_lane, "density": density, "timer": time_left, "emergency": emergency}
        try: db.child("live_traffic").set(payload)
        except: pass

        # UI Visualization
        with stats_window.container():
            st.markdown(f"### 🚦 Phase: ` {active_lane} `")
            
            # BIG COUNTDOWN
            t_color = "#FF4B4B" if time_left < 5 else "#FFD700"
            st.markdown(f"<h1 style='text-align: center; color: {t_color}; font-size: 70px;'>{time_left}s</h1>", unsafe_allow_html=True)
            
            if emergency: st.error("🚨 EMERGENCY PRIORITY ACTIVE")
            
            st.divider()
            
            # Vehicle Breakdown Multi-metric
            m1, m2 = st.columns(2)
            m1.metric("Congestion", f"{density}%")
            m2.metric("Total Vehicles", len(labels))
            
            # Vehicle Type Breakdown
            if obj_counts:
                st.write("**Live Breakdown:**")
                st.caption(", ".join([f"{k}: {v}" for k, v in obj_counts.items()]))
            
            # Real-time Trend
            new_data = pd.DataFrame([[timestamp, density]], columns=["Time", "Density"])
            st.session_state.history = pd.concat([st.session_state.history, new_data]).tail(15)
            st.line_chart(st.session_state.history.set_index("Time")["Density"])

        frame_window.image(results[0].plot(), channels="BGR", use_container_width=True)

    cap.release()

# --- 4. ENHANCED DASHBOARD ---
st.set_page_config(page_title="AI Fog-Node Dashboard", layout="wide")

# Stylish Header
st.title("AI-Integrated Fog-Node")
st.markdown("---")

# System Health Row
h1, h2, h3, h4 = st.columns(4)
h1.info("**Node ID:** FOG-DHK-01")
h2.success("**Firebase:** Connected")
h3.warning("**Logic:** Predictive Actuated")
h4.error("**Priority:** Emergency Enabled")

uploaded_file = st.file_uploader("📂 Upload Traffic Feed (MP4)", type=["mp4"])
if uploaded_file:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    if st.button("🚀 DEPLOY TO EDGE NODE"):
        run_fog_node(tfile.name)