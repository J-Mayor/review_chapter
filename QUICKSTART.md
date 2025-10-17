# Quick Start Guide

## Installation

```bash
git clone https://github.com/J-Mayor/review_chapter.git
cd review_chapter
pip install -r requirements.txt
```

## Generate Your First Review

### Option 1: Use the Command Line Tool (Recommended for Beginners)

```bash
# Initialize and generate everything in one step
python main.py --all
```

This creates:
- `review.tex` - LaTeX version of your review
- `review.md` - Markdown version
- `references.bib` - Bibliography file
- `queries_and_provenance.md` - Search query log
- `citation_ledger.json` - Citation verification ledger

### Option 2: Step-by-Step

```bash
# 1. Initialize the project
python main.py --init

# 2. Check status
python main.py --status

# 3. Generate documents
python main.py --generate

# 4. Verify citations (requires internet)
python main.py --verify
```

## Customize the Configuration

Edit `config.yaml` to customize:

```yaml
review:
  title: "Your Review Title Here"
  target_venue: "PASA"  # or ARA&A, Living Reviews, etc.
  word_count_min: 12000
  word_count_max: 20000

authors:
  - name: "Your Name"
    affiliations: [1]
    email: "you@university.edu"
```

## Add Your Own Citations

### Method 1: Edit references.bib directly

Add BibTeX entries to `references.bib`:

```bibtex
@article{author2024paper,
  title={Your Paper Title},
  author={First Author and Second Author},
  year={2024},
  journal={Monthly Notices},
  doi={10.1093/mnras/xxx}
}
```

### Method 2: Use Python (Programmatic)

```python
from citation_manager import Citation, CitationManager
from review_generator import load_config

config = load_config('config.yaml')
manager = CitationManager(config)

citation = Citation(
    citekey="author2024paper",
    title="Your Paper Title",
    authors=["First Author", "Second Author"],
    year=2024,
    journal="Monthly Notices",
    doi="10.1093/mnras/xxx"
)

manager.add_citation(citation)
manager.generate_bibtex("references.bib")
```

## Expand the Content

Edit the generated sections in your preferred way:

### Option 1: Edit LaTeX Directly

Open `review.tex` in your favorite editor and add content to the sections.

### Option 2: Use Python to Generate Sections

```python
from review_generator import ReviewDocument, ReviewSection, load_config

config = load_config('config.yaml')
doc = ReviewDocument(config)

# Create a section
section = ReviewSection("My New Section", level=1)
section.content = "Content goes here with \\citep{citations}."

# Add subsection
subsection = ReviewSection("Details", level=2)
subsection.content = "More details..."
section.add_subsection(subsection)

# Add to document
doc.add_section(section)
doc.save_latex("review.tex")
```

## Compile the PDF

```bash
pdflatex review.tex
bibtex review
pdflatex review.tex
pdflatex review.tex
```

## Common Tasks

### View Current Status
```bash
python main.py --status
```

### Regenerate All Files
```bash
python main.py --generate
```

### Verify All Citations
```bash
python main.py --verify
```

### Run Example
```bash
python example_usage.py
```

## Workflow Example

Here's a typical workflow:

1. **Initialize**: `python main.py --all`
2. **Review**: Check `review.tex` and `queries_and_provenance.md`
3. **Customize**: Edit `config.yaml` with your details
4. **Add Citations**: Edit `references.bib` or use Python API
5. **Expand Content**: Add content to sections in `review.tex`
6. **Verify**: `python main.py --verify` to check URLs
7. **Regenerate**: `python main.py --generate` after changes
8. **Compile**: `pdflatex review.tex && bibtex review && pdflatex review.tex && pdflatex review.tex`
9. **Iterate**: Repeat steps 4-8 until complete

## Tips

- The default outline includes 10 major sections covering TF PV comprehensively
- Use `\citep{}` for citations in parentheses, `\citet{}` for in-text citations
- All URLs in citations are verified when you run `python main.py --verify`
- The system tracks which papers are included/excluded in `queries_and_provenance.md`
- Generated files can be safely regenerated from the configuration and citation data

## Getting Help

- Check `README.md` for full documentation
- Run `python main.py --help` for command-line options
- Look at `example_usage.py` for programmatic examples
- Review `config.yaml` for all configuration options

## Next Steps

1. Customize the configuration for your needs
2. Add your citations and references
3. Expand the default outline with content
4. Compile and review your PDF
5. Iterate and refine

Happy writing!
