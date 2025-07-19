from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import uuid
import threading
import time
from datetime import datetime
import zipfile
import json
from text_processor import TextProcessor
from file_extractor import FileExtractor

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PROCESSED_FOLDER'] = 'processed'
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Create necessary directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

# Global storage for processing status
processing_status = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file selected'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check file extension
        allowed_extensions = {'.pdf', '.html', '.htm', '.zip', '.doc', '.docx', '.txt'}
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            return jsonify({'error': 'File type not supported. Please upload PDF, HTML, ZIP, DOC, DOCX, or TXT files.'}), 400
        
        # Generate unique job ID
        job_id = str(uuid.uuid4())
        filename = secure_filename(f"{job_id}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save uploaded file
        file.save(filepath)
        
        # Initialize processing status
        processing_status[job_id] = {
            'status': 'uploaded',
            'progress': 0,
            'message': 'File uploaded successfully',
            'original_filename': file.filename,
            'upload_time': datetime.now().isoformat(),
            'file_path': filepath
        }
        
        # Start background processing
        thread = threading.Thread(target=process_file_background, args=(job_id, filepath, file.filename))
        thread.daemon = True
        thread.start()
        
        return jsonify({'job_id': job_id, 'message': 'File uploaded successfully. Processing started.'})
    
    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/status/<job_id>')
def get_status(job_id):
    if job_id not in processing_status:
        return jsonify({'error': 'Job not found'}), 404
    
    return jsonify(processing_status[job_id])

@app.route('/download/<job_id>')
def download_file(job_id):
    if job_id not in processing_status:
        return jsonify({'error': 'Job not found'}), 404
    
    status = processing_status[job_id]
    if status['status'] != 'completed':
        return jsonify({'error': 'Processing not completed yet'}), 400
    
    try:
        output_file = status['output_file']
        return send_file(output_file, as_attachment=True, 
                        download_name=f"hinglish_{status['original_filename'].rsplit('.', 1)[0]}.txt")
    except Exception as e:
        return jsonify({'error': f'Download failed: {str(e)}'}), 500

def process_file_background(job_id, filepath, original_filename):
    """Background processing function"""
    try:
        # Update status
        processing_status[job_id]['status'] = 'processing'
        processing_status[job_id]['progress'] = 10
        processing_status[job_id]['message'] = 'Extracting text from file...'
        
        # Extract text from file
        extractor = FileExtractor()
        extracted_text = extractor.extract_text(filepath)
        
        if not extracted_text.strip():
            processing_status[job_id]['status'] = 'error'
            processing_status[job_id]['message'] = 'No text could be extracted from the file'
            return
        
        processing_status[job_id]['progress'] = 30
        processing_status[job_id]['message'] = 'Text extracted. Starting Hinglish translation...'
        
        # Process text to Hinglish
        processor = TextProcessor()
        
        # Split text into manageable chunks for processing
        chunks = processor.split_text_into_chunks(extracted_text)
        total_chunks = len(chunks)
        
        translated_chunks = []
        for i, chunk in enumerate(chunks):
            processing_status[job_id]['progress'] = 30 + (i / total_chunks) * 50
            processing_status[job_id]['message'] = f'Translating chunk {i+1} of {total_chunks}...'
            
            translated_chunk = processor.translate_to_hinglish(chunk)
            translated_chunks.append(translated_chunk)
        
        # Combine translated text
        full_translation = '\n\n'.join(translated_chunks)
        
        processing_status[job_id]['progress'] = 85
        processing_status[job_id]['message'] = 'Generating summary...'
        
        # Generate concise summary
        summary = processor.generate_summary(full_translation)
        
        # Create output file
        output_filename = f"hinglish_translation_{job_id}.txt"
        output_path = os.path.join(app.config['PROCESSED_FOLDER'], output_filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("HINGLISH TRANSLATION\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Original File: {original_filename}\n")
            f.write(f"Processed On: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Characters: {len(extracted_text)}\n\n")
            f.write("=" * 80 + "\n")
            f.write("FULL TRANSLATION\n")
            f.write("=" * 80 + "\n\n")
            f.write(full_translation)
            f.write("\n\n" + "=" * 80 + "\n")
            f.write("CONCISE SUMMARY (ESSENCE)\n")
            f.write("=" * 80 + "\n\n")
            f.write(summary)
        
        # Update final status
        processing_status[job_id]['status'] = 'completed'
        processing_status[job_id]['progress'] = 100
        processing_status[job_id]['message'] = 'Translation completed successfully'
        processing_status[job_id]['output_file'] = output_path
        processing_status[job_id]['completion_time'] = datetime.now().isoformat()
        
        # Clean up uploaded file
        try:
            os.remove(filepath)
        except:
            pass
            
    except Exception as e:
        processing_status[job_id]['status'] = 'error'
        processing_status[job_id]['message'] = f'Processing failed: {str(e)}'
        print(f"Error processing file: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)