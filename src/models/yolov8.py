from ultralytics import YOLO

def train_yolo_model(dataset_yaml_path, epochs=50, batch_size=16, model_name='yolov8n.pt'):
    """
    Trains a YOLOv8 model on a custom dataset.
    """
    print("--- Starting YOLOv8 Training ---")
    
    # Load a pretrained YOLOv8 model
    model = YOLO(model_name)
    
    print(f"Loaded model: {model_name}")
    print(f"Training for {epochs} epochs with a batch size of {batch_size}.")
    
    # Train the model
    results = model.train(
        data=dataset_yaml_path,
        epochs=epochs,
        batch=batch_size,
        imgsz=640,
        project='runs/train', # Save results to 'runs/train' directory
        name='yolo_lunar_detector', # Subdirectory name for this run
        # Disable augmentations that caused issues in Colab
        mosaic=0.0,
        mixup=0.0,
        copy_paste=0.0
    )
    
    print("--- YOLOv8 Training Finished ---")
    print(f"Model and results saved to: {results.save_dir}")

if __name__ == '__main__':
    DATASET_CONFIG = 'data/yolo_moon_dataset/dataset.yaml'
    train_yolo_model(DATASET_CONFIG)


