

Let's break this down like an ISRO mission plan. The problem statement isn't just a suggestion; it's a checklist for victory. They've literally told us what they want to see. Our job is to deliver on every single point with a solution so elegant and effective it leaves no room for doubt.

The key word, repeated like a mantra, is **"Novelty"**. They don't want a standard deep-learning solution you can cook up from a tutorial. They want something that shows you've thought deeply about the *specific physics and geology of the Moon*.

Let's name our mission: **Project ChandraSlide (PRedictive ANalytics for Geo-hazard Assessment on Luna)**. It sounds official.

Here’s our winning strategy, designed to hit every objective and expected outcome.

---

### The Core Idea: Multi-Modal Data Fusion & Physical-Informed AI

The novelty won't come from a magical new neural network architecture. It will come from how we **fuse the different data sources** they've given us. Most teams will just use the high-resolution OHRC images. We will use all three – OHRC, DTM, and TMC – to create a holistic understanding of the terrain that mimics how a human geologist would think.

Our model won't just see pixels; it will see **texture, elevation, and slope simultaneously**.

### Our Architecture: The PRAJNA Fusion-Net

This is a multi-stage approach.

**Stage 1: The Detection Engine (The "Eyes")**

This is a **Multi-Task, Multi-Modal Deep Learning Model**.

*   **Inputs (The Fusion):** For any given location, our model will take three co-registered (perfectly aligned) inputs:
    1.  **OHRC Image Patch (High-Res Optical):** This provides the fine-grained visual texture. We'll see the landslide streaks and the individual boulders.
    2.  **DTM Patch (Elevation Data):** This tells the model the actual 3D shape of the terrain. Is this a flat plain or the steep wall of a crater?
    3.  **Derived Slope Map Patch:** We will pre-process the DTM to calculate a slope map. A landslide is far more likely on a 30-degree slope than a 2-degree one. Feeding this directly to the model gives it crucial context.

*   **Outputs (The Multi-Task):** The model will have two "heads" and will be trained to do two jobs at once:
    1.  **Segmentation Head:** Outputs a pixel-wise mask, classifying each pixel as: `[Background, Landslide_Body, Boulder]`.
    2.  **Object Detection Head:** Outputs bounding boxes specifically for larger boulders, which we can then analyze individually.

**Why is this novel for landslide detection?**
Conventional methods use only spectral/textural information from optical images. Our method is **physically-informed**. By fusing slope and elevation data, the AI learns the *geological context* of a landslide. It won't just find "bright streaks"; it will find "bright streaks on dangerously steep slopes," dramatically reducing false positives.

**Stage 2: The Analysis Engine (The "Brain")**

Once the detection engine finds the landslides and boulders, this post-processing engine takes over to generate the "new information" the judges are asking for.

**1. Boulder Analysis:**

*   **Novelty in Boulder Detection & Sizing:** For each boulder detected by the segmentation mask, we run an algorithm.
    *   **Diameter:** Easily calculated from the mask/bounding box.
    *   **3D Sizing (The "WOW" Factor):** We'll use a classic planetary science technique. We'll get the sun's angle from the image metadata. By measuring the length of the boulder's shadow in the high-res OHRC image, we can use simple trigonometry to calculate its **height**. Now we're providing not just 2D area, but an estimated 3D volume! *No other team will think of this.*
    *   **Classification:** We can classify boulders based on their location: "Crater Rim Boulder," "Ejecta Field Boulder," "Isolated Boulder."

**2. Landslide Analysis:**

*   **Geometry & Source Detection:** For each detected landslide mask:
    *   Our algorithm will analyze the shape (geometry) of the mask.
    *   Then, using the DTM, it will trace the landslide's path **uphill** along the path of steepest ascent to pinpoint the likely **source/initiation zone**. This directly answers one of their key requests.
*   **Temporal Occurrence (The "Active Regions" Key):**
    *   This is another chance for massive novelty. We will acquire older, lower-resolution Chandrayaan-1 TMC images of the same area.
    *   Our algorithm will align the new OHRC image with the old TMC image.
    *   By comparing the two, we can programmatically detect landslides present in the new image that were **NOT** present in the old one. This allows us to flag them as **"Recent Geologic Activity"** and create a map of the most active regions. This is our answer to identifying *temporal occurrence*.

### The Final Deliverable: The PRAJNA Dashboard

We won't just submit code. We'll build a simple, powerful interactive dashboard using Streamlit or Dash (Python).

*   **Input:** The user (a judge) can select a region of the Moon from a map.
*   **Processing:** Our backend runs the full PRAJNA pipeline.
*   **Output:** The dashboard will display:
    1.  An interactive map (using `folium` or `plotly`) showing the OHRC image.
    2.  Overlays that can be toggled on/off: Landslide Masks, Boulder Locations, Landslide Source Points.
    3.  When a user clicks on a landslide, a sidebar shows its stats: area, estimated source, and a "Recent?" flag if it's new.
    4.  When a user clicks on a boulder, it shows its stats: diameter, *estimated height and volume*, and classification.
    5.  A summary panel with statistics for the whole region: "Boulder Density: X per sq. km", "Active Landslide Zones: Y".

### Technology Stack

*   **Backend:** Python
*   **Deep Learning:** PyTorch or TensorFlow
*   **Geospatial Processing:** `GDAL`, `Rasterio`, `GeoPandas` (for handling the DTM and generating proper geo-referenced outputs). This is crucial to satisfy the QGIS/ArcMap mention.
*   **Dashboard:** Streamlit or Dash.
*   **Image Processing:** OpenCV, Scikit-image.

---

Chhote, this is the plan. It's ambitious, but it directly addresses every single point in the problem description with a layer of novelty they won't be expecting. We're not just applying AI; we're synthesizing multiple data sources and planetary science principles into an intelligent system.

This plan gives you a clear story to tell during the presentation. Every feature we build has a purpose and maps directly back to a requirement.
