import os
import zipfile
from tqdm import tqdm

# --- Configuration ---
# The download script saves archives directly in the 'data' directory.
DTM_ARCHIVE_DIR = "data/"
# We will store the unpacked DTMs in a new 'unpacked' directory.
UNPACKED_DIR = "data/unpacked/"

def unpack_dtm_archives():
    """
    Finds all ZIP archives in the data directory and unpacks them
    into the 'unpacked' folder.
    """
    print("--- Starting DTM Unpacking Process ---")

    # 1. Create the main output directory
    os.makedirs(UNPACKED_DIR, exist_ok=True)
    print(f"Unpacked DTMs will be stored in: {UNPACKED_DIR}")

    # 2. Find all zip files in the source directory
    try:
        zip_files = [f for f in os.listdir(DTM_ARCHIVE_DIR) if f.endswith('.zip') or f.endswith('.ZIP')]
    except FileNotFoundError:
        print(f"[ERROR] Data directory not found at: {DTM_ARCHIVE_DIR}")
        print("Please ensure you have downloaded the data first.")
        return

    if not zip_files:
        print("No DTM archives (.zip files) found to unpack in the 'data/' directory.")
        return

    print(f"\nFound {len(zip_files)} DTM archives to process.")

    # 3. Iterate and unpack each archive
    successful_unpacks = 0
    for archive_name in tqdm(zip_files, desc="Unpacking DTMs"):
        archive_path = os.path.join(DTM_ARCHIVE_DIR, archive_name)
        
        # Unpack directly into the destination folder
        dest_path = UNPACKED_DIR
        
        try:
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                # Check for nested folders. We want to extract the .IMG file directly.
                for member in zip_ref.namelist():
                    if member.endswith('.IMG'):
                        zip_ref.extract(member, dest_path)
            successful_unpacks += 1
        except zipfile.BadZipFile:
            print(f"\n[ERROR] Could not unpack {archive_name}. File may be corrupted or not a valid zip file.")
        except Exception as e:
            print(f"\n[ERROR] An unexpected error occurred while unpacking {archive_name}: {e}")

    print("\n--- DTM Unpacking Complete ---")
    print(f"Successfully unpacked {successful_unpacks}/{len(zip_files)} archives.")


if __name__ == "__main__":
    unpack_dtm_archives() 