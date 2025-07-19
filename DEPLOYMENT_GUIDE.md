# Hinglish Translation Tool - Deployment Guide 🇮🇳

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ (tested with Python 3.13)
- Virtual environment support
- 2GB+ RAM recommended
- Linux/Mac/Windows compatible

### Installation & Launch

```bash
# 1. Clone or download the project
cd /workspace

# 2. Install dependencies
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Launch the application
./run.sh
# Or manually: python app.py
```

### Access the Application
Open your browser and go to: **http://localhost:5000**

---

## 📋 Features Overview

### ✅ Supported File Formats
- **PDF** (up to 1000 pages)
- **HTML/HTM** files
- **ZIP** archives (auto-extracts)
- **DOC/DOCX** documents
- **TXT** text files

### ✅ Core Capabilities
- **🔄 Cloud Processing**: Background task handling
- **🇮🇳 Natural Hinglish**: Context-aware translation
- **📋 Smart Summary**: Automatic essence extraction
- **💻 Modern UI**: Responsive web interface
- **🔒 Security**: Automatic file cleanup
- **📊 Progress Tracking**: Real-time status updates

---

## 🏗️ Architecture

### Backend Components
```
app.py              # Main Flask application
text_processor.py   # Hinglish translation engine
file_extractor.py   # Multi-format text extraction
config.py          # Configuration settings
```

### Frontend
```
templates/index.html # Modern responsive UI
```

### Processing Flow
1. **File Upload** → Validation & Storage
2. **Text Extraction** → Format-specific processing
3. **Background Translation** → Hinglish conversion
4. **Summary Generation** → Key points extraction
5. **Download Ready** → Processed file delivery

---

## 📁 Project Structure

```
hinglish-translator/
├── app.py                 # Flask web application
├── text_processor.py      # Hinglish translation logic
├── file_extractor.py      # File format handlers
├── config.py             # Application settings
├── requirements.txt      # Python dependencies
├── run.sh               # Launch script
├── README.md           # Documentation
├── test_sample.py      # Testing utilities
├── templates/
│   └── index.html      # Web interface
├── uploads/            # Temporary upload storage
├── processed/          # Processed file output
└── venv/              # Virtual environment
```

---

## ⚙️ Configuration

### File Size Limits
- **Maximum file size**: 100MB
- **PDF page limit**: 1000 pages
- **Processing timeout**: 30 minutes

### Customization (config.py)
```python
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB
MAX_PDF_PAGES = 1000
ALLOWED_EXTENSIONS = {'.pdf', '.html', '.zip', '.doc', '.docx', '.txt'}
```

---

## 🔧 API Endpoints

### Web Interface
- `GET /` - Main upload interface
- `POST /upload` - File upload handler
- `GET /status/<task_id>` - Processing status
- `GET /download/<task_id>` - Download processed file

### Processing Flow
1. Upload file via web interface
2. Monitor progress with real-time updates
3. Download processed Hinglish version
4. Download concise summary (optional)

---

## 🧪 Testing

### Run Tests
```bash
source venv/bin/activate
python test_sample.py
```

### Test Features
- ✅ Text processing engine
- ✅ File extraction capabilities
- ✅ Hinglish translation quality
- ✅ Summary generation
- ✅ Error handling

---

## 🔍 Troubleshooting

### Common Issues

**1. Port Already in Use**
```bash
# Check what's using port 5000
lsof -i :5000
# Kill the process if needed
kill -9 <PID>
```

**2. Missing Dependencies**
```bash
pip install -r requirements.txt
```

**3. Permission Denied**
```bash
chmod +x run.sh
```

**4. Virtual Environment Issues**
```bash
deactivate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🚀 Production Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

### Environment Variables
```bash
export FLASK_ENV=production
export SECRET_KEY=your-secret-key
export MAX_CONTENT_LENGTH=104857600
```

---

## 🛡️ Security Considerations

### File Handling
- ✅ Automatic cleanup of uploaded files
- ✅ File type validation
- ✅ Size limits enforced
- ✅ Secure filename handling

### Best Practices
- Change default secret key in production
- Use HTTPS in production
- Implement rate limiting
- Regular security updates

---

## 📊 Performance

### Optimization Tips
- **Large Files**: Process in chunks
- **Memory Usage**: Automatic cleanup
- **Concurrent Users**: Background processing
- **Response Time**: Real-time progress

### Scaling
- Use Redis for task queue in production
- Implement horizontal scaling with load balancer
- Consider CDN for file downloads
- Database for persistent storage

---

## 📝 License & Credits

**Hinglish Translation Tool**
- Modern web-based document translation system
- Converts complex English to natural Hinglish
- Built with Flask, NLTK, and modern web technologies

### Dependencies
- Flask 2.3.3 - Web framework
- NLTK 3.8.1 - Natural language processing
- pdfplumber 0.10.3 - PDF text extraction
- beautifulsoup4 4.12.2 - HTML parsing
- python-docx 0.8.11 - Word document handling

---

## 🎯 Usage Examples

### 1. PDF Document
Upload a technical PDF → Get simplified Hinglish version

### 2. Academic Paper
Complex research → Easy-to-understand Hinglish summary

### 3. Legal Document
Legal jargon → Plain Hinglish explanation

### 4. Technical Manual
Technical instructions → User-friendly Hinglish guide

---

## 🤝 Support

For issues, questions, or contributions:
1. Check the troubleshooting section
2. Run test_sample.py to verify installation
3. Review logs in the console output
4. Ensure all dependencies are installed

**Happy Translating! 🇮🇳✨**