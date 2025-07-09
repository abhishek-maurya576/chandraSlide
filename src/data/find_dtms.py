import os
import re
import geopandas as gpd
import pandas as pd

# ----------------------------------------------------------------------------------
# MANUAL DOWNLOAD REQUIRED
# ----------------------------------------------------------------------------------
# 1. Download: https://wms.lroc.asu.edu/files/rdr/SHAPEFILE_NAC_DTMS_360.zip
# 2. Create a folder named 'shapefile' in the project root.
# 3. Unzip the contents into the 'shapefile' folder.
# 4. Run this script.
# ----------------------------------------------------------------------------------

SHAPEFILE_PATH = "shapefile/NAC_DTMS_360.SHP"

def get_core_id(id_string):
    """
    Robustly extracts the numeric core from an LROC ID string (e.g., "M12345RC" -> "12345").
    Returns None if no match is found.
    """
    if not isinstance(id_string, str):
        return None
    match = re.search(r'M(\d+)', id_string.strip())
    return match.group(1) if match else None

def extract_image_ids_from_shapefile(dtm_gdf):
    """
    Scans the entire DTM shapefile and extracts a unique set of all
    source image IDs used to create the DTMs.
    """
    print("\n--- Extracting All Unique Source Image IDs from Shapefile ---")
    
    all_source_image_ids = set()

    # Iterate over each DTM entry in the shapefile
    for index, row in dtm_gdf.iterrows():
        images_used_str = str(row['images'])
        
        # Extract all core IDs from the comma-separated string in the 'images' column.
        source_ids_in_row = images_used_str.split(',')
        
        for img_id in source_ids_in_row:
            cleaned_id = img_id.strip()
            if cleaned_id:
                all_source_image_ids.add(cleaned_id)
    
    print(f"Found {len(all_source_image_ids)} unique source image IDs.")
    
    return sorted(list(all_source_image_ids))


if __name__ == "__main__":
    if not os.path.exists(SHAPEFILE_PATH):
        print(f"Error: Shapefile not found at '{SHAPEFILE_PATH}'")
        print("Please ensure the file from the manual download exists at that exact path.")
    else:
        try:
            print(f"Loading shapefile: {SHAPEFILE_PATH}")
            dtm_footprints_gdf = gpd.read_file(SHAPEFILE_PATH)
            
            # Extract all unique image IDs from the shapefile
            image_ids_with_dtms = extract_image_ids_from_shapefile(dtm_footprints_gdf)

            if image_ids_with_dtms:
                # Create a DataFrame to save the results
                df = pd.DataFrame(image_ids_with_dtms, columns=["ImageID"])
                
                output_csv = "data/images_with_dtms.csv"
                df.to_csv(output_csv, index=False)
                print(f"--- Results saved to {output_csv} ---")
            else:
                print("No source image IDs could be extracted from the shapefile.")

        except Exception as e:
            print(f"An error occurred: {e}") 