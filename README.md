🚦 Smart Traffic: Fog-Based Congestion Management System
An AI-driven traffic management system designed for high-density urban environments. This project utilizes Edge/Fog Computing to process real-time video analytics locally, significantly reducing latency and cloud bandwidth consumption.

🌟 Project Overview
Traditional traffic systems rely on fixed timers or centralized cloud processing, which are often inefficient for dynamic, high-volume urban traffic. This system implements a Fog Node architecture where vehicle detection and congestion logic happen at the intersection level.

Key Features
Real-time Vehicle Detection: Powered by YOLOv8 for high-accuracy object tracking and classification.

Fog Computing Architecture: Heavy video processing is handled locally; only processed metadata (Congestion Index) is synced to the cloud.

Adaptive Signal Logic: Dynamically calculates traffic light duration based on real-time vehicle density (e.g., triggering "Priority Green" at 90% congestion).

Spatial Filtering (ROI): Implements Region of Interest (ROI) masks to monitor specific lanes and ignore irrelevant background or opposite-lane traffic.

🏗️ System Architecture
The project follows a tiered architecture to ensure scalability and speed:

Perception Layer: IP Cameras capturing high-definition traffic streams.

Fog Node (Edge): Local processing unit (Python/YOLOv8) performing spatial filtering and vehicle counting.

Cloud Layer: Integration for logging traffic trends and system monitoring (e.g., Firebase/GitHub).

🛠️ Tech Stack
Language: Python 3.10+

AI Model: YOLOv8 (Ultralytics)

Frontend: Streamlit (Traffic Dashboard)

Database: Firebase Realtime Database (Cloud Sync)

Libraries: OpenCV, Git, NumPy, PyTorch

🚀 Installation & Setup
1. Clone the Repository
Bash
git clone https://github.com/Kamalesh-19/Traffic-Congestion-Management.git
cd Traffic-Congestion-Management
2. Set Up Virtual Environment
Bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/Mac:
source .venv/bin/activate
3. Install Dependencies
Bash
pip install -r requirement.txt
📊 Data Management Policy
Note on Dataset: To comply with Edge Computing best practices and repository storage limits, the Master Traffic Dataset is hosted locally at the Fog Node.

This repository contains the Inference Logic, Source Code, and Model Configurations.

To replicate results, place your traffic video files in the inputs/ directory.

🎯 Lane Detection & ROI
To ensure the system only monitors relevant traffic, we utilize a coordinate-based Region of Interest (ROI). This prevents the AI from double-counting vehicles in the opposite lane or background areas.

Python
# Example ROI Filtering Logic
if car_center_x < LANE_DIVIDER_THRESHOLD and car_center_y > HORIZON_LINE:
    count_as_congestion(vehicle)
📜 License
Distributed under the MIT License. See LICENSE for more information.
