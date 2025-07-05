import streamlit as st
import numpy as np
from PIL import Image
import os
import tempfile
import plotly.express as px
import plotly.graph_objects as go
import sys

# Add the project root to the Python path to allow for absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the backend functions
from src.inference.predict import run_pipeline
from src.analysis.temporal_analysis import detect_temporal_changes

def visualize_results_interactively(image, results):
    """
    Helper function to create a rich, interactive Plotly visualization of the results.
    This allows for zooming, panning, and inspecting the analysis overlays.
    """
    fig = px.imshow(image)
    
    # Add contours for the landslide segmentation mask
    # This draws the boundaries of the detected area without obscuring the underlying image.
    mask_landslide = (results['segmentation_mask'] == 1).astype(np.uint8)
    if np.any(mask_landslide):
        fig.add_trace(go.Contour(
            z=mask_landslide,
            contours_coloring='lines',
            line_width=3,
            line_color='red',
            name='Landslide Area',
            showlegend=True
        ))

    # Add contours for the temporal change mask if it exists
    if 'change_mask' in results and np.any(results['change_mask']):
        fig.add_trace(go.Contour(
            z=results['change_mask'],
            contours_coloring='lines',
            line_width=3,
            line_color='cyan', # Use a distinct color for recent changes
            name='Recent Activity',
            showlegend=True
        ))

    # Add bounding box shapes for each detected boulder
    boulder_shapes = []
    for boulder in results['boulders']:
        x0, y0, x1, y1 = boulder['bbox']
        boulder_shapes.append(
            go.layout.Shape(
                type="rect",
                x0=x0, y0=y0, x1=x1, y1=y1,
                line=dict(color="yellow", width=2),
                name=f"Boulder {boulder['id']}"
            )
        )
    fig.update_layout(shapes=boulder_shapes)
    
    # Improve layout
    fig.update_layout(
        dragmode="pan",
        legend=dict(x=0, y=1, bgcolor='rgba(255,255,255,0.5)'),
        title="Interactive Analysis Map (Zoom and Pan Enabled)"
    )
    
    return fig

def main():
    """
    The main function that runs the Streamlit dashboard.
    """
    st.set_page_config(page_title="PRAJNA Dashboard", layout="wide")

    st.title("🌑 Project ChandraSlide: Lunar Landslide & Boulder Detection")
    st.markdown("""
        *An interactive dashboard for visualizing AI-detected geological features on the Moon.*
        
        **Instructions:**
        1.  Upload a lunar image (OHRC) and its corresponding Digital Terrain Model (DTM).
        2.  Click the "Analyze Region" button to run the detection pipeline.
        3.  Explore the results on the map and in the analysis panel.
    """)

    # --- Sidebar for Inputs ---
    st.sidebar.header("Mission Control")
    
    with st.sidebar.expander("Single Image Analysis"):
        uploaded_ohrc = st.file_uploader("Upload High-Res OHRC Image", type=["tif", "png", "jpg"], key="single_ohrc")
        uploaded_dtm = st.file_uploader("Upload Digital Terrain Model (DTM)", type=["tif"], key="single_dtm")
        if st.button("Analyze Single Region", key="analyze_single"):
            # ... (logic for single image analysis is similar to before)
            pass # Simplified for brevity

    with st.sidebar.expander("Temporal Change Analysis", expanded=True):
        uploaded_ohrc_before = st.file_uploader("Upload 'Before' Image (e.g., Chandrayaan-1)", type=["tif", "png", "jpg"], key="before_img")
        uploaded_ohrc_after = st.file_uploader("Upload 'After' Image (e.g., Chandrayaan-2 OHRC)", type=["tif", "png", "jpg"], key="after_img")
        uploaded_dtm_after = st.file_uploader("Upload 'After' DTM", type=["tif"], key="after_dtm")

        if st.button("Analyze for Changes", key="analyze_temporal"):
            if uploaded_ohrc_before and uploaded_ohrc_after and uploaded_dtm_after:
                with st.spinner('Running Full Pipeline & Temporal Analysis...'):
                    # --- Setup Temporary Files ---
                    # (This logic is similar to before, creating temp files for the pipeline)
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_before, \
                         tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_after, \
                         tempfile.NamedTemporaryFile(delete=False, suffix=".tif") as temp_dtm:
                        
                        after_image = Image.open(uploaded_ohrc_after).convert("RGB").resize((512, 512))
                        after_image.save(temp_after, "PNG")
                        
                        before_image = Image.open(uploaded_ohrc_before).convert("RGB").resize((512, 512))
                        before_image.save(temp_before, "PNG")

                        uploaded_dtm_after.seek(0)
                        temp_dtm.write(uploaded_dtm_after.read())
                        
                        temp_after_path = temp_after.name
                        temp_before_path = temp_before.name
                        temp_dtm_path = temp_dtm.name

                    # --- Run Backend ---
                    results = run_pipeline(temp_after_path, temp_dtm_path)
                    change_mask = detect_temporal_changes(temp_before_path, temp_after_path)
                    
                    # --- Store Results ---
                    if results:
                        st.session_state.ohrc_image = after_image
                        results['change_mask'] = change_mask
                        st.session_state.results = results
                        st.session_state.analysis_complete = True
                    else:
                        st.error("The analysis pipeline failed to run.")
                    
                    # --- Cleanup ---
                    os.remove(temp_after_path)
                    os.remove(temp_before_path)
                    os.remove(temp_dtm_path)

                if 'analysis_complete' in st.session_state:
                    st.sidebar.success("Analysis Complete!")
            else:
                st.sidebar.error("Please upload all three files for temporal analysis.")

    # --- Main Panel for Outputs ---
    if st.session_state.get('analysis_complete', False):
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("Visual Analysis")
            # Replace static image with interactive Plotly chart
            fig = visualize_results_interactively(st.session_state.ohrc_image, st.session_state.results)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Quantitative Analysis")
            results = st.session_state.results
            
            # --- Landslide Stats ---
            st.metric("Total Landslide Area (pixels)", f"{results['landslide_pixel_count']:,}")
            st.info(f"Estimated Landslide Source: {results['landslide_source']}")

            # --- Boulder Stats ---
            st.markdown(f"**Detected Boulders: {len(results['boulders'])}**")
            boulder_ids = [b['id'] for b in results['boulders']]
            if boulder_ids:
                selected_boulder_id = st.selectbox("Select a Boulder to Inspect:", options=boulder_ids)
                selected_boulder = next(b for b in results['boulders'] if b['id'] == selected_boulder_id)
                st.json(selected_boulder)

if __name__ == '__main__':
    main()
