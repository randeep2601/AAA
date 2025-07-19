# Hinglish Translation Tool

A comprehensive cloud-based tool that converts entire text documents into basic Hinglish language while preserving the original meaning. The tool supports multiple file formats and provides both full translations and concise summaries.

## 🌟 Features

- **Multiple File Format Support**: PDF (up to 1000 pages), HTML, ZIP, DOC, DOCX, TXT
- **Cloud Processing**: Background processing with real-time progress tracking
- **Intelligent Translation**: Converts complex English to natural, easy-to-understand Hinglish
- **Smart Summarization**: Generates concise summaries capturing document essence
- **Large File Handling**: Supports files up to 100MB
- **Modern Web Interface**: Responsive design with drag-and-drop functionality
- **Real-time Progress**: Live updates during processing
- **Download Management**: Secure file download with automatic cleanup

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd hinglish-translation-tool
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Download NLTK data** (automatically handled on first run)
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

4. **Run the application**
```bash
python app.py
```

5. **Access the application**
Open your web browser and go to: `http://localhost:5000`

## 📚 Usage

### Web Interface

1. **Upload Document**
   - Drag and drop your file onto the upload area, or
   - Click "Choose File" to browse and select your document

2. **Monitor Progress**
   - Real-time progress bar shows processing status
   - Status messages indicate current processing stage

3. **Download Results**
   - Once complete, download your Hinglish translation
   - File includes both full translation and concise summary

### Supported File Types

| Format | Extension | Max Size | Notes |
|--------|-----------|----------|-------|
| PDF | .pdf | 100MB | Up to 1000 pages |
| HTML | .html, .htm | 100MB | Web pages and documents |
| Word Document | .docx | 100MB | Modern Word format |
| Legacy Word | .doc | 100MB | Older Word format (basic extraction) |
| Text File | .txt | 100MB | Plain text files |
| ZIP Archive | .zip | 100MB | Contains supported document types |

## 🛠️ API Endpoints

### Upload File
```
POST /upload
Content-Type: multipart/form-data

Returns: {
  "job_id": "uuid",
  "message": "File uploaded successfully. Processing started."
}
```

### Check Status
```
GET /status/<job_id>

Returns: {
  "status": "processing|completed|error",
  "progress": 0-100,
  "message": "Current status message",
  ...
}
```

### Download Result
```
GET /download/<job_id>

Returns: File download (Hinglish translation)
```

## 🧠 How It Works

### 1. File Processing
- **Text Extraction**: Extracts text from various file formats using specialized libraries
- **Content Validation**: Ensures extracted text is substantial and processable
- **Chunking**: Splits large documents into manageable pieces for efficient processing

### 2. Hinglish Translation
- **Dictionary-Based Translation**: Uses comprehensive English-to-Hinglish word mappings
- **Grammar Adaptation**: Applies Hinglish grammar rules and sentence structures
- **Context Preservation**: Maintains technical terms and proper nouns
- **Natural Flow**: Adds appropriate connectors and transitions

### 3. Summary Generation
- **Extractive Summarization**: Identifies key sentences based on content importance
- **Position Weighting**: Prioritizes sentences from document beginning and end
- **Length Optimization**: Creates concise summaries capturing document essence

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │  File Storage   │
│   (HTML/JS)     │◄──►│   (Flask)       │◄──►│  (Local/Cloud)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Upload Interface│    │ Background Jobs │    │ Text Processing │
│ Progress Track  │    │ Status Tracking │    │ Hinglish Trans  │
│ Download Mgmt   │    │ File Management │    │ Summarization   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📦 Project Structure

```
hinglish-translation-tool/
├── app.py                 # Main Flask application
├── text_processor.py      # Hinglish translation engine
├── file_extractor.py      # Multi-format text extraction
├── requirements.txt       # Python dependencies
├── README.md             # Documentation
├── templates/
│   └── index.html        # Web interface
├── uploads/              # Temporary file storage
└── processed/            # Output file storage
```

## 🔧 Configuration

### Environment Variables
```bash
export FLASK_ENV=development  # For development
export FLASK_DEBUG=1         # Enable debug mode
```

### Application Settings
Edit `app.py` to modify:
- Maximum file size (default: 100MB)
- Maximum PDF pages (default: 1000)
- Upload and processed folders
- Secret key for session management

## 🌐 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
For production deployment, consider:
- Using WSGI server (Gunicorn, uWSGI)
- Setting up reverse proxy (Nginx)
- Configuring SSL certificates
- Setting up proper logging
- Using cloud storage for files

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📝 Output Format

The generated Hinglish translation file includes:

```
================================================================================
HINGLISH TRANSLATION
================================================================================

Original File: document.pdf
Processed On: 2024-01-15 14:30:25
Total Characters: 45,678

================================================================================
FULL TRANSLATION
================================================================================

[Complete Hinglish translation of the document]

================================================================================
CONCISE SUMMARY (ESSENCE)
================================================================================

Ye document ka main essence hai:

[Key points summarized in Hinglish]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

**"PDF processing libraries not available"**
```bash
pip install PyPDF2 pdfplumber
```

**"HTML processing library not available"**
```bash
pip install beautifulsoup4 lxml
```

**"DOCX processing library not available"**
```bash
pip install python-docx
```

**Memory issues with large files**
- Reduce file size or split into smaller documents
- Increase system memory allocation
- Use chunked processing for very large texts

### Performance Tips

- For best PDF processing, ensure files are text-based (not scanned images)
- Large ZIP files may take longer to process
- Complex HTML documents might need preprocessing
- DOC files have basic extraction; consider converting to DOCX

## 🚀 Future Enhancements

- [ ] Advanced AI-powered translation using transformer models
- [ ] Support for more Indian languages
- [ ] Batch file processing
- [ ] User authentication and file management
- [ ] Integration with cloud storage services
- [ ] Mobile app development
- [ ] OCR support for image-based PDFs
- [ ] Real-time collaborative translation

## 💡 Technical Details

### Translation Algorithm
The tool uses a hybrid approach:
1. **Dictionary Mapping**: Core English-Hinglish word translations
2. **Grammar Rules**: Sentence structure adaptation
3. **Context Preservation**: Technical terms and proper nouns
4. **Flow Enhancement**: Natural Hinglish connectors

### Performance Metrics
- Processing Speed: ~1000 characters per second
- Memory Usage: ~50MB for typical documents
- Supported Concurrency: Multiple simultaneous uploads
- Maximum Processing Time: Auto-timeout after 30 minutes

---

For support or questions, please open an issue or contact the development team.