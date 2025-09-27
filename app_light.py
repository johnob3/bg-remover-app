import os
import base64
import time
from flask import Flask, request, jsonify, render_template, send_file
from werkzeug.utils import secure_filename
from PIL import Image
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024  # 8MB max file size (reduced)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'

# Create directories if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def remove_background_simple(image_path, output_path):
    """Simple background removal using PIL (fallback method)"""
    try:
        # Open the image
        with Image.open(image_path) as img:
            # Convert to RGBA if not already
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Get image data
            data = img.getdata()
            
            # Create new data with transparent background
            new_data = []
            for item in data:
                # Simple threshold-based background removal
                # If pixel is close to white/light colors, make it transparent
                if item[0] > 240 and item[1] > 240 and item[2] > 240:
                    new_data.append((255, 255, 255, 0))  # Transparent
                else:
                    new_data.append(item)
            
            # Update image data
            img.putdata(new_data)
            
            # Save as PNG to preserve transparency
            img.save(output_path, 'PNG')
            return True
            
    except Exception as e:
        logger.error(f"Error in simple background removal: {str(e)}")
        return False

def remove_background_rembg_light(image_path, output_path):
    """Lightweight background removal using rembg with smaller model"""
    try:
        # Import rembg only when needed to save memory
        from rembg import remove, new_session
        
        # Use a smaller, lighter model
        session = new_session('u2netp')  # Smaller model than u2net
        
        with open(image_path, 'rb') as input_file:
            input_data = input_file.read()
        
        output_data = remove(input_data, session=session)
        
        with open(output_path, 'wb') as output_file:
            output_file.write(output_data)
        
        # Clean up session to free memory
        del session
        
        return True
    except Exception as e:
        logger.error(f"Error in rembg: {str(e)}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Please upload PNG, JPG, JPEG, GIF, BMP, or WEBP'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = str(int(time.time()))
        unique_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        # Resize image to reduce memory usage
        try:
            with Image.open(filepath) as img:
                # Resize if image is too large
                max_size = 1024
                if img.width > max_size or img.height > max_size:
                    img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                    img.save(filepath, optimize=True, quality=85)
        except Exception as e:
            logger.warning(f"Could not resize image: {e}")
        
        # Generate output filename
        output_filename = f"removed_bg_{unique_filename}"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        # Try lightweight rembg first, fallback to simple method
        success = remove_background_rembg_light(filepath, output_path)
        if not success:
            logger.info("Rembg failed, trying simple method")
            success = remove_background_simple(filepath, output_path)
        
        if success:
            # Convert output to base64 for preview
            with open(output_path, 'rb') as f:
                output_data = f.read()
                output_base64 = base64.b64encode(output_data).decode('utf-8')
            
            # Clean up uploaded file
            os.remove(filepath)
            
            return jsonify({
                'success': True,
                'output_filename': output_filename,
                'preview': f"data:image/png;base64,{output_base64}"
            })
        else:
            # Clean up files on failure
            if os.path.exists(filepath):
                os.remove(filepath)
            if os.path.exists(output_path):
                os.remove(output_path)
            
            return jsonify({'error': 'Failed to remove background'}), 500
            
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/download/<filename>')
def download_file(filename):
    try:
        filepath = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        if os.path.exists(filepath):
            return send_file(filepath, as_attachment=True, download_name=filename)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        logger.error(f"Download error: {str(e)}")
        return jsonify({'error': 'Download failed'}), 500

@app.route('/cleanup/<filename>', methods=['DELETE'])
def cleanup_file(filename):
    try:
        filepath = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        logger.error(f"Cleanup error: {str(e)}")
        return jsonify({'error': 'Cleanup failed'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint for deployment platforms"""
    return jsonify({
        'status': 'healthy',
        'message': 'Lightweight Background Remover App is running',
        'memory_optimized': True,
        'max_file_size': '8MB'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
