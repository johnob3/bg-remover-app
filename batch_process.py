#!/usr/bin/env python3
"""
Batch Background Removal Script

This script allows you to process multiple images at once,
removing backgrounds from all images in a specified folder.

Usage:
    python batch_process.py input_folder output_folder

Example:
    python batch_process.py ./input_images ./output_images
"""

import os
import sys
import glob
import time
from pathlib import Path
from rembg import remove, new_session
from PIL import Image

def get_supported_extensions():
    """Get list of supported image extensions"""
    return {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.tiff', '.tif'}

def is_image_file(filepath):
    """Check if file is a supported image format"""
    return Path(filepath).suffix.lower() in get_supported_extensions()

def get_image_files(folder):
    """Get all image files from a folder"""
    image_files = []
    for ext in get_supported_extensions():
        pattern = os.path.join(folder, f'*{ext}')
        image_files.extend(glob.glob(pattern))
        # Also check uppercase extensions
        pattern = os.path.join(folder, f'*{ext.upper()}')
        image_files.extend(glob.glob(pattern))
    return sorted(list(set(image_files)))

def process_image(input_path, output_path, session):
    """Process a single image to remove background"""
    try:
        with open(input_path, 'rb') as input_file:
            input_data = input_file.read()
        
        output_data = remove(input_data, session=session)
        
        with open(output_path, 'wb') as output_file:
            output_file.write(output_data)
        
        return True, None
    except Exception as e:
        return False, str(e)

def batch_remove_background(input_folder, output_folder, model='u2net'):
    """
    Remove backgrounds from all images in input folder
    
    Args:
        input_folder (str): Path to folder containing input images
        output_folder (str): Path to folder for output images
        model (str): Rembg model to use ('u2net', 'u2netp', 'u2net_human_seg', etc.)
    """
    # Validate input folder
    if not os.path.exists(input_folder):
        print(f"❌ Error: Input folder '{input_folder}' does not exist")
        return False
    
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Get all image files
    image_files = get_image_files(input_folder)
    
    if not image_files:
        print(f"❌ No supported image files found in '{input_folder}'")
        print(f"Supported formats: {', '.join(get_supported_extensions())}")
        return False
    
    print(f"🚀 Starting batch processing...")
    print(f"📁 Input folder: {input_folder}")
    print(f"📁 Output folder: {output_folder}")
    print(f"🤖 Model: {model}")
    print(f"📊 Found {len(image_files)} images to process")
    print("-" * 50)
    
    # Initialize rembg session
    try:
        session = new_session(model)
        print(f"✅ Initialized {model} model")
    except Exception as e:
        print(f"❌ Failed to initialize model: {e}")
        return False
    
    # Process each image
    successful = 0
    failed = 0
    start_time = time.time()
    
    for i, input_path in enumerate(image_files, 1):
        filename = os.path.basename(input_path)
        name, ext = os.path.splitext(filename)
        output_filename = f"{name}_no_bg.png"  # Always save as PNG to preserve transparency
        output_path = os.path.join(output_folder, output_filename)
        
        print(f"[{i}/{len(image_files)}] Processing: {filename}", end=" ... ")
        
        success, error = process_image(input_path, output_path, session)
        
        if success:
            print("✅ Success")
            successful += 1
        else:
            print(f"❌ Failed: {error}")
            failed += 1
    
    # Print summary
    end_time = time.time()
    duration = end_time - start_time
    
    print("-" * 50)
    print(f"📊 Processing complete!")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"⏱️  Total time: {duration:.2f} seconds")
    print(f"⚡ Average time per image: {duration/len(image_files):.2f} seconds")
    
    if successful > 0:
        print(f"🎉 Processed images saved to: {output_folder}")
    
    return successful > 0

def main():
    """Main function to handle command line arguments"""
    if len(sys.argv) < 3:
        print("Usage: python batch_process.py <input_folder> <output_folder> [model]")
        print("\nExamples:")
        print("  python batch_process.py ./input_images ./output_images")
        print("  python batch_process.py ./photos ./results u2net_human_seg")
        print("\nAvailable models:")
        print("  - u2net (default, general purpose)")
        print("  - u2netp (lighter version)")
        print("  - u2net_human_seg (optimized for people)")
        print("  - u2net_cloth_seg (optimized for clothing)")
        print("  - silueta (silhouette detection)")
        sys.exit(1)
    
    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    model = sys.argv[3] if len(sys.argv) > 3 else 'u2net'
    
    # Convert to absolute paths
    input_folder = os.path.abspath(input_folder)
    output_folder = os.path.abspath(output_folder)
    
    success = batch_remove_background(input_folder, output_folder, model)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
