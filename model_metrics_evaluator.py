import os
from ultralytics import YOLO

# --- CONFIGURATION ---
# Use 'os.path.abspath' to ensure Windows finds the file correctly
MODEL_PATH = r'D:\finalyearproject\runs\detect\runs\train\fog_traffic_model\weights\best.pt'
YAML_PATH = os.path.abspath(r'D:\finalyearproject\traffic_config.yaml') # Change name if yours is data.yaml

def print_evaluation_scores():
    print(f"🚀 Checking YAML path: {YAML_PATH}")
    
    if not os.path.exists(YAML_PATH):
        print(f"❌ ERROR: YAML file not found at {YAML_PATH}")
        print("Please check your folder D:\\finalyearproject\\ for the correct file name.")
        return

    print("📊 Loading model for evaluation...")
    model = YOLO(MODEL_PATH)

    # Run validation
    # Using the absolute path 'YAML_PATH' here
    metrics = model.val(data=YAML_PATH, imgsz=1024, split='val', verbose=True)

    # Printing Results
    print("\n" + "="*30)
    print(f"mAP@50:      {metrics.results_dict['metrics/mAP50(B)']:.4f}")
    print(f"Precision:   {metrics.results_dict['metrics/precision(B)']:.4f}")
    print(f"Recall:      {metrics.results_dict['metrics/recall(B)']:.4f}")
    print("="*30)

if __name__ == "__main__":
    print_evaluation_scores()