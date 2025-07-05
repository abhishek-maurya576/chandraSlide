import numpy as np
import cv2

def calculate_boulder_height_from_shadow(boulder_bbox, shadow_length, sun_angle_deg):
    """
    Estimates the height of a boulder using its shadow length and sun elevation angle.
    This is a key "novelty" feature of our project.

    Args:
        boulder_bbox (tuple): The bounding box of the boulder (x, y, w, h).
        shadow_length (float): The length of the shadow in pixels, measured from the image.
        sun_angle_deg (float): The angle of the sun above the horizon in degrees.

    Returns:
        float: The estimated height of the boulder in the same units as shadow_length
               (e.g., pixels, which can be converted to meters later).
    """
    if sun_angle_deg <= 0:
        return 0.0
        
    # Convert sun angle to radians for numpy trigonometry functions
    sun_angle_rad = np.deg2rad(sun_angle_deg)
    
    # Simple trigonometry: height = tan(angle) * shadow_length
    height = np.tan(sun_angle_rad) * shadow_length
    
    return height

def find_landslide_source(landslide_mask, dtm_array):
    """
    Traces a landslide mask uphill on a DTM to find its likely source region.

    Args:
        landslide_mask (np.ndarray): A binary mask of the landslide area.
        dtm_array (np.ndarray): The corresponding Digital Terrain Model data.

    Returns:
        tuple: The (row, col) coordinates of the estimated source point.
    """
    print("Analyzing landslide mask to find source...")
    
    # Ensure the mask and DTM have the same shape
    if landslide_mask.shape != dtm_array.shape:
        raise ValueError("Mask and DTM must have the same dimensions.")
        
    # Get the coordinates of all points within the landslide mask
    landslide_points = np.argwhere(landslide_mask > 0)
    
    if len(landslide_points) == 0:
        return None # No landslide detected
        
    # Find the point within the landslide that has the highest elevation
    # This is a simple but effective heuristic for the source.
    highest_point_idx = np.argmax(dtm_array[landslide_points[:, 0], landslide_points[:, 1]])
    source_point = landslide_points[highest_point_idx]
    
    print(f"Estimated landslide source found at coordinates: {source_point}")
    # A more advanced method would trace the path of steepest ascent from
    # multiple points within the mask.
    
    return tuple(source_point)

if __name__ == '__main__':
    print("Running post-processing analysis demonstration...")
    
    # --- 1. Demonstrate Boulder Height Calculation ---
    print("\n--- Boulder Height Estimation ---")
    dummy_boulder_bbox = (100, 100, 50, 50) # A 50x50 pixel boulder
    measured_shadow_length_px = 80.0 # We would measure this from the image
    lunar_sun_angle = 30.0 # From image metadata
    
    estimated_height_px = calculate_boulder_height_from_shadow(
        dummy_boulder_bbox, 
        measured_shadow_length_px, 
        lunar_sun_angle
    )
    
    print(f"Boulder with shadow length {measured_shadow_length_px}px and sun angle {lunar_sun_angle}deg")
    print(f"Estimated height: {estimated_height_px:.2f} pixels")
    # To get meters, we would need pixel_scale (meters/pixel) from the image metadata.
    # e.g., height_meters = estimated_height_px * pixel_scale

    # --- 2. Demonstrate Landslide Source Detection ---
    print("\n--- Landslide Source Detection ---")
    # Create a dummy DTM with a clear slope
    dummy_dtm = np.arange(256*256).reshape(256, 256)
    
    # Create a dummy landslide mask on the slope
    dummy_mask = np.zeros((256, 256), dtype=np.uint8)
    # The landslide runs from row 100 to 200, col 128
    dummy_mask[100:200, 128:132] = 1 
    
    # The source should be the highest point, which is at the "top" of the mask
    # around row 199, col 130.
    source_coords = find_landslide_source(dummy_mask, dummy_dtm)
    
    print(f"Function returned source coordinates: {source_coords}")
    # Expected output should be near (199, 130)
    if source_coords:
        assert source_coords[0] == 199, "Source row detection failed."

    print("\nPost-processing analysis demonstration finished.")


