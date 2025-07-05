
## 🌑🔍 **Core Project Goal Summary**

> Create a **novel algorithm** to detect **landslides and boulder falls** using **Chandrayaan-1 & 2 images (TMC, OHRC, DTM)**, provide **measurements**, **detect source regions**, and identify **activity-prone zones**.

---

## ✅ 🧠 **SOLUTION 1: Multi-Modal Fusion with Deep Semantic Segmentation + Morphological Analysis**

### 🔧 Tools:

* **Model**: UNet++ or DeepLabv3+ with multi-channel input (TMC grayscale + DTM elevation)
* **Libraries**: PyTorch, OpenCV, rasterio, NumPy
* **Post-processing**: Shape analysis, slope detection (QGIS plugin or Python)

### 🧪 Novelty:

* **Fusion of optical + elevation data** (TMC + DTM) to learn slope-based segmentation
* **Pixel-wise semantic segmentation** detects precise boundaries of landslide zones
* Use **morphological filters** to remove noise, detect scar edges
* **Watershed algorithm** or **active contour** to trace boulders
* Automatically **extract geometry** (area, slope, direction) of landslide mass

### 📊 Output:

* Segmentation mask (landslide zones in red, boulders in blue)
* CSV with area, bounding box, direction of slide, source crater
* Auto-generated **landslide source map**

### 🎯 Success Potential:

* **90%+ IoU** on known landslide zones (based on DEM + image)
* Scalable to most terrain regions

---

## ✅ 📦 **SOLUTION 2: Attention-based Object Detection for Boulder Detection (YOLOv8 + Contour Estimation)**

### 🔧 Tools:

* YOLOv8 or YOLO-NAS (for small-object detection)
* DTM overlay for slope context
* Post-processing: Contour detection (OpenCV) + Shape descriptors

### 🧪 Novelty:

* Train YOLOv8 to detect **individual boulders**, fine-tuned for **lunar lighting conditions**
* Add **contextual filters** — elevation drop + shadow length — to differentiate between **embedded rocks vs. displaced boulders**
* Auto-measure boulder **diameter/length** using pixel-to-meter conversion via metadata

### 📊 Output:

* Annotated image with boulder boxes + labels
* Table with coordinates, size, potential movement direction
* Distinguish **static vs. displaced** boulders (change-based heuristic)

### 🎯 Success Potential:

* **75–85% mAP** on large boulders
* Size detection accuracy within **±5% error margin**

---

## ✅ 🌋 **SOLUTION 3: Spatiotemporal Change Detection (CDNet + Optical Flow + DEM Gradient Analysis)**

### 🔧 Tools:

* CDNet or Siamese CNN for temporal change
* Optical flow to detect **mass movement pattern**
* DTM gradient + shadow analysis to detect slope triggers

### 🧪 Novelty:

* Input: 2 time-separated OHRC/TMC images
* Model detects **change in terrain pattern**
* Optical flow identifies direction of mass movement
* Use DTM slope drop to predict **source crater/fault line**
* Detect most **"active" zones** using cumulative terrain change

### 📊 Output:

* Color-coded map: active, semi-active, inactive regions
* "Trigger heatmap" – landslide initiation probability
* Summary report: top 5 most unstable regions

### 🎯 Success Potential:

* **High novelty** — few lunar systems use temporal geospatial ML
* Activity prediction accuracy: **80–90%** (based on DEM + slope + terrain change)

---

## 📊 Example Output Summary

| Feature            | Example Output                             |
| ------------------ | ------------------------------------------ |
| Landslide Location | `(lat, long)` + slope direction            |
| Boulder Detection  | 231 boulders; range: 0.7m – 11.3m          |
| Geometry Stats     | Landslide area: 2.4 km², Slope angle: 36°  |
| Activity Zones     | Red: Active, Yellow: Medium, Green: Stable |
| Source Detection   | Triggered by crater at `(x, y)`            |

---

## 🚀 Final Fusion Architecture (Recommended for Submission)

### 🔁 Hybrid Approach:

| Step | Task                                            |
| ---- | ----------------------------------------------- |
| 1.   | Segment landslides using UNet + DEM             |
| 2.   | Detect boulders using YOLOv8                    |
| 3.   | Extract diameter using pixel-mapping            |
| 4.   | Identify source using slope flow + watershed    |
| 5.   | Predict active zone using temporal + DEM change |
| 6.   | Visualize with annotated maps & summary stats   |

---

## 📁 Bonus: Public Resources

| Resource                                                                      | Use                      |
| ----------------------------------------------------------------------------- | ------------------------ |
| [LROC QuickMap](https://quickmap.lroc.asu.edu)                                | Lunar region exploration |
| [ISRO Bhuvan Portal](https://bhuvan.nrsc.gov.in)                              | Chandrayaan data access  |
| [NASA PDS Lunar Orbiter](https://pds-imaging.jpl.nasa.gov/volumes/lunar.html) | DEM & OHRC datasets      |
| [QGIS Plugins](https://plugins.qgis.org)                                      | Terrain, slope, 3D tools |

---

## 📄 Report / Thesis Section Ideas

* Introduction (Lunar geology, importance of boulder/landslide mapping)
* Dataset Description (Chandrayaan-1/2, OHRC, DTM)
* Proposed Method (Your novel fusion pipeline)
* Implementation (code, model, training stats)
* Results (maps, charts, stats)
* Comparison with conventional techniques
* Conclusion + Future Scope (rover path planning, hazard mapping)

