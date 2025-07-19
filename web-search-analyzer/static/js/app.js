// Web Search Analyzer - Main JavaScript Application
class WebSearchAnalyzer {
    constructor() {
        this.currentResults = [];
        this.selectedUrls = new Set();
        this.currentDocument = null;
        this.currentAnalysis = null;
        
        this.initializeEventListeners();
        this.initializeUI();
    }
    
    initializeEventListeners() {
        // Search functionality
        document.getElementById('search-btn').addEventListener('click', () => this.performSearch());
        document.getElementById('search-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.performSearch();
        });
        
        // Suggestion buttons
        document.querySelectorAll('.suggestion-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const query = e.target.dataset.query;
                document.getElementById('search-input').value = query;
                this.performSearch();
            });
        });
        
        // Results controls
        document.getElementById('select-all-btn').addEventListener('click', () => this.selectAllResults());
        document.getElementById('clear-selection-btn').addEventListener('click', () => this.clearSelection());
        document.getElementById('extract-btn').addEventListener('click', () => this.extractContent());
        
        // Summary type buttons
        document.querySelectorAll('.summary-type-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.selectSummaryType(e.target.closest('.summary-type-btn')));
        });
        
        // Document actions
        document.getElementById('view-raw-btn').addEventListener('click', () => this.viewRawDocument());
        document.getElementById('download-doc-btn').addEventListener('click', () => this.downloadDocument());
        document.getElementById('view-sources-btn').addEventListener('click', () => this.viewSources());
        
        // Modal controls
        document.querySelectorAll('.modal-close').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const modalId = e.target.dataset.modal;
                this.closeModal(modalId);
            });
        });
        
        // Message close buttons
        document.getElementById('error-close').addEventListener('click', () => this.hideMessage('error'));
        document.getElementById('success-close').addEventListener('click', () => this.hideMessage('success'));
        
        // Click outside modal to close
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal')) {
                e.target.style.display = 'none';
            }
        });
    }
    
    initializeUI() {
        // Set initial states
        this.updateSelectedCount();
        this.toggleExtractButton();
    }
    
    async performSearch() {
        const query = document.getElementById('search-input').value.trim();
        const numResults = parseInt(document.getElementById('num-results').value);
        
        if (!query) {
            this.showMessage('error', 'Please enter a search query');
            return;
        }
        
        this.showLoading('Searching the web...', 'Finding relevant content for your query');
        
        try {
            const response = await fetch('/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    query: query,
                    num_results: numResults
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.currentResults = data.results;
                this.displayResults(data.results);
                this.showSection('results-section');
                this.showMessage('success', `Found ${data.total_results} results for "${query}"`);
            } else {
                throw new Error(data.error || 'Search failed');
            }
        } catch (error) {
            console.error('Search error:', error);
            this.showMessage('error', `Search failed: ${error.message}`);
        } finally {
            this.hideLoading();
        }
    }
    
    displayResults(results) {
        const container = document.getElementById('search-results');
        container.innerHTML = '';
        
        if (results.length === 0) {
            container.innerHTML = '<p class="no-results">No results found. Try a different search query.</p>';
            return;
        }
        
        results.forEach((result, index) => {
            const resultElement = this.createResultElement(result, index);
            container.appendChild(resultElement);
        });
        
        this.clearSelection();
    }
    
    createResultElement(result, index) {
        const div = document.createElement('div');
        div.className = 'result-item';
        div.dataset.url = result.url;
        div.dataset.index = index;
        
        div.innerHTML = `
            <input type="checkbox" class="result-checkbox" id="result-${index}">
            <div class="result-title">${this.escapeHtml(result.title)}</div>
            <div class="result-url">${this.escapeHtml(result.url)}</div>
            <div class="result-snippet">${this.escapeHtml(result.snippet)}</div>
            <span class="result-source">${this.escapeHtml(result.source)}</span>
        `;
        
        // Add click handlers
        const checkbox = div.querySelector('.result-checkbox');
        
        div.addEventListener('click', (e) => {
            if (e.target.type !== 'checkbox') {
                checkbox.click();
            }
        });
        
        checkbox.addEventListener('change', (e) => {
            e.stopPropagation();
            this.toggleResultSelection(result.url, div, checkbox.checked);
        });
        
        return div;
    }
    
    toggleResultSelection(url, element, selected) {
        if (selected && this.selectedUrls.size >= 10) {
            this.showMessage('error', 'Maximum 10 links can be selected');
            element.querySelector('.result-checkbox').checked = false;
            return;
        }
        
        if (selected) {
            this.selectedUrls.add(url);
            element.classList.add('selected');
        } else {
            this.selectedUrls.delete(url);
            element.classList.remove('selected');
        }
        
        this.updateSelectedCount();
        this.toggleExtractButton();
    }
    
    selectAllResults() {
        const checkboxes = document.querySelectorAll('.result-checkbox');
        const maxSelections = Math.min(10, checkboxes.length);
        
        this.clearSelection();
        
        for (let i = 0; i < maxSelections; i++) {
            const checkbox = checkboxes[i];
            const resultItem = checkbox.closest('.result-item');
            const url = resultItem.dataset.url;
            
            checkbox.checked = true;
            this.selectedUrls.add(url);
            resultItem.classList.add('selected');
        }
        
        this.updateSelectedCount();
        this.toggleExtractButton();
        
        if (checkboxes.length > 10) {
            this.showMessage('success', 'Selected first 10 results (maximum allowed)');
        }
    }
    
    clearSelection() {
        this.selectedUrls.clear();
        document.querySelectorAll('.result-item').forEach(item => {
            item.classList.remove('selected');
            item.querySelector('.result-checkbox').checked = false;
        });
        
        this.updateSelectedCount();
        this.toggleExtractButton();
    }
    
    updateSelectedCount() {
        document.getElementById('selected-count').textContent = this.selectedUrls.size;
    }
    
    toggleExtractButton() {
        const extractBtn = document.getElementById('extract-btn');
        extractBtn.disabled = this.selectedUrls.size === 0;
    }
    
    async extractContent() {
        if (this.selectedUrls.size === 0) {
            this.showMessage('error', 'Please select at least one link');
            return;
        }
        
        const urls = Array.from(this.selectedUrls);
        
        this.showLoading('Extracting content...', `Processing ${urls.length} selected sources`);
        
        try {
            const response = await fetch('/extract', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    urls: urls
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.currentDocument = data.document;
                this.currentAnalysis = data.analysis;
                
                this.displayAnalysisSection();
                this.showSection('analysis-section');
                this.showMessage('success', `Successfully extracted content from ${data.extracted_count} sources`);
            } else {
                throw new Error(data.error || 'Content extraction failed');
            }
        } catch (error) {
            console.error('Extraction error:', error);
            this.showMessage('error', `Content extraction failed: ${error.message}`);
        } finally {
            this.hideLoading();
        }
    }
    
    displayAnalysisSection() {
        if (!this.currentDocument) return;
        
        // Update stats
        document.getElementById('sources-count').textContent = this.currentDocument.total_sources;
        document.getElementById('words-count').textContent = this.currentDocument.total_words.toLocaleString();
        
        // Calculate reading time (average 200 words per minute)
        const readingTime = Math.ceil(this.currentDocument.total_words / 200);
        document.getElementById('reading-time').textContent = `${readingTime} min`;
        
        // Clear previous summary
        const summaryDisplay = document.getElementById('summary-display');
        summaryDisplay.style.display = 'none';
        summaryDisplay.innerHTML = '';
        
        // Clear previous selections
        document.querySelectorAll('.summary-type-btn').forEach(btn => {
            btn.classList.remove('selected');
        });
    }
    
    async selectSummaryType(button) {
        // Update UI
        document.querySelectorAll('.summary-type-btn').forEach(btn => {
            btn.classList.remove('selected');
        });
        button.classList.add('selected');
        
        const summaryType = button.dataset.type;
        
        this.showLoading('Generating summary...', `Creating ${button.querySelector('.type-name').textContent}`);
        
        try {
            const response = await fetch('/generate_summary', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    document: this.currentDocument,
                    type: summaryType
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.displaySummary(data.result, data.type);
                this.showMessage('success', 'Summary generated successfully');
            } else {
                throw new Error(data.error || 'Summary generation failed');
            }
        } catch (error) {
            console.error('Summary generation error:', error);
            this.showMessage('error', `Summary generation failed: ${error.message}`);
        } finally {
            this.hideLoading();
        }
    }
    
    displaySummary(summaryData, type) {
        const summaryDisplay = document.getElementById('summary-display');
        summaryDisplay.innerHTML = this.formatSummaryContent(summaryData, type);
        summaryDisplay.style.display = 'block';
        
        // Scroll to summary
        summaryDisplay.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    
    formatSummaryContent(data, type) {
        let html = `<div class="summary-content">`;
        
        switch (type) {
            case 'essay':
                html += this.formatEssay(data);
                break;
            case 'detailed_summary':
                html += this.formatDetailedSummary(data);
                break;
            case 'comprehensive_analysis':
                html += this.formatComprehensiveAnalysis(data);
                break;
            case 'simple_translation':
                html += this.formatSimpleTranslation(data);
                break;
            case 'visual_report':
                html += this.formatVisualReport(data);
                break;
            case 'crux':
                html += this.formatCrux(data);
                break;
            case 'conclusion':
                html += this.formatConclusion(data);
                break;
            case 'ai_summary':
                html += this.formatAISummary(data);
                break;
            default:
                html += `<p>${this.escapeHtml(JSON.stringify(data, null, 2))}</p>`;
        }
        
        html += `</div>`;
        return html;
    }
    
    formatEssay(data) {
        let html = `<h2>Essay: ${data.style} Style</h2>`;
        
        if (data.structure) {
            html += `<h3>Introduction</h3>`;
            html += `<p>${this.escapeHtml(data.structure.introduction)}</p>`;
            
            html += `<h3>Main Content</h3>`;
            data.structure.body_paragraphs.forEach((paragraph, index) => {
                html += `<p><strong>Paragraph ${index + 1}:</strong> ${this.escapeHtml(paragraph)}</p>`;
            });
            
            html += `<h3>Conclusion</h3>`;
            html += `<p>${this.escapeHtml(data.structure.conclusion)}</p>`;
        }
        
        if (data.word_count) {
            html += `<p><em>Word count: ${data.word_count}</em></p>`;
        }
        
        return html;
    }
    
    formatDetailedSummary(data) {
        let html = `<h2>Detailed Summary</h2>`;
        
        if (data.sections) {
            if (data.sections.executive_summary) {
                html += `<h3>Executive Summary</h3>`;
                html += `<p>${this.escapeHtml(data.sections.executive_summary)}</p>`;
            }
            
            if (data.sections.key_findings && data.sections.key_findings.length > 0) {
                html += `<h3>Key Findings</h3>`;
                html += `<ul>`;
                data.sections.key_findings.forEach(finding => {
                    html += `<li>${this.escapeHtml(finding)}</li>`;
                });
                html += `</ul>`;
            }
            
            if (data.sections.main_topics && Object.keys(data.sections.main_topics).length > 0) {
                html += `<h3>Main Topics</h3>`;
                Object.entries(data.sections.main_topics).forEach(([topic, keywords]) => {
                    html += `<h4>${this.escapeHtml(topic)}</h4>`;
                    html += `<p>Keywords: ${keywords.map(k => k[0]).join(', ')}</p>`;
                });
            }
        }
        
        return html;
    }
    
    formatComprehensiveAnalysis(data) {
        let html = `<h2>Comprehensive Analysis Report</h2>`;
        
        if (data.metadata) {
            html += `<h3>Analysis Metadata</h3>`;
            html += `<ul>`;
            html += `<li>Sources Analyzed: ${data.metadata.sources_analyzed}</li>`;
            html += `<li>Total Words: ${data.metadata.total_words?.toLocaleString()}</li>`;
            html += `<li>Analysis Date: ${new Date(data.metadata.analysis_date).toLocaleDateString()}</li>`;
            html += `</ul>`;
        }
        
        if (data.sections) {
            Object.entries(data.sections).forEach(([sectionName, sectionData]) => {
                if (sectionData && typeof sectionData === 'object' && Object.keys(sectionData).length > 0) {
                    html += `<h3>${this.formatSectionName(sectionName)}</h3>`;
                    html += `<div class="analysis-section">`;
                    
                    if (Array.isArray(sectionData)) {
                        html += `<ul>`;
                        sectionData.forEach(item => {
                            html += `<li>${this.escapeHtml(item)}</li>`;
                        });
                        html += `</ul>`;
                    } else {
                        html += `<pre>${this.escapeHtml(JSON.stringify(sectionData, null, 2))}</pre>`;
                    }
                    
                    html += `</div>`;
                }
            });
        }
        
        return html;
    }
    
    formatSimpleTranslation(data) {
        let html = `<h2>Simple Language Translation</h2>`;
        
        html += `<div class="translation-info">`;
        html += `<p><strong>Readability Level:</strong> ${data.readability_level}</p>`;
        html += `<p><strong>Original Language:</strong> ${data.original_language}</p>`;
        html += `</div>`;
        
        if (data.sections?.simplified_text) {
            html += `<h3>Simplified Text</h3>`;
            html += `<div class="simplified-content">${this.escapeHtml(data.sections.simplified_text)}</div>`;
        }
        
        if (data.sections?.key_terms_glossary && Object.keys(data.sections.key_terms_glossary).length > 0) {
            html += `<h3>Key Terms Glossary</h3>`;
            html += `<dl>`;
            Object.entries(data.sections.key_terms_glossary).forEach(([term, definition]) => {
                html += `<dt><strong>${this.escapeHtml(term)}</strong></dt>`;
                html += `<dd>${this.escapeHtml(definition)}</dd>`;
            });
            html += `</dl>`;
        }
        
        return html;
    }
    
    formatVisualReport(data) {
        let html = `<h2>Visual Report</h2>`;
        
        if (data.visualizations?.word_cloud) {
            html += `<h3>Word Cloud</h3>`;
            html += `<div class="chart-container">`;
            if (data.visualizations.word_cloud.image_data) {
                html += `<img src="${data.visualizations.word_cloud.image_data}" alt="Word Cloud" />`;
            } else if (data.visualizations.word_cloud.error) {
                html += `<p>Error generating word cloud: ${this.escapeHtml(data.visualizations.word_cloud.error)}</p>`;
            }
            html += `</div>`;
        }
        
        if (data.charts && data.charts.length > 0) {
            html += `<h3>Charts and Graphs</h3>`;
            data.charts.forEach((chart, index) => {
                html += `<div class="chart-container" id="chart-${index}">`;
                html += `<h4>${chart.title || `Chart ${index + 1}`}</h4>`;
                // Chart content would be rendered here using Plotly or similar
                html += `<div class="chart-placeholder">Chart data available</div>`;
                html += `</div>`;
            });
        }
        
        return html;
    }
    
    formatCrux(data) {
        let html = `<h2>Crux - Essential Points</h2>`;
        
        if (data.core_message) {
            html += `<h3>Core Message</h3>`;
            html += `<p class="core-message">${this.escapeHtml(data.core_message)}</p>`;
        }
        
        if (data.essential_points && data.essential_points.length > 0) {
            html += `<h3>Essential Points</h3>`;
            html += `<ol>`;
            data.essential_points.forEach(point => {
                html += `<li>${this.escapeHtml(point)}</li>`;
            });
            html += `</ol>`;
        }
        
        if (data.key_takeaways && data.key_takeaways.length > 0) {
            html += `<h3>Key Takeaways</h3>`;
            html += `<ul>`;
            data.key_takeaways.forEach(takeaway => {
                html += `<li>${this.escapeHtml(takeaway)}</li>`;
            });
            html += `</ul>`;
        }
        
        return html;
    }
    
    formatConclusion(data) {
        let html = `<h2>Conclusion</h2>`;
        
        if (data.synthesis) {
            html += `<h3>Synthesis</h3>`;
            html += `<p>${this.escapeHtml(data.synthesis)}</p>`;
        }
        
        if (data.main_findings && data.main_findings.length > 0) {
            html += `<h3>Main Findings</h3>`;
            html += `<ul>`;
            data.main_findings.forEach(finding => {
                html += `<li>${this.escapeHtml(finding)}</li>`;
            });
            html += `</ul>`;
        }
        
        if (data.implications && data.implications.length > 0) {
            html += `<h3>Implications</h3>`;
            html += `<ul>`;
            data.implications.forEach(implication => {
                html += `<li>${this.escapeHtml(implication)}</li>`;
            });
            html += `</ul>`;
        }
        
        if (data.final_thoughts) {
            html += `<h3>Final Thoughts</h3>`;
            html += `<p>${this.escapeHtml(data.final_thoughts)}</p>`;
        }
        
        return html;
    }
    
    formatAISummary(data) {
        let html = `<h2>AI-Generated Summary</h2>`;
        
        html += `<div class="summary-meta">`;
        html += `<p><strong>Target Words:</strong> ${data.target_word_count}</p>`;
        html += `<p><strong>Actual Words:</strong> ${data.actual_word_count}</p>`;
        if (data.confidence_score) {
            html += `<p><strong>Confidence Score:</strong> ${(data.confidence_score * 100).toFixed(1)}%</p>`;
        }
        html += `</div>`;
        
        if (data.content) {
            html += `<div class="ai-summary-content">`;
            html += `<p>${this.escapeHtml(data.content)}</p>`;
            html += `</div>`;
        }
        
        if (data.key_themes && data.key_themes.length > 0) {
            html += `<h3>Key Themes</h3>`;
            html += `<p><em>${data.key_themes.join(', ')}</em></p>`;
        }
        
        return html;
    }
    
    formatSectionName(name) {
        return name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    }
    
    viewRawDocument() {
        if (!this.currentDocument) {
            this.showMessage('error', 'No document available');
            return;
        }
        
        const modal = document.getElementById('raw-document-modal');
        const content = document.getElementById('raw-document-content');
        
        content.textContent = this.currentDocument.full_text;
        modal.style.display = 'flex';
    }
    
    downloadDocument() {
        if (!this.currentDocument) {
            this.showMessage('error', 'No document available');
            return;
        }
        
        const content = JSON.stringify(this.currentDocument, null, 2);
        const blob = new Blob([content], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = `web-search-analysis-${new Date().toISOString().split('T')[0]}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        this.showMessage('success', 'Document downloaded successfully');
    }
    
    viewSources() {
        if (!this.currentDocument || !this.currentDocument.sources) {
            this.showMessage('error', 'No sources available');
            return;
        }
        
        const modal = document.getElementById('sources-modal');
        const content = document.getElementById('sources-content');
        
        content.innerHTML = '';
        
        this.currentDocument.sources.forEach(source => {
            const sourceDiv = document.createElement('div');
            sourceDiv.className = 'source-item';
            
            sourceDiv.innerHTML = `
                <div class="source-title">${this.escapeHtml(source.title)}</div>
                <div class="source-url">${this.escapeHtml(source.url)}</div>
                <div class="source-meta">
                    <span>Words: ${source.word_count}</span>
                    <span>Method: ${source.extraction_method}</span>
                    ${source.author ? `<span>Author: ${this.escapeHtml(source.author)}</span>` : ''}
                    ${source.publish_date ? `<span>Published: ${source.publish_date}</span>` : ''}
                </div>
            `;
            
            content.appendChild(sourceDiv);
        });
        
        modal.style.display = 'flex';
    }
    
    closeModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.style.display = 'none';
        }
    }
    
    showSection(sectionId) {
        document.querySelectorAll('.section').forEach(section => {
            section.classList.remove('active');
        });
        
        document.getElementById(sectionId).classList.add('active');
    }
    
    showLoading(title, details) {
        const overlay = document.getElementById('loading-overlay');
        const titleElement = document.getElementById('loading-text');
        const detailsElement = document.getElementById('loading-details');
        
        titleElement.textContent = title;
        detailsElement.textContent = details;
        overlay.style.display = 'flex';
    }
    
    hideLoading() {
        document.getElementById('loading-overlay').style.display = 'none';
    }
    
    showMessage(type, message) {
        const messageElement = document.getElementById(`${type}-message`);
        const textElement = document.getElementById(`${type}-text`);
        
        textElement.textContent = message;
        messageElement.style.display = 'block';
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            this.hideMessage(type);
        }, 5000);
    }
    
    hideMessage(type) {
        document.getElementById(`${type}-message`).style.display = 'none';
    }
    
    escapeHtml(text) {
        if (typeof text !== 'string') {
            return text;
        }
        
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize the application when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new WebSearchAnalyzer();
});

// Add some utility functions for enhanced functionality
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}