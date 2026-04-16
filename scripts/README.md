# Scripts

## parse_meditations.py

Extracts quotes from the full text of "Meditations" by Marcus Aurelius.

### What it does:
1. Downloads the complete text from Project Gutenberg (public domain)
2. Parses all 12 books to extract individual passages
3. Filters passages into meaningful quotes (30-60 words)
4. Saves 1,700+ quotes to `data/marcus_aurelius_quotes.json`

### Usage:
```bash
python3 scripts/parse_meditations.py
```

### Source:
- Project Gutenberg eBook #2680
- https://www.gutenberg.org/files/2680/2680-0.txt
- Translation by Meric Casaubon
- Public domain text

### Output:
- Generates `data/marcus_aurelius_quotes.json` with 1,700+ quotes
- Replaces any existing quotes file
- Each run downloads fresh text from Project Gutenberg

### Re-running:
If you want to regenerate the quotes (e.g., to adjust filtering parameters), just run the script again. The text is cached in `/tmp/meditations.txt` for faster subsequent runs.
