import os
import torch
from torchvision import transforms, datasets
from torch.utils.data import DataLoader, random_split

def get_transforms():
    """Returns data augmentation and normalization transforms."""
    train_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(degrees=15),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
        transforms.RandomAffine(degrees=0, translate=(0.1, 0.1)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    val_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    return train_transform, val_transform

def prepare_data(data_dir, batch_size=32, val_split=0.2):
    """
    Prepares DataLoaders for training and validation.
    Note: Since our current structure is flat (data/images), we might need to 
    restructure it into class-based folders if we want to use ImageFolder,
    or create a custom Dataset class that maps filename to symbol ID.
    """
    train_transform, val_transform = get_transforms()
    
    # For now, let's assume class folders: data/dataset/{class_name}/*.jpg
    # If it's still flat, we'll need a custom dataset.
    # Given we have symbols_data.json, we can map filenames.
    
    try:
        dataset = datasets.ImageFolder(data_dir, transform=train_transform)
        
        train_size = int((1 - val_split) * len(dataset))
        val_size = len(dataset) - train_size
        
        train_dataset, val_dataset = random_split(dataset, [train_size, val_size])
        
        # Apply validation transform to validation dataset
        val_dataset.dataset.transform = val_transform
        
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
        
        return train_loader, val_loader, dataset.classes
    except Exception as e:
        print(f"Error preparing data: {e}")
        return None, None, []

if __name__ == "__main__":
    # Placeholder directory for when we restructure
    prepare_data('data/dataset')
