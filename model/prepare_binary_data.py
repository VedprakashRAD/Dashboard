import os

def convert_to_binary(labels_dir):
    """Converts all YOLO labels to a single class (0)."""
    if not os.path.exists(labels_dir):
        print(f"Labels directory not found: {labels_dir}")
        return

    label_files = [f for f in os.listdir(labels_dir) if f.endswith('.txt')]
    for filename in label_files:
        path = os.path.join(labels_dir, filename)
        with open(path, 'r') as f:
            lines = f.readlines()
        
        new_lines = []
        for line in lines:
            parts = line.strip().split()
            if parts:
                parts[0] = '0' # Set class to 0
                new_lines.append(" ".join(parts))
        
        with open(path, 'w') as f:
            f.write("\n".join(new_lines) + "\n")
    
    print(f"Converted {len(label_files)} label files to binary.")

if __name__ == "__main__":
    convert_to_binary('data/yolo_dataset/labels')
