import numpy as np
import rasterio
from rasterio.warp import reproject, Resampling

def calculate_slope(dtm_path):
    """
    Calculates a slope map from a Digital Terrain Model (DTM).

    Args:
        dtm_path (str): The file path to the DTM GeoTIFF.

    Returns:
        numpy.ndarray: A 2D array representing the slope in degrees.
    """
    print(f"Calculating slope for {dtm_path}...")
    # This is a placeholder for a more complex implementation.
    # A real implementation would use GDAL or a similar library
    # to calculate terrain slope from the elevation data.
    with rasterio.open(dtm_path) as dtm:
        elevation = dtm.read(1)
        # Simple gradient calculation as a placeholder
        dx, dy = np.gradient(elevation, dtm.res[0], dtm.res[1])
        slope = np.arctan(np.sqrt(dx**2 + dy**2)) * (180.0 / np.pi)
    print("Slope calculation complete.")
    return slope

def align_and_fuse_data(ohrc_path, dtm_path, target_crs='EPSG:4326'):
    """
    Aligns OHRC and DTM data to a common Coordinate Reference System (CRS)
    and resolution, then fuses them into a multi-channel array.

    Args:
        ohrc_path (str): File path to the OHRC image.
        dtm_path (str): File path to the DTM.
        target_crs (str, optional): The target CRS for alignment. Defaults to 'EPSG:4326'.

    Returns:
        numpy.ndarray: A 3D array where channels are [OHRC, DTM, Slope].
                         Returns None on failure.
    """
    print(f"Starting data fusion for {ohrc_path} and {dtm_path}...")
    
    try:
        # Open datasets
        with rasterio.open(ohrc_path) as ohrc_src, rasterio.open(dtm_path) as dtm_src:
            
            # --- Reproject DTM to match OHRC ---
            # This is a critical step to ensure pixels align perfectly.
            # We create a new in-memory dataset for the reprojected DTM.
            reprojected_dtm_array = np.zeros(ohrc_src.shape, dtype=dtm_src.dtypes[0])

            reproject(
                source=rasterio.band(dtm_src, 1),
                destination=reprojected_dtm_array,
                src_transform=dtm_src.transform,
                src_crs=dtm_src.crs,
                dst_transform=ohrc_src.transform,
                dst_crs=ohrc_src.crs,
                resampling=Resampling.bilinear)

            # --- Calculate Slope from the aligned DTM ---
            # For simplicity, we'll calculate slope on the reprojected DTM array.
            # A more robust method would calculate it before reprojection
            # and then reproject the slope map itself.
            dx, dy = np.gradient(reprojected_dtm_array, ohrc_src.res[0], ohrc_src.res[1])
            slope_array = np.arctan(np.sqrt(dx**2 + dy**2)) * (180.0 / np.pi)
            
            # --- Fuse into a single multi-channel array ---
            # Read the OHRC data
            ohrc_array = ohrc_src.read(1)

            # Stack the arrays along a new axis to create channels
            # Shape: (channels, height, width)
            fused_data = np.stack([
                ohrc_array,
                reprojected_dtm_array,
                slope_array
            ], axis=0)

            print("Data fusion complete.")
            # In a real pipeline, we would save this fused data or pass it to a dataset loader.
            return fused_data

    except Exception as e:
        print(f"An error occurred during data fusion: {e}")
        return None

if __name__ == '__main__':
    # This is a placeholder for example usage.
    # In a real scenario, you would replace these with actual file paths
    # and likely process a directory of files.
    print("Running preprocessing script...")
    
    # Create dummy data for demonstration purposes
    # A real run would use actual Chandrayaan data files.
    dummy_ohrc_path = 'dummy_ohrc.tif'
    dummy_dtm_path = 'dummy_dtm.tif'
    
    # Create a dummy OHRC file
    with rasterio.open(dummy_ohrc_path, 'w', driver='GTiff', height=100, width=100, count=1, dtype=np.uint8, crs='EPSG:4326', transform=rasterio.transform.from_origin(0, 100, 1, 1)) as dst:
        dst.write(np.random.randint(0, 256, (100, 100), dtype=np.uint8), 1)

    # Create a dummy DTM file
    with rasterio.open(dummy_dtm_path, 'w', driver='GTiff', height=100, width=100, count=1, dtype=np.float32, crs='EPSG:4326', transform=rasterio.transform.from_origin(0, 100, 1, 1)) as dst:
        dst.write(np.random.rand(100, 100).astype(np.float32) * 1000, 1)

    fused_array = align_and_fuse_data(dummy_ohrc_path, dummy_dtm_path)
    
    if fused_array is not None:
        print(f"Successfully fused data into an array of shape: {fused_array.shape}")
        # Expected shape: (3, 100, 100) -> (channels, height, width)
    
    # Clean up dummy files
    import os
    os.remove(dummy_ohrc_path)
    os.remove(dummy_dtm_path)
    
    print("Preprocessing script finished.")

