import torch
import numpy as np
from PIL import Image
import os
import rasterio

# Import all the necessary components from our project structure
from src.models.unet import UNet
from src.models.yolov8 import run_boulder_inference
from src.data.preprocessing import align_and_fuse_data
from src.analysis.postprocessing import find_landslide_source, calculate_boulder_height_from_shadow

# --- Configuration ---
SEGMENTATION_MODEL_PATH = 'models/unet_landslide_detector.pth'
BOULDER_MODEL_PATH = 'yolov8n.pt' # Using a standard pretrained model for demo
NUM_CLASSES = 3
INPUT_CHANNELS = 3

def run_pipeline(ohrc_path, dtm_path):
    """
    Runs the full end-to-end inference pipeline.

    This function simulates the complete workflow:
    1. Preprocesses the input imagery.
    2. Runs the landslide segmentation model.
    3. Runs the boulder detection model (simulated).
    4. Performs post-processing analysis.

    Args:
        ohrc_path (str): Path to the high-resolution OHRC image.
        dtm_path (str): Path to the Digital Terrain Model.

    Returns:
        dict: A dictionary containing all the analysis results.
              Returns None if the pipeline fails.
    """
    print("--- Starting Full Inference Pipeline ---")
    
    try:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        # --- 1. Preprocessing (Real) ---
        print("Step 1: Fusing OHRC, DTM, and Slope data...")
        # This now calls the actual preprocessing function.
        fused_array = align_and_fuse_data(ohrc_path, dtm_path)
        
        if fused_array is None:
            raise RuntimeError("Data preprocessing and fusion failed.")
        
        # The fused data needs to be a tensor for the model.
        # It also needs a batch dimension.
        fused_tensor = torch.from_numpy(fused_array).float().unsqueeze(0).to(device)
        
        # We also need the DTM for analysis. We'll use the reprojected one from the fused data.
        # Fused array is [OHRC, DTM, Slope]. Channel 1 is the DTM.
        dtm_array = fused_array[1] 
        print("Data fusion complete.")

        # --- 2. Landslide Segmentation ---
        print("Step 2: Running Landslide Segmentation Model...")
        # The model input size should match the data from preprocessing.
        # Let's get the height and width from the fused tensor.
        _, _, height, width = fused_tensor.shape
        model = UNet(n_channels=INPUT_CHANNELS, n_classes=NUM_CLASSES).to(device)
        
        # Load the trained model weights if they exist, otherwise use the initialized model.
        if os.path.exists(SEGMENTATION_MODEL_PATH):
            model.load_state_dict(torch.load(SEGMENTATION_MODEL_PATH, map_location=device))
            print("Loaded trained model weights.")
        else:
            print("WARNING: Trained model weights not found. Using initialized model.")
        
        model.eval()
        with torch.no_grad():
            output_logits = model(fused_tensor)
            # Convert logits to a class prediction mask
            segmentation_mask = torch.argmax(output_logits, dim=1).squeeze(0).cpu().numpy()
        print("Segmentation complete.")

        # --- 3. Boulder Detection (Simulated) ---
        print("Step 3: Running Boulder Detection (Simulated)...")
        # Here we would call the run_boulder_inference function from yolov8.py.
        # For this demo, we'll just create some dummy boulder bounding boxes.
        detected_boulders = [
            {'bbox': (100, 120, 150, 170), 'confidence': 0.95},
            {'bbox': (300, 350, 340, 390), 'confidence': 0.88},
            {'bbox': (400, 100, 450, 150), 'confidence': 0.91},
        ]
        print(f"Detected {len(detected_boulders)} boulders.")

        # --- 4. Post-processing Analysis ---
        print("Step 4: Performing Post-processing Analysis...")
        # Separate the landslide mask for analysis
        landslide_only_mask = (segmentation_mask == 1).astype(np.uint8)
        
        # Find landslide source
        landslide_source = find_landslide_source(landslide_only_mask, dtm_array)

        # Analyze each boulder
        boulder_analysis_results = []
        for i, boulder in enumerate(detected_boulders):
            # Simulate shadow measurement and height calculation
            shadow_len = np.random.uniform(5, 20) # Dummy shadow length in pixels
            sun_angle = 30.0 # From metadata
            est_height = calculate_boulder_height_from_shadow(boulder['bbox'], shadow_len, sun_angle)
            boulder_analysis_results.append({
                'id': i + 1,
                'bbox': boulder['bbox'],
                'height_m': round(est_height * 0.25, 2) # Assume 0.25 m/pixel scale
            })
        print("Analysis complete.")

        # --- 5. Compile Results ---
        results = {
            'segmentation_mask': segmentation_mask,
            'landslide_source': landslide_source,
            'boulders': boulder_analysis_results,
            'landslide_pixel_count': np.sum(landslide_only_mask)
        }
        
        print("--- Inference Pipeline Finished Successfully ---")
        return results

    except Exception as e:
        print(f"An error occurred in the pipeline: {e}")
        return None

if __name__ == '__main__':
    # This block demonstrates how to run the full pipeline.
    # It now uses dummy file creation that the REAL preprocessing function can use.
    
    # Create dummy GeoTIFF files that rasterio can actually open
    ohrc_transform = rasterio.transform.from_origin(0, 512, 1, 1)
    dtm_transform = rasterio.transform.from_origin(0, 512, 0.5, 0.5) # Different resolution
    crs = 'EPSG:32610' # A sample projected CRS

    with rasterio.open('dummy_ohrc.tif', 'w', driver='GTiff', height=512, width=512, count=1, dtype=np.uint8, crs=crs, transform=ohrc_transform) as dst:
        dst.write(np.random.randint(0, 255, (512, 512), dtype=np.uint8), 1)

    with rasterio.open('dummy_dtm.tif', 'w', driver='GTiff', height=1024, width=1024, count=1, dtype=np.float32, crs=crs, transform=dtm_transform) as dst:
        dst.write(np.random.rand(1024, 1024).astype(np.float32) * 1000, 1)

    pipeline_results = run_pipeline('dummy_ohrc.tif', 'dummy_dtm.tif')

    if pipeline_results:
        print("\n--- Pipeline Output Summary ---")
        print(f"Segmentation mask shape: {pipeline_results['segmentation_mask'].shape}")
        print(f"Detected {len(pipeline_results['boulders'])} boulders.")
        print(f"Estimated landslide source: {pipeline_results['landslide_source']}")
        print(f"Total landslide area: {pipeline_results['landslide_pixel_count']} pixels")
        print("Boulder 1 details:", pipeline_results['boulders'][0])
        
    # Clean up dummy files
    os.remove('dummy_ohrc.tif')
    os.remove('dummy_dtm.tif')
