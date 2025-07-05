import os
import rasterio
import numpy as np
from PIL import Image

def tile_geospatial_data(image_path, mask_path, output_dir_images, output_dir_masks, tile_size=(512, 512), overlap=0.2):
    """
    Tiles a large multi-channel geospatial image and its corresponding mask
    into smaller, overlapping patches suitable for deep learning.
    Image tiles are saved as .npy files to preserve all channels and data types.
    """
    print(f"Tiling {image_path} and {mask_path}...")
    os.makedirs(output_dir_images, exist_ok=True)
    os.makedirs(output_dir_masks, exist_ok=True)
    
    tile_w, tile_h = tile_size
    stride = int(tile_w * (1 - overlap))
    
    with rasterio.open(image_path) as src_image, rasterio.open(mask_path) as src_mask:
        
        if src_image.height != src_mask.height or src_image.width != src_mask.width:
            raise ValueError("Source image and mask must have the exact same dimensions.")
            
        width, height = src_image.width, src_image.height
        
        tile_count = 0
        for y in range(0, height, stride):
            for x in range(0, width, stride):
                window = rasterio.windows.Window(x, y, tile_w, tile_h)
                
                # Read all bands from the source image
                # The result is (bands, height, width)
                img_tile = src_image.read(window=window)
                mask_tile = src_mask.read(1, window=window)
                
                # Skip tiles that are too small (at the edges)
                if img_tile.shape[1] != tile_h or img_tile.shape[2] != tile_w:
                    continue
                
                # Skip tiles that are mostly empty
                if np.mean(img_tile[0]) < 5: # Check first channel for darkness
                    continue
                    
                filename = f"{os.path.splitext(os.path.basename(image_path))[0]}_tile_{tile_count}"
                
                # Save the image tile as a numpy array to preserve multi-channel float data
                np.save(os.path.join(output_dir_images, f"{filename}.npy"), img_tile)
                
                # Save the mask tile as a standard PNG
                Image.fromarray(mask_tile).save(os.path.join(output_dir_masks, f"{filename}.png"))
                
                tile_count += 1
                
    print(f"Tiling complete. Generated {tile_count} tiles.")

if __name__ == '__main__':
    # This script is intended to be run to prepare the *actual* training data.
    
    # --- Configuration for Real Lunar Data ---
    # We need to define the paths to our actual large-format lunar images and masks.
    # This is a placeholder and needs to be adapted based on where the raw,
    # fused GeoTIFFs are stored.
    SOURCE_IMAGE_DIR = 'data/raw/images'  # e.g., where fused_ortho_1.tif is
    SOURCE_MASK_DIR = 'data/raw/masks'   # e.g., where fused_mask_1.tif is

    # Output directories are where the training script will look for the data.
    OUTPUT_IMAGE_DIR = 'data/processed/segmentation'
    OUTPUT_MASK_DIR = 'data/labeled/segmentation'

    print("--- Starting Data Preparation for Lunar Surface Analysis ---")
    
    # Example of how you would run this for a single pair of files.
    # In a real pipeline, you would loop over all files in the source directories.
    try:
        # This is an example for one file. You'll need to adapt this to your file structure.
        image_files = os.listdir(SOURCE_IMAGE_DIR)
        mask_files = os.listdir(SOURCE_MASK_DIR)

        if not image_files or not mask_files:
            raise FileNotFoundError("Source directories are empty.")

        # Process each image-mask pair
        for img_name in image_files:
            mask_name = img_name.replace('image', 'mask') # Example logic
            if mask_name in mask_files:
                image_path = os.path.join(SOURCE_IMAGE_DIR, img_name)
                mask_path = os.path.join(SOURCE_MASK_DIR, mask_name)
                
                tile_geospatial_data(
                    image_path=image_path,
                    mask_path=mask_path,
                    output_dir_images=OUTPUT_IMAGE_DIR,
                    output_dir_masks=OUTPUT_MASK_DIR
                )

    except FileNotFoundError:
        print(f"\nERROR: Could not find source data.")
        print(f"Please place your raw, fused GeoTIFF images in '{SOURCE_IMAGE_DIR}'")
        print(f"and your corresponding masks in '{SOURCE_MASK_DIR}'.")
        print("The script is currently configured to look for files there.")

    print("\n--- Data Preparation Finished ---")


