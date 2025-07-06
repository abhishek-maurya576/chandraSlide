import os
from ultralytics import YOLO
from PIL import Image

def run_inference(model_path, image_path, output_dir='runs/inference'):
    """
    Runs YOLOv8 inference on a single image and saves the result.

    Args:
        model_path (str): Path to the trained .pt model file.
        image_path (str): Path to the input image.
        output_dir (str): Directory to save the output image with detections.
    """
    print(f"--- Running Inference ---")
    print(f"Model: {model_path}")
    print(f"Image: {image_path}")

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Load the trained YOLOv8 model
    try:
        model = YOLO(model_path)
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    # Run inference on the image
    results = model(image_path)

    # The results object contains all information.
    # We can access bounding boxes, masks, confidences, etc.
    # For now, we will just save the plotted image.
    
    # Plot the results on the image
    # The plot() method returns a BGR numpy array
    annotated_image_array = results[0].plot()

    # Convert the BGR numpy array to an RGB image
    annotated_image = Image.fromarray(annotated_image_array[..., ::-1])  # BGR to RGB

    # Save the annotated image
    base_filename = os.path.basename(image_path)
    output_path = os.path.join(output_dir, base_filename)
    annotated_image.save(output_path)

    print(f"\nInference complete. Annotated image saved to: {output_path}")

if __name__ == '__main__':
    # Define the paths for the model and a sample test image
    MODEL_PATH = 'models/lunar_rockfall_detector.pt'
    
    # TODO: This should be replaced with a proper data loading mechanism
    TEST_IMAGE = 'data/raw/moon/test_images/neg1.tif' 

    run_inference(MODEL_PATH, TEST_IMAGE)
