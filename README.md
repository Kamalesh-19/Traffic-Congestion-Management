# 🚦 Smart Traffic: Fog-Based Congestion Management System

An AI-driven traffic management system designed for high-density urban environments. This project leverages **Edge/Fog Computing** to perform real-time video analytics locally, reducing latency and minimizing cloud bandwidth usage.

---

## 🌟 Project Overview

Traditional traffic systems rely on fixed timers or centralized cloud processing, which are inefficient for dynamic, high-volume urban traffic.

This project introduces a **Fog Node-based architecture**, where:
- Vehicle detection happens locally at intersections
- Only processed data is sent to the cloud
- Traffic signals adapt in real time

---

## ✨ Key Features

### 🚗 Real-Time Vehicle Detection
- Powered by **YOLOv8 (Ultralytics)**
- High-accuracy object detection and classification

### 🌐 Fog Computing Architecture
- Video processing handled locally at edge nodes
- Only metadata (e.g., Congestion Index) synced to cloud
- Reduces latency and bandwidth usage

### 🚦 Adaptive Signal Logic
- Dynamically adjusts traffic light duration
- Example: Triggers **Priority Green** at 90% congestion

### 🎯 Spatial Filtering (ROI)
- Uses Region of Interest (ROI) masks
- Monitors specific lanes only
- Eliminates noise from background/opposite lanes

---

## 🏗️ System Architecture

The system follows a **three-tier architecture**:

### 1. Perception Layer
- IP Cameras capture live traffic feeds

### 2. Fog Node (Edge Layer)
- Local processing using Python + YOLOv8
- Performs:
  - Vehicle detection
  - ROI filtering
  - Congestion estimation

### 3. Cloud Layer
- Stores traffic data and analytics
- Enables remote monitoring
- Tools: Firebase / GitHub

---

## 🛠️ Tech Stack

| Category       | Technology |
|---------------|-----------|
| Language      | Python 3.10+ |
| AI Model      | YOLOv8 (Ultralytics) |
| Frontend      | Streamlit |
| Database      | Firebase Realtime Database |
| Libraries     | OpenCV, NumPy, PyTorch, Git |

---

## 🚀 Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Kamalesh-19/Traffic-Congestion-Management.git
cd Traffic-Congestion-Management
```

---


### 2️⃣ Set Up Virtual Environment

```bash
python -m venv .venv

# On Windows
.venv\Scripts\activate

# On Linux / Mac
source .venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 📊 Data Management Policy

### ⚠️ Dataset Note

The master traffic dataset is **not included** in this repository.

It is stored locally at the **Fog Node** to:

* Reduce repository size
* Follow edge computing principles

---

## 📁 To Run the Project

Place your traffic videos inside:

```bash
inputs/
```

---

## 🎯 Lane Detection & ROI

To avoid incorrect vehicle counts, the system uses **coordinate-based filtering**:

```python
# Example ROI Filtering Logic
if car_center_x < LANE_DIVIDER_THRESHOLD and car_center_y > HORIZON_LINE:
    count_as_congestion(vehicle)
```

### ✅ Benefits

* Prevents double counting
* Ignores irrelevant regions
* Improves accuracy

---

## 📊 Output Metrics

* 🚗 Vehicle Count
* 📏 Lane-wise Density
* 🚦 Congestion Index
* ⏱️ Signal Timing Decisions

---

## 🔮 Future Enhancements

* Multi-intersection coordination
* Emergency vehicle prioritization
* Integration with smart city infrastructure
* AI-based traffic prediction models

---

## 📜 License

This project is licensed under the **MIT License**.
See the `LICENSE` file for details.

---

## 👨‍💻 Author

**Kamalesh**
GitHub: https://github.com/Kamalesh-19

---

## ⭐ Support

If you find this project useful:

* ⭐ Star the repository
* 🍴 Fork it
* 🛠️ Contribute improvements
