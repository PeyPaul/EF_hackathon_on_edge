import json
import glob
import os

def merge_json_files(folder_path):
    """
    Merge multiple JSON files containing lists of images, suffixes, and prefixes.
    Each JSON file should have the format: {"images": [...], "suffixes": [...], "prefixes": [...]}
    
    Args:
        folder_path (str): Path to the folder containing JSON files
        
    Returns:
        dict: Merged JSON data with concatenated lists
    """
    # Initialize the merged data structure
    merged_data = {
        "images": [],
        "suffixes": [],
        "prefixes": []
    }
    
    # Find all JSON files in the folder
    json_files = glob.glob(os.path.join(folder_path, "*.json"))
    
    # Process each JSON file
    for json_file in json_files:
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
                
            # Extend each list with the data from the current file
            merged_data["images"].extend(f"runs/{data['images']}")
            merged_data["suffixes"].extend(data["suffixes"])
            merged_data["prefixes"].extend(data["prefixes"])
            
            print(f"Successfully processed: {json_file}")
            
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in {json_file}")
        except KeyError as e:
            print(f"Error: Missing required key {e} in {json_file}")
        except Exception as e:
            print(f"Error processing {json_file}: {str(e)}")
    
    # Save the merged data to a new JSON file
    output_path = os.path.join(folder_path, "merged_output.json")
    with open(output_path, 'w') as f:
        json.dump(merged_data, f, indent=2)
    
    print(f"\nMerged data saved to: {output_path}")
    print(f"Total items merged:")
    print(f"Images: {len(merged_data['images'])}")
    print(f"Suffixes: {len(merged_data['suffixes'])}")
    print(f"Prefixes: {len(merged_data['prefixes'])}")
    
    return merged_data

# Example usage
if __name__ == "__main__":
    folder_path = "runs"  # Replace with your folder path if different
    merged_data = merge_json_files(folder_path)