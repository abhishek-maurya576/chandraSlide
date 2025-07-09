import os
import zipfile
from tqdm import tqdm

# --- Configuration ---
DTM_ARCHIVE_DIR = "data/raw/orbital_data/dtm"
DTM_PROCESSED_DIR = "data/processed/dtms"

def unpack_dtm_archives():
    """
    Finds all ZIP archives in the raw DTM directory and unpacks them
    into their own named subdirectories in the processed data folder.
    """
    print("--- Starting DTM Unpacking Process ---")

    # 1. Create the main output directory
    os.makedirs(DTM_PROCESSED_DIR, exist_ok=True)
    print(f"Unpacked DTMs will be stored in: {DTM_PROCESSED_DIR}")

    # 2. Find all zip files in the source directory
    try:
        zip_files = [f for f in os.listdir(DTM_ARCHIVE_DIR) if f.endswith('.zip') or f.endswith('.ZIP')]
    except FileNotFoundError:
        print(f"[ERROR] Raw DTM directory not found at: {DTM_ARCHIVE_DIR}")
        print("Please ensure the download process has created this directory.")
        return

    if not zip_files:
        print("No DTM archives (.zip files) found to unpack.")
        return

    print(f"\nFound {len(zip_files)} DTM archives to process.")

    # 3. Iterate and unpack each archive
    successful_unpacks = 0
    for archive_name in tqdm(zip_files, desc="Unpacking DTMs"):
        archive_path = os.path.join(DTM_ARCHIVE_DIR, archive_name)
        
        # Create a destination folder named after the archive (without the .zip extension)
        dtm_name = os.path.splitext(archive_name)[0]
        dest_path = os.path.join(DTM_PROCESSED_DIR, dtm_name)

        if os.path.exists(dest_path) and os.listdir(dest_path):
            # print(f"Skipping already unpacked archive: {dtm_name}")
            successful_unpacks +=1
            continue
        
        os.makedirs(dest_path, exist_ok=True)
        
        try:
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(dest_path)
            successful_unpacks += 1
        except zipfile.BadZipFile:
            print(f"\n[ERROR] Could not unpack {archive_name}. File may be corrupted or not a valid zip file.")
        except Exception as e:
            print(f"\n[ERROR] An unexpected error occurred while unpacking {archive_name}: {e}")

    print("\n--- DTM Unpacking Complete ---")
    print(f"Successfully unpacked {successful_unpacks}/{len(zip_files)} archives.")


if __name__ == "__main__":
    unpack_dtm_archives() 