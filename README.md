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

Because the dataset is too large to be stored on GitHub, you need to upload it to your Google Drive first.

1.  Create a zip file of the `moon` directory.
2.  Upload the `moon.zip` file to the root of your Google Drive.

### 2. Colab Notebook Setup

1.  Open Google Colab and create a new notebook.
2.  Clone this GitHub repository into your Colab environment:
    ```python
    !git clone https://github.com/abhishek-maurya576/chandraSlide.git
    %cd chandraSlide
    ```
3.  Mount your Google Drive to access the dataset:
    ```python
    from google.colab import drive
    drive.mount('/content/drive')
    ```
4.  Unzip the dataset from your Drive into the correct location in the cloned repository:
    ```python
    !unzip /content/drive/My\ Drive/moon.zip -d .
    ```
5.  Install the required dependencies:
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
    !python -m src.models.yolov8
    ```

The trained model will be saved in the `models/` directory inside your Colab environment. You can then download it back to your local machine.

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

- `data/`: This directory is intended for processed data, but the raw dataset is currently located in `moon/`.

#### Moon Dataset

-   **Location:** `moon/`
-   **Training Images:** `moon/train_images/` (contains `.tif` files)
-   **Training Labels:** `moon/train_labels/` (contains `train_classes_m.csv` and `train_labels_m.csv`)
-   **Test Images:** `moon/test_images/` (contains `.tif` files)
-   **Test Labels:** `moon/test_labels/` (contains `test_classes_m.csv` and `test_labels_m.csv`)
