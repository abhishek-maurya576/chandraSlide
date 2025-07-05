# 🌑 Project Overview

**Project ChandraSlide** is a scientific research and development initiative at the intersection of artificial intelligence and planetary science. As a project developed by an AI/ML Developer and ISRO Scientist, its primary mission is to create a novel system for the automated detection and analysis of landslides and boulder falls on the Moon.

## Core Objective

The project aims to process high-resolution satellite imagery from India's **Chandrayaan-1 and Chandrayaan-2 missions** to identify and map geological surface events. This contributes critical data for future lunar exploration, enhancing the safety and efficiency of mission planning.

## Novelty and Approach

The core of the project is a custom-built AI pipeline named **PRAJNA Fusion-Net**. The novelty of this system lies in its multi-modal approach to data analysis.

Instead of relying on purely visual information from optical images, our pipeline fuses three distinct types of data for a more holistic and physically-informed understanding of the lunar terrain:

1.  **High-Resolution Optical Imagery (OHRC):** Provides the fine-grained visual texture for identifying features.
2.  **Digital Terrain Models (DTM):** Provides 3D elevation data.
3.  **Derived Slope Maps:** Calculated from the DTM to give the model an intrinsic understanding of surface geology and gravity's potential influence.

By training our models on this fused data, the system learns to recognize not just "what a landslide looks like," but "the geological context in which a landslide occurs." This significantly improves detection accuracy and reduces false positives.

Furthermore, the project incorporates advanced analytical modules to:
-   **Estimate Boulder Dimensions:** Calculates boulder height and volume by analyzing shadow lengths, a novel application of planetary science principles in an automated AI workflow.
-   **Identify Landslide Sources:** Traces detected landslides uphill on the DTM to pinpoint their likely origin points.
-   **Map Active Regions:** Prepares for temporal analysis by comparing historical and recent images to identify newly formed features.


