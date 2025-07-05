# 🖥️ User Guide

This guide explains how to use the **PRAJNA Dashboard**, the interactive web application for Project ChandraSlide.

## 1. Launching the Application

Before you begin, ensure you have followed the setup and installation instructions in the [Developer Guide](./developer_guide.md).

To start the dashboard, navigate to the project's root directory in your terminal and run the following command:

```bash
streamlit run dashboard/app.py
```

This will launch a local web server and open the dashboard in your default web browser.

## 2. Dashboard Interface

The dashboard is divided into two main sections:

-   **Mission Control (Sidebar):** The panel on the left where you provide inputs.
-   **Main Panel:** The large area on the right where the results are displayed.

![Dashboard Layout](https://path-to-your-screenshot/dashboard_layout.png) <!-- Placeholder for a screenshot -->

## 3. Running an Analysis

Follow these steps to analyze a lunar region:

1.  **Upload OHRC Image:** In the sidebar, click the "Browse files" button under "Upload High-Res OHRC Image" and select the optical image file (`.png`, `.jpg`, `.tif`) you wish to analyze.

2.  **Upload DTM File:** Click the "Browse files" button under "Upload Digital Terrain Model (DTM)" and select the corresponding elevation data file (`.tif`).

3.  **Start Analysis:** Click the **`Analyze Region`** button. The application will display a spinner while the backend AI pipeline processes the data. This involves several steps, including data fusion, landslide segmentation, and boulder detection, so it may take a few moments.

## 4. Interpreting the Results

Once the analysis is complete, the main panel will update with two columns of information:

### Visual Analysis (Left Column)

-   This section displays the OHRC image you uploaded, now with colorful overlays representing the AI-detected features.
    -   <span style="color:red;">**Red Areas:**</span> Indicate regions classified as landslides.
    -   <span style="color:blue;">**Blue Areas:**</span> Indicate pixels classified as boulders by the segmentation model.
    -   <span style="color:yellow;">**Yellow Bounding Boxes:**</span> Indicate individual boulders detected by the object detection model.

### Quantitative Analysis (Right Column)

-   This section provides detailed statistics derived from the model's predictions.
    -   **Total Landslide Area:** The total number of pixels classified as a landslide.
    -   **Estimated Landslide Source:** The (row, column) coordinate of the likely origin point of the landslide, traced by the analysis engine.
    -   **Boulder Inspector:** A dropdown menu allows you to select each individually detected boulder. Selecting a boulder will display a JSON object containing its ID, bounding box coordinates, and its estimated height in meters (calculated from shadow analysis).


