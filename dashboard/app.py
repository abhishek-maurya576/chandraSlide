import streamlit as st
from PIL import Image
import os
import tempfile
from ultralytics import YOLO
import numpy as np

# --- Configuration ---
# This path points to the actual output of the YOLOv8 training script
MODEL_PATH = "runs/train/yolo_lunar_detector/weights/best.pt"

def run_detection(image_path, model):
    """
    Runs YOLOv8 detection on an image and returns the annotated image.
    """
    results = model(image_path)
    annotated_image_array = results[0].plot()
    annotated_image_rgb = Image.fromarray(annotated_image_array[..., ::-1])
    return annotated_image_rgb

def main():
    """
    Main function for the Streamlit dashboard.
    """
    st.set_page_config(page_title="ChandraSlide Detector", layout="wide")

    st.title("🌑 ChandraSlide: Lunar Rockfall Detection")
    st.markdown("Upload a lunar image to detect potential rockfalls using our trained YOLOv8 model.")

    st.sidebar.header("Controls")
    uploaded_image = st.sidebar.file_uploader("Upload Lunar Image", type=["tif", "png", "jpg", "jpeg"])

    if uploaded_image is not None:
        original_image = Image.open(uploaded_image).convert("RGB")
        st.sidebar.image(original_image, caption="Uploaded Image", use_column_width='always')

        if st.sidebar.button("Detect Rockfalls"):
            if not os.path.exists(MODEL_PATH):
                st.error(f"Model not found at {MODEL_PATH}. Please ensure the training process has completed successfully.")
                return

            with st.spinner('Model is running...'):
                try:
                    model = YOLO(MODEL_PATH)
                except Exception as e:
                    st.error(f"Error loading the model: {e}")
                    return

                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_image.name)[1]) as tfile:
                    tfile.write(uploaded_image.getvalue())
                    temp_image_path = tfile.name

                annotated_image = run_detection(temp_image_path, model)

                st.success("Detection Complete!")
                st.image(annotated_image, caption="Detection Results", use_column_width='always')

                os.remove(temp_image_path)

if __name__ == '__main__':
    main()
