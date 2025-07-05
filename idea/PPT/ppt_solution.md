# Project ChandraSlide: Presentation Content

## 1. Brief about the Idea

**Project ChandraSlide** is an ambitious initiative to develop a novel, AI-powered system for automatically detecting and analyzing landslides and boulders on the Moon's surface. Leveraging a unique combination of high-resolution images (OHRC), digital terrain models (DTM), and temporal data from India's Chandrayaan missions, the project aims to go beyond simple identification. It seeks to provide deep geological insights, such as the size and volume of boulders, the origin points of landslides, and a dynamic map of the most geologically active lunar regions. The final goal is to create an interactive dashboard that allows scientists to explore these findings, effectively turning raw satellite data into actionable scientific intelligence.

---

## 2. Opportunity

#### How is it different from other existing ideas?

The novelty of this approach lies in three key areas:

1.  **Physics-Informed AI through Data Fusion:** Unlike conventional methods that rely solely on optical images, our model fuses three types of data: high-resolution imagery (what it looks like), digital terrain models (its 3D shape), and derived slope maps (its steepness). This allows the AI to learn the *geological context* of the terrain, dramatically reducing false positives by understanding that landslides occur on steep slopes, not flat plains.
2.  **Advanced 3D Boulder Analysis:** We move beyond simple 2D detection. By analyzing the length of a boulder's shadow in conjunction with the sun's angle (from image metadata), our system can calculate the boulder's **height and estimate its 3D volume**. This provides a far richer dataset for geological analysis than any standard detection method.
3.  **Temporal Change Detection for Activity Mapping:** By comparing recent high-resolution images with older, archival images of the same location, the system can automatically flag landslides that have appeared recently. This allows us to identify and map **"Recent Geologic Activity,"** providing crucial information about the most dynamic and hazardous regions on the Moon.

#### How will it be able to solve the problem?

The proposed solution directly addresses every core requirement of the problem statement:

*   **To Identify Landslides & Boulders:** A hybrid deep learning architecture is used, with a U-Net model precisely segmenting landslide areas and a YOLOv8 model detecting individual boulders.
*   **To Provide Detailed Statistics:** Post-processing algorithms automatically measure the geometry of landslides (area, length) and boulders (diameter, estimated 3D volume).
*   **To Find the Source:** By analyzing the digital terrain model, the system traces a landslide's path uphill along the steepest gradient to pinpoint its likely initiation zone.
*   **To Highlight Active Regions:** The temporal analysis module specifically identifies new formations, enabling the creation of a "hotspot" map showing where the lunar surface is currently most active.

#### What is the USP (Unique Selling Proposition) of the proposed solution?

The primary USP is that **Project ChandraSlide is not just a detection tool, but a comprehensive analytical engine.**

It delivers a multi-layered understanding of lunar geology that is currently unavailable. Instead of just showing *where* a landslide is, it explains its **geometry**, its likely **source**, its **recency**, and provides detailed metrics on associated debris, including **3D volume estimates**. This holistic, data-fused approach transforms raw images into a rich, interactive scientific dashboard, offering deeper insights and significantly higher accuracy than any conventional method.

---

## 3. Features Offered by the Solution

Our solution, **Project ChandraSlide**, is an end-to-end system that transforms raw satellite imagery into actionable geological intelligence. Here are its key features:

**1. AI-Powered Multi-Feature Detection:**
*   **Precise Landslide Segmentation:** Automatically outlines the exact boundaries of landslide zones using a U-Net model that understands terrain shape, not just texture.
*   **Accurate Boulder Detection:** Utilizes a fine-tuned YOLOv8 model to detect individual boulders, capable of identifying even small objects in challenging lunar lighting.

**2. Advanced Geospatial & 3D Analysis:**
*   **Automated Landslide Source-Finding:** By analyzing the 3D Digital Terrain Model (DTM), the system algorithmically traces a landslide's path uphill to pinpoint its likely origin point.
*   **Novel 3D Boulder Sizing:** Goes beyond 2D measurement by using shadow analysis to calculate a boulder's **height and estimate its volume**, providing far richer data for scientific study.
*   **Comprehensive Geometric Stats:** Generates a full report for each landslide, detailing its surface area, average slope angle, and flow direction.

**3. Dynamic Temporal Activity Monitoring:**
*   **Automated Change Detection:** Compares recent Chandrayaan-2 images with older ones to automatically identify new geological events.
*   **Active Zone "Hotspot" Mapping:** Creates a dynamic map that highlights the most geologically active regions, which is critical for planning future lunar missions and scientific research.

**4. Interactive Visualization Dashboard:**
*   **Unified Data Hub:** A user-friendly dashboard that centralizes all maps, data, and analytical outputs in one place.
*   **Toggleable Map Layers:** Allows users to interactively overlay landslide masks, boulder locations, and source points on a high-resolution lunar map.
*   **Click-to-Analyze Functionality:** Users can simply click on any detected landslide or boulder to instantly view a detailed report of its characteristics (e.g., a boulder's volume or a landslide's origin).

---

## 4. Visual Workflow Diagram

This diagram illustrates the entire process, from data input to final analysis.

[Link to Workflow Diagram](./workflow_diagram.md)

```
![Workflow Diagram](workflow_diagram.md)
```

---

## 5. Wireframes/Mockups of Proposed Solution

This wireframe illustrates the main interface of the **ChandraSlide Dashboard**. It shows the control panel for analysis, the central interactive map, and the information panel that displays results and statistics.

[Link to Dashboard Wireframe](./dashboard_wireframe.md)

```
![Dashboard Wireframe](dashboard_wireframe.md)
```

---

## 7. Estimated Implementation Cost

The primary investment for this project is in specialized human resources and computational time, as the core technology stack is entirely based on open-source software, eliminating licensing fees.

The following is a high-level estimate based on a projected 6-month timeline.

### A. Personnel Resources (Estimated Effort)

The cost is broken down by required expertise over the project lifecycle.

*   **AI/ML Scientist (Project Lead):**
    *   **Focus:** Core model development, data fusion logic, result validation.
    *   **Estimated Effort:** 6 person-months.
*   **Data Engineer / GIS Specialist:**
    *   **Focus:** Sourcing data, preprocessing geospatial files (DTM, OHRC), and ensuring data alignment.
    *   **Estimated Effort:** 3 person-months.
*   **Software Developer (Backend & Dashboard):**
    *   **Focus:** Building the Streamlit application, creating the backend API, and deploying the final solution.
    *   **Estimated Effort:** 3 person-months.
*   **Total Estimated Effort:** **12 person-months.**

### B. Computing & Cloud Resources

This covers the infrastructure needed for model training and hosting the final application.

*   **GPU Cloud Computing:**
    *   **Purpose:** Training the U-Net and YOLOv8 models on the large lunar datasets.
    *   **Estimate:** ~400 hours of a high-performance GPU instance (e.g., NVIDIA A100 or V100).
*   **Cloud Hosting & Storage:**
    *   **Purpose:** Hosting the live dashboard and storing the extensive satellite imagery and model files.
    *   **Estimate:** Standard cloud server instance for 6 months + ~5 TB of high-availability storage.

### C. Software Licensing Costs

*   **Total Cost:** **$0.** The project exclusively uses a powerful stack of open-source software (Python, PyTorch, GDAL, Streamlit), making it a highly cost-effective and sustainable solution.

---

## 8. Use-Case Diagram

This diagram shows the primary ways a scientist would interact with the ChandraSlide system.

[Link to Use-Case Diagram](./use_case_diagram.md)

```
![Use-Case Diagram](use_case_diagram.md)
``` 