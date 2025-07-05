import streamlit as st
from PIL import Image
import os
import tempfile
from ultralytics import YOLO
import numpy as np

# --- Configuration ---
MODEL_PATH = "models/lunar_rockfall_detector.pt" # Path to your trained model

def run_detection(image_path, model):
    """
    Runs YOLOv8 detection on an image and returns the annotated image.
    """
    results = model(image_path)
    # The results object contains plotting capabilities.
    # .plot() returns a BGR numpy array of the image with detections.
    annotated_image_array = results[0].plot()
    # Convert BGR to RGB for displaying with PIL/Streamlit
    annotated_image_rgb = Image.fromarray(annotated_image_array[..., ::-1])
    return annotated_image_rgb

def main():
    """
    Main function for the Streamlit dashboard.
    """
    st.set_page_config(page_title="ChandraSlide Detector", layout="wide")

    st.title("🌑 ChandraSlide: Lunar Rockfall Detection")
    st.markdown("Upload a lunar image to detect potential rockfalls using our trained YOLOv8 model.")

    # --- Sidebar for Inputs ---
    st.sidebar.header("Controls")
    uploaded_image = st.sidebar.file_uploader("Upload Lunar Image", type=["tif", "png", "jpg", "jpeg"])

    if uploaded_image is not None:
        # Display the uploaded image
        original_image = Image.open(uploaded_image).convert("RGB")
        st.sidebar.image(original_image, caption="Uploaded Image", use_column_width=True)

        if st.sidebar.button("Detect Rockfalls"):
            with st.spinner('Model is running...'):
                # --- Model Loading ---
                # Load the model only when the button is pressed.
                # You could cache this for performance with @st.cache_resource
                try:
                    model = YOLO(MODEL_PATH)
                except Exception as e:
                    st.error(f"Error loading the model: {e}")
                    return

                # --- Inference ---
                # Use a temporary file to save the uploaded image
                # so that YOLO can read it from a path.
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_image.name)[1]) as tfile:
                    tfile.write(uploaded_image.getvalue())
                    temp_image_path = tfile.name

                # Run detection on the temporary image file
                annotated_image = run_detection(temp_image_path, model)

                # --- Display Results ---
                st.success("Detection Complete!")
                st.image(annotated_image, caption="Detection Results", use_column_width=True)

                # Clean up the temporary file
                os.remove(temp_image_path)

if __name__ == '__main__':
    main()
