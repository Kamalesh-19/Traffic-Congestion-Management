from ultralytics import YOLO
import torch

def start_training():
    # Load the pretrained Nano model (best for Fog Nodes)
    model = YOLO('models/yolov8n.pt') 

    # Begin Training
    model.train(
        data='traffic_config.yaml',
        epochs=50,
        imgsz=640,
        batch=8,          # Optimized for 4GB/6GB VRAM
        device=0,         # Force GPU usage
        workers=4,        # CPU threads for data loading
        project='runs/train',
        name='fog_traffic_model'
    )

if __name__ == "__main__":
    if torch.cuda.is_available():
        print(f"🚀 Found GPU: {torch.cuda.get_device_name(0)}")
        start_training()
    else:
        print("⚠️ GPU not found! Check your CUDA installation.")