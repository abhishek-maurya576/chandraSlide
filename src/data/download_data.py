import os
import pandas as pd
import requests
from tqdm import tqdm
import urllib.parse
import argparse

# --- Configuration ---
MANIFEST_PATH = "data/download_manifest.csv"
# All raw data (images and zips) will be saved directly in the 'data' directory.
OUTPUT_DIR = "data/"
# DOWNLOAD_LIMIT = 5  # Set to None to download all files - Now handled by argparse

def download_file(url, output_path, force=False):
    """
    Downloads a file from a URL to a given path, showing a progress bar.
    Skips download if the file already exists, unless 'force' is True.
    """
    if not force and os.path.exists(output_path):
        print(f"Skipping existing file: {os.path.basename(output_path)}")
        return True
        
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        total_size_in_bytes = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 Kibibyte

        progress_bar = tqdm(
            total=total_size_in_bytes,
            unit='iB',
            unit_scale=True,
            desc=f"Downloading {os.path.basename(output_path)}"
        )
        
        with open(output_path, 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        
        progress_bar.close()
        
        if total_size_in_bytes != 0 and progress_bar.n < total_size_in_bytes:
            print(f"[WARNING] Download for {os.path.basename(output_path)} may be incomplete.")
            
        return True

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Could not download {url}. Reason: {e}")
        return False

def start_download_process(download_limit, force_download):
    """
    Main function to orchestrate the data download process based on the manifest.
    """
    print("--- Starting Data Acquisition Process ---")

    # 1. Validate manifest file exists
    if not os.path.exists(MANIFEST_PATH):
        print(f"[ERROR] Manifest file not found at: {MANIFEST_PATH}")
        return

    # 2. Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Data will be saved to: {OUTPUT_DIR}")


    # 3. Read the manifest
    manifest_df = pd.read_csv(MANIFEST_PATH)
    
    # Apply download limit for testing
    if download_limit is not None:
        print(f"\n[INFO] Applying download limit. Only the first {download_limit} pairs will be downloaded.")
        manifest_df = manifest_df.head(download_limit)

    if force_download:
        print("[INFO] Force mode enabled. Files will be re-downloaded even if they exist.")

    print(f"\nPreparing to download {len(manifest_df)} Image-DTM pairs...")
    
    successful_downloads = 0
    total_downloads = 0

    # 4. Iterate through manifest and download files
    for index, row in manifest_df.iterrows():
        print(f"\nProcessing pair {index + 1}/{len(manifest_df)}:")
        
        # --- Download Optical Image ---
        image_id = row['ImageID']
        image_url = row['ImageURL']
        image_filename = os.path.basename(urllib.parse.unquote(image_url))
        image_output_path = os.path.join(OUTPUT_DIR, image_filename)
        
        print(f"  - Target Optical Image: {image_filename}")
        total_downloads += 1
        if download_file(image_url, image_output_path, force=force_download):
            successful_downloads += 1

        # --- Download DTM ---
        dtm_name = row['DTM_Name']
        dtm_url = row['DTM_URL']
        # DTMs are often zipped, so we preserve the original filename from the URL
        dtm_filename = os.path.basename(urllib.parse.unquote(dtm_url))
        dtm_output_path = os.path.join(OUTPUT_DIR, dtm_filename)

        print(f"  - Target DTM: {dtm_filename}")
        total_downloads += 1
        if download_file(dtm_url, dtm_output_path, force=force_download):
            successful_downloads += 1

    print("\n--- Data Acquisition Complete ---")
    print(f"Successfully downloaded {successful_downloads} out of {total_downloads} files.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download high-resolution orbital imagery and DTMs.")
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit the number of Image-DTM pairs to download. Defaults to all."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force re-download of files even if they appear to exist."
    )
    args = parser.parse_args()

    start_download_process(args.limit, args.force) 