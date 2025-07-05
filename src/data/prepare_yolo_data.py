import os
import pandas as pd
from sklearn.model_selection import train_test_split
import yaml
import shutil

def create_yolo_dataset(image_dir, label_csv_path, output_dir, train_size=0.8):
    """
    Converts a dataset with CSV-based bounding box labels into the format
    required by YOLOv8.

    This involves:
    1. Reading the CSV and image dimensions.
    2. Converting bounding boxes to the YOLO format (class, x_center, y_center, width, height).
    3. Splitting the data into training and validation sets.
    4. Creating the directory structure and .yaml file for YOLO training.
    """
    print("--- Creating YOLOv8 Dataset ---")
    
    # --- Clean and create directories ---
    for subdir in ['images/train', 'images/val', 'labels/train', 'labels/val']:
        dir_path = os.path.join(output_dir, subdir)
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
        os.makedirs(dir_path)

    print("Cleaned and recreated dataset directories.")

    # --- Read and process labels ---
    labels_df = pd.read_csv(label_csv_path, header=None)
    labels_df.columns = ['filename', 'xmin', 'ymin', 'xmax', 'ymax', 'class']
    labels_df.dropna(subset=['class'], inplace=True)
    
    # Get unique filenames and split them
    unique_files = labels_df.filename.unique()
    train_files, val_files = train_test_split(unique_files, train_size=train_size, random_state=42)
    
    file_sets = {'train': train_files, 'val': val_files}
    
    # --- Class mapping ---
    class_names = labels_df['class'].unique().tolist()
    class_to_id = {name: i for i, name in enumerate(class_names)}
    
    print(f"Found classes: {class_names}")

    # --- Process and write labels ---
    for split, files in file_sets.items():
        print(f"Processing {split} set...")
        for filename in files:
            source_img_path = os.path.join(image_dir, filename)
            # Change the extension to .jpg for the destination
            base_filename = os.path.splitext(filename)[0]
            dest_img_path = os.path.join(output_dir, 'images', split, f"{base_filename}.jpg")
            
            from PIL import Image
            
            with Image.open(source_img_path) as img:
                img_width, img_height = img.size
                
                # Convert the image to RGB and save as JPEG
                rgb_img = img.convert('RGB')
                rgb_img.save(dest_img_path, 'jpeg')

            # Get labels for this image
            records = labels_df[labels_df.filename == filename]
            
            # Write YOLO label file, ensuring it has a .txt extension
            label_filename = f"{base_filename}.txt"
            with open(os.path.join(output_dir, 'labels', split, label_filename), 'w') as f:
                for _, row in records.iterrows():
                    class_id = class_to_id[row['class']]
                    
                    # Convert to YOLO format
                    box_width = row['xmax'] - row['xmin']
                    box_height = row['ymax'] - row['ymin']
                    x_center = row['xmin'] + box_width / 2
                    y_center = row['ymin'] + box_height / 2
                    
                    # Normalize
                    x_center /= img_width
                    y_center /= img_height
                    box_width /= img_width
                    box_height /= img_height
                    
                    f.write(f"{class_id} {x_center} {y_center} {box_width} {box_height}\n")

    # --- Create dataset.yaml file ---
    yaml_data = {
        'path': os.path.abspath(output_dir),
        'train': 'images/train',
        'val': 'images/val',
        'names': class_names
    }
    
    yaml_path = os.path.join(output_dir, 'dataset.yaml')
    with open(yaml_path, 'w') as f:
        yaml.dump(yaml_data, f, sort_keys=False)
        
    print(f"--- YOLOv8 Dataset created successfully at {output_dir} ---")
    print(f"YAML configuration file created at {yaml_path}")


if __name__ == '__main__':
    # --- Configuration ---
    MOON_IMAGE_DIR = 'moon/train_images'
    MOON_LABEL_PATH = 'moon/train_labels/train_labels_m.csv'
    OUTPUT_DATA_DIR = 'data/yolo_moon_dataset'

    create_yolo_dataset(
        image_dir=MOON_IMAGE_DIR,
        label_csv_path=MOON_LABEL_PATH,
        output_dir=OUTPUT_DATA_DIR
    ) 