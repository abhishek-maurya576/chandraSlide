# Project ChandraSlide: AI-Powered Lunar Landslide & Boulder Detection

Welcome to **Project ChandraSlide**, a research initiative to automate the detection and analysis of landslides and boulder falls on the Moon using deep learning and data from the Chandrayaan missions.

This repository contains all the source code for the project's multi-modal AI pipeline, **PRAJNA Fusion-Net**, and the interactive **PRAJNA Dashboard** for visualizing the results.

---

## 📚 Full Documentation

This README provides a brief overview. For detailed information on the project's architecture, setup, usage, and contribution guidelines, please see the full documentation:

### **[➡️ Go to the Full Documentation](./docs/index.md)**

---

## 🚀 Quick Start

To launch the interactive dashboard directly:

1.  Ensure you have followed the setup instructions in the [Developer Guide](./docs/developer_guide.md).
2.  Run the following command from the project root:

    ```bash
    streamlit run dashboard/app.py
    ```

---

## ☁️ Training on Google Colab

Since training a deep learning model requires significant GPU resources, it is highly recommended to use Google Colab.

### 1. Data Setup on Google Drive

Because the dataset is too large to be stored on GitHub, you need to upload it to your Google Drive.

1.  Upload your raw dataset folders (e.g., `moon`, `mars`) to a directory in your Google Drive. For example, you might have it at `My Drive/ChandraSlide/datasets/`.

### 2. Colab Notebook Setup

1.  Open Google Colab and create a new notebook.
2.  **Clone the repository** into your Colab environment:
    ```python
    !git clone https://github.com/abhishek-maurya576/chandraSlide.git
    %cd chandraSlide
    ```
3.  **Mount your Google Drive** to access the dataset:
    ```python
    from google.colab import drive
    drive.mount('/content/drive')
    ```
4.  **Create the necessary directory structure** and **copy the dataset** from your Drive into the cloned repository. This makes the files accessible to the training scripts.
    ```python
    # Create the directory for raw data
    !mkdir -p data/raw

    # Adjust the source path to match where you stored the data in your Drive
    # This command copies the 'moon' folder into the 'data/raw/' directory
    !cp -r "/content/drive/My Drive/ChandraSlide/datasets/moon" data/raw/
    ```
5.  **Install the required dependencies**:
    ```python
    !pip install -r requirements.txt
    ```

### 3. Run Training

You are now ready to run the data preparation and training scripts.

1.  **Prepare the data for YOLOv8:**
    ```python
    !python -m src.data.prepare_yolo_data
    ```
2.  **Start the training process:**
    ```python
    # This first line helps prevent a common library conflict error in Colab
    import os
    os.environ['KMP_DUPLICATE_LIB_OK']='True'

    !python -m src.models.yolov8
    ```

The trained model will be saved in the `runs/` directory inside your Colab environment. You can then download it back to your local machine.

---

## Dataset

This project uses a dataset for lunar landslides.

### Citation

Please cite this dataset as:

```
A labeled training and testing dataset for deep learning-driven rockfall detection on the Moon and Mars
Bickel, V. T., Mandrake, L., and Doran, G.
Jet Propulsion Laboratory, Machine Learning and Instrument Autonomy Group, Pasadena, CA, USA
Max Planck Institute for Solar System Research, Department Planets and Comets, Goettingen, Germany
ETH Zurich, Department of Earth Sciences, Zurich, Switzerland

Correspondence: V. T. Bickel: bickel@mps.mpg.de / vbickel@jpl.nasa.gov

doi:   https://doi.org/10.3389/frsen.2021.640034
```

### Structure

The data is organized as follows:

- `data/raw/`: This directory contains the original, unaltered datasets (e.g., `moon/`, `mars/`). This data is not tracked by Git.
- `data/processed/`: This directory contains datasets that have been cleaned, transformed, or otherwise prepared for model training (e.g., `yolo_moon_dataset/`). The processed data files are not tracked by Git, but the directory structure and any configuration files are.

An example structure for the raw moon dataset is:

-   **Location:** `data/raw/moon/`
-   **Training Images:** `data/raw/moon/train_images/` (contains `.tif` files)
-   **Training Labels:** `data/raw/moon/train_labels/` (contains `train_classes_m.csv` and `train_labels_m.csv`)
-   **Test Images:** `data/raw/moon/test_images/` (contains `.tif` files)
-   **Test Labels:** `data/raw/moon/test_labels/` (contains `test_classes_m.csv` and `test_labels_m.csv`)

### Manual Installation Steps

A key component of this project, **GDAL (Geospatial Data Abstraction Library)**, is used for processing orbital imagery. Due to its complex nature as a C++ library, it cannot be installed with a simple `pip install`. Please follow these steps carefully.

**1. Determine Python Version and Architecture**

You must match the GDAL version to your specific Python interpreter. First, activate your project's virtual environment. Then, run the following command:

```bash
python -c "import sys; print(sys.version)"
```

Look for two pieces of information:
- **Python Version:** e.g., `3.8.10` (you need `3.8`).
- **Architecture:** e.g., `64 bit (AMD64)` (you need a `win_amd64` file) or `32 bit` (you need a `win32` file).

**2. Download the GDAL Wheel File**

Go to the [Unofficial Windows Binaries for Python Extension Packages](https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal) website.

Find the section for **GDAL**. Download the wheel (`.whl`) file that matches your specifications. The filename format is `GDAL‑[version]‑cp[python_version]‑cp[python_version]‑[architecture].whl`.

*   `cp38` corresponds to Python 3.8.
*   `win_amd64` corresponds to 64-bit.
*   `win32` corresponds to 32-bit.

For example, for Python 3.8 (64-bit), you would download a file like `GDAL‑3.4.3‑cp38‑cp38‑win_amd64.whl`.

**3. Install the Wheel File**

Navigate your terminal to the directory where you downloaded the wheel file. Then, run the following command, replacing the filename with the one you downloaded:

```bash
pip install GDAL-3.4.3-cp38-cp38-win_amd64.whl
```

**4. Set Environment Variables**

GDAL needs two environment variables to locate its essential data files.

*   **For Windows:**
    You can set these permanently through the System Properties dialog, or temporarily in your command prompt for the current session:
    ```cmd
    set GDAL_DATA=[PATH_TO_YOUR_PYTHON_ENV]\Lib\site-packages\osgeo\data\gdal
    set PROJ_LIB=[PATH_TO_YOUR_PYTHON_ENV]\Lib\site-packages\osgeo\data\proj
    ```
    Replace `[PATH_TO_YOUR_PYTHON_ENV]` with the actual path to your Python environment (e.g., `C:\Users\YourUser\my-env`).

*   **For Linux/macOS:**
    ```bash
    export GDAL_DATA=[PATH_TO_YOUR_PYTHON_ENV]/lib/python3.8/site-packages/osgeo/data/gdal
    export PROJ_LIB=[PATH_TO_YOUR_PYTHON_ENV]/lib/python3.8/site-packages/osgeo/data/proj
    ```

**5. Verify Installation**

After completing the steps above, you can verify the installation by running:

```bash
python -c "from osgeo import gdal; print(gdal.__version__)"
```

If this command prints the GDAL version number without any errors, the installation was successful.
