import argparse
import re
import textwrap
from typing import List, Dict

import nltk
from summarizer import Summarizer
from wordfreq import zipf_frequency
from nltk.corpus import wordnet as wn
from functools import lru_cache
import os

# Try to import google-generativeai lazily; only required if the user selects the Gemini engine.
try:
    import google.generativeai as genai  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    genai = None  # will raise later if engine requires it


# Download necessary NLTK data at runtime (first invocation only)
for corpus in ("punkt", "wordnet", "omw-1.4"):
    try:
        nltk.data.find(corpus)
    except LookupError:
        nltk.download(corpus)


# ------------------------
# Helper functions
# ------------------------

def _split_sentences(text: str) -> List[str]:
    """Split text into sentences using NLTK."""
    return nltk.tokenize.sent_tokenize(text)


def _extract_jargon(text: str, frequency_threshold: float = 3.5) -> List[str]:
    """Return list of potential jargon/technical terms.

    We consider words with length > 4 and Zipf frequency below
    `frequency_threshold` as jargon. Duplicate words are removed, and the
    original casing from the source text is preserved when possible.
    """
    # Map lowercase token -> original token (first occurrence)
    original_case: Dict[str, str] = {}
    for match in re.finditer(r"[A-Za-z][A-Za-z\-']+", text):
        token = match.group(0)
        lower = token.lower()
        if lower not in original_case:
            original_case[lower] = token

    jargon_candidates = []
    for lower, original in original_case.items():
        if len(lower) <= 4:
            continue
        if zipf_frequency(lower, "en") < frequency_threshold:
            jargon_candidates.append(original)
    return sorted(jargon_candidates, key=str.lower)


def _get_definition(word: str) -> str:
    """Return the first WordNet definition for the given word, if available."""
    synsets = wn.synsets(word)
    if not synsets:
        return "(No definition found)"
    # Prefer the first definition (most common sense)
    return synsets[0].definition()


# ------------------------
# Core processing
# ------------------------

def summarize_text(text: str, ratio: float = 0.15) -> str:
    """Generate an extractive summary using a BERT-based model.

    Parameters
    ----------
    text: str
        The full input text.
    ratio: float
        Fraction of the original sentences to include in the summary.
    """
    model = Summarizer()
    summary = model(text, ratio=ratio)
    # Ensure summary is plain string (model may return list)
    if isinstance(summary, list):
        summary = " ".join(summary)
    # Re-wrap to shorter lines for readability
    return textwrap.fill(summary, width=80)


def build_glossary(text: str) -> Dict[str, str]:
    """Build a glossary of jargon terms and their definitions."""
    terms = _extract_jargon(text)
    return {term: _get_definition(term) for term in terms}


@lru_cache(maxsize=1)
def _get_gemini_model(api_key: str):
    """Return a cached Gemini model instance."""
    if genai is None:  # pragma: no cover
        raise RuntimeError(
            "google-generativeai package is required for Gemini engine. Please install google-generativeai>=0.3.2"
        )
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-pro")


def summarize_with_gemini(text: str, api_key: str) -> str:
    """Use Google's Gemini model to create a child-friendly summary and glossary."""
    model = _get_gemini_model(api_key)

    prompt = (
        "You are an assistant who explains things to young children. "
        "Read the given text and produce a short explanation with simple words.\n\n"
        "1. Provide a heading line: '🐣 Here is a short and simple explanation of the file:'\n"
        "2. Provide the explanation as bullet points, each starting with '• '.\n"
        "3. Then write a blank line and the heading '🧩 Tricky words and what they mean:'\n"
        "4. List any difficult or uncommon words from the text with their definitions, each starting with '- '.\n\n"
        "Keep important terms exactly as they appear in the text. \n\n"
        "Text to explain:\n" + text
    )

    response = model.generate_content(prompt)
    return response.text.strip()


# ------------------------
# CLI
# ------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a child-friendly summary of a file using a BERT summarizer and provide definitions for jargon terms.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("input", help="Path to the input text file")
    parser.add_argument("-o", "--output", help="Optional path to save the summary (defaults to stdout)")
    parser.add_argument(
        "--ratio",
        type=float,
        default=0.15,
        help="Fraction of sentences to keep in the summary (only for BERT engine)",
    )
    parser.add_argument(
        "--engine",
        choices=["auto", "bert", "gemini"],
        default="auto",
        help="Choose which backend to use: 'bert' extractive model, 'gemini' LLM, or 'auto' to decide based on the presence of GOOGLE_API_KEY.",
    )
    parser.add_argument(
        "--api-key",
        help="Google API key for Gemini. Can also be set via the GOOGLE_API_KEY environment variable.",
    )

    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        raw_text = f.read()

    # Determine which engine to use
    api_key = args.api_key or os.getenv("GOOGLE_API_KEY")
    selected_engine: str
    if args.engine == "auto":
        selected_engine = "gemini" if api_key else "bert"
    else:
        selected_engine = args.engine

    if selected_engine == "gemini":
        if not api_key:
            raise SystemExit("Gemini engine selected but no API key provided (use --api-key or set GOOGLE_API_KEY).")

        final_output = summarize_with_gemini(raw_text, api_key)
    else:
        summary = summarize_text(raw_text, ratio=args.ratio)
        glossary = build_glossary(raw_text)

        # Craft child-friendly output using local models
        output_lines: List[str] = []
        output_lines.append("🐣 Here is a short and simple explanation of the file: \n")
        for sentence in _split_sentences(summary):
            output_lines.append(f"• {sentence.strip()}")

        if glossary:
            output_lines.append("\n🧩 Tricky words and what they mean:")
            for term, definition in glossary.items():
                output_lines.append(f"- {term}: {definition}")

        final_output = "\n".join(output_lines)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as out_f:
            out_f.write(final_output)
    else:
        print(final_output)


if __name__ == "__main__":
    main()