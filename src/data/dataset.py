import torch
from torch.utils.data import Dataset
import numpy as np
import os
from PIL import Image

class LunarDataset(Dataset):
    """
    PyTorch Dataset for loading lunar data patches for semantic segmentation.
    This dataset loads multi-channel image tiles (.npy) and their
    corresponding single-channel segmentation masks (.png).
    """
    def __init__(self, data_dir, masks_dir, transform=None):
        """
        Args:
            data_dir (str): Directory path containing the fused data tiles (.npy files).
            masks_dir (str): Directory path containing the ground-truth mask tiles (.png files).
            transform (callable, optional): Optional transform to be applied on a sample.
        """
        self.data_dir = data_dir
        self.masks_dir = masks_dir
        self.transform = transform
        
        self.data_files = sorted([os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith('.npy')])
        self.mask_files = sorted([os.path.join(masks_dir, f) for f in os.listdir(masks_dir) if f.endswith('.png')])

        if not self.data_files or not self.mask_files:
            raise RuntimeError(f"No data found. Check data_dir '{data_dir}' and masks_dir '{masks_dir}'.")
            
        if len(self.data_files) != len(self.mask_files):
            raise ValueError("Number of data files and mask files do not match.")

    def __len__(self):
        return len(self.data_files)

    def __getitem__(self, idx):
        """
        Fetches the data and mask for a given index.
        """
        # Load the multi-channel fused data tile
        fused_data = np.load(self.data_files[idx])

        # Load the single-channel mask tile
        mask = np.array(Image.open(self.mask_files[idx]))
        
        # Convert to PyTorch Tensors
        # The UNet expects float tensors for data and long tensors for masks
        fused_data = torch.from_numpy(fused_data).float()
        mask = torch.from_numpy(mask).long()
        
        sample = {'data': fused_data, 'mask': mask}

        if self.transform:
            sample = self.transform(sample)

        return sample

if __name__ == '__main__':
    # This block demonstrates how to use the updated LunarDataset class.
    print("Running updated LunarDataset demonstration...")

    # Create dummy directories and files that mimic the output of prepare_training_data.py
    os.makedirs('dummy_processed/segmentation', exist_ok=True)
    os.makedirs('dummy_labeled/segmentation', exist_ok=True)

    for i in range(5):
        # Create a dummy 3-channel .npy image file
        dummy_image = np.random.rand(3, 256, 256).astype(np.float32)
        np.save(f'dummy_processed/segmentation/tile_{i}.npy', dummy_image)
        
        # Create a dummy single-channel .png mask file
        dummy_mask = np.random.randint(0, 3, (256, 256), dtype=np.uint8)
        Image.fromarray(dummy_mask).save(f'dummy_labeled/segmentation/tile_{i}.png')
    
    # Instantiate the dataset
    lunar_dataset = LunarDataset(
        data_dir='dummy_processed/segmentation', 
        masks_dir='dummy_labeled/segmentation'
    )

    print(f"Dataset size: {len(lunar_dataset)}")

    # Get a sample
    sample = lunar_dataset[0]
    data_sample, mask_sample = sample['data'], sample['mask']
    
    print(f"Sample data shape: {data_sample.shape}")
    print(f"Sample mask shape: {mask_sample.shape}")
    print(f"Sample data type: {data_sample.dtype}")
    print(f"Sample mask type: {mask_sample.dtype}")
    
    # Verify the output types
    assert data_sample.dtype == torch.float32
    assert mask_sample.dtype == torch.long

    # Clean up
    import shutil
    shutil.rmtree('dummy_processed')
    shutil.rmtree('dummy_labeled')
    
    print("Updated LunarDataset demonstration finished successfully.")

