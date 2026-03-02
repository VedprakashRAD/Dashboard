import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import models
from preprocess import prepare_data
import os

def train_model(data_dir, num_epochs=20, learning_rate=0.001):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if torch.backends.mps.is_available():
        device = torch.device("mps")
    
    print(f"Using device: {device}")

    # Prepare data
    train_loader, val_loader, class_names = prepare_data(data_dir)
    if train_loader is None or len(class_names) == 0:
        print("Data preparation failed. Exiting.")
        return

    num_classes = 89 # Fixed as per our symbols_data.json
    
    # Load pre-trained ResNet-18
    model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
    
    # Freeze initial layers (Transfer Learning)
    for param in model.parameters():
        param.requires_grad = False
        
    # Replace final layer
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, num_classes)
    
    model = model.to(device)

    # Loss and Optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.fc.parameters(), lr=learning_rate)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=num_epochs)

    # Training Loop
    print("Starting training...")
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
        
        scheduler.step()
        epoch_loss = running_loss / len(train_loader.dataset)
        
        # Validation
        model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
        
        acc = 100 * correct / total
        print(f"Epoch {epoch+1}/{num_epochs} - Loss: {epoch_loss:.4f} - Val Acc: {acc:.2f}%")
        
        if acc > best_acc:
            best_acc = acc
            torch.save(model.state_dict(), 'model/best_symbol_model.pth')
            print("Model saved.")

    print(f"Training complete. Best Val Acc: {best_acc:.2f}%")

if __name__ == "__main__":
    train_model('data/dataset')
