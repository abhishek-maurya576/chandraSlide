# 🛠️ Developer Guide

This guide provides technical instructions for setting up the development environment, training the models, and contributing to the `Project ChandraSlide` codebase.

## 1. Environment Setup

A `conda` environment is recommended to manage project dependencies and ensure reproducibility.

### Prerequisites
- Python 3.8+
- [Anaconda](https://www.anaconda.com/products/distribution) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html).
- `git` for cloning the repository.

### Installation Steps

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd ChandraSlide
    ```

2.  **Create and activate the Conda environment:**
    ```bash
    conda create --name chandraslide python=3.9
    conda activate chandraslide
    ```

3.  **Install Python dependencies:**
    The `requirements.txt` file lists all necessary packages.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Install PyTorch with GPU Support (Recommended):**
    For optimal performance, it is crucial to install a version of PyTorch that is compatible with your system's CUDA toolkit. Follow the official, platform-specific instructions at [pytorch.org/get-started/locally/](https://pytorch.org/get-started/locally/).

5.  **Install Geospatial Libraries (GDAL):**
    `GDAL` can sometimes have complex dependencies. If `pip install gdal` fails, it is often easier to install it via `conda`:
    ```bash
    conda install -c conda-forge gdal
    ```

## 2. Data Preparation

The AI models require data to be in a specific format.

1.  **Raw Data:** Place your raw Chandrayaan data (e.g., OHRC `.tif` files and DTM `.tif` files) into the `data/raw/` directory.
2.  **Preprocessing:** Run the preprocessing script to align, fuse, and generate slope maps from your raw data.
    ```bash
    # (Future Implementation Step)
    python src/data/run_preprocessing.py --input-dir data/raw/ --output-dir data/processed/
    ```
3.  **Labeling:** For training custom models, labeled data is required. Landslide masks and boulder bounding boxes should be placed in `data/labeled/`.

## 3. Model Training

The project includes separate scripts for training the different models.

### Landslide Segmentation (UNet)
-   Once your processed data and labels are ready, you can start the training process by running:
    ```bash
    python src/training/train.py
    ```
-   Model weights will be saved to the `models/` directory.

### Boulder Detection (YOLOv8)
-   The YOLOv8 model requires a specific dataset format (images and `.txt` label files) and a `data.yaml` configuration file.
-   Once the dataset is prepared, initiate training with:
    ```bash
    python src/models/yolov8.py
    ```

## 4. Code Contribution

-   **Branching:** Create a new feature branch for any additions (`git checkout -b feature/my-new-feature`).
-   **Docstrings:** All new functions and classes should include a comprehensive docstring explaining their purpose, arguments, and return values.
-   **Testing:** Ensure that your changes do not break existing functionality. Run the demonstration blocks in each script to confirm.
-   **Pull Requests:** Submit a pull request with a clear description of the changes made.


