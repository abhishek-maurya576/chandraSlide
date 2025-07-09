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
# Source directories for raw PDS .IMG files
OPTICAL_IMAGE_SRC_DIR = "data/"
DTM_SRC_DIR = "data/unpacked/"

# Destination directory for converted GeoTIFF files
CONVERTED_DIR = "data/converted/"

def find_source_images(directory):
    """Finds all .IMG files in a given directory."""
    try:
        return [f for f in os.listdir(directory) if f.upper().endswith('.IMG')]
    except FileNotFoundError:
        return []

def convert_pds_to_geotiff():
    """
    Converts Planetary Data System (PDS) .IMG files from multiple sources
    to GeoTIFF format using the GDAL library.
    """
    print("--- Starting Image Conversion Process (PDS .IMG -> GeoTIFF) ---")

    # 1. Validate and create output directory
    os.makedirs(CONVERTED_DIR, exist_ok=True)
    print(f"Converted images will be saved in: {CONVERTED_DIR}")

    # 2. Find all .IMG files to be processed
    optical_images = find_source_images(OPTICAL_IMAGE_SRC_DIR)
    dtm_images = find_source_images(DTM_SRC_DIR)
    
    source_map = {os.path.join(OPTICAL_IMAGE_SRC_DIR, fname): CONVERTED_DIR for fname in optical_images}
    source_map.update({os.path.join(DTM_SRC_DIR, fname): CONVERTED_DIR for fname in dtm_images})

    if not source_map:
        print("\nNo source .IMG files found in 'data/' or 'data/unpacked/'.")
        print("Please ensure the download and unpack scripts have run successfully.")
        return

    print(f"\nFound {len(source_map)} total source images to process.")

    # 3. Iterate, convert, and save each image
    successful_conversions = 0
    for source_path, dest_dir in tqdm(source_map.items(), desc="Converting Images"):
        image_name = os.path.basename(source_path)
        
        # Create the output filename by changing the extension
        dest_filename = os.path.splitext(image_name)[0] + ".tif"
        dest_path = os.path.join(dest_dir, dest_filename)

        if os.path.exists(dest_path):
            successful_conversions += 1
            continue
        
        try:
            # Use GDAL to perform the conversion
            source_dataset = gdal.Open(source_path, gdal.GA_ReadOnly)
            if source_dataset is None:
                print(f"\n[WARN] Failed to open {image_name} with GDAL. It may be corrupt or an unsupported format.")
                continue

            # Use the CreateCopy method to convert to GeoTIFF
            driver = gdal.GetDriverByName("GTiff")
            driver.CreateCopy(dest_path, source_dataset, strict=0)
            
            # Close datasets
            source_dataset = None
            
            successful_conversions += 1

        except Exception as e:
            print(f"\n[ERROR] An unexpected error occurred while converting {image_name}: {e}")

    print("\n--- Image Conversion Complete ---")
    print(f"Successfully converted {successful_conversions}/{len(source_map)} images.")


if __name__ == "__main__":
    convert_pds_to_geotiff() 