import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

def detect_temporal_changes(image_before_path, image_after_path, threshold=0.9):
    """
    Detects significant changes between two registered images of the same location.

    This function uses the Structural Similarity Index (SSIM) to compare the two
    images, which is more robust to minor lighting changes than simple subtraction.

    Args:
        image_before_path (str): File path to the older image (e.g., from Chandrayaan-1).
        image_after_path (str): File path to the newer image (e.g., from Chandrayaan-2).
        threshold (float): The SSIM threshold. Lower values detect more (and potentially
                           less significant) changes. Defaults to 0.9.

    Returns:
        np.ndarray: A binary mask where '1' represents areas of significant change.
                    Returns None on failure.
    """
    try:
        # Load images in grayscale
        img_before = cv2.imread(image_before_path, cv2.IMREAD_GRAYSCALE)
        img_after = cv2.imread(image_after_path, cv2.IMREAD_GRAYSCALE)

        if img_before is None or img_after is None:
            raise FileNotFoundError("One or both images could not be loaded.")

        # Ensure images are the same size (a prerequisite for this simple method)
        if img_before.shape != img_after.shape:
            # In a real pipeline, we would use `align_and_fuse_data` to handle this.
            # Here, we'll resize for demonstration purposes.
            h, w = img_after.shape
            img_before = cv2.resize(img_before, (w, h))
        
        # Compute the Structural Similarity Index (SSIM) between the two images
        (score, diff) = ssim(img_before, img_after, full=True)
        diff = (diff * 255).astype("uint8")

        # Threshold the difference image to get the regions of significant change
        thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        
        # Perform some morphological operations to clean up noise
        kernel = np.ones((5,5), np.uint8)
        change_mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

        print(f"Temporal analysis complete. SSIM score: {score:.4f}")
        return change_mask

    except Exception as e:
        print(f"An error occurred during temporal analysis: {e}")
        return None

if __name__ == '__main__':
    print("Running temporal analysis demonstration...")
    
    # --- Create Dummy 'Before' and 'After' Images ---
    # Create a base image
    before_image = np.zeros((512, 512), dtype="uint8")
    cv2.rectangle(before_image, (100, 100), (200, 200), 255, -1)
    cv2.circle(before_image, (400, 400), 50, 150, -1)
    cv2.imwrite("dummy_before.png", before_image)
    
    # Create an 'after' image with a significant change (a new feature)
    after_image = before_image.copy()
    cv2.rectangle(after_image, (300, 150), (450, 300), 100, -1) # This is the new landslide
    cv2.imwrite("dummy_after.png", after_image)

    # --- Run Change Detection ---
    change_mask = detect_temporal_changes("dummy_before.png", "dummy_after.png")

    if change_mask is not None:
        print(f"Change mask generated with shape: {change_mask.shape}")
        
        # The change mask should highlight the new rectangle.
        # We can verify this by checking if there are non-zero pixels in that area.
        change_area = np.sum(change_mask[150:300, 300:450])
        assert change_area > 0, "Change detection failed to identify the new feature."
        print("Successfully detected the change area.")

        # Save the change mask for visual inspection
        cv2.imwrite("dummy_change_mask.png", change_mask)
        print("Change mask saved to 'dummy_change_mask.png'")

    # --- Cleanup ---
    import os
    os.remove("dummy_before.png")
    os.remove("dummy_after.png")
    os.remove("dummy_change_mask.png")
    
    print("\nTemporal analysis demonstration finished.")


