"""
Main orchestration script for TF PV Literature Review System
Coordinates all components to generate the review
"""

import argparse
import yaml
import sys
from pathlib import Path
from datetime import datetime

from citation_manager import CitationManager, create_citation_from_bibtex
from review_generator import ReviewDocument, load_config
from provenance_tracker import ProvenanceTracker, create_default_queries


class ReviewOrchestrator:
    """Main orchestrator for the literature review system"""
    
    def __init__(self, config_path: str):
        self.config = load_config(config_path)
        self.citation_manager = CitationManager(self.config)
        self.provenance_tracker = ProvenanceTracker(self.config)
        self.review_doc = ReviewDocument(self.config)
        
        # Set up output directories
        self._setup_directories()
        
    def _setup_directories(self) -> None:
        """Create necessary output directories"""
        for dir_name in ['figures', 'tables']:
            dir_path = Path(self.config['outputs'].get(f'{dir_name}_dir', dir_name))
            dir_path.mkdir(exist_ok=True)
            
    def initialize_project(self) -> None:
        """Initialize a new review project"""
        print("Initializing TF PV Literature Review Project...")
        print(f"Title: {self.config['review']['title']}")
        print(f"Target venue: {self.config['review']['target_venue']}")
        print(f"Word count target: {self.config['review']['word_count_min']}-{self.config['review']['word_count_max']}")
        print()
        
        # Create default queries
        print("Creating default search queries...")
        queries = create_default_queries(self.config)
        for query in queries:
            self.provenance_tracker.add_query(query)
        print(f"Created {len(queries)} default ADS queries")
        print()
        
        # Create default outline
        print("Creating default outline...")
        self.review_doc.create_default_outline()
        print(f"Created outline with {len(self.review_doc.sections)} sections")
        print()
        
        # Set placeholder abstract
        self.review_doc.set_abstract(
            "Tully–Fisher (TF)–based peculiar velocity (PV) surveys provide a powerful "
            "probe of large-scale structure, the growth of cosmic structure, and tests of "
            "gravity. This review comprehensively surveys the use of the TF relation for "
            "PV measurements, covering historical foundations, major surveys and catalogs, "
            "methodological developments, cosmological results, and forecasts for the Square "
            "Kilometre Array (SKA) era. We critically assess systematic uncertainties, "
            "discuss complementarity with other cosmological probes, and outline future "
            "opportunities for this field."
        )
        
        # Load existing bibliography if present
        bib_file = self.config['outputs']['bibliography']
        if Path(bib_file).exists():
            print(f"Loading existing bibliography from {bib_file}...")
            self._load_existing_bibliography(bib_file)
            print(f"Loaded {len(self.citation_manager.citations)} citations")
        
    def _load_existing_bibliography(self, bib_path: str) -> None:
        """Load citations from existing .bib file"""
        try:
            with open(bib_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Split into individual entries
            entries = []
            current_entry = []
            in_entry = False
            
            for line in content.split('\n'):
                if line.strip().startswith('@'):
                    if current_entry:
                        entries.append('\n'.join(current_entry))
                    current_entry = [line]
                    in_entry = True
                elif in_entry:
                    current_entry.append(line)
                    if line.strip() == '}':
                        in_entry = False
                        
            if current_entry:
                entries.append('\n'.join(current_entry))
                
            # Parse each entry
            for entry in entries:
                citation = create_citation_from_bibtex(entry)
                if citation:
                    self.citation_manager.add_citation(citation)
                    
        except Exception as e:
            print(f"Error loading bibliography: {e}")
            
    def generate_documents(self) -> None:
        """Generate LaTeX and Markdown versions of the review"""
        print("Generating review documents...")
        
        # Generate LaTeX
        latex_path = self.config['outputs']['main_tex']
        print(f"Writing LaTeX to {latex_path}...")
        self.review_doc.save_latex(latex_path)
        
        # Generate Markdown
        md_path = self.config['outputs']['main_md']
        print(f"Writing Markdown to {md_path}...")
        self.review_doc.save_markdown(md_path)
        
        print("Documents generated successfully")
        print()
        
    def generate_bibliography(self) -> None:
        """Generate BibTeX file"""
        print("Generating bibliography...")
        bib_path = self.config['outputs']['bibliography']
        self.citation_manager.generate_bibtex(bib_path)
        print(f"Bibliography written to {bib_path}")
        print(f"Total citations: {len(self.citation_manager.citations)}")
        print()
        
    def verify_citations(self) -> None:
        """Verify all citations"""
        print("Verifying citations...")
        print("This may take some time as we check URLs...")
        print()
        
        results = self.citation_manager.verify_all_citations()
        report = self.citation_manager.get_verification_report()
        
        print("Verification Report:")
        print(f"  Total citations: {report['total_citations']}")
        print(f"  Verified: {report['verified_count']}")
        print(f"  ADS URLs valid: {report['ads_urls_valid']}")
        print(f"  DOI URLs valid: {report['doi_urls_valid']}")
        print(f"  Verification percentage: {report['verification_percentage']:.1f}%")
        print()
        
        # Save ledger
        ledger_path = self.config['outputs']['citation_ledger']
        self.citation_manager.save_to_ledger(ledger_path)
        print(f"Citation ledger saved to {ledger_path}")
        print()
        
    def generate_provenance_report(self) -> None:
        """Generate queries and provenance documentation"""
        print("Generating provenance report...")
        
        queries_path = self.config['outputs']['queries_log']
        self.provenance_tracker.save_report(queries_path)
        print(f"Provenance report written to {queries_path}")
        print()
        
    def generate_all(self) -> None:
        """Generate all outputs"""
        self.initialize_project()
        self.generate_documents()
        self.generate_bibliography()
        self.generate_provenance_report()
        
        print("=" * 60)
        print("Review project initialized successfully!")
        print("=" * 60)
        print()
        print("Next steps:")
        print("1. Review the generated outline in review.tex")
        print("2. Add citations to references.bib or use citation tools")
        print("3. Expand sections with content")
        print("4. Run verification: python main.py --verify")
        print("5. Iterate and refine")
        print()
        
    def show_status(self) -> None:
        """Show current project status"""
        print("=" * 60)
        print("TF PV Literature Review - Project Status")
        print("=" * 60)
        print()
        
        print(f"Title: {self.config['review']['title']}")
        print(f"Target venue: {self.config['review']['target_venue']}")
        print()
        
        print(f"Sections: {len(self.review_doc.sections)}")
        print(f"Citations: {len(self.citation_manager.citations)}")
        print(f"Search queries: {len(self.provenance_tracker.queries)}")
        print()
        
        # Check file existence
        outputs = self.config['outputs']
        print("Generated files:")
        for key, filename in outputs.items():
            if not key.endswith('_dir'):
                exists = "✓" if Path(filename).exists() else "✗"
                print(f"  {exists} {filename}")
        print()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="TF PV Literature Review System"
    )
    parser.add_argument(
        '--config',
        default='config.yaml',
        help='Path to configuration file'
    )
    parser.add_argument(
        '--init',
        action='store_true',
        help='Initialize new review project'
    )
    parser.add_argument(
        '--generate',
        action='store_true',
        help='Generate review documents'
    )
    parser.add_argument(
        '--verify',
        action='store_true',
        help='Verify citations'
    )
    parser.add_argument(
        '--status',
        action='store_true',
        help='Show project status'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Initialize and generate all outputs'
    )
    
    args = parser.parse_args()
    
    # Check config exists
    if not Path(args.config).exists():
        print(f"Error: Configuration file {args.config} not found")
        sys.exit(1)
        
    orchestrator = ReviewOrchestrator(args.config)
    
    if args.all:
        orchestrator.generate_all()
    elif args.init:
        orchestrator.initialize_project()
        orchestrator.generate_provenance_report()
    elif args.generate:
        orchestrator.generate_documents()
        orchestrator.generate_bibliography()
    elif args.verify:
        orchestrator.verify_citations()
    elif args.status:
        orchestrator.show_status()
    else:
        # Default: show status
        orchestrator.show_status()


if __name__ == '__main__':
    main()
