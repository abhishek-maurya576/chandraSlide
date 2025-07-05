import os
import pandas as pd
from sklearn.model_selection import train_test_split
import yaml
from PIL import Image
import shutil

def create_yolo_dataset(image_dir, label_csv_path, output_dir, train_size=0.8):
    """
    Converts a dataset with CSV-based bounding box labels into the format
    required by YOLOv8.
    """
    print("--- Creating YOLOv8 Dataset ---")

    # Clean and create directories
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        print(f"Removed existing directory: {output_dir}")

    os.makedirs(os.path.join(output_dir, 'images/train'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'images/val'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'labels/train'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'labels/val'), exist_ok=True)
    print("Cleaned and recreated dataset directories.")

    # Read and process labels
    labels_df = pd.read_csv(label_csv_path, header=None)
    labels_df.columns = ['filename', 'xmin', 'ymin', 'xmax', 'ymax', 'class']
    labels_df.dropna(subset=['class'], inplace=True)

    # Get unique filenames and split them
    unique_files = labels_df.filename.unique()
    train_files, val_files = train_test_split(unique_files, train_size=train_size, random_state=42)
    file_sets = {'train': train_files, 'val': val_files}

    for split, files in file_sets.items():
        print(f"Processing {split} set...")
        for filename in files:
            source_img_path = os.path.join(image_dir, filename)
            base_filename = os.path.splitext(filename)[0]
            dest_img_filename = f"{base_filename}.jpg"
            dest_img_path = os.path.join(output_dir, 'images', split, dest_img_filename)
            
            try:
                # Open image, get dimensions, and save as 3-channel JPEG
                with Image.open(source_img_path) as img:
                    img_width, img_height = img.size
                    rgb_img = img.convert('RGB')
                    rgb_img.save(dest_img_path, 'jpeg')

                # Get labels for this image
                records = labels_df[labels_df.filename == filename]
                label_filename = f"{base_filename}.txt"
                label_path = os.path.join(output_dir, 'labels', split, label_filename)
                
                # Write YOLO label file
                with open(label_path, 'w') as f:
                    for _, row in records.iterrows():
                        # Convert bbox to YOLO format
                        x_center = (row.xmin + row.xmax) / 2 / img_width
                        y_center = (row.ymin + row.ymax) / 2 / img_height
                        width = (row.xmax - row.xmin) / img_width
                        height = (row.ymax - row.ymin) / img_height
                        class_id = 0  # Assuming 'rockfall' is the only class (class_id 0)
                        f.write(f"{class_id} {x_center} {y_center} {width} {height}\n")
            except FileNotFoundError:
                print(f"Warning: Image file not found, skipping: {source_img_path}")
            except Exception as e:
                print(f"Error processing file {filename}: {e}")

    # Create dataset.yaml file
    class_names = ['rockfall']
    yaml_path = os.path.join(output_dir, 'dataset.yaml')
    yaml_data = {
        'path': os.path.abspath(output_dir),
        'train': 'images/train',
        'val': 'images/val',
        'names': {i: name for i, name in enumerate(class_names)}
    }
    with open(yaml_path, 'w') as f:
        yaml.dump(yaml_data, f, sort_keys=False)

    print(f"Created dataset.yaml at {yaml_path}")
    print("--- YOLOv8 Dataset Creation Complete ---")

if __name__ == '__main__':
    # These paths are relative to the project root where you run the script
    LUNAR_IMAGE_DIR = 'moon/train_images'
    LUNAR_LABEL_CSV = 'moon/train_labels/train_labels_m.csv'
    OUTPUT_YOLO_DIR = 'data/yolo_moon_dataset'

    create_yolo_dataset(LUNAR_IMAGE_DIR, LUNAR_LABEL_CSV, OUTPUT_YOLO_DIR) 