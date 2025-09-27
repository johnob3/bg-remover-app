# 🚀 Quick Start Guide

## Get Started in 3 Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python app.py
```
*Or use the convenient startup script:*
```bash
python run.py
```

### 3. Open Your Browser
Navigate to: **http://localhost:5000**

## 🎯 What You Can Do

- **Upload Images**: Drag & drop or click to select
- **AI Background Removal**: Automatic processing with U2Net model
- **Preview Results**: See before/after comparison
- **Download**: Save processed images with transparent backgrounds
- **Batch Processing**: Use `batch_process.py` for multiple images

## 📁 File Structure
```
bg-remover/
├── app.py              # Main Flask application
├── run.py              # Easy startup script
├── batch_process.py    # Batch processing tool
├── demo.py             # Demo and examples
├── requirements.txt    # Dependencies
├── templates/
│   └── index.html     # Web interface
└── README.md          # Full documentation
```

## 🛠️ Quick Commands

```bash
# Start the web app
python app.py

# Process multiple images
python batch_process.py input_folder output_folder

# Run demos
python demo.py

# Check dependencies
python run.py
```

## 🎨 Features

- ✅ AI-powered background removal
- ✅ Modern web interface
- ✅ Drag & drop upload
- ✅ Real-time preview
- ✅ Multiple format support
- ✅ Batch processing
- ✅ Mobile friendly
- ✅ Privacy safe (local processing)

## 🆘 Need Help?

1. Check the full [README.md](README.md) for detailed instructions
2. Run `python demo.py` to see examples
3. Use `python batch_process.py --help` for batch processing options

---

**Ready to remove backgrounds? Start with `python app.py`!** 🎉
