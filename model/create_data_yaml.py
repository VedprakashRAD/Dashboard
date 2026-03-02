import os
import yaml
import json

def create_yaml(dataset_dir, output_file):
    # Load original symbol data
    with open('data/symbols_data.json', 'r') as f:
        symbol_list = json.load(f)
        symbols_dict = {str(s['id']): s['name'] for s in symbol_list}
    
    # Get the same sorted classes as used in synthetic generation/annotation
    # They are subdirectory names (symbol IDs)
    classes = sorted([d for d in os.listdir('data/dataset') if os.path.isdir(os.path.join('data/dataset', d)) and d.isdigit()])
    
    # Map index to name
    names = {i: symbols_dict.get(cls, f"Unknown_{cls}") for i, cls in enumerate(classes)}
    
    data = {
        'path': os.path.abspath(dataset_dir),
        'train': 'images',
        'val': 'images',
        'names': names
    }

    with open(output_file, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)
    
    print(f"Created YOLO manifest with {len(names)} classes.")

if __name__ == "__main__":
    create_yaml('data/yolo_dataset', 'data/yolo_dataset/data.yaml')
