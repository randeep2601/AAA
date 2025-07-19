from flask import Flask, render_template, request, jsonify, send_file
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import json
import time
import re
from urllib.parse import urljoin, urlparse
import os
import sys
import nltk
from transformers import pipeline
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from wordcloud import WordCloud
import base64
from io import BytesIO
import textstat
from langdetect import detect
from googletrans import Translator
from newspaper import Article
import threading
from datetime import datetime
from summary_generator import SummaryGenerator

app = Flask(__name__, template_folder='../templates', static_folder='../static')

class WebSearchAnalyzer:
    def __init__(self):
        self.setup_nltk()
        self.translator = Translator()
        self.summarizer = None
        self.setup_ai_models()
        
    def setup_nltk(self):
        """Download required NLTK data"""
        try:
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)
            nltk.download('vader_lexicon', quiet=True)
        except:
            pass
    
    def setup_ai_models(self):
        """Initialize AI models for summarization"""
        try:
            self.summarizer = pipeline("summarization", 
                                     model="facebook/bart-large-cnn",
                                     device=-1)  # CPU
        except Exception as e:
            print(f"Warning: Could not load AI summarization model: {e}")
    
    def get_webdriver(self):
        """Setup Chrome webdriver with options"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            return driver
        except Exception as e:
            print(f"Error setting up webdriver: {e}")
            return None
    
    def search_web(self, query, num_results=20):
        """Perform web search using multiple search engines"""
        results = []
        
        # Search using DuckDuckGo (more privacy-friendly)
        try:
            results.extend(self._search_duckduckgo(query, num_results))
        except Exception as e:
            print(f"DuckDuckGo search failed: {e}")
        
        # Search using Bing (backup)
        try:
            results.extend(self._search_bing(query, num_results))
        except Exception as e:
            print(f"Bing search failed: {e}")
        
        # Remove duplicates and limit results
        unique_results = []
        seen_urls = set()
        for result in results:
            if result['url'] not in seen_urls and len(unique_results) < num_results:
                unique_results.append(result)
                seen_urls.add(result['url'])
        
        return unique_results
    
    def _search_duckduckgo(self, query, num_results):
        """Search using DuckDuckGo"""
        results = []
        driver = self.get_webdriver()
        
        if not driver:
            return results
        
        try:
            search_url = f"https://duckduckgo.com/?q={query.replace(' ', '+')}"
            driver.get(search_url)
            
            # Wait for results to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-result]"))
            )
            
            # Extract search results
            result_elements = driver.find_elements(By.CSS_SELECTOR, "[data-result]")
            
            for element in result_elements[:num_results]:
                try:
                    title_elem = element.find_element(By.CSS_SELECTOR, "h2 a")
                    title = title_elem.text
                    url = title_elem.get_attribute("href")
                    
                    try:
                        snippet_elem = element.find_element(By.CSS_SELECTOR, "[data-result] > div > div")
                        snippet = snippet_elem.text
                    except:
                        snippet = ""
                    
                    if title and url:
                        results.append({
                            'title': title,
                            'url': url,
                            'snippet': snippet,
                            'source': 'DuckDuckGo'
                        })
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"DuckDuckGo search error: {e}")
        finally:
            driver.quit()
        
        return results
    
    def _search_bing(self, query, num_results):
        """Search using Bing"""
        results = []
        driver = self.get_webdriver()
        
        if not driver:
            return results
        
        try:
            search_url = f"https://www.bing.com/search?q={query.replace(' ', '+')}"
            driver.get(search_url)
            
            # Wait for results to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".b_algo"))
            )
            
            # Extract search results
            result_elements = driver.find_elements(By.CSS_SELECTOR, ".b_algo")
            
            for element in result_elements[:num_results]:
                try:
                    title_elem = element.find_element(By.CSS_SELECTOR, "h2 a")
                    title = title_elem.text
                    url = title_elem.get_attribute("href")
                    
                    try:
                        snippet_elem = element.find_element(By.CSS_SELECTOR, ".b_caption p")
                        snippet = snippet_elem.text
                    except:
                        snippet = ""
                    
                    if title and url:
                        results.append({
                            'title': title,
                            'url': url,
                            'snippet': snippet,
                            'source': 'Bing'
                        })
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"Bing search error: {e}")
        finally:
            driver.quit()
        
        return results
    
    def extract_content(self, urls):
        """Extract content from multiple URLs"""
        extracted_content = []
        
        def extract_single(url):
            try:
                content = self._extract_single_content(url)
                if content:
                    extracted_content.append(content)
            except Exception as e:
                print(f"Error extracting from {url}: {e}")
        
        # Use threading for parallel extraction
        threads = []
        for url in urls[:10]:  # Limit to 10 URLs as requested
            thread = threading.Thread(target=extract_single, args=(url,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        return extracted_content
    
    def _extract_single_content(self, url):
        """Extract content from a single URL using multiple methods"""
        content = {
            'url': url,
            'title': '',
            'text': '',
            'author': '',
            'publish_date': '',
            'extraction_method': '',
            'word_count': 0
        }
        
        # Method 1: Try newspaper3k (best for articles)
        try:
            article = Article(url)
            article.download()
            article.parse()
            
            if article.text and len(article.text) > 100:
                content.update({
                    'title': article.title or '',
                    'text': article.text,
                    'author': ', '.join(article.authors) if article.authors else '',
                    'publish_date': str(article.publish_date) if article.publish_date else '',
                    'extraction_method': 'newspaper3k',
                    'word_count': len(article.text.split())
                })
                return content
        except Exception as e:
            print(f"Newspaper3k failed for {url}: {e}")
        
        # Method 2: Try BeautifulSoup with requests
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unwanted elements
            for elem in soup(['script', 'style', 'nav', 'header', 'footer', 
                            'aside', 'advertisement', '.ad', '#ad']):
                elem.decompose()
            
            # Extract title
            title_elem = soup.find('title')
            title = title_elem.get_text().strip() if title_elem else ''
            
            # Extract main content
            text_content = ''
            
            # Try common content selectors
            content_selectors = [
                'article', '.content', '.main-content', '.post-content',
                '.entry-content', '.article-content', 'main', '.text'
            ]
            
            for selector in content_selectors:
                content_elem = soup.select_one(selector)
                if content_elem:
                    text_content = content_elem.get_text(separator=' ', strip=True)
                    break
            
            # Fallback to body text
            if not text_content:
                body = soup.find('body')
                if body:
                    text_content = body.get_text(separator=' ', strip=True)
            
            # Clean and validate content
            text_content = re.sub(r'\s+', ' ', text_content).strip()
            
            if text_content and len(text_content) > 100:
                content.update({
                    'title': title,
                    'text': text_content,
                    'extraction_method': 'BeautifulSoup',
                    'word_count': len(text_content.split())
                })
                return content
                
        except Exception as e:
            print(f"BeautifulSoup failed for {url}: {e}")
        
        # Method 3: Try Selenium as last resort
        try:
            driver = self.get_webdriver()
            if driver:
                driver.get(url)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                
                # Remove ads and unnecessary elements
                try:
                    driver.execute_script("""
                        var ads = document.querySelectorAll('[class*="ad"], [id*="ad"], [class*="advertisement"]');
                        ads.forEach(function(ad) { ad.remove(); });
                    """)
                except:
                    pass
                
                title = driver.title
                text_content = driver.find_element(By.TAG_NAME, "body").text
                
                driver.quit()
                
                text_content = re.sub(r'\s+', ' ', text_content).strip()
                
                if text_content and len(text_content) > 100:
                    content.update({
                        'title': title,
                        'text': text_content,
                        'extraction_method': 'Selenium',
                        'word_count': len(text_content.split())
                    })
                    return content
                    
        except Exception as e:
            print(f"Selenium failed for {url}: {e}")
        
        return None
    
    def compile_document(self, extracted_contents):
        """Compile all extracted content into a single document"""
        compiled_doc = {
            'title': 'Compiled Web Search Results',
            'creation_date': datetime.now().isoformat(),
            'total_sources': len(extracted_contents),
            'total_words': sum(content['word_count'] for content in extracted_contents),
            'sources': [],
            'full_text': ''
        }
        
        full_text_parts = []
        
        for i, content in enumerate(extracted_contents, 1):
            source_info = {
                'index': i,
                'title': content['title'],
                'url': content['url'],
                'author': content['author'],
                'publish_date': content['publish_date'],
                'word_count': content['word_count'],
                'extraction_method': content['extraction_method']
            }
            compiled_doc['sources'].append(source_info)
            
            # Add to full text with source markers
            section_header = f"\n\n--- SOURCE {i}: {content['title']} ---\n"
            section_text = content['text']
            full_text_parts.append(section_header + section_text)
        
        compiled_doc['full_text'] = '\n'.join(full_text_parts)
        return compiled_doc
    
    def analyze_document(self, document):
        """Perform comprehensive analysis of the compiled document"""
        text = document['full_text']
        
        analysis = {
            'basic_stats': self._get_basic_stats(text),
            'readability': self._get_readability_stats(text),
            'language_detection': self._detect_language(text),
            'sentiment_analysis': self._analyze_sentiment(text),
            'keyword_analysis': self._extract_keywords(text),
            'topic_analysis': self._analyze_topics(text)
        }
        
        return analysis
    
    def _get_basic_stats(self, text):
        """Get basic text statistics"""
        words = text.split()
        sentences = text.split('.')
        paragraphs = text.split('\n\n')
        
        return {
            'character_count': len(text),
            'word_count': len(words),
            'sentence_count': len(sentences),
            'paragraph_count': len(paragraphs),
            'avg_words_per_sentence': len(words) / max(len(sentences), 1),
            'avg_chars_per_word': len(text) / max(len(words), 1)
        }
    
    def _get_readability_stats(self, text):
        """Calculate readability scores"""
        try:
            return {
                'flesch_reading_ease': textstat.flesch_reading_ease(text),
                'flesch_kincaid_grade': textstat.flesch_kincaid_grade(text),
                'gunning_fog': textstat.gunning_fog(text),
                'automated_readability_index': textstat.automated_readability_index(text),
                'reading_time_minutes': textstat.reading_time(text, ms_per_char=14.69)
            }
        except:
            return {
                'flesch_reading_ease': 0,
                'flesch_kincaid_grade': 0,
                'gunning_fog': 0,
                'automated_readability_index': 0,
                'reading_time_minutes': len(text.split()) / 200  # Rough estimate
            }
    
    def _detect_language(self, text):
        """Detect the language of the text"""
        try:
            return detect(text)
        except:
            return 'unknown'
    
    def _analyze_sentiment(self, text):
        """Analyze sentiment using NLTK's VADER"""
        try:
            from nltk.sentiment import SentimentIntensityAnalyzer
            sia = SentimentIntensityAnalyzer()
            scores = sia.polarity_scores(text)
            return scores
        except:
            return {'compound': 0, 'pos': 0, 'neu': 1, 'neg': 0}
    
    def _extract_keywords(self, text):
        """Extract keywords and their frequencies"""
        try:
            from nltk.tokenize import word_tokenize
            from nltk.corpus import stopwords
            from collections import Counter
            import string
            
            # Tokenize and clean
            tokens = word_tokenize(text.lower())
            stop_words = set(stopwords.words('english'))
            
            # Filter out stopwords, punctuation, and short words
            keywords = [word for word in tokens 
                       if word not in stop_words 
                       and word not in string.punctuation 
                       and len(word) > 3]
            
            # Get frequency distribution
            keyword_freq = Counter(keywords)
            return dict(keyword_freq.most_common(20))
        except:
            return {}
    
    def _analyze_topics(self, text):
        """Basic topic analysis using keyword clustering"""
        keywords = self._extract_keywords(text)
        
        # Simple topic categorization based on common themes
        topics = {
            'technology': ['technology', 'computer', 'software', 'digital', 'internet', 'data'],
            'business': ['business', 'company', 'market', 'financial', 'economic', 'profit'],
            'science': ['research', 'study', 'analysis', 'scientific', 'experiment', 'theory'],
            'health': ['health', 'medical', 'treatment', 'patient', 'disease', 'healthcare'],
            'education': ['education', 'learning', 'student', 'school', 'university', 'teaching']
        }
        
        topic_scores = {}
        for topic, topic_words in topics.items():
            score = sum(keywords.get(word, 0) for word in topic_words)
            if score > 0:
                topic_scores[topic] = score
        
        return topic_scores

# Initialize the analyzer and summary generator
analyzer = WebSearchAnalyzer()
summary_generator = SummaryGenerator()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    """Handle web search requests"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        num_results = data.get('num_results', 20)
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        # Perform web search
        results = analyzer.search_web(query, num_results)
        
        return jsonify({
            'success': True,
            'query': query,
            'results': results,
            'total_results': len(results)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/extract', methods=['POST'])
def extract_content():
    """Handle content extraction from selected URLs"""
    try:
        data = request.get_json()
        urls = data.get('urls', [])
        
        if not urls or len(urls) > 10:
            return jsonify({'error': 'Please provide 1-10 URLs'}), 400
        
        # Extract content
        extracted_contents = analyzer.extract_content(urls)
        
        # Compile document
        compiled_doc = analyzer.compile_document(extracted_contents)
        
        # Analyze document
        analysis = analyzer.analyze_document(compiled_doc)
        
        return jsonify({
            'success': True,
            'document': compiled_doc,
            'analysis': analysis,
            'extracted_count': len(extracted_contents)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate_summary', methods=['POST'])
def generate_summary():
    """Generate various types of summaries and analyses"""
    try:
        data = request.get_json()
        document = data.get('document', {})
        summary_type = data.get('type', 'detailed_summary')
        
        text = document.get('full_text', '')
        if not text:
            return jsonify({'error': 'No text to summarize'}), 400
        
        # Generate the requested summary type
        result = summary_generator.generate_summary_by_type(text, summary_type, document)
        
        return jsonify({
            'success': True,
            'type': summary_type,
            'result': result
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)