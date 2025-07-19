# Web Search Analyzer

An advanced AI-powered web search and content analysis tool that provides comprehensive text analysis and summarization capabilities with 8 different summary types and 10 analytical approaches.

## Features

### 🔍 **Advanced Web Search**
- Google-like search interface with modern, responsive design
- Multi-engine search capabilities (DuckDuckGo, Bing)
- Selectable result count (10-30 results)
- Smart duplicate removal and result ranking

### 📝 **Intelligent Content Extraction**
- Multi-method content extraction using:
  - **Newspaper3k** - Best for news articles and blog posts
  - **BeautifulSoup** - General web content with ad filtering
  - **Selenium** - Dynamic content and fallback extraction
- Automatic ad and irrelevant content filtering
- Support for up to 10 sources per analysis (as requested)
- Parallel processing for faster extraction

### 🧠 **Comprehensive Text Analysis**
- **Basic Statistics**: Word count, reading time, sentence analysis
- **Readability Analysis**: Flesch scores, grade levels, complexity metrics
- **Sentiment Analysis**: NLTK VADER sentiment scoring
- **Language Detection**: Automatic language identification
- **Keyword Extraction**: Frequency analysis and topic clustering
- **Topic Analysis**: Automatic categorization and theme identification

### 📊 **8 Summary Types Available**

1. **📝 Essay Format**
   - Structured academic writing with introduction, body, and conclusion
   - 10 different writing styles: Academic, Journalistic, Narrative, Analytical, Persuasive, Descriptive, Comparative, Chronological, Cause & Effect, Problem-Solution

2. **📋 Detailed Summary**
   - Executive summary, key findings, main topics
   - Important quotes and statistical data
   - Actionable recommendations

3. **📈 Comprehensive Analysis Report**
   - Content, thematic, sentiment, and linguistic analysis
   - Structural and comparative analysis
   - Implications and limitations assessment

4. **🌍 Simple Language Translation**
   - Complex text simplified to Grade 6-8 reading level
   - Technical terms glossary
   - Concept explanations with jargon replacement

5. **📊 Visual Report**
   - Word clouds and keyword frequency charts
   - Sentiment distribution graphs
   - Reading statistics visualizations
   - Topic distribution and source analysis charts

6. **🎯 Crux (Essential Points)**
   - Core message identification
   - Essential points extraction
   - Key takeaways and critical information
   - Decision points identification

7. **🏁 Conclusion**
   - Main findings synthesis
   - Implications and future directions
   - Final thoughts and recommendations

8. **🤖 AI-Generated Summary (700 words)**
   - AI-powered summarization using BART model
   - Exactly 700 words as requested
   - Key themes extraction
   - Confidence scoring

### 🎨 **Modern User Interface**
- Google-inspired search design with glassmorphism effects
- Responsive layout for all devices
- Smooth animations and transitions
- Dark/light theme support
- Real-time loading indicators
- Toast notifications for user feedback

### 💾 **Document Management**
- View raw compiled document
- Download analysis as JSON
- Source list with metadata
- Content extraction method tracking

## Installation

### Prerequisites
- Python 3.8+
- Chrome browser (for Selenium WebDriver)
- 4GB+ RAM recommended for AI models

### Quick Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd web-search-analyzer
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Install Chrome WebDriver**
```bash
# WebDriver Manager will handle this automatically
# Or install manually from: https://chromedriver.chromium.org/
```

4. **Set up NLTK data**
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('vader_lexicon')"
```

5. **Run the application**
```bash
cd backend
python app.py
```

6. **Access the application**
Open your browser and navigate to: `http://localhost:5000`

## Usage Guide

### 1. **Performing a Search**
- Enter your search query in the Google-like search bar
- Select the number of results (10-30)
- Click "Search" or press Enter
- Browse through the search results from multiple sources

### 2. **Selecting Content**
- Click on search result items to select them (checkboxes)
- Select up to 10 links maximum (as specified in requirements)
- Use "Select All" to quickly select the first 10 results
- Use "Clear Selection" to deselect all items

### 3. **Extracting Content**
- Click "Extract Content from Selected Links"
- Wait for the system to process and extract content
- The tool will automatically filter out ads and irrelevant content
- Progress indicators show the extraction status

### 4. **Generating Summaries**
- Choose from 8 different summary types
- Each type offers unique perspectives and analysis styles
- The AI will process your compiled document
- View results in the formatted display area

### 5. **Accessing Raw Data**
- Use "View Raw Document" to see the complete extracted text
- "Download Document" saves the analysis as JSON
- "View Source List" shows metadata about each source

## Technical Architecture

### Backend Components

**app.py** - Flask web server with API endpoints:
- `/search` - Web search functionality
- `/extract` - Content extraction from URLs
- `/generate_summary` - Summary generation

**summary_generator.py** - AI-powered analysis engine:
- 8 different summary generation methods
- 10 different analytical approaches
- Advanced NLP processing
- Visual report generation

### Frontend Components

**templates/index.html** - Modern, responsive UI
**static/css/styles.css** - Beautiful styling with animations
**static/js/app.js** - Interactive JavaScript application

### Key Technologies

- **Backend**: Flask, BeautifulSoup, Selenium, NLTK, Transformers
- **AI/ML**: BART summarization model, VADER sentiment analysis
- **Frontend**: Vanilla JavaScript, CSS3, HTML5
- **Visualization**: Plotly.js, WordCloud, Matplotlib
- **Data Processing**: Pandas, NumPy

## API Endpoints

### POST /search
Search the web for content
```json
{
  "query": "search terms",
  "num_results": 20
}
```

### POST /extract
Extract content from selected URLs
```json
{
  "urls": ["url1", "url2", ...]
}
```

### POST /generate_summary
Generate specific type of summary
```json
{
  "document": {...},
  "type": "essay|detailed_summary|comprehensive_analysis|..."
}
```

## Configuration

### Environment Variables
- `FLASK_ENV` - Set to 'development' for debug mode
- `OPENAI_API_KEY` - Optional: For enhanced AI features
- `ANTHROPIC_API_KEY` - Optional: For additional AI capabilities

### Customization Options
- Modify search engines in `WebSearchAnalyzer.search_web()`
- Adjust content extraction methods in `_extract_single_content()`
- Customize summary styles in `SummaryGenerator`
- Update UI themes in `styles.css`

## Performance Optimization

- **Parallel Processing**: Content extraction uses threading
- **Caching**: Browser sessions cached for faster searches
- **Resource Management**: Automatic cleanup of WebDriver instances
- **Memory Optimization**: Chunked processing for large documents

## Security Features

- **Input Sanitization**: All user inputs are validated and escaped
- **Safe Content Extraction**: Protection against malicious websites
- **CSRF Protection**: Built-in Flask security measures
- **Rate Limiting**: Prevents abuse of search endpoints

## Browser Compatibility

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Known Limitations

1. **Content Extraction**: Some heavily JavaScript-dependent sites may not extract perfectly
2. **AI Models**: BART model requires significant computational resources
3. **Rate Limits**: Search engines may impose rate limiting
4. **Language Support**: Best results with English content

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or contributions:
- Create an issue on GitHub
- Check the troubleshooting section below

## Troubleshooting

### Common Issues

**Chrome WebDriver Issues**
```bash
# Update WebDriver
pip install --upgrade webdriver-manager
```

**Memory Issues with AI Models**
```bash
# Reduce model size or use CPU-only mode
# Modify setup_ai_models() in summary_generator.py
```

**Search Not Working**
- Check internet connection
- Verify search engines are accessible
- Review browser permissions

**Content Extraction Failing**
- Some sites block automated access
- Try different extraction methods
- Check if sites require authentication

## Future Enhancements

- [ ] Support for more languages
- [ ] Advanced AI model integration
- [ ] Export to multiple formats (PDF, Word, etc.)
- [ ] Real-time collaboration features
- [ ] Custom analysis templates
- [ ] API rate limiting and quotas
- [ ] User authentication and saved searches
- [ ] Advanced visualization options

---

**Created with ❤️ for comprehensive web content analysis and summarization**