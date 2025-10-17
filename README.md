# Tully–Fisher Peculiar Velocity Survey Literature Review System

A comprehensive, automated system for generating a rigorous, publication-ready literature review on Tully–Fisher (TF)–based peculiar velocity (PV) surveys and their cosmological applications.

## Overview

This system implements a complete workflow for creating a scholarly review article, including:

- **Automated literature discovery** via NASA/ADS and arXiv queries
- **Citation management** with verification, deduplication, and NASA/ADS-compliant BibTeX generation
- **Document generation** in both LaTeX and Markdown formats
- **Provenance tracking** for reproducibility
- **Multi-pass iteration** framework with self-critique capabilities
- **SKA forecast utilities** for future survey predictions

## Features

### Citation Management
- Parse and validate BibTeX entries
- Verify ADS URLs and DOI links (HTTP 200 checks)
- Track verification status with timestamps
- Deduplicate citations based on title and year
- Generate NASA/ADS-compliant .bib files
- Maintain citation ledger (JSON format) with full metadata

### Review Document Generation
- Structured outline for TF PV review
- LaTeX output compatible with PASA/ARA&A/A&A Review templates
- Markdown export for accessibility
- Configurable sections and subsections
- Author and affiliation management

### Provenance and Reproducibility
- Log all search queries with timestamps
- Track inclusion/exclusion decisions with rationales
- Generate provenance reports in Markdown
- Export queries and decisions to JSON

### Literature Search
- Pre-configured ADS queries for TF PV topics
- Search coverage: historical origins to current literature
- Inclusion/exclusion criteria enforcement
- Configurable databases: NASA/ADS, arXiv, Crossref

## Installation

```bash
# Clone the repository
git clone https://github.com/J-Mayor/review_chapter.git
cd review_chapter

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### Initialize a New Review Project

```bash
python main.py --all
```

This will:
1. Create the default outline structure
2. Generate initial LaTeX and Markdown documents
3. Set up search queries
4. Create provenance tracking

### Check Project Status

```bash
python main.py --status
```

### Generate Documents Only

```bash
python main.py --generate
```

### Verify Citations

```bash
python main.py --verify
```

This will check all ADS URLs and DOI links, updating the citation ledger with verification status.

## Configuration

Edit `config.yaml` to customize:

- **Review metadata**: title, target venue, word count
- **Authors and affiliations**
- **Scope and focus**: strict TF vs. including FP/SNe Ia context
- **Figure/table budget**
- **LaTeX class and bibliography style**
- **Citation requirements**: ADS bibcode, DOI, arXiv ID
- **Literature search queries**
- **Inclusion/exclusion criteria**
- **SKA forecast parameters**

### Example Configuration

```yaml
review:
  title: "Tully-Fisher Peculiar Velocity Surveys and Cosmological Applications"
  target_venue: "PASA"
  word_count_min: 12000
  word_count_max: 20000

scope:
  strict_tf_focus: true
  include_ska_forecasts: true
  
figures:
  max_count: 12
  required_figures:
    - "TF PV survey timeline"
    - "Survey comparison table"
```

## Project Structure

```
review_chapter/
├── config.yaml                  # Main configuration
├── main.py                      # Orchestration script
├── citation_manager.py          # Citation handling and verification
├── review_generator.py          # LaTeX/Markdown generation
├── provenance_tracker.py        # Search query and decision tracking
├── requirements.txt             # Python dependencies
├── review.tex                   # Generated LaTeX document
├── review.md                    # Generated Markdown document
├── references.bib               # NASA/ADS-compliant bibliography
├── citation_ledger.json         # Citation verification ledger
├── queries_and_provenance.md    # Search queries and decisions
├── figures/                     # Figure assets
└── tables/                      # Table assets
```

## Workflow

### 1. Initialization
```bash
python main.py --init
```

Creates default outline, queries, and file structure.

### 2. Literature Discovery
- Search NASA/ADS with configured queries
- Import results to citation manager
- Make inclusion/exclusion decisions
- Record rationales in provenance tracker

### 3. Writing and Content Development
- Expand outline sections with content
- Add citations using `\citep{}` or `\citet{}`
- Include figures and tables
- Add cross-references

### 4. Citation Management
```bash
# Add citations to references.bib manually or programmatically
# Then verify:
python main.py --verify
```

### 5. Document Generation
```bash
python main.py --generate
```

Generates both LaTeX and Markdown versions.

### 6. Iteration
- Review generated documents
- Identify gaps in coverage
- Refine content
- Add missing citations
- Re-verify and regenerate

### 7. Compilation
```bash
pdflatex review.tex
bibtex review
pdflatex review.tex
pdflatex review.tex
```

## Citation Ledger Format

The `citation_ledger.json` file tracks verification state:

```json
[
  {
    "citekey": "braun2019anticipatedperformancesquarekilometre",
    "title": "Anticipated Performance of the Square Kilometre Array",
    "authors": ["Robert Braun", "Anna Bonaldi", ...],
    "year": 2019,
    "journal": null,
    "ads_bibcode": null,
    "doi": null,
    "arxiv_id": "1912.12699",
    "ads_url": null,
    "publisher_url": "https://doi.org/...",
    "last_verified": "2025-10-16T20:35:00Z",
    "http_status_ads": null,
    "http_status_doi": 200,
    "crossref_match": false,
    "ads_match": false,
    "notes": ""
  }
]
```

## Default Review Outline

The system generates a comprehensive outline covering:

1. **Introduction and Historical Context**
   - Scope and Objectives
   - Historical Development

2. **The Tully–Fisher Relation as a Distance and Velocity Probe**
   - Physical Basis and Calibration
   - Optical, NIR, and Baryonic Variants
   - Systematic Uncertainties

3. **Survey Landscape for TF Peculiar Velocities**
   - Major Surveys and Catalogs
   - Survey Characteristics and Comparison

4. **Methodological Foundations**
   - Peculiar Velocity Statistics in Linear Theory
   - Velocity Field Reconstruction
   - Bias Corrections and Hierarchical Modeling

5. **Cosmological Results from TF Peculiar Velocities**
   - Growth Rate and fσ₈ Constraints
   - Hubble Constant and Distance Scale
   - Bulk Flows and Large-Scale Structure

6. **Simulations and Mocks for TF Peculiar Velocities**
   - N-body and Hydrodynamic Mocks
   - Survey Realism and Selection Functions

7. **SKA Era Forecasts and Prospects**
   - SKA1-MID and SKA1-SUR Capabilities
   - Precursors and Pathfinders
   - Forecast Assumptions and Systematics Budgets
   - Multi-Probe Synergies

8. **Comparison with Other PV Probes**
   - Fundamental Plane Peculiar Velocities
   - Type Ia Supernovae Peculiar Velocities

9. **Open Problems and Future Directions**
   - Outstanding Systematics
   - Theoretical Developments
   - Observational Opportunities

10. **Conclusions**

## Advanced Usage

### Custom Sections

```python
from review_generator import ReviewSection

# Create custom section
custom_section = ReviewSection("My Custom Section", level=1)
custom_section.content = "Custom content here..."

# Add subsection
subsection = ReviewSection("Subsection", level=2, content="Details...")
custom_section.add_subsection(subsection)

# Add to document
review_doc.add_section(custom_section)
```

### Programmatic Citation Addition

```python
from citation_manager import Citation

citation = Citation(
    citekey="author2024paper",
    title="An Important Paper",
    authors=["First Author", "Second Author"],
    year=2024,
    journal="Monthly Notices",
    doi="10.1093/mnras/...",
    ads_bibcode="2024MNRAS.xxx.yyyy"
)

citation_manager.add_citation(citation)
```

### Custom Search Queries

Edit `config.yaml`:

```yaml
literature_search:
  ads_queries:
    - "Your custom query here"
    - "Another search term"
```

## Requirements

- Python 3.7+
- PyYAML
- requests
- LaTeX distribution (for PDF compilation)

## Testing

Run the comprehensive test suite to verify installation:

```bash
python test_suite.py
```

This tests:
- Module imports
- Configuration loading
- Citation management
- Document generation
- Provenance tracking
- Survey table generation
- File I/O operations

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Citation

If you use this system for your research, please cite:

```bibtex
@software{tfpv_review_system,
  title={Tully-Fisher Peculiar Velocity Survey Literature Review System},
  author={Author Name},
  year={2025},
  url={https://github.com/J-Mayor/review_chapter}
}
```

## License

[Add license information]

## Contact

For questions or issues, please open a GitHub issue or contact [email].

## Acknowledgments

This system was developed to facilitate comprehensive literature reviews for the Square Kilometre Array (SKA) and related radio astronomy projects.
