#!/usr/bin/env python3

import os
import json
from pathlib import Path

def create_tree_json(directory):
    """
    Create a JSON structure from a directory of MDX files.
    Each directory becomes a group, and its MDX files become pages.
    """
    result = {
        "group": os.path.basename(directory).title(),
        "pages": []
    }
    
    try:
        # Sort entries to ensure consistent output
        entries = sorted(os.scandir(directory), key=lambda e: e.name)
        
        for entry in entries:
            # Skip hidden files and special directories
            if entry.name.startswith('.'):
                continue
                
            if entry.is_file() and entry.name.endswith('.mdx'):
                # Add file path without .mdx extension
                file_path = str(Path(entry.path)).replace('\\', '/')  # Normalize path separators
                page_path = file_path[:-4]  # Remove .mdx extension
                result["pages"].append(page_path)
                
            elif entry.is_dir():
                # Recursively process subdirectories
                subdirectory = create_tree_json(entry.path)
                if subdirectory["pages"]:  # Only add if there are MDX files
                    result["pages"].append(subdirectory)
    
    except Exception as e:
        print(f"Error processing directory {directory}: {e}")
        return result
    
    return result

def main():
    start_dir = "api-reference"
    if not os.path.exists(start_dir):
        print(f"Error: Directory '{start_dir}' not found")
        return
    
    tree = create_tree_json(start_dir)
    # Print formatted JSON
    print(json.dumps(tree, indent=2))

if __name__ == "__main__":
    main() 