#!/usr/bin/env python3
"""
Parse Meditations by Marcus Aurelius from Project Gutenberg
and extract individual passages as quotes.
"""
import re
import json
from pathlib import Path


def download_meditations():
    """Download the text from Project Gutenberg if not already cached"""
    import urllib.request

    cache_file = Path("/tmp/meditations.txt")
    if cache_file.exists():
        print(f"Using cached file: {cache_file}")
        return cache_file

    url = "https://www.gutenberg.org/files/2680/2680-0.txt"
    print(f"Downloading from {url}...")
    urllib.request.urlretrieve(url, cache_file)
    print(f"Downloaded to {cache_file}")
    return cache_file


def parse_passages(text):
    """Extract individual passages from the Meditations"""
    passages = []

    # Find where the actual meditations begin (after introduction)
    # The books are marked with headers like "FIRST BOOK", "SECOND BOOK", etc.

    # Split by book sections
    # Each passage typically starts with a Roman numeral followed by a period
    # But the format is inconsistent, so we'll use a more flexible approach

    lines = text.split('\n')
    current_passage = []
    in_meditation = False

    for i, line in enumerate(lines):
        line = line.strip()

        # Skip empty lines at the start of a passage
        if not line and not current_passage:
            continue

        # Check if we're at the start of the meditations
        if 'THE FIRST BOOK' in line and not in_meditation:
            in_meditation = True
            continue

        # Check if we've reached the end (appendix or glossary)
        if in_meditation and ('APPENDIX' in line or 'GLOSSARY' in line or 'END OF' in line):
            break

        # Skip book headers
        if re.match(r'^THE (FIRST|SECOND|THIRD|FOURTH|FIFTH|SIXTH|SEVENTH|EIGHTH|NINTH|TENTH|ELEVENTH|TWELFTH) BOOK', line):
            continue

        if not in_meditation:
            continue

        # Check if this is the start of a new passage (Roman numeral)
        # Match I., II., III., IV., V., etc. at the start of a line
        if re.match(r'^[IVXLCDM]+\.', line):
            # Save the previous passage if it exists
            if current_passage:
                passage_text = ' '.join(current_passage).strip()
                if len(passage_text) > 50:  # Only keep substantial passages
                    passages.append(passage_text)

            # Start new passage (remove the Roman numeral)
            current_passage = [re.sub(r'^[IVXLCDM]+\.\s*', '', line)]
        elif current_passage:
            # Continue building current passage
            current_passage.append(line)

    # Don't forget the last passage
    if current_passage:
        passage_text = ' '.join(current_passage).strip()
        if len(passage_text) > 50:
            passages.append(passage_text)

    return passages


def filter_quotes(passages, max_words=60):
    """Filter passages to make good quotes (not too long, meaningful)"""
    quotes = []

    for passage in passages:
        # Split long passages into sentences
        sentences = re.split(r'[.!?]\s+', passage)

        for sentence in sentences:
            sentence = sentence.strip()

            # Skip empty or very short sentences
            if len(sentence) < 30:
                continue

            # Skip sentences that are too long
            word_count = len(sentence.split())
            if word_count > max_words:
                continue

            # Clean up the sentence
            sentence = re.sub(r'\s+', ' ', sentence)  # Normalize whitespace
            sentence = sentence.strip()

            # Add period if missing
            if sentence and sentence[-1] not in '.!?':
                sentence += '.'

            # Skip duplicates
            if sentence not in quotes:
                quotes.append(sentence)

    return quotes


def main():
    print("Parsing Meditations by Marcus Aurelius...")

    # Download the text
    text_file = download_meditations()

    # Read the file
    with open(text_file, 'r', encoding='utf-8') as f:
        text = f.read()

    # Parse passages
    print("Extracting passages...")
    passages = parse_passages(text)
    print(f"Found {len(passages)} passages")

    # Filter into good quotes
    print("Filtering into quotes...")
    quotes = filter_quotes(passages)
    print(f"Extracted {len(quotes)} quotes")

    # Save to JSON
    output_file = Path("data/marcus_aurelius_quotes.json")
    output_file.parent.mkdir(exist_ok=True)

    data = {"quotes": quotes}

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Saved {len(quotes)} quotes to {output_file}")

    # Show a few examples
    print("\nExample quotes:")
    import random
    for quote in random.sample(quotes, min(5, len(quotes))):
        print(f"\n  • {quote}")


if __name__ == "__main__":
    main()
