import torch
import torch.nn as nn
from torch.utils.data import DataLoader, random_split
import torch.optim as optim
from tqdm import tqdm
import os
import numpy as np

from src.models.unet import UNet
from src.data.dataset import LunarDataset

# --- Configuration ---
DATA_DIR = 'data/processed/segmentation'
MASKS_DIR = 'data/labeled/segmentation'
MODEL_SAVE_PATH = 'models/unet_landslide_detector_best.pth'
NUM_CLASSES = 3
INPUT_CHANNELS = 3
LEARNING_RATE = 1e-4
BATCH_SIZE = 8
NUM_EPOCHS = 50
VALIDATION_SPLIT = 0.2

def evaluate_model(model, device, val_loader, criterion):
    """
    Evaluates the model on the validation set.
    """
    model.eval() # Set model to evaluation mode
    epoch_loss = 0
    with torch.no_grad():
        for batch in tqdm(val_loader, desc='Validating', leave=False):
            data = batch['data'].to(device)
            masks = batch['mask'].to(device)
            
            outputs = model(data)
            loss = criterion(outputs, masks)
            epoch_loss += loss.item()
            
    return epoch_loss / len(val_loader)

def main():
    """
    Main function to orchestrate the training and validation process.
    """
    print("--- Starting Professional Training Pipeline ---")

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")

    # --- Data Loading and Splitting ---
    print("Loading and splitting dataset...")
    try:
        dataset = LunarDataset(data_dir=DATA_DIR, masks_dir=MASKS_DIR)
    except (RuntimeError, ValueError) as e:
        print(f"\nERROR: Could not load dataset. {e}")
        print("Please ensure you have run the 'prepare_training_data.py' script on your labeled data first.")
        return

    val_size = int(len(dataset) * VALIDATION_SPLIT)
    train_size = len(dataset) - val_size
    train_set, val_set = random_split(dataset, [train_size, val_size])

    train_loader = DataLoader(train_set, batch_size=BATCH_SIZE, shuffle=True, num_workers=4, pin_memory=True)
    val_loader = DataLoader(val_set, batch_size=BATCH_SIZE, shuffle=False, num_workers=4, pin_memory=True)
    print(f"Dataset loaded: {len(train_set)} training samples, {len(val_set)} validation samples.")

    # --- Model, Optimizer, and Loss Function ---
    print("Initializing model, optimizer, and loss function...")
    model = UNet(n_channels=INPUT_CHANNELS, n_classes=NUM_CLASSES).to(device)
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE, weight_decay=1e-8)
    criterion = nn.CrossEntropyLoss()

    # --- Training Loop ---
    print("Starting training loop...")
    best_val_loss = float('inf')
    
    for epoch in range(NUM_EPOCHS):
        model.train()
        train_loss = 0
        
        # Training loop with progress bar
        for batch in tqdm(train_loader, desc=f'Epoch {epoch+1}/{NUM_EPOCHS} [Training]', leave=True):
            data = batch['data'].to(device)
            masks = batch['mask'].to(device)
            
            optimizer.zero_grad()
            outputs = model(data)
            loss = criterion(outputs, masks)
            loss.backward()
            optimizer.step()
            train_loss += loss.item()
        
        avg_train_loss = train_loss / len(train_loader)
        
        # Validation loop
        avg_val_loss = evaluate_model(model, device, val_loader, criterion)
        
        print(f"Epoch {epoch+1}/{NUM_EPOCHS} -> Train Loss: {avg_train_loss:.4f}, Val Loss: {avg_val_loss:.4f}")
        
        # Save the best model
        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)
            torch.save(model.state_dict(), MODEL_SAVE_PATH)
            print(f"  -> New best model saved to {MODEL_SAVE_PATH} (Val Loss: {best_val_loss:.4f})")

    print("\n--- Training Finished ---")
    print(f"Best validation loss: {best_val_loss:.4f}")
    print(f"Best model saved at: {MODEL_SAVE_PATH}")

if __name__ == '__main__':
    # This script is now intended to be run on real data.
    # The LunarDataset class has its own __main__ block for demonstration.
    main()


