import os
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import geopandas as gpd

# --- Configuration ---
SHAPEFILE_PATH = "shapefile/NAC_DTMS_360.SHP"
IMAGE_ID_LIST_PATH = "data/images_with_dtms.csv"
OUTPUT_MANIFEST_PATH = "data/download_manifest.csv"

def find_image_download_url(image_id, session):
    """
    Finds the direct download URL for a calibrated image by scraping its data page.
    Example ID: M1192739321L
    """
    # Construct the URL to the observation page
    # The EDR (raw) product ID is needed for the page URL. 'E' is appended.
    if image_id.endswith('L') or image_id.endswith('R'):
        product_id = image_id + 'E'
    else:
        # This is an assumption for IDs without a suffix.
        product_id = image_id + 'LE' 
        
    page_url = f"https://wms.lroc.asu.edu/lroc/view_lroc/LRO-L-LROC-2-EDR-V1.0/{product_id}"

    try:
        response = session.get(page_url, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the link that points to the Calibrated Data Record (CDR)
        # It usually contains 'LRO-L-LROC-3-CDR' and ends with 'C.IMG'
        cdr_id_suffix = image_id[-1] + 'C.IMG' # e.g., LC.IMG or RC.IMG
        
        # A more robust regex to find the CDR link
        cdr_link_pattern = re.compile(r"LRO-L-LROC-3-CDR-V1\.0.*" + re.escape(image_id) + r"C\.IMG", re.IGNORECASE)
        
        link = soup.find('a', href=cdr_link_pattern)
        
        if link and link.has_attr('href'):
            # The href is relative, so we need to prepend the host if it's missing
            url = link['href']
            if url.startswith('//'):
                return "https:" + url
            return url
        else:
            # Fallback for a different pattern if the first fails
            link = soup.find('a', string=re.compile(r'Download CDR', re.IGNORECASE))
            if link and link.has_attr('href'):
                url = link['href']
                if url.startswith('//'):
                    return "https:" + url
                return url

    except requests.exceptions.RequestException as e:
        print(f"\n[WARN] Could not access page {page_url}. Reason: {e}")
        
    return "URL_NOT_FOUND"


def generate_manifest():
    """
    Generates or updates a CSV manifest with verified download URLs for images and DTMs.
    """
    print("--- Starting Download Manifest Generation (V2) ---")
    
    # --- Load Local Data ---
    if not os.path.exists(IMAGE_ID_LIST_PATH):
        print(f"[ERROR] Image ID list not found at: {IMAGE_ID_LIST_PATH}")
        return
    image_df = pd.read_csv(IMAGE_ID_LIST_PATH)
    target_image_ids = set(image_df['ImageID'].str.strip())

    if not os.path.exists(SHAPEFILE_PATH):
        print(f"[ERROR] DTM Shapefile not found at: {SHAPEFILE_PATH}")
        return
    dtm_gdf = gpd.read_file(SHAPEFILE_PATH)
    
    # --- Initialize Manifest ---
    if os.path.exists(OUTPUT_MANIFEST_PATH):
        print(f"1. Loading existing manifest from {OUTPUT_MANIFEST_PATH} to update.")
        manifest_df = pd.read_csv(OUTPUT_MANIFEST_PATH)
    else:
        print("1. No existing manifest found. A new one will be created.")
        manifest_df = pd.DataFrame(columns=["ImageID", "ImageURL", "DTM_Name", "DTM_URL"])

    # --- Match DTMs to Images ---
    print("2. Matching images to their DTMs...")
    records_to_add = []
    # Create a dictionary for quick lookup of existing ImageIDs in the manifest
    existing_ids = set(manifest_df['ImageID'])

    for _, row in tqdm(dtm_gdf.iterrows(), total=dtm_gdf.shape[0], desc="Processing DTMs"):
        images_used_str = str(row.get('images', ''))
        matched_ids = target_image_ids.intersection({img.strip() for img in images_used_str.split(',')})

        for image_id in matched_ids:
            if image_id not in existing_ids:
                records_to_add.append({
                    "ImageID": image_id,
                    "ImageURL": "URL_PENDING_DISCOVERY",
                    "DTM_Name": row.get('DTM_NAME'),
                    "DTM_URL": row.get('url')
                })
    
    if records_to_add:
        new_records_df = pd.DataFrame(records_to_add)
        manifest_df = pd.concat([manifest_df, new_records_df], ignore_index=True)
        manifest_df.drop_duplicates(subset=['ImageID', 'DTM_Name'], inplace=True, keep='last')

    # --- Discover Image URLs ---
    print("\n3. Discovering image download URLs (this may be slow on the first run)...")
    
    # Use a session object for connection pooling
    with requests.Session() as session:
        # Find all rows where the URL is a placeholder or known to have failed
        pending_urls = manifest_df[manifest_df['ImageURL'].str.contains("URL_PENDING_DISCOVERY|URL_NOT_FOUND|URL_UNKNOWN_FOR", na=False)]
        
        if pending_urls.empty:
            print("All image URLs have already been discovered and appear valid.")
        else:
            for index, row in tqdm(pending_urls.iterrows(), total=pending_urls.shape[0], desc="Finding URLs"):
                image_id = row['ImageID']
                found_url = find_image_download_url(image_id, session)
                manifest_df.loc[index, 'ImageURL'] = found_url

    # --- Save Final Manifest ---
    print("\n4. Saving updated manifest...")
    manifest_df.to_csv(OUTPUT_MANIFEST_PATH, index=False)
    print(f"--- Manifest successfully saved to {OUTPUT_MANIFEST_PATH} ---")
    
    # --- Final Report ---
    not_found_count = len(manifest_df[manifest_df['ImageURL'] == "URL_NOT_FOUND"])
    if not_found_count > 0:
        print(f"\n[INFO] Could not find URLs for {not_found_count} images. They are marked in the manifest.")


if __name__ == "__main__":
    generate_manifest() 