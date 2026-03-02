import os
import json
from backend.models_manager import get_model_manager

def verify_models():
    # Load symbol data for mapping names
    with open('data/symbols_data.json', 'r') as f:
        symbols_data = json.load(f)
    id_to_name = {str(s['id']): s['name'] for s in symbols_data}
    
    manager = get_model_manager()
    
    test_cases = [
        ("data/dataset/6/battery_charge_warning.jpg", "6"),
        ("data/dataset/7/coolant_temperature_warning_light.jpg", "7"),
        ("data/dataset/8/tire_pressure_warning_light.jpg", "8")
    ]
    
    print(f"{'Path':<60} | {'Expected':<35} | {'Detected':<35} | {'Status'}")
    print("-" * 150)
    
    for path, expected_id in test_cases:
        if not os.path.exists(path):
            print(f"Skipping {path}, file not found.")
            continue
            
        detections = manager.predict(path, confidence=0.1)
        
        detected_names = []
        status = "FAIL"
        
        for det in detections:
            sid = str(det['symbol_id'])
            name = id_to_name.get(sid, f"Unknown({sid})")
            detected_names.append(name)
            if sid == expected_id:
                status = "PASS"
        
        detected_str = ", ".join(detected_names) if detected_names else "None"
        expected_name = id_to_name.get(expected_id, "Unknown")
        
        print(f"{path:<60} | {expected_name:<35} | {detected_str:<35} | {status}")

if __name__ == "__main__":
    verify_models()
