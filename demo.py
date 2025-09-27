#!/usr/bin/env python3
"""
Demo script showing how to use the background removal functionality programmatically
"""

import os
import time
from rembg import remove, new_session
from PIL import Image
import requests

def demo_single_image():
    """Demo: Remove background from a single image"""
    print("🎯 Demo: Single Image Background Removal")
    print("-" * 40)
    
    # Create a sample image (you can replace this with your own image path)
    sample_image_path = "sample_image.jpg"
    
    if not os.path.exists(sample_image_path):
        print(f"❌ Sample image '{sample_image_path}' not found")
        print("💡 Place an image file named 'sample_image.jpg' in this directory to test")
        return False
    
    # Initialize rembg session
    print("🤖 Initializing AI model...")
    session = new_session('u2net')
    
    # Process the image
    print(f"🔄 Processing {sample_image_path}...")
    start_time = time.time()
    
    try:
        with open(sample_image_path, 'rb') as input_file:
            input_data = input_file.read()
        
        output_data = remove(input_data, session=session)
        
        output_path = "demo_output.png"
        with open(output_path, 'wb') as output_file:
            output_file.write(output_data)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        print(f"✅ Background removed successfully!")
        print(f"📁 Output saved as: {output_path}")
        print(f"⏱️  Processing time: {processing_time:.2f} seconds")
        
        # Show image info
        with Image.open(output_path) as img:
            print(f"📊 Output image size: {img.size}")
            print(f"🎨 Output image mode: {img.mode}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error processing image: {e}")
        return False

def demo_batch_processing():
    """Demo: Batch process multiple images"""
    print("\n🎯 Demo: Batch Processing")
    print("-" * 40)
    
    # Create input and output directories
    input_dir = "demo_input"
    output_dir = "demo_output"
    
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    # Check if there are images in input directory
    image_files = [f for f in os.listdir(input_dir) 
                   if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    
    if not image_files:
        print(f"❌ No images found in '{input_dir}' directory")
        print("💡 Place some images in the 'demo_input' directory to test batch processing")
        return False
    
    print(f"📁 Found {len(image_files)} images in '{input_dir}'")
    
    # Initialize rembg session
    session = new_session('u2net')
    
    # Process each image
    successful = 0
    start_time = time.time()
    
    for i, filename in enumerate(image_files, 1):
        input_path = os.path.join(input_dir, filename)
        output_filename = f"processed_{filename}"
        output_path = os.path.join(output_dir, output_filename)
        
        print(f"[{i}/{len(image_files)}] Processing: {filename}", end=" ... ")
        
        try:
            with open(input_path, 'rb') as input_file:
                input_data = input_file.read()
            
            output_data = remove(input_data, session=session)
            
            with open(output_path, 'wb') as output_file:
                output_file.write(output_data)
            
            print("✅")
            successful += 1
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"\n📊 Batch processing complete!")
    print(f"✅ Successful: {successful}/{len(image_files)}")
    print(f"⏱️  Total time: {total_time:.2f} seconds")
    print(f"📁 Results saved in: {output_dir}")
    
    return successful > 0

def demo_different_models():
    """Demo: Compare different AI models"""
    print("\n🎯 Demo: Different AI Models")
    print("-" * 40)
    
    sample_image_path = "sample_image.jpg"
    if not os.path.exists(sample_image_path):
        print(f"❌ Sample image '{sample_image_path}' not found")
        return False
    
    models = [
        ('u2net', 'General purpose (best quality)'),
        ('u2netp', 'Lighter version (faster)'),
        ('u2net_human_seg', 'Optimized for people'),
    ]
    
    print("🤖 Testing different AI models...")
    
    for model_name, description in models:
        print(f"\n🔄 Testing {model_name} - {description}")
        
        try:
            session = new_session(model_name)
            
            start_time = time.time()
            with open(sample_image_path, 'rb') as input_file:
                input_data = input_file.read()
            
            output_data = remove(input_data, session=session)
            
            output_path = f"demo_{model_name}_output.png"
            with open(output_path, 'wb') as output_file:
                output_file.write(output_data)
            
            end_time = time.time()
            processing_time = end_time - start_time
            
            print(f"✅ {model_name}: {processing_time:.2f}s - saved as {output_path}")
            
        except Exception as e:
            print(f"❌ {model_name}: Error - {e}")

def main():
    """Main demo function"""
    print("🎨 Background Remover - Demo Script")
    print("=" * 50)
    
    # Check if rembg is available
    try:
        import rembg
        print("✅ Rembg library is available")
    except ImportError:
        print("❌ Rembg library not found. Please install: pip install rembg")
        return
    
    # Run demos
    demos = [
        ("Single Image Processing", demo_single_image),
        ("Batch Processing", demo_batch_processing),
        ("Different AI Models", demo_different_models),
    ]
    
    for demo_name, demo_func in demos:
        print(f"\n{'='*20} {demo_name} {'='*20}")
        try:
            demo_func()
        except KeyboardInterrupt:
            print("\n⏹️  Demo interrupted by user")
            break
        except Exception as e:
            print(f"❌ Demo failed: {e}")
    
    print(f"\n🎉 Demo completed!")
    print("💡 Check the generated output files to see the results")

if __name__ == "__main__":
    main()
