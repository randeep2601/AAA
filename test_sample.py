#!/usr/bin/env python3
"""
Test script for Hinglish Translation Tool
This script demonstrates the text processing capabilities with sample text.
"""

from text_processor import TextProcessor
from file_extractor import FileExtractor
import tempfile
import os

def test_text_processing():
    """Test the text processing functionality"""
    print("=" * 60)
    print("HINGLISH TRANSLATION TOOL - TEST DEMO")
    print("=" * 60)
    
    # Initialize processor
    processor = TextProcessor()
    
    # Sample English text
    sample_text = """
    Hello everyone! Welcome to our new technology platform. This system is designed to help 
    users understand complex information in a simple way. We believe that technology should 
    be accessible to everyone, regardless of their background or education level.
    
    Our platform offers many features including document processing, text translation, and 
    content summarization. Users can upload various file formats like PDF, Word documents, 
    and HTML pages. The system will automatically extract text and convert it into 
    easy-to-understand language.
    
    We hope this tool will be useful for students, professionals, and anyone who wants to 
    make sense of difficult documents. Thank you for using our service!
    """
    
    print("\n📄 ORIGINAL TEXT:")
    print("-" * 40)
    print(sample_text.strip())
    
    print("\n🔄 PROCESSING...")
    print("-" * 40)
    
    # Translate to Hinglish
    hinglish_text = processor.translate_to_hinglish(sample_text)
    
    print("\n🇮🇳 HINGLISH TRANSLATION:")
    print("-" * 40)
    print(hinglish_text)
    
    # Generate summary
    summary = processor.generate_summary(hinglish_text)
    
    print("\n📋 CONCISE SUMMARY:")
    print("-" * 40)
    print(summary)
    
    print("\n" + "=" * 60)
    print("TEST COMPLETED SUCCESSFULLY!")
    print("=" * 60)

def test_file_extraction():
    """Test file extraction with a temporary text file"""
    print("\n" + "=" * 60)
    print("FILE EXTRACTION TEST")
    print("=" * 60)
    
    # Create a temporary text file
    test_content = """
    This is a test document for the Hinglish Translation Tool.
    
    The document contains multiple paragraphs with different types of content.
    We have technical terms, simple sentences, and complex information.
    
    The system should be able to extract this text and convert it properly.
    """
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(test_content)
        temp_file_path = f.name
    
    try:
        # Initialize extractor
        extractor = FileExtractor()
        
        print(f"\n📁 Created temporary file: {temp_file_path}")
        
        # Get file info
        file_info = extractor.get_file_info(temp_file_path)
        print(f"\n📊 File Info:")
        for key, value in file_info.items():
            print(f"   {key}: {value}")
        
        # Extract text
        extracted_text = extractor.extract_text(temp_file_path)
        
        print(f"\n📄 Extracted Text:")
        print("-" * 40)
        print(extracted_text)
        
        # Process with Hinglish translator
        processor = TextProcessor()
        hinglish_result = processor.translate_to_hinglish(extracted_text)
        
        print(f"\n🇮🇳 Hinglish Translation:")
        print("-" * 40)
        print(hinglish_result)
        
    finally:
        # Clean up temporary file
        os.unlink(temp_file_path)
        print(f"\n🗑️ Cleaned up temporary file")

def display_features():
    """Display the key features of the tool"""
    print("\n" + "=" * 60)
    print("HINGLISH TRANSLATION TOOL FEATURES")
    print("=" * 60)
    
    features = [
        "📄 Multi-format Support: PDF, HTML, DOC, DOCX, TXT, ZIP",
        "🔄 Background Processing: Real-time progress tracking",
        "🇮🇳 Natural Hinglish: Easy-to-understand translations",
        "📋 Smart Summaries: Key points extraction",
        "☁️ Cloud Ready: Scalable architecture",
        "💻 Web Interface: Modern, responsive design",
        "🔒 Secure: Automatic file cleanup",
        "📊 Large Files: Up to 100MB, 1000 pages"
    ]
    
    for feature in features:
        print(f"  ✓ {feature}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    print("Starting Hinglish Translation Tool Test...")
    
    try:
        # Display features
        display_features()
        
        # Test text processing
        test_text_processing()
        
        # Test file extraction
        test_file_extraction()
        
        print("\n🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
        print("\nTo run the web application:")
        print("   python app.py")
        print("\nThen open: http://localhost:5000")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        print("\nPlease install required dependencies:")
        print("   pip install -r requirements.txt")
        raise