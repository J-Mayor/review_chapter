#!/usr/bin/env python3
"""
Example usage of the TF PV Literature Review System
Demonstrates how to programmatically add citations and generate documents
"""

import yaml
from citation_manager import CitationManager, Citation
from review_generator import ReviewDocument, ReviewSection
from provenance_tracker import ProvenanceTracker, SearchQuery, InclusionDecision
from datetime import datetime


def main():
    """Example workflow"""
    
    # Load configuration
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    print("TF PV Literature Review System - Example Usage")
    print("=" * 60)
    print()
    
    # 1. Initialize components
    print("1. Initializing components...")
    citation_manager = CitationManager(config)
    review_doc = ReviewDocument(config)
    provenance = ProvenanceTracker(config)
    print("   ✓ Components initialized")
    print()
    
    # 2. Add some example citations
    print("2. Adding example citations...")
    
    # Original Tully-Fisher paper
    tf_paper = Citation(
        citekey="tully1977new",
        title="A New Method of Determining Distances to Galaxies",
        authors=["R. Brent Tully", "J. Richard Fisher"],
        year=1977,
        journal="Astronomy and Astrophysics",
        ads_bibcode="1977A&A....54..661T",
        ads_url="https://ui.adsabs.harvard.edu/abs/1977A&A....54..661T"
    )
    citation_manager.add_citation(tf_paper)
    print(f"   ✓ Added: {tf_paper.citekey}")
    
    # Cosmicflows-3 paper
    cf3_paper = Citation(
        citekey="tully2016cosmicflows3",
        title="Cosmicflows-3",
        authors=["R. Brent Tully", "Hélène M. Courtois", "Jenny G. Sorce"],
        year=2016,
        journal="The Astronomical Journal",
        doi="10.3847/0004-6256/152/2/50",
        ads_bibcode="2016AJ....152...50T",
        ads_url="https://ui.adsabs.harvard.edu/abs/2016AJ....152...50T"
    )
    citation_manager.add_citation(cf3_paper)
    print(f"   ✓ Added: {cf3_paper.citekey}")
    
    # SKA paper
    ska_paper = Citation(
        citekey="braun2019anticipatedperformancesquarekilometre",
        title="Anticipated Performance of the Square Kilometre Array -- Phase 1 (SKA1)",
        authors=["Robert Braun", "Anna Bonaldi", "Tyler Bourke", "Evan Keane", "Jeff Wagg"],
        year=2019,
        arxiv_id="1912.12699",
        publisher_url="https://arxiv.org/abs/1912.12699"
    )
    citation_manager.add_citation(ska_paper)
    print(f"   ✓ Added: {ska_paper.citekey}")
    print()
    
    # 3. Record search queries
    print("3. Recording search queries...")
    query = SearchQuery(
        query_string="Tully-Fisher peculiar velocities",
        database="NASA/ADS",
        timestamp=datetime.now().isoformat(),
        num_results=150,
        included_count=3,
        notes="Example query"
    )
    provenance.add_query(query)
    print(f"   ✓ Recorded query: {query.query_string}")
    print()
    
    # 4. Record inclusion decision
    print("4. Recording inclusion decision...")
    decision = InclusionDecision(
        citekey="tully1977new",
        title=tf_paper.title,
        decision="included",
        rationale="Seminal work establishing the TF relation",
        criteria_met=["Methodological significance", "Historical importance"],
        criteria_failed=[],
        timestamp=datetime.now().isoformat()
    )
    provenance.add_decision(decision)
    print(f"   ✓ Recorded decision for: {decision.citekey}")
    print()
    
    # 5. Create custom section
    print("5. Creating custom section...")
    custom_section = ReviewSection("Example Custom Section", level=1)
    custom_section.content = """This is an example of adding custom content. 
The original Tully-Fisher relation \\citep{tully1977new} has been extensively 
applied to peculiar velocity surveys. Modern catalogs like Cosmicflows-3 
\\citep{tully2016cosmicflows3} have enabled unprecedented constraints on 
large-scale structure. Future surveys with SKA \\citep{braun2019anticipatedperformancesquarekilometre} 
will revolutionize this field."""
    
    # Add subsection
    subsection = ReviewSection("Example Subsection", level=2)
    subsection.content = "Additional details can be organized in subsections."
    custom_section.add_subsection(subsection)
    
    review_doc.add_section(custom_section)
    print(f"   ✓ Added custom section with {len(custom_section.subsections)} subsection(s)")
    print()
    
    # 6. Set abstract
    print("6. Setting abstract...")
    review_doc.set_abstract(
        "This example demonstrates the capabilities of the TF PV Literature Review System. "
        "We show how to programmatically add citations, create custom sections, and generate "
        "outputs in multiple formats."
    )
    print("   ✓ Abstract set")
    print()
    
    # 7. Generate outputs
    print("7. Generating outputs...")
    
    # Generate bibliography
    citation_manager.generate_bibtex("example_references.bib")
    print("   ✓ Generated example_references.bib")
    
    # Generate citation ledger
    citation_manager.save_to_ledger("example_ledger.json")
    print("   ✓ Generated example_ledger.json")
    
    # Generate LaTeX
    review_doc.bibliography_file = "example_references"
    review_doc.save_latex("example_review.tex")
    print("   ✓ Generated example_review.tex")
    
    # Generate Markdown
    review_doc.save_markdown("example_review.md")
    print("   ✓ Generated example_review.md")
    
    # Generate provenance report
    provenance.save_report("example_provenance.md")
    print("   ✓ Generated example_provenance.md")
    print()
    
    # 8. Summary
    print("=" * 60)
    print("Summary:")
    print(f"  Citations: {len(citation_manager.citations)}")
    print(f"  Sections: {len(review_doc.sections)}")
    print(f"  Queries: {len(provenance.queries)}")
    print(f"  Decisions: {len(provenance.decisions)}")
    print()
    print("Example outputs generated successfully!")
    print("Check example_review.tex, example_review.md, and other example_* files")
    print()


if __name__ == '__main__':
    main()
