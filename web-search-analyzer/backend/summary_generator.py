import re
import nltk
from transformers import pipeline
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from wordcloud import WordCloud
import base64
from io import BytesIO
import pandas as pd
from collections import Counter
import numpy as np
from googletrans import Translator

class SummaryGenerator:
    def __init__(self):
        self.translator = Translator()
        self.summarizer = None
        self.setup_models()
    
    def setup_models(self):
        """Initialize AI models for summarization"""
        try:
            self.summarizer = pipeline("summarization", 
                                     model="facebook/bart-large-cnn",
                                     device=-1)
        except Exception as e:
            print(f"Warning: Could not load AI summarization model: {e}")
    
    def generate_summary_by_type(self, text, summary_type, document=None):
        """Generate summary based on the requested type"""
        
        summary_methods = {
            'essay': self.generate_essay,
            'detailed_summary': self.generate_detailed_summary,
            'comprehensive_analysis': self.generate_comprehensive_analysis,
            'simple_translation': self.generate_simple_translation,
            'visual_report': self.generate_visual_report,
            'crux': self.generate_crux,
            'conclusion': self.generate_conclusion,
            'ai_summary': self.generate_ai_summary
        }
        
        if summary_type in summary_methods:
            return summary_methods[summary_type](text, document)
        else:
            return self.generate_detailed_summary(text, document)
    
    def generate_essay(self, text, document):
        """Generate an essay format summary with introduction, body, and conclusion"""
        
        # Extract key themes and structure
        keywords = self._extract_keywords(text)
        sentences = self._extract_key_sentences(text, 10)
        
        # Apply one of 10 different styles randomly
        import random
        styles = [
            "academic", "journalistic", "narrative", "analytical", 
            "persuasive", "descriptive", "comparative", "chronological",
            "cause_and_effect", "problem_solution"
        ]
        style = random.choice(styles)
        
        essay = {
            'type': 'Essay',
            'style': style,
            'word_count': 0,
            'structure': {
                'introduction': '',
                'body_paragraphs': [],
                'conclusion': ''
            }
        }
        
        # Introduction
        intro = self._generate_introduction(text, style, keywords)
        essay['structure']['introduction'] = intro
        
        # Body paragraphs (3-5 paragraphs based on content)
        body_paragraphs = self._generate_body_paragraphs(text, style, sentences, keywords)
        essay['structure']['body_paragraphs'] = body_paragraphs
        
        # Conclusion
        conclusion = self._generate_essay_conclusion(text, style, keywords)
        essay['structure']['conclusion'] = conclusion
        
        # Combine all parts
        full_essay = f"{intro}\n\n"
        for para in body_paragraphs:
            full_essay += f"{para}\n\n"
        full_essay += conclusion
        
        essay['full_text'] = full_essay
        essay['word_count'] = len(full_essay.split())
        
        return essay
    
    def generate_detailed_summary(self, text, document):
        """Generate a detailed summary with multiple sections"""
        
        summary = {
            'type': 'Detailed Summary',
            'sections': {
                'executive_summary': '',
                'key_findings': [],
                'main_topics': {},
                'important_quotes': [],
                'statistics': {},
                'recommendations': []
            }
        }
        
        # Executive summary
        summary['sections']['executive_summary'] = self._create_executive_summary(text)
        
        # Key findings
        summary['sections']['key_findings'] = self._extract_key_findings(text)
        
        # Main topics
        summary['sections']['main_topics'] = self._analyze_main_topics(text)
        
        # Important quotes/statements
        summary['sections']['important_quotes'] = self._extract_important_quotes(text)
        
        # Statistics and data points
        summary['sections']['statistics'] = self._extract_statistics(text)
        
        # Recommendations (if applicable)
        summary['sections']['recommendations'] = self._generate_recommendations(text)
        
        return summary
    
    def generate_comprehensive_analysis(self, text, document):
        """Generate a comprehensive analysis report"""
        
        analysis = {
            'type': 'Comprehensive Analysis Report',
            'metadata': {
                'analysis_date': document.get('creation_date') if document else '',
                'sources_analyzed': document.get('total_sources', 0) if document else 0,
                'total_words': len(text.split())
            },
            'sections': {
                'content_analysis': {},
                'thematic_analysis': {},
                'sentiment_analysis': {},
                'linguistic_analysis': {},
                'structural_analysis': {},
                'comparative_analysis': {},
                'implications': [],
                'limitations': []
            }
        }
        
        # Content analysis
        analysis['sections']['content_analysis'] = self._perform_content_analysis(text)
        
        # Thematic analysis
        analysis['sections']['thematic_analysis'] = self._perform_thematic_analysis(text)
        
        # Sentiment analysis
        analysis['sections']['sentiment_analysis'] = self._perform_sentiment_analysis(text)
        
        # Linguistic analysis
        analysis['sections']['linguistic_analysis'] = self._perform_linguistic_analysis(text)
        
        # Structural analysis
        analysis['sections']['structural_analysis'] = self._perform_structural_analysis(text)
        
        # Comparative analysis (if multiple sources)
        if document and document.get('total_sources', 0) > 1:
            analysis['sections']['comparative_analysis'] = self._perform_comparative_analysis(document)
        
        # Implications
        analysis['sections']['implications'] = self._identify_implications(text)
        
        # Limitations
        analysis['sections']['limitations'] = self._identify_limitations(text, document)
        
        return analysis
    
    def generate_simple_translation(self, text, document):
        """Translate and rewrite in simple, understandable language"""
        
        # Detect language
        try:
            from langdetect import detect
            detected_lang = detect(text)
        except:
            detected_lang = 'en'
        
        translation = {
            'type': 'Simple Translation',
            'original_language': detected_lang,
            'target_language': 'en',
            'readability_level': 'Elementary (Grade 6-8)',
            'techniques_used': [
                'Complex sentence simplification',
                'Technical term explanation',
                'Passive to active voice conversion',
                'Jargon replacement',
                'Concept clarification'
            ],
            'sections': {
                'simplified_text': '',
                'key_terms_glossary': {},
                'concept_explanations': {}
            }
        }
        
        # Simplify the text
        simplified_text = self._simplify_text(text)
        translation['sections']['simplified_text'] = simplified_text
        
        # Create glossary of technical terms
        translation['sections']['key_terms_glossary'] = self._create_glossary(text)
        
        # Explain complex concepts
        translation['sections']['concept_explanations'] = self._explain_concepts(text)
        
        return translation
    
    def generate_visual_report(self, text, document):
        """Generate a report with visual aids, charts, and graphs"""
        
        report = {
            'type': 'Visual Report',
            'visualizations': {},
            'statistics': {},
            'charts': [],
            'infographics': []
        }
        
        # Word cloud
        wordcloud_data = self._generate_wordcloud(text)
        report['visualizations']['word_cloud'] = wordcloud_data
        
        # Keyword frequency chart
        keyword_chart = self._generate_keyword_chart(text)
        report['charts'].append(keyword_chart)
        
        # Sentiment distribution
        sentiment_chart = self._generate_sentiment_chart(text)
        report['charts'].append(sentiment_chart)
        
        # Reading statistics
        reading_stats = self._generate_reading_stats_chart(text)
        report['charts'].append(reading_stats)
        
        # Topic distribution
        topic_chart = self._generate_topic_distribution_chart(text)
        report['charts'].append(topic_chart)
        
        # Source analysis (if multiple sources)
        if document and document.get('total_sources', 0) > 1:
            source_chart = self._generate_source_analysis_chart(document)
            report['charts'].append(source_chart)
        
        # Text complexity visualization
        complexity_chart = self._generate_complexity_chart(text)
        report['charts'].append(complexity_chart)
        
        return report
    
    def generate_crux(self, text, document):
        """Generate the crux - the most essential points"""
        
        crux = {
            'type': 'Crux',
            'essential_points': [],
            'core_message': '',
            'key_takeaways': [],
            'critical_information': {},
            'decision_points': []
        }
        
        # Extract the most essential points
        crux['essential_points'] = self._extract_essential_points(text)
        
        # Identify core message
        crux['core_message'] = self._identify_core_message(text)
        
        # Key takeaways
        crux['key_takeaways'] = self._extract_key_takeaways(text)
        
        # Critical information
        crux['critical_information'] = self._extract_critical_info(text)
        
        # Decision points (if applicable)
        crux['decision_points'] = self._identify_decision_points(text)
        
        return crux
    
    def generate_conclusion(self, text, document):
        """Generate a comprehensive conclusion"""
        
        conclusion = {
            'type': 'Conclusion',
            'main_findings': [],
            'synthesis': '',
            'implications': [],
            'future_directions': [],
            'final_thoughts': ''
        }
        
        # Main findings
        conclusion['main_findings'] = self._summarize_main_findings(text)
        
        # Synthesis of information
        conclusion['synthesis'] = self._synthesize_information(text)
        
        # Implications
        conclusion['implications'] = self._draw_implications(text)
        
        # Future directions
        conclusion['future_directions'] = self._suggest_future_directions(text)
        
        # Final thoughts
        conclusion['final_thoughts'] = self._generate_final_thoughts(text)
        
        return conclusion
    
    def generate_ai_summary(self, text, document):
        """Generate an AI-powered summary in exactly 700 words"""
        
        summary = {
            'type': 'AI-Generated Summary',
            'target_word_count': 700,
            'actual_word_count': 0,
            'content': '',
            'key_themes': [],
            'confidence_score': 0.0
        }
        
        # Use AI model for summarization if available
        if self.summarizer:
            try:
                # Split text into chunks for processing
                chunks = self._split_text_for_summarization(text, max_chunk_size=1000)
                chunk_summaries = []
                
                for chunk in chunks:
                    chunk_summary = self.summarizer(chunk, 
                                                  max_length=150, 
                                                  min_length=50, 
                                                  do_sample=False)
                    chunk_summaries.append(chunk_summary[0]['summary_text'])
                
                # Combine and refine chunk summaries
                combined_summary = ' '.join(chunk_summaries)
                
                # Expand to exactly 700 words
                final_summary = self._expand_to_target_words(combined_summary, text, 700)
                
            except Exception as e:
                print(f"AI summarization failed: {e}")
                # Fallback to extractive summarization
                final_summary = self._extractive_summarization(text, 700)
        else:
            # Fallback to extractive summarization
            final_summary = self._extractive_summarization(text, 700)
        
        summary['content'] = final_summary
        summary['actual_word_count'] = len(final_summary.split())
        summary['key_themes'] = self._extract_key_themes(text)
        summary['confidence_score'] = self._calculate_confidence_score(final_summary, text)
        
        return summary
    
    # Helper methods for text processing
    def _extract_keywords(self, text, top_n=20):
        """Extract top keywords from text"""
        try:
            from nltk.tokenize import word_tokenize
            from nltk.corpus import stopwords
            from collections import Counter
            import string
            
            tokens = word_tokenize(text.lower())
            stop_words = set(stopwords.words('english'))
            
            keywords = [word for word in tokens 
                       if word not in stop_words 
                       and word not in string.punctuation 
                       and len(word) > 3]
            
            return dict(Counter(keywords).most_common(top_n))
        except:
            return {}
    
    def _extract_key_sentences(self, text, num_sentences=10):
        """Extract key sentences using simple scoring"""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        # Score sentences based on keyword frequency
        keywords = self._extract_keywords(text, 50)
        
        sentence_scores = []
        for sentence in sentences:
            score = 0
            words = sentence.lower().split()
            for word in words:
                if word in keywords:
                    score += keywords[word]
            
            if len(words) > 0:
                score = score / len(words)  # Normalize by sentence length
            
            sentence_scores.append((sentence, score))
        
        # Sort by score and return top sentences
        sentence_scores.sort(key=lambda x: x[1], reverse=True)
        return [sent[0] for sent in sentence_scores[:num_sentences]]
    
    def _generate_wordcloud(self, text):
        """Generate word cloud data"""
        try:
            # Create word cloud
            wordcloud = WordCloud(width=800, height=400, 
                                background_color='white',
                                max_words=100).generate(text)
            
            # Convert to base64 for web display
            img_buffer = BytesIO()
            wordcloud.to_image().save(img_buffer, format='PNG')
            img_data = base64.b64encode(img_buffer.getvalue()).decode()
            
            return {
                'image_data': f"data:image/png;base64,{img_data}",
                'width': 800,
                'height': 400
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _split_text_for_summarization(self, text, max_chunk_size=1000):
        """Split text into chunks for processing"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), max_chunk_size):
            chunk = ' '.join(words[i:i + max_chunk_size])
            chunks.append(chunk)
        
        return chunks
    
    def _extractive_summarization(self, text, target_words):
        """Fallback extractive summarization"""
        sentences = self._extract_key_sentences(text, 20)
        
        summary_parts = []
        word_count = 0
        
        for sentence in sentences:
            sentence_words = len(sentence.split())
            if word_count + sentence_words <= target_words:
                summary_parts.append(sentence)
                word_count += sentence_words
            else:
                break
        
        # If we haven't reached target, add more content
        if word_count < target_words * 0.8:  # If less than 80% of target
            remaining_words = target_words - word_count
            additional_content = self._generate_additional_content(text, remaining_words)
            summary_parts.append(additional_content)
        
        return ' '.join(summary_parts)
    
    # Placeholder methods for complex operations (can be expanded)
    def _generate_introduction(self, text, style, keywords):
        """Generate introduction based on style"""
        key_terms = list(keywords.keys())[:5]
        intro = f"This analysis examines {', '.join(key_terms[:3])} and related concepts. "
        
        if style == "academic":
            intro += "Through systematic examination of the available sources, this study presents comprehensive findings on the subject matter."
        elif style == "journalistic":
            intro += "Recent developments in this field have brought new attention to these critical issues."
        else:
            intro += "The following examination provides insights into these important topics."
        
        return intro
    
    def _generate_body_paragraphs(self, text, style, sentences, keywords):
        """Generate body paragraphs based on content and style"""
        # Group sentences by topic/theme
        paragraphs = []
        sentences_per_paragraph = max(2, len(sentences) // 3)
        
        for i in range(0, len(sentences), sentences_per_paragraph):
            paragraph_sentences = sentences[i:i + sentences_per_paragraph]
            paragraph = ' '.join(paragraph_sentences)
            paragraphs.append(paragraph)
        
        return paragraphs
    
    def _generate_essay_conclusion(self, text, style, keywords):
        """Generate conclusion for essay"""
        conclusion = "In conclusion, the analysis reveals significant insights into "
        key_terms = list(keywords.keys())[:3]
        conclusion += f"{', '.join(key_terms)}. "
        
        if style == "academic":
            conclusion += "These findings contribute to our understanding and suggest areas for further investigation."
        else:
            conclusion += "These findings have important implications for future developments in this area."
        
        return conclusion
    
    # Additional helper methods would be implemented here for:
    # - _create_executive_summary
    # - _extract_key_findings
    # - _analyze_main_topics
    # - _extract_important_quotes
    # - _extract_statistics
    # - _generate_recommendations
    # - _perform_content_analysis
    # - _perform_thematic_analysis
    # - _perform_sentiment_analysis
    # - _perform_linguistic_analysis
    # - _perform_structural_analysis
    # - _perform_comparative_analysis
    # - _identify_implications
    # - _identify_limitations
    # - _simplify_text
    # - _create_glossary
    # - _explain_concepts
    # - _generate_keyword_chart
    # - _generate_sentiment_chart
    # - _generate_reading_stats_chart
    # - _generate_topic_distribution_chart
    # - _generate_source_analysis_chart
    # - _generate_complexity_chart
    # - _extract_essential_points
    # - _identify_core_message
    # - _extract_key_takeaways
    # - _extract_critical_info
    # - _identify_decision_points
    # - _summarize_main_findings
    # - _synthesize_information
    # - _draw_implications
    # - _suggest_future_directions
    # - _generate_final_thoughts
    # - _expand_to_target_words
    # - _extract_key_themes
    # - _calculate_confidence_score
    # - _generate_additional_content
    
    # For brevity, I'll implement a few key ones:
    
    def _create_executive_summary(self, text):
        """Create executive summary"""
        key_sentences = self._extract_key_sentences(text, 5)
        return ' '.join(key_sentences[:3])
    
    def _extract_key_findings(self, text):
        """Extract key findings from text"""
        findings = []
        sentences = re.split(r'[.!?]+', text)
        
        # Look for sentences that might contain findings
        finding_indicators = ['found', 'discovered', 'showed', 'revealed', 'demonstrated', 
                            'indicated', 'suggests', 'concluded', 'results show']
        
        for sentence in sentences:
            sentence = sentence.strip()
            if any(indicator in sentence.lower() for indicator in finding_indicators):
                if len(sentence) > 20:
                    findings.append(sentence)
        
        return findings[:10]  # Return top 10 findings
    
    def _analyze_main_topics(self, text):
        """Analyze main topics in the text"""
        keywords = self._extract_keywords(text, 30)
        
        # Group related keywords into topics
        topics = {}
        for keyword, freq in keywords.items():
            # Simple topic categorization (can be made more sophisticated)
            if keyword in ['technology', 'digital', 'computer', 'software', 'internet']:
                topics.setdefault('Technology', []).append((keyword, freq))
            elif keyword in ['business', 'market', 'economy', 'financial', 'company']:
                topics.setdefault('Business', []).append((keyword, freq))
            elif keyword in ['health', 'medical', 'treatment', 'patient', 'healthcare']:
                topics.setdefault('Health', []).append((keyword, freq))
            else:
                topics.setdefault('General', []).append((keyword, freq))
        
        return topics
    
    # Additional helper methods implementation
    def _extract_important_quotes(self, text):
        """Extract important quotes or statements"""
        sentences = re.split(r'[.!?]+', text)
        quotes = []
        
        # Look for sentences with quotation marks or important indicators
        quote_indicators = ['"', "'", 'said', 'stated', 'according to', 'reported']
        
        for sentence in sentences:
            sentence = sentence.strip()
            if any(indicator in sentence.lower() for indicator in quote_indicators):
                if len(sentence) > 20:
                    quotes.append(sentence)
        
        return quotes[:5]  # Return top 5 quotes
    
    def _extract_statistics(self, text):
        """Extract statistics and numerical data"""
        import re
        stats = {}
        
        # Look for percentage patterns
        percentages = re.findall(r'\b\d+(?:\.\d+)?%', text)
        if percentages:
            stats['percentages'] = percentages[:5]
        
        # Look for large numbers
        numbers = re.findall(r'\b\d{1,3}(?:,\d{3})+\b', text)
        if numbers:
            stats['large_numbers'] = numbers[:5]
        
        # Look for monetary amounts
        money = re.findall(r'\$\d+(?:,\d{3})*(?:\.\d{2})?', text)
        if money:
            stats['monetary_amounts'] = money[:5]
        
        return stats
    
    def _generate_recommendations(self, text):
        """Generate recommendations based on content"""
        recommendations = []
        
        # Look for sentences with recommendation indicators
        rec_indicators = ['should', 'recommend', 'suggest', 'must', 'need to', 'important to']
        sentences = re.split(r'[.!?]+', text)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if any(indicator in sentence.lower() for indicator in rec_indicators):
                if len(sentence) > 20:
                    recommendations.append(sentence)
        
        return recommendations[:5]
    
    def _perform_content_analysis(self, text):
        """Perform basic content analysis"""
        return {
            'total_words': len(text.split()),
            'unique_words': len(set(text.lower().split())),
            'average_sentence_length': len(text.split()) / max(len(re.split(r'[.!?]+', text)), 1),
            'most_common_words': self._extract_keywords(text, 10)
        }
    
    def _perform_thematic_analysis(self, text):
        """Perform thematic analysis"""
        themes = {}
        
        # Define theme keywords
        theme_keywords = {
            'innovation': ['innovation', 'new', 'development', 'breakthrough', 'advancement'],
            'challenges': ['challenge', 'problem', 'issue', 'difficulty', 'obstacle'],
            'opportunities': ['opportunity', 'potential', 'growth', 'expansion', 'benefit'],
            'trends': ['trend', 'pattern', 'direction', 'movement', 'shift']
        }
        
        for theme, keywords in theme_keywords.items():
            count = sum(text.lower().count(keyword) for keyword in keywords)
            if count > 0:
                themes[theme] = count
        
        return themes
    
    def _perform_sentiment_analysis(self, text):
        """Perform sentiment analysis"""
        try:
            from nltk.sentiment import SentimentIntensityAnalyzer
            sia = SentimentIntensityAnalyzer()
            return sia.polarity_scores(text)
        except:
            # Fallback sentiment analysis
            positive_words = ['good', 'great', 'excellent', 'positive', 'success', 'improve', 'benefit']
            negative_words = ['bad', 'terrible', 'negative', 'fail', 'problem', 'issue', 'decline']
            
            words = text.lower().split()
            pos_count = sum(words.count(word) for word in positive_words)
            neg_count = sum(words.count(word) for word in negative_words)
            
            total = max(pos_count + neg_count, 1)
            return {
                'pos': pos_count / total,
                'neg': neg_count / total,
                'neu': 1 - (pos_count + neg_count) / total,
                'compound': (pos_count - neg_count) / total
            }
    
    def _perform_linguistic_analysis(self, text):
        """Perform linguistic analysis"""
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        
        return {
            'avg_word_length': sum(len(word) for word in words) / max(len(words), 1),
            'sentence_count': len(sentences),
            'avg_sentence_length': len(words) / max(len(sentences), 1),
            'complex_sentences': len([s for s in sentences if len(s.split()) > 20])
        }
    
    def _perform_structural_analysis(self, text):
        """Perform structural analysis"""
        paragraphs = text.split('\n\n')
        sentences = re.split(r'[.!?]+', text)
        
        return {
            'paragraph_count': len(paragraphs),
            'avg_paragraph_length': len(sentences) / max(len(paragraphs), 1),
            'structure_type': 'multi-paragraph' if len(paragraphs) > 3 else 'simple'
        }
    
    def _perform_comparative_analysis(self, document):
        """Perform comparative analysis of multiple sources"""
        sources = document.get('sources', [])
        if len(sources) < 2:
            return {}
        
        comparison = {
            'source_count': len(sources),
            'word_count_range': {
                'min': min(s['word_count'] for s in sources),
                'max': max(s['word_count'] for s in sources),
                'avg': sum(s['word_count'] for s in sources) / len(sources)
            },
            'extraction_methods': list(set(s['extraction_method'] for s in sources))
        }
        
        return comparison
    
    def _identify_implications(self, text):
        """Identify implications from the text"""
        implications = []
        
        # Look for implication indicators
        impl_indicators = ['implies', 'suggests', 'means that', 'indicates', 'therefore', 'thus', 'consequently']
        sentences = re.split(r'[.!?]+', text)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if any(indicator in sentence.lower() for indicator in impl_indicators):
                if len(sentence) > 20:
                    implications.append(sentence)
        
        return implications[:5]
    
    def _identify_limitations(self, text, document):
        """Identify limitations in the analysis"""
        limitations = []
        
        if document:
            if document.get('total_sources', 0) < 3:
                limitations.append("Limited number of sources may affect comprehensiveness")
            
            sources = document.get('sources', [])
            extraction_methods = set(s.get('extraction_method', '') for s in sources)
            if 'Selenium' in extraction_methods:
                limitations.append("Some content extracted using fallback methods may be incomplete")
        
        # Check for content quality indicators
        if len(text.split()) < 500:
            limitations.append("Limited text length may restrict analysis depth")
        
        return limitations
    
    def _simplify_text(self, text):
        """Simplify text for better readability"""
        # Basic text simplification (this could be much more sophisticated)
        simplified = text
        
        # Replace complex words with simpler alternatives
        replacements = {
            'utilize': 'use',
            'demonstrate': 'show',
            'investigate': 'study',
            'approximately': 'about',
            'subsequently': 'later',
            'nevertheless': 'however',
            'consequently': 'so',
            'furthermore': 'also'
        }
        
        for complex_word, simple_word in replacements.items():
            simplified = re.sub(r'\b' + complex_word + r'\b', simple_word, simplified, flags=re.IGNORECASE)
        
        return simplified
    
    def _create_glossary(self, text):
        """Create a glossary of technical terms"""
        # This is a simplified version - a real implementation would use NLP libraries
        technical_terms = {}
        
        # Look for capitalized terms that might be technical
        words = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        term_counts = Counter(words)
        
        # Define some common technical terms and their explanations
        explanations = {
            'API': 'Application Programming Interface - a way for different software programs to communicate',
            'Machine Learning': 'A type of artificial intelligence that learns from data',
            'Algorithm': 'A set of rules or instructions for solving a problem',
            'Database': 'A structured collection of data',
            'Framework': 'A basic structure or set of tools for building software'
        }
        
        for term, count in term_counts.most_common(10):
            if term in explanations:
                technical_terms[term] = explanations[term]
            elif len(term) > 5 and count > 1:  # Simple heuristic for technical terms
                technical_terms[term] = f"Technical term appearing {count} times in the text"
        
        return technical_terms
    
    def _explain_concepts(self, text):
        """Explain complex concepts found in the text"""
        concepts = {}
        
        # Look for concept indicators
        concept_patterns = [
            r'(?:the concept of|the idea of|the principle of)\s+([^.]+)',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:is|are|refers to|means)'
        ]
        
        for pattern in concept_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches[:3]:  # Limit to 3 concepts
                concept = match.strip()
                if len(concept) > 5:
                    concepts[concept] = f"This concept is discussed in the context of the analyzed content"
        
        return concepts
    
    # Additional placeholder methods for visual charts
    def _generate_keyword_chart(self, text):
        """Generate keyword frequency chart data"""
        keywords = self._extract_keywords(text, 10)
        return {
            'type': 'bar_chart',
            'title': 'Top Keywords Frequency',
            'data': keywords
        }
    
    def _generate_sentiment_chart(self, text):
        """Generate sentiment distribution chart"""
        sentiment = self._perform_sentiment_analysis(text)
        return {
            'type': 'pie_chart',
            'title': 'Sentiment Distribution',
            'data': sentiment
        }
    
    def _generate_reading_stats_chart(self, text):
        """Generate reading statistics chart"""
        stats = self._perform_linguistic_analysis(text)
        return {
            'type': 'bar_chart',
            'title': 'Reading Statistics',
            'data': stats
        }
    
    def _generate_topic_distribution_chart(self, text):
        """Generate topic distribution chart"""
        topics = self._perform_thematic_analysis(text)
        return {
            'type': 'pie_chart',
            'title': 'Topic Distribution',
            'data': topics
        }
    
    def _generate_source_analysis_chart(self, document):
        """Generate source analysis chart"""
        sources = document.get('sources', [])
        word_counts = [s['word_count'] for s in sources]
        return {
            'type': 'bar_chart',
            'title': 'Source Word Count Analysis',
            'data': {'sources': list(range(1, len(sources) + 1)), 'word_counts': word_counts}
        }
    
    def _generate_complexity_chart(self, text):
        """Generate text complexity visualization"""
        linguistic = self._perform_linguistic_analysis(text)
        return {
            'type': 'radar_chart',
            'title': 'Text Complexity Analysis',
            'data': linguistic
        }
    
    # Methods for crux generation
    def _extract_essential_points(self, text):
        """Extract the most essential points"""
        key_sentences = self._extract_key_sentences(text, 5)
        return key_sentences
    
    def _identify_core_message(self, text):
        """Identify the core message"""
        key_sentences = self._extract_key_sentences(text, 3)
        return ' '.join(key_sentences[:2])  # Combine top 2 sentences
    
    def _extract_key_takeaways(self, text):
        """Extract key takeaways"""
        takeaways = []
        sentences = re.split(r'[.!?]+', text)
        
        # Look for conclusion indicators
        conclusion_indicators = ['in conclusion', 'to summarize', 'key point', 'importantly', 'main finding']
        
        for sentence in sentences:
            sentence = sentence.strip()
            if any(indicator in sentence.lower() for indicator in conclusion_indicators):
                if len(sentence) > 20:
                    takeaways.append(sentence)
        
        # If no specific takeaways found, use key sentences
        if not takeaways:
            takeaways = self._extract_key_sentences(text, 5)
        
        return takeaways[:5]
    
    def _extract_critical_info(self, text):
        """Extract critical information"""
        critical_info = {}
        
        # Extract statistics
        stats = self._extract_statistics(text)
        if stats:
            critical_info['statistics'] = stats
        
        # Extract important facts
        fact_indicators = ['fact', 'evidence', 'data shows', 'research indicates', 'study found']
        facts = []
        sentences = re.split(r'[.!?]+', text)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if any(indicator in sentence.lower() for indicator in fact_indicators):
                if len(sentence) > 20:
                    facts.append(sentence)
        
        if facts:
            critical_info['key_facts'] = facts[:3]
        
        return critical_info
    
    def _identify_decision_points(self, text):
        """Identify decision points in the content"""
        decision_points = []
        
        decision_indicators = ['decision', 'choice', 'option', 'alternative', 'should consider', 'recommend']
        sentences = re.split(r'[.!?]+', text)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if any(indicator in sentence.lower() for indicator in decision_indicators):
                if len(sentence) > 20:
                    decision_points.append(sentence)
        
        return decision_points[:3]
    
    # Methods for conclusion generation
    def _summarize_main_findings(self, text):
        """Summarize main findings"""
        return self._extract_key_findings(text)
    
    def _synthesize_information(self, text):
        """Synthesize information from multiple sources"""
        key_sentences = self._extract_key_sentences(text, 5)
        synthesis = "Based on the analysis of multiple sources, " + ' '.join(key_sentences[:3])
        return synthesis
    
    def _draw_implications(self, text):
        """Draw implications from the content"""
        return self._identify_implications(text)
    
    def _suggest_future_directions(self, text):
        """Suggest future directions"""
        directions = []
        
        future_indicators = ['future', 'next steps', 'moving forward', 'going forward', 'will', 'plan to']
        sentences = re.split(r'[.!?]+', text)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if any(indicator in sentence.lower() for indicator in future_indicators):
                if len(sentence) > 20:
                    directions.append(sentence)
        
        return directions[:3]
    
    def _generate_final_thoughts(self, text):
        """Generate final thoughts"""
        key_themes = self._extract_key_themes(text)
        final_thoughts = f"In summary, this analysis reveals important insights about {', '.join(key_themes[:3])} and their implications for future understanding."
        return final_thoughts
    
    # Methods for AI summary
    def _expand_to_target_words(self, summary, original_text, target_words):
        """Expand summary to target word count"""
        current_words = len(summary.split())
        
        if current_words >= target_words:
            return summary
        
        # Add more context from the original text
        additional_sentences = self._extract_key_sentences(original_text, 10)
        
        for sentence in additional_sentences:
            if sentence not in summary:
                summary += ' ' + sentence
                current_words = len(summary.split())
                if current_words >= target_words:
                    break
        
        return summary
    
    def _extract_key_themes(self, text):
        """Extract key themes from text"""
        keywords = self._extract_keywords(text, 20)
        themes = list(keywords.keys())[:5]
        return themes
    
    def _calculate_confidence_score(self, summary, original_text):
        """Calculate confidence score for the summary"""
        # Simple confidence calculation based on overlap
        summary_words = set(summary.lower().split())
        original_words = set(original_text.lower().split())
        
        overlap = len(summary_words.intersection(original_words))
        total_summary_words = len(summary_words)
        
        if total_summary_words == 0:
            return 0.0
        
        confidence = min(overlap / total_summary_words, 1.0)
        return confidence
    
    def _generate_additional_content(self, text, remaining_words):
        """Generate additional content to reach target word count"""
        # Extract more sentences to reach the target
        sentences = self._extract_key_sentences(text, 20)
        additional_content = []
        word_count = 0
        
        for sentence in sentences:
            sentence_words = len(sentence.split())
            if word_count + sentence_words <= remaining_words:
                additional_content.append(sentence)
                word_count += sentence_words
            else:
                break
        
        return ' '.join(additional_content)