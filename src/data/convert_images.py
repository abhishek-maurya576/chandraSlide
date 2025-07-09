import os
from tqdm import tqdm

try:
    from osgeo import gdal
except ImportError:
    print("-----------------------------------------------------------------")
    print("ERROR: The 'gdal' library was not found.")
    print("This is a critical dependency for processing the orbital imagery.")
    print("Please follow the manual installation instructions in README.md.")
    print("-----------------------------------------------------------------")
    exit()

# --- Configuration ---
RAW_IMAGE_DIR = "data/raw/orbital_data/optical"
PROCESSED_IMAGE_DIR = "data/processed/optical"

def convert_pds_to_geotiff():
    """
    Converts Planetary Data System (PDS) .IMG files to GeoTIFF format
    using the GDAL library.
    """
    print("--- Starting Image Conversion Process (PDS .IMG -> GeoTIFF) ---")

    # 1. Validate and create directories
    if not os.path.exists(RAW_IMAGE_DIR):
        print(f"[ERROR] Raw image directory not found at: {RAW_IMAGE_DIR}")
        print("Please ensure the download process has run and populated this directory.")
        return
        
    os.makedirs(PROCESSED_IMAGE_DIR, exist_ok=True)
    print(f"Converted images will be saved in: {PROCESSED_IMAGE_DIR}")

    # 2. Find all .IMG files to be processed
    try:
        source_images = [f for f in os.listdir(RAW_IMAGE_DIR) if f.upper().endswith('.IMG')]
    except FileNotFoundError:
        print(f"[ERROR] Could not read from source directory: {RAW_IMAGE_DIR}")
        return

    if not source_images:
        print("No source .IMG files found to convert.")
        return

    print(f"\nFound {len(source_images)} source images to process.")

    # 3. Iterate, convert, and save each image
    successful_conversions = 0
    for image_name in tqdm(source_images, desc="Converting Images"):
        source_path = os.path.join(RAW_IMAGE_DIR, image_name)
        
        # Create the output filename by changing the extension
        dest_filename = os.path.splitext(image_name)[0] + ".tif"
        dest_path = os.path.join(PROCESSED_IMAGE_DIR, dest_filename)

        if os.path.exists(dest_path):
            # print(f"Skipping already converted image: {dest_filename}")
            successful_conversions += 1
            continue
        
        try:
            # Use GDAL to perform the conversion
            # Open the source PDS file
            source_dataset = gdal.Open(source_path, gdal.GA_ReadOnly)
            if source_dataset is None:
                print(f"\n[WARN] Failed to open {image_name} with GDAL. It may be corrupt or an unsupported format.")
                continue

            # Use the CreateCopy method to convert to GeoTIFF
            # This preserves georeferencing, projections, etc.
            driver = gdal.GetDriverByName("GTiff")
            dest_dataset = driver.CreateCopy(dest_path, source_dataset, strict=0)
            
            # Close datasets to flush to disk
            dest_dataset = None
            source_dataset = None
            
            successful_conversions += 1

        except Exception as e:
            print(f"\n[ERROR] An unexpected error occurred while converting {image_name}: {e}")

    print("\n--- Image Conversion Complete ---")
    print(f"Successfully converted {successful_conversions}/{len(source_images)} images.")


if __name__ == "__main__":
    convert_pds_to_geotiff() 