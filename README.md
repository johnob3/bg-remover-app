# 🎨 Background Remover App

A powerful, AI-powered background removal application that allows users to remove backgrounds from images with high precision. Built with Python Flask backend and a modern web interface.

## ✨ Features

- **AI-Powered Background Removal**: Uses state-of-the-art `rembg` library with U2Net model
- **Fallback Method**: OpenCV-based background removal as backup
- **Modern Web Interface**: Beautiful, responsive design with drag-and-drop functionality
- **Real-time Preview**: See original and processed images side by side
- **Multiple Format Support**: PNG, JPG, JPEG, GIF, BMP, WEBP
- **High-Quality Output**: Preserves transparency and image quality
- **Mobile Friendly**: Responsive design works on all devices
- **Fast Processing**: Optimized for quick background removal
- **Privacy Safe**: All processing happens locally

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or download this repository**
   ```bash
   git clone <your-repo-url>
   cd bg-remover
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000`

## 📁 Project Structure

```
bg-remover/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Web interface
├── static/               # Static files (CSS, JS, images)
├── uploads/              # Temporary uploaded files
├── outputs/              # Processed images
└── README.md            # This file
```

## 🛠️ How It Works

### Background Removal Methods

1. **Primary Method - Rembg (AI-Powered)**
   - Uses U2Net deep learning model
   - Provides high-quality, precise background removal
   - Handles complex backgrounds and fine details

2. **Fallback Method - OpenCV**
   - Traditional computer vision approach
   - Uses thresholding and morphological operations
   - Activated when AI method fails

### Technical Details

- **Backend**: Flask web framework
- **AI Model**: U2Net (via rembg library)
- **Image Processing**: OpenCV, PIL (Pillow)
- **Frontend**: HTML5, CSS3, JavaScript
- **File Handling**: Secure file upload with validation

## 🎯 Usage

### Web Interface

1. **Upload Image**: Drag and drop or click to select an image
2. **Automatic Processing**: The app automatically removes the background
3. **Preview Results**: Compare original and processed images
4. **Download**: Save the result with transparent background

### API Endpoints

- `GET /` - Main web interface
- `POST /upload` - Upload and process image
- `GET /download/<filename>` - Download processed image
- `DELETE /cleanup/<filename>` - Clean up processed file

### Supported File Types

- PNG (recommended for best quality)
- JPG/JPEG
- GIF
- BMP
- WEBP

## ⚙️ Configuration

### Environment Variables

Create a `.env` file for custom configuration:

```env
FLASK_ENV=development
MAX_CONTENT_LENGTH=16777216  # 16MB
UPLOAD_FOLDER=uploads
OUTPUT_FOLDER=outputs
```

### Customization

- **Model Selection**: Change the rembg model in `app.py`
- **File Size Limit**: Modify `MAX_CONTENT_LENGTH` in Flask config
- **Styling**: Edit CSS in `templates/index.html`

## 🔧 Advanced Usage

### Batch Processing Script

Create a `batch_process.py` file for processing multiple images:

```python
import os
import glob
from rembg import remove, new_session

def batch_remove_background(input_folder, output_folder):
    session = new_session('u2net')
    
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Process all images in input folder
    for image_path in glob.glob(os.path.join(input_folder, '*')):
        if image_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            with open(image_path, 'rb') as input_file:
                input_data = input_file.read()
            
            output_data = remove(input_data, session=session)
            
            # Save with transparent background
            output_path = os.path.join(output_folder, f"processed_{os.path.basename(image_path)}")
            with open(output_path, 'wb') as output_file:
                output_file.write(output_data)
            
            print(f"Processed: {image_path} -> {output_path}")

# Usage
batch_remove_background('input_images', 'output_images')
```

### Command Line Usage

```bash
# Process single image
python -c "from rembg import remove; open('output.png', 'wb').write(remove(open('input.jpg', 'rb').read()))"

# Batch process
python batch_process.py
```

## 🚀 Deployment

### Local Development

```bash
python app.py
```

### Production Deployment

1. **Using Gunicorn**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Using Docker**
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   EXPOSE 5000
   CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
   ```

3. **Environment Variables for Production**
   ```env
   FLASK_ENV=production
   FLASK_DEBUG=False
   ```

## 🐛 Troubleshooting

### Common Issues

1. **"Module not found" errors**
   ```bash
   pip install -r requirements.txt
   ```

2. **Out of memory errors**
   - Reduce image size before processing
   - Use smaller rembg models

3. **Slow processing**
   - Ensure you have sufficient RAM
   - Consider using GPU acceleration (if available)

4. **Permission errors**
   ```bash
   chmod +x app.py
   ```

### Performance Tips

- **Image Size**: Smaller images process faster
- **Model Selection**: U2Net provides best quality but uses more memory
- **Batch Processing**: Process multiple images in sequence for efficiency

## 📊 Performance

### Benchmarks (approximate)

- **Small images (500x500)**: 2-5 seconds
- **Medium images (1000x1000)**: 5-15 seconds
- **Large images (2000x2000)**: 15-30 seconds

*Performance depends on hardware specifications*

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- [rembg](https://github.com/danielgatis/rembg) - AI background removal library
- [U2Net](https://github.com/xuebinqin/U-2-Net) - Deep learning model
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [OpenCV](https://opencv.org/) - Computer vision library

## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section
2. Search existing issues
3. Create a new issue with detailed information

---

**Made with ❤️ for easy background removal**
