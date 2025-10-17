# Comprehensive Usage Guide

This guide walks through the complete workflow for creating a TF PV literature review from scratch.

## Table of Contents

1. [Installation and Setup](#installation-and-setup)
2. [Initial Project Setup](#initial-project-setup)
3. [Adding Citations](#adding-citations)
4. [Customizing Content](#customizing-content)
5. [Generating Tables](#generating-tables)
6. [Verifying Citations](#verifying-citations)
7. [Compiling the Document](#compiling-the-document)
8. [Iteration Workflow](#iteration-workflow)
9. [Advanced Topics](#advanced-topics)

## Installation and Setup

### 1. Clone and Install

```bash
git clone https://github.com/J-Mayor/review_chapter.git
cd review_chapter
pip install -r requirements.txt
```

### 2. Verify Installation

```bash
python test_suite.py
```

You should see: `🎉 All tests passed!`

## Initial Project Setup

### Generate Default Review Structure

```bash
python main.py --all
```

This creates:
- `review.tex` - Your LaTeX document with default outline
- `review.md` - Markdown version for easy reading
- `references.bib` - Empty bibliography (to be filled)
- `queries_and_provenance.md` - Search query documentation
- `figures/` and `tables/` directories

### Review the Structure

```bash
python main.py --status
```

Check what was generated:
- `review.tex` - Review the section structure
- `queries_and_provenance.md` - See the default search queries

## Adding Citations

### Method 1: Manual BibTeX Entry

Edit `references.bib` and add entries:

```bibtex
@article{tully1977new,
  title={A New Method of Determining Distances to Galaxies},
  author={Tully, R. Brent and Fisher, J. Richard},
  year={1977},
  journal={Astronomy and Astrophysics},
  volume={54},
  pages={661-673},
  ads_bibcode={1977A&A....54..661T}
}

@article{tully2016cosmicflows3,
  title={Cosmicflows-3},
  author={Tully, R. Brent and Courtois, Hélène M. and Sorce, Jenny G.},
  year={2016},
  journal={The Astronomical Journal},
  volume={152},
  number={2},
  pages={50},
  doi={10.3847/0004-6256/152/2/50}
}
```

### Method 2: Programmatic Addition

Create a script `add_citations.py`:

```python
from citation_manager import CitationManager, Citation
from review_generator import load_config

config = load_config('config.yaml')
manager = CitationManager(config)

# Load existing citations
manager.load_from_ledger('citation_ledger.json')

# Add new citations
citations = [
    Citation(
        citekey="tully1977new",
        title="A New Method of Determining Distances to Galaxies",
        authors=["R. Brent Tully", "J. Richard Fisher"],
        year=1977,
        journal="Astronomy and Astrophysics",
        ads_bibcode="1977A&A....54..661T",
        ads_url="https://ui.adsabs.harvard.edu/abs/1977A&A....54..661T"
    ),
    Citation(
        citekey="springob2016sfi++",
        title="The Spitzer Extended Tully-Fisher Survey (S4TF)",
        authors=["C. M. Springob", "et al."],
        year=2016,
        journal="MNRAS",
        doi="10.1093/mnras/stw1618",
        ads_bibcode="2016MNRAS.462.1910S"
    )
]

for citation in citations:
    manager.add_citation(citation)

# Save
manager.generate_bibtex('references.bib')
manager.save_to_ledger('citation_ledger.json')
```

Run: `python add_citations.py`

### Method 3: Import from Existing BibTeX

If you have an existing `.bib` file:

```python
from citation_manager import create_citation_from_bibtex, CitationManager
from review_generator import load_config

config = load_config('config.yaml')
manager = CitationManager(config)

# Read existing bib file
with open('existing.bib', 'r') as f:
    content = f.read()
    
# Parse entries (simple split by @)
entries = content.split('@')[1:]  # Skip first empty
for entry in entries:
    entry = '@' + entry.strip()
    citation = create_citation_from_bibtex(entry)
    if citation:
        manager.add_citation(citation)

manager.generate_bibtex('references.bib')
```

## Customizing Content

### Edit Configuration

Edit `config.yaml` to customize:

```yaml
review:
  title: "Your Custom Title Here"
  target_venue: "PASA"  # or ARA&A, Living Reviews, etc.

authors:
  - name: "Your Name"
    affiliations: [1]
    email: "you@university.edu"

affiliations:
  - id: 1
    name: "Your Institution, City, Country"
```

### Modify Sections

#### Option 1: Edit LaTeX Directly

Open `review.tex` and edit sections:

```latex
\section{Introduction and Historical Context}

The measurement of peculiar velocities—deviations from the smooth Hubble 
flow—provides a direct probe of the growth of cosmic structure \citep{tully1977new}.
[Add your content here...]

\subsection{Scope and Objectives}

This review covers... [expand with details]
```

#### Option 2: Generate Programmatically

Create `customize_sections.py`:

```python
from review_generator import ReviewDocument, ReviewSection, load_config

config = load_config('config.yaml')
doc = ReviewDocument(config)

# Create custom introduction
intro = ReviewSection("Introduction", level=1)
intro.content = """
Peculiar velocities—the deviations of galaxy velocities from the smooth 
Hubble expansion—encode information about the growth of cosmic structure 
and the gravitational field on large scales \\citep{tully1977new}. Among 
the various distance indicators used to measure peculiar velocities, the 
Tully–Fisher (TF) relation has proven to be one of the most productive, 
enabling surveys of thousands of spiral galaxies across large volumes 
\\citep{springob2016sfi++,tully2016cosmicflows3}.
"""

# Add subsections
scope = ReviewSection("Scope and Objectives", level=2)
scope.content = """
This review provides a comprehensive examination of TF-based peculiar 
velocity surveys, covering:
\\begin{itemize}
\\item Historical development and physical basis of the TF relation
\\item Major survey programs and their characteristics
\\item Methodological advances in bias correction and analysis
\\item Cosmological constraints from TF peculiar velocities
\\item Future prospects with the Square Kilometre Array
\\end{itemize}
"""
intro.add_subsection(scope)

doc.add_section(intro)

# Add more sections...
# [continue building document]

# Save
doc.save_latex('review.tex')
doc.save_markdown('review.md')
```

## Generating Tables

### Create Standard Survey Tables

```bash
python survey_tables.py
```

This generates three tables in `tables/`:
- `survey_comparison.tex` - Major TF PV surveys
- `ska_forecast.tex` - SKA forecast parameters
- `method_comparison.tex` - PV method comparison

### Include Tables in Document

Add to your `review.tex`:

```latex
\section{Survey Landscape}

Table~\ref{tab:survey_comparison} summarizes the major TF peculiar velocity 
surveys conducted to date.

\input{tables/survey_comparison}

The diversity of approaches reflects different optimization strategies...
```

### Create Custom Tables

```python
from survey_tables import Survey, generate_survey_comparison_table

# Define custom surveys
my_surveys = [
    Survey(
        name="Custom Survey",
        year=2024,
        sample_size="~5000",
        bands="g, r, i",
        depth="z < 0.1",
        reference="\\citet{author2024}"
    )
]

table = generate_survey_comparison_table(my_surveys)
with open('tables/custom_survey.tex', 'w') as f:
    f.write(table)
```

## Verifying Citations

### Run Citation Verification

```bash
python main.py --verify
```

This will:
1. Check all ADS URLs (HTTP 200 status)
2. Verify DOI links
3. Update `citation_ledger.json` with verification status
4. Report any broken links

### Review Verification Results

Check `citation_ledger.json`:

```json
{
  "citekey": "tully1977new",
  "last_verified": "2025-10-16T20:00:00Z",
  "http_status_ads": 200,
  "http_status_doi": null,
  "ads_match": true,
  ...
}
```

### Fix Broken Links

If verification finds broken links:

1. Check the citation in `references.bib`
2. Update the DOI or ADS bibcode
3. Re-run verification

## Compiling the Document

### Compile to PDF

```bash
pdflatex review.tex
bibtex review
pdflatex review.tex
pdflatex review.tex
```

### Using latexmk (Alternative)

```bash
latexmk -pdf review.tex
```

### Check for LaTeX Errors

If compilation fails:
1. Check the `.log` file: `less review.log`
2. Common issues:
   - Missing citations: Add to `references.bib`
   - Undefined references: Run `bibtex` then `pdflatex` again
   - Package errors: Install missing LaTeX packages

## Iteration Workflow

### Version 1: Outline and Structure

```bash
# 1. Generate initial structure
python main.py --all

# 2. Review outline
cat review.tex

# 3. Customize configuration
nano config.yaml

# 4. Regenerate
python main.py --generate
```

### Version 2: Add Content

```bash
# 1. Add citations
nano references.bib

# 2. Expand sections
nano review.tex

# 3. Generate tables
python survey_tables.py

# 4. Include tables
nano review.tex  # Add \input{tables/...}

# 5. Compile and review
pdflatex review.tex && bibtex review && pdflatex review.tex && pdflatex review.tex
```

### Version 3: Verify and Polish

```bash
# 1. Verify all citations
python main.py --verify

# 2. Fix any broken links
nano references.bib

# 3. Re-verify
python main.py --verify

# 4. Final compile
latexmk -pdf review.tex
```

## Advanced Topics

### Custom Citation Verification

```python
from citation_manager import CitationManager
from review_generator import load_config

config = load_config('config.yaml')
manager = CitationManager(config)
manager.load_from_ledger('citation_ledger.json')

# Verify specific citation
result = manager.verify_citation('tully1977new')
print(f"ADS URL valid: {result['ads_url_valid']}")
print(f"DOI URL valid: {result['doi_url_valid']}")

# Get verification report
report = manager.get_verification_report()
print(f"Total: {report['total_citations']}")
print(f"Verified: {report['verification_percentage']:.1f}%")
```

### Batch Import from ADS

(Requires ADS API token - set as environment variable)

```python
from citation_manager import CitationManager
from review_generator import load_config
import os

# Set your ADS API token
os.environ['ADS_API_TOKEN'] = 'your_token_here'

config = load_config('config.yaml')
manager = CitationManager(config)

# Search ADS
results = manager.search_ads("Tully-Fisher peculiar velocities", max_results=50)

# Process results...
# (This requires the full ADS API implementation)
```

### Programmatic Section Generation

```python
from review_generator import ReviewDocument, ReviewSection, load_config

def generate_survey_section(survey_name, reference, details):
    """Generate a section describing a survey"""
    section = ReviewSection(survey_name, level=2)
    section.content = f"""
The {survey_name} survey \\citep{{{reference}}} provided {details['sample_size']} 
TF distance measurements in the {details['bands']} band(s). 
{details['description']}
"""
    return section

config = load_config('config.yaml')
doc = ReviewDocument(config)

# Main section
surveys_section = ReviewSection("Major Surveys", level=1)

# Add survey subsections
surveys = [
    ("SFI++", "springob2016sfi++", {
        "sample_size": "~4800",
        "bands": "I",
        "description": "This extended the original SFI survey to larger volumes."
    }),
    # ... more surveys
]

for name, ref, details in surveys:
    subsection = generate_survey_section(name, ref, details)
    surveys_section.add_subsection(subsection)

doc.add_section(surveys_section)
doc.save_latex('review.tex')
```

### Custom Provenance Tracking

```python
from provenance_tracker import ProvenanceTracker, SearchQuery, InclusionDecision
from review_generator import load_config
from datetime import datetime

config = load_config('config.yaml')
tracker = ProvenanceTracker(config)

# Record custom query
query = SearchQuery(
    query_string='full:"Tully-Fisher" AND full:"peculiar velocity" year:2020-2025',
    database="NASA/ADS",
    timestamp=datetime.now().isoformat(),
    num_results=75,
    included_count=12,
    notes="Recent papers (2020-2025)"
)
tracker.add_query(query)

# Record inclusion decision
decision = InclusionDecision(
    citekey="author2024paper",
    title="Important Recent Work",
    decision="included",
    rationale="Novel methodology for bias correction",
    criteria_met=["Methodological significance", "Recent"],
    criteria_failed=[],
    timestamp=datetime.now().isoformat(),
    reviewed_by="Your Name"
)
tracker.add_decision(decision)

tracker.save_report('queries_and_provenance.md')
tracker.save_json('provenance.json')
```

## Summary

This comprehensive guide covers:
1. ✅ Installation and verification
2. ✅ Project initialization
3. ✅ Citation management (manual, programmatic, import)
4. ✅ Content customization (config, sections)
5. ✅ Table generation
6. ✅ Citation verification
7. ✅ Document compilation
8. ✅ Iteration workflow
9. ✅ Advanced programmatic usage

For more help:
- See `README.md` for overview
- See `QUICKSTART.md` for quick reference
- Run `python test_suite.py` to verify system health
- Check `example_usage.py` for code examples
