# 🚦 Smart Traffic: Fog-Based Congestion Management System

An AI-driven traffic management system designed for high-density urban environments. This project leverages **Edge/Fog Computing** to perform real-time video analytics locally, reducing latency and minimizing cloud bandwidth usage.

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

Created by @kamalesh-19, @Aasis-Mohamed2208 © 2026
