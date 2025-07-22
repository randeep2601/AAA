# AAA

# Simple BERT Summarizer 🐣

A tiny command-line helper that reads any text file, uses a BERT-based model to pick out the most important sentences, and then rewrites everything in a way that even a small child can understand.  It also keeps all the big, important words and explains them so you know what they mean.

## Installation

1.  Make sure you have Python 3.9+ and `pip`.
2.  Create a virtual environment (optional but recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

3.  Install the requirements:

```bash
pip install -r simple_bert_tool/requirements.txt
```

The first time you run the tool it may download the pre-trained BERT model (~400 MB) and some NLTK data sets.  This only happens once.

## Usage

```bash
python -m simple_bert_tool.simple_bert_summarizer path/to/your/file.txt
```

Options:

* `--ratio` – percentage (0-1) of sentences to keep in the summary.  Default is 0.15 (≈15 %).
* `--output` – path to save the result.  If omitted the summary is printed to *stdout*.

Example:

```bash
python -m simple_bert_tool.simple_bert_summarizer research_paper.txt --ratio 0.1 --output summary.txt
```

---

**Output format**

```
🐣 Here is a short and simple explanation of the file:
• …
• …

🧩 Tricky words and what they mean:
- photosynthesis: the process by which green plants make their own food using sunlight
- chlorophyll: a green pigment that helps plants absorb light
```

Enjoy! 🌟