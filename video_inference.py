import cv2
import os
import json
import numpy as np
from datetime import datetime
from ultralytics import YOLO

# --- CONFIGURATION ---
MODEL_PATH = r'D:\finalyearproject\runs\detect\runs\train\fog_traffic_model\weights\best.pt'
VIDEO_PATH = r"D:\finalyearproject\inputs\Dhaka Bangladesh _Dhaka _dhakacity _Bangladesh _traffic _trafficjam _shorts(720P_HD).mp4"
OUTPUT_DIR = r'D:\finalyearproject\output'
LOG_FILE = os.path.join(OUTPUT_DIR, "video_fog_sync.json")

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def process_traffic_video():
    # 1. Load Model
    if not os.path.exists(MODEL_PATH):
        print(f"❌ Error: Model not found at {MODEL_PATH}")
        return
    
    # FIX: Use 'model' directly, not 'self.model'
    model = YOLO(MODEL_PATH)

    # 2. Open Video
    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        print(f"❌ Error: Could not open video at {VIDEO_PATH}")
        return

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    output_video_path = os.path.join(OUTPUT_DIR, "processed_traffic.avi")
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    print(f"🎬 Fog Node Processing started...")
    frame_count = 0

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Process every 5th or 10th frame for efficiency
            if frame_count % 5 == 0:
                # FIX: Removed 'self.' and kept your optimized confidence settings
                results = model(frame, conf=0.20, iou=0.45, augment=True, verbose=False)
                
                # Dynamic Traffic Logic
                detections = results[0].boxes.cls.tolist()
                
                # Weighting: Bus/Truck (10), Car/Motorcycle (5), Others (2)
                score = sum(10 if cid in [3, 5] else 5 if cid in [1, 2] else 2 for cid in detections)
                score = min(score, 100)
                green_time = int(15 + (score / 100) * 45)

                # Fog Logging (Cloud Sync Simulation)
                packet = {
                    "timestamp": datetime.now().isoformat(), 
                    "congestion": int(score), 
                    "green_time": green_time,
                    "vehicle_count": len(detections)
                }
                with open(LOG_FILE, "a") as f:
                    f.write(json.dumps(packet) + "\n")

                # Visuals
                annotated_frame = results[0].plot()
                cv2.putText(annotated_frame, f"FOG NODE: {score}% Density | {green_time}s Green", 
                            (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                
                out.write(annotated_frame)
                cv2.imshow("Smart Traffic Fog Node", annotated_frame)
            
            frame_count += 1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    except Exception as e:
        print(f"❌ An error occurred: {e}")
    finally:
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        
        # --- PROJECT COMPARISON REPORT ---
        raw_video_size = os.path.getsize(VIDEO_PATH) / (1024 * 1024) # MB
        log_file_size = os.path.getsize(LOG_FILE) / (1024 * 1024)   # MB
        savings = ((raw_video_size - log_file_size) / raw_video_size) * 100

        print("\n" + "="*40)
        print("📊 FOG VS CLOUD EFFICIENCY REPORT")
        print("="*40)
        print(f"Cloud Storage Needed (Raw Video): {raw_video_size:.2f} MB")
        print(f"Fog Storage Needed (JSON Logs):  {log_file_size:.4f} MB")
        print(f"Bandwidth/Storage Saved:        {savings:.2f}%")
        print("="*40)
        print(f"✅ Output Saved: {OUTPUT_DIR}")

if __name__ == "__main__":
    process_traffic_video()