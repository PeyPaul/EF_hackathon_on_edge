import os
import json
import cv2
from parser import get_elements, show_frame_with_elements

path = "../big_dataset"

# Load metadata
with open(f"{path}/metadata.json", "r") as f:
    metadata = json.load(f)

def serialize_element(element):
    return {
        "x": element.x,
        "y": element.y,
        "w": element.w,
        "h": element.h,
        "text": element.text
    }

def serialize_entry(entry):
    return {
        "from_city": entry["from_city"],
        "to_city": entry["to_city"],
        "from_date": entry["from_date"],
        "to_date": entry["to_date"],
        "elements": [serialize_element(element) for element in entry["elements"]]
    }

# Process first 80 entries
for entry in metadata:
    entry["elements"] = []
    # Save metadata
    with open(f"{path}/metadata_parsed.json", "w") as f:
        json.dump(metadata, f, indent=4)

    for timestamp in entry["timestamps"]:
        # Original filename is just timestamp + .png
        orig_filename = f"{timestamp}.png"
        
        if os.path.exists(f"{path}/{orig_filename}"):
            # Create new filename with _parsed before extension
            new_filename = f"{timestamp}_parsed.png"
            
            # Open, process and save image
            try:
                elements = get_elements(f"{path}/{orig_filename}")
                entry["elements"] += [[serialize_element(element) for element in elements]]
                # Save with _parsed suffix
                img = show_frame_with_elements(f"{path}/{orig_filename}", elements)
                cv2.imwrite(f"{path}/{new_filename}", img)
                print(f"Processed {orig_filename} -> {new_filename}")
            except Exception as e:
                print(f"Error processing {orig_filename}: {e}")
        else:
            print(f"File not found: {orig_filename}")

