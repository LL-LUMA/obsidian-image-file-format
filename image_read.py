import argparse
import json
from pathlib import Path

def load_color_data(json_path):
    """Load color data from JSON file"""
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
            # Create a lookup dictionary for hex codes to names
            return {color['hex'].upper(): color['name'] for color in data['colors']}
    except FileNotFoundError:
        print(f"Error: Color data file '{json_path}' not found.")
        exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in file '{json_path}'.")
        exit(1)
    except Exception as e:
        print(f"Error loading color data: {str(e)}")
        exit(1)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Process file content with color matching')
    parser.add_argument('--image', type=str, required=True, help='Path to the file to process')
    
    # Path to the JSON color data file (change this to your actual path)
    COLOR_JSON_PATH = Path('C:/obsidian/.hex/pixels.json')  # Assuming it's in the same directory
    
    # Load color data
    color_map = load_color_data(COLOR_JSON_PATH)
    
    # Parse arguments
    args = parser.parse_args()
    
    try:
        with open(args.image, 'r') as file:
            # Skip the first line and read the rest
            lines = file.readlines()[1:]
            
            # Combine all lines into a single string, remove '|' characters, and remove newlines
            content = ''.join(line.strip().replace('|', '') for line in lines)
            
            # Split into chunks of 6 characters each
            chunk_size = 6
            chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
            
            # Display file info
            print(f"\nProcessing file: {args.image}")
            print(f"Using color data from: {COLOR_JSON_PATH}")
            print(f"Skipped first line. Removed '|' characters. Found {len(chunks)} chunks of {chunk_size} characters each:\n")
            
            # Display and store each chunk with color names
            variables = {}
            for chunk in chunks:
                hex_code = f"#{chunk}"
                color_name = color_map.get(hex_code.upper())
                var_name = f"pixel_{color_name}" if color_name else f"var_unknown_{chunk}"
                variables[var_name] = hex_code
                print(f"{var_name}: {hex_code}")
            
    except FileNotFoundError:
        print(f"Error: The file '{args.image}' was not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()