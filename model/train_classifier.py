import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, models, transforms
from torch.utils.data import DataLoader
import os
import json

def train_classifier(data_dir='data/classifier_train_data', num_epochs=30, batch_size=64):
    # Data augmentation for training
    train_transforms = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(15),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    val_transforms = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    # Load dataset
    full_dataset = datasets.ImageFolder(data_dir, transform=train_transforms)
    
    # Split into train and val
    train_size = int(0.8 * len(full_dataset))
    val_size = len(full_dataset) - train_size
    train_dataset, val_dataset = torch.utils.data.random_split(full_dataset, [train_size, val_size])
    
    # Override val transforms
    val_dataset.dataset.transform = val_transforms
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    
    # Model: EfficientNet-B0 or ResNet18
    model = models.resnet18(pretrained=True)
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, len(full_dataset.classes))
    
    # Move to GPU if available
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    model = model.to(device)
    
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    print(f"Starting training for {len(full_dataset.classes)} classes on {device}...")
    
    best_acc = 0.0
    
    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item() * inputs.size(0)
            
        epoch_loss = running_loss / train_size
        
        # Validation
        model.eval()
        correct = 0
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                _, preds = torch.max(outputs, 1)
                correct += torch.sum(preds == labels.data)
        
        val_acc = correct.float() / val_size
        print(f'Epoch {epoch}/{num_epochs - 1} | Loss: {epoch_loss:.4f} | Val Acc: {val_acc:.4f}')
        
        if val_acc > best_acc:
            best_acc = val_acc
            torch.save(model.state_dict(), 'model/weights/best_classifier.pth')
            # Save class mapping
            class_mapping = {i: cls for i, cls in enumerate(full_dataset.classes)}
            with open('model/weights/classifier_mapping.json', 'w') as f:
                json.dump(class_mapping, f)

    print(f'Training complete. Best Val Acc: {best_acc:.4f}')

if __name__ == "__main__":
    train_classifier('data/dataset')
