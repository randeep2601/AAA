import re
import time
from typing import List
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import requests
import json

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class TextProcessor:
    def __init__(self):
        self.hinglish_dict = self._load_hinglish_dictionary()
        self.english_stopwords = set(stopwords.words('english'))
        
    def _load_hinglish_dictionary(self):
        """Load basic English to Hinglish word mappings"""
        return {
            # Common words
            'the': 'ye', 'and': 'aur', 'or': 'ya', 'but': 'lekin', 'with': 'ke saath',
            'for': 'ke liye', 'from': 'se', 'to': 'ko', 'in': 'mein', 'on': 'par',
            'at': 'pe', 'by': 'se', 'of': 'ka', 'is': 'hai', 'are': 'hain',
            'was': 'tha', 'were': 'the', 'will': 'hoga', 'would': 'hota',
            'can': 'kar sakta', 'could': 'kar sakta tha', 'should': 'chahiye',
            'must': 'zaroor', 'may': 'shayad', 'might': 'ho sakta hai',
            
            # Pronouns
            'i': 'main', 'you': 'tum', 'he': 'wo', 'she': 'wo', 'it': 'ye',
            'we': 'hum', 'they': 'wo log', 'me': 'mujhe', 'him': 'usse',
            'her': 'usse', 'us': 'humein', 'them': 'unko', 'my': 'mera',
            'your': 'tumhara', 'his': 'uska', 'our': 'humara', 'their': 'unka',
            
            # Common verbs
            'go': 'jaana', 'come': 'aana', 'see': 'dekhna', 'know': 'jaanna',
            'think': 'sochna', 'want': 'chahna', 'need': 'chahiye', 'like': 'pasand',
            'love': 'pyaar', 'hate': 'nafrat', 'eat': 'khaana', 'drink': 'peena',
            'sleep': 'sona', 'work': 'kaam', 'play': 'khelna', 'study': 'padhna',
            'write': 'likhna', 'read': 'padhna', 'speak': 'bolna', 'listen': 'sunna',
            
            # Common nouns
            'house': 'ghar', 'home': 'ghar', 'school': 'school', 'college': 'college',
            'office': 'office', 'car': 'gaadi', 'bike': 'bike', 'phone': 'phone',
            'computer': 'computer', 'book': 'kitaab', 'food': 'khaana', 'water': 'paani',
            'money': 'paisa', 'time': 'time', 'day': 'din', 'night': 'raat',
            'morning': 'subah', 'evening': 'shaam', 'friend': 'dost', 'family': 'family',
            
            # Adjectives
            'good': 'achha', 'bad': 'bura', 'big': 'bada', 'small': 'chota',
            'new': 'naya', 'old': 'purana', 'hot': 'garam', 'cold': 'thanda',
            'fast': 'tez', 'slow': 'dheema', 'easy': 'aasan', 'difficult': 'mushkil',
            'important': 'zaroori', 'nice': 'achha', 'beautiful': 'sundar',
            
            # Numbers
            'one': 'ek', 'two': 'do', 'three': 'teen', 'four': 'chaar',
            'five': 'paanch', 'six': 'che', 'seven': 'saat', 'eight': 'aath',
            'nine': 'nau', 'ten': 'das', 'hundred': 'sau', 'thousand': 'hazaar',
            
            # Question words
            'what': 'kya', 'where': 'kahan', 'when': 'kab', 'why': 'kyun',
            'how': 'kaise', 'who': 'kaun', 'which': 'konsa',
            
            # Common phrases
            'please': 'please', 'thank you': 'dhanyawad', 'sorry': 'sorry',
            'excuse me': 'excuse me', 'hello': 'namaste', 'goodbye': 'alvida',
            'yes': 'haan', 'no': 'nahi', 'maybe': 'shayad', 'okay': 'theek hai',
            'right now': 'abhi', 'later': 'baad mein', 'always': 'hamesha',
            'never': 'kabhi nahi', 'sometimes': 'kabhi kabhi', 'often': 'aksar'
        }
    
    def split_text_into_chunks(self, text: str, chunk_size: int = 2000) -> List[str]:
        """Split text into manageable chunks for processing"""
        sentences = sent_tokenize(text)
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) + 1 <= chunk_size:
                current_chunk += sentence + " "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + " "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def translate_to_hinglish(self, text: str) -> str:
        """Translate English text to Hinglish"""
        # Clean and preprocess text
        text = self._clean_text(text)
        
        # Split into sentences for better translation
        sentences = sent_tokenize(text)
        translated_sentences = []
        
        for sentence in sentences:
            translated_sentence = self._translate_sentence(sentence)
            translated_sentences.append(translated_sentence)
        
        return ' '.join(translated_sentences)
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?;:()-]', '', text)
        return text.strip()
    
    def _translate_sentence(self, sentence: str) -> str:
        """Translate a single sentence to Hinglish"""
        words = word_tokenize(sentence.lower())
        translated_words = []
        
        for word in words:
            # Remove punctuation for lookup
            clean_word = re.sub(r'[^\w]', '', word)
            
            if clean_word in self.hinglish_dict:
                # Use Hinglish equivalent
                translated_words.append(self.hinglish_dict[clean_word])
            elif len(clean_word) > 0:
                # Keep original word for complex/technical terms
                translated_words.append(word)
        
        # Reconstruct sentence with basic Hinglish grammar
        result = ' '.join(translated_words)
        
        # Apply basic grammar transformations
        result = self._apply_hinglish_grammar(result)
        
        return result
    
    def _apply_hinglish_grammar(self, text: str) -> str:
        """Apply basic Hinglish grammar rules"""
        # Simple transformations for common patterns
        
        # "I am" -> "main hun"
        text = re.sub(r'\bmain am\b', 'main hun', text, flags=re.IGNORECASE)
        
        # "you are" -> "tum ho"
        text = re.sub(r'\btum are\b', 'tum ho', text, flags=re.IGNORECASE)
        
        # "he/she is" -> "wo hai"
        text = re.sub(r'\bwo is\b', 'wo hai', text, flags=re.IGNORECASE)
        
        # "we are" -> "hum hain"
        text = re.sub(r'\bhum are\b', 'hum hain', text, flags=re.IGNORECASE)
        
        # "they are" -> "wo log hain"
        text = re.sub(r'\bwo log are\b', 'wo log hain', text, flags=re.IGNORECASE)
        
        # Add more natural Hinglish flow
        text = self._add_hinglish_connectors(text)
        
        return text
    
    def _add_hinglish_connectors(self, text: str) -> str:
        """Add natural Hinglish connectors and flow"""
        # Replace formal connectors with Hinglish ones
        replacements = {
            'however': 'lekin',
            'therefore': 'isliye',
            'moreover': 'aur bhi',
            'furthermore': 'aage',
            'additionally': 'saath mein',
            'consequently': 'result mein',
            'meanwhile': 'same time mein',
            'nevertheless': 'phir bhi',
            'although': 'jabki',
            'because': 'kyunki',
            'since': 'jab se',
            'while': 'jab tak',
            'unless': 'agar nahi',
            'until': 'jab tak nahi'
        }
        
        for eng, hin in replacements.items():
            text = re.sub(r'\b' + eng + r'\b', hin, text, flags=re.IGNORECASE)
        
        return text
    
    def generate_summary(self, text: str, max_sentences: int = 5) -> str:
        """Generate a concise summary of the translated text"""
        sentences = sent_tokenize(text)
        
        if len(sentences) <= max_sentences:
            return text
        
        # Simple extractive summary based on sentence importance
        sentence_scores = {}
        
        for i, sentence in enumerate(sentences):
            words = word_tokenize(sentence.lower())
            # Remove stopwords and punctuation
            filtered_words = [word for word in words if word.isalnum() and word not in self.english_stopwords]
            
            # Score based on word frequency and position
            score = len(filtered_words)
            
            # Boost sentences at the beginning and end
            if i < len(sentences) * 0.1:  # First 10%
                score *= 1.5
            elif i > len(sentences) * 0.9:  # Last 10%
                score *= 1.3
            
            sentence_scores[i] = score
        
        # Select top sentences
        top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:max_sentences]
        top_sentences = sorted(top_sentences, key=lambda x: x[0])  # Sort by original order
        
        summary_sentences = [sentences[i] for i, _ in top_sentences]
        summary = ' '.join(summary_sentences)
        
        # Add summary header in Hinglish
        summary_header = "Ye document ka main essence hai:\n\n"
        
        return summary_header + summary
    
    def estimate_processing_time(self, text_length: int) -> int:
        """Estimate processing time in seconds based on text length"""
        # Rough estimate: 1000 characters per second
        return max(5, text_length // 1000)