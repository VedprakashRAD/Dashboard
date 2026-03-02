import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, models, transforms
from torch.utils.data import DataLoader
import os
import json

def train_professional_classifier(data_dir='data/classifier_train_data', num_epochs=10, batch_size=64):
    # Professional-grade augmentations
    train_transforms = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomAffine(degrees=20, translate=(0.1, 0.1), scale=(0.8, 1.2)),
        transforms.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.3, hue=0.1),
        transforms.RandomGrayscale(p=0.1),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    val_transforms = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    if not os.path.exists(data_dir):
        print(f"Data dir {data_dir} not found. Run expansion script first.")
        return

    full_dataset = datasets.ImageFolder(data_dir, transform=train_transforms)
    train_size = int(0.9 * len(full_dataset))
    val_size = len(full_dataset) - train_size
    train_dataset, val_dataset = torch.utils.data.random_split(full_dataset, [train_size, val_size])
    val_dataset.dataset.transform = val_transforms
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=0)
    
    # Using ResNet50 for higher capacity
    model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
    num_ftrs = model.fc.in_features
    # We have however many folders exist in data_dir
    model.fc = nn.Linear(num_ftrs, len(full_dataset.classes))
    
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    model = model.to(device)
    
    criterion = nn.CrossEntropyLoss()
    # Using a learning rate scheduler for better convergence
    optimizer = optim.AdamW(model.parameters(), lr=0.0001, weight_decay=0.01)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, 'min', patience=5, factor=0.5)
    
    print(f"Starting professional training for {len(full_dataset.classes)} symbols on {device}...")
    
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
        
        model.eval()
        correct = 0
        val_running_loss = 0.0
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                v_loss = criterion(outputs, labels)
                val_running_loss += v_loss.item() * inputs.size(0)
                _, preds = torch.max(outputs, 1)
                correct += torch.sum(preds == labels.data)
        
        val_acc = correct.float() / val_size
        val_epoch_loss = val_running_loss / val_size
        scheduler.step(val_epoch_loss)
        
        print(f'Epoch {epoch}/{num_epochs - 1} | Loss: {epoch_loss:.4f} | Val Acc: {val_acc:.4f} | LR: {optimizer.param_groups[0]["lr"]:.6f}')
        
        if val_acc > best_acc:
            best_acc = val_acc
            torch.save(model.state_dict(), 'model/weights/best_classifier.pth')
            # Save exact mapping used by this ImageFolder
            class_mapping = {i: cls for i, cls in enumerate(full_dataset.classes)}
            with open('model/weights/classifier_mapping.json', 'w') as f:
                json.dump(class_mapping, f)

if __name__ == "__main__":
    train_professional_classifier()
