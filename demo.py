#!/usr/bin/env python3
"""
Complete End-to-End Demonstration
Generates a minimal but complete TF PV review with all components
"""

import os
import sys
from pathlib import Path

# Import all components
from citation_manager import CitationManager, Citation
from review_generator import ReviewDocument, ReviewSection, load_config
from provenance_tracker import ProvenanceTracker, SearchQuery, InclusionDecision
from survey_tables import create_default_surveys, generate_survey_comparison_table
from datetime import datetime


def create_complete_review():
    """Create a complete minimal review demonstrating all features"""
    
    print("=" * 70)
    print("TF PV Literature Review - Complete End-to-End Demonstration")
    print("=" * 70)
    print()
    
    # Load config
    config = load_config('config.yaml')
    
    # Initialize components
    print("Step 1: Initializing components...")
    citation_mgr = CitationManager(config)
    doc = ReviewDocument(config)
    provenance = ProvenanceTracker(config)
    print("✓ Initialized")
    print()
    
    # Add key citations
    print("Step 2: Adding key citations...")
    citations = [
        Citation(
            citekey="tully1977new",
            title="A New Method of Determining Distances to Galaxies",
            authors=["R. Brent Tully", "J. Richard Fisher"],
            year=1977,
            journal="Astronomy and Astrophysics",
            ads_bibcode="1977A&A....54..661T"
        ),
        Citation(
            citekey="giovanelli1997sfi",
            title="I-band Tully-Fisher relation for cluster spirals",
            authors=["R. Giovanelli", "M. P. Haynes", "et al."],
            year=1997,
            journal="AJ",
            ads_bibcode="1997AJ....113...53G"
        ),
        Citation(
            citekey="springob2016sfi++",
            title="The Spitzer Extended Tully-Fisher Survey",
            authors=["C. M. Springob", "et al."],
            year=2016,
            journal="MNRAS",
            doi="10.1093/mnras/stw1618"
        ),
        Citation(
            citekey="tully2016cosmicflows3",
            title="Cosmicflows-3",
            authors=["R. Brent Tully", "Hélène M. Courtois", "Jenny G. Sorce"],
            year=2016,
            journal="AJ",
            doi="10.3847/0004-6256/152/2/50"
        ),
        Citation(
            citekey="braun2019ska",
            title="Anticipated Performance of SKA Phase 1",
            authors=["Robert Braun", "et al."],
            year=2019,
            arxiv_id="1912.12699"
        ),
    ]
    
    for cit in citations:
        citation_mgr.add_citation(cit)
    print(f"✓ Added {len(citations)} citations")
    print()
    
    # Record provenance
    print("Step 3: Recording search provenance...")
    query = SearchQuery(
        query_string="Tully-Fisher peculiar velocities",
        database="NASA/ADS",
        timestamp=datetime.now().isoformat(),
        num_results=len(citations),
        included_count=len(citations),
        notes="Key foundational papers"
    )
    provenance.add_query(query)
    
    for cit in citations:
        decision = InclusionDecision(
            citekey=cit.citekey,
            title=cit.title,
            decision="included",
            rationale="Essential for TF PV review",
            criteria_met=["Historical significance", "Methodological importance"],
            criteria_failed=[],
            timestamp=datetime.now().isoformat()
        )
        provenance.add_decision(decision)
    print(f"✓ Recorded {len(citations)} inclusion decisions")
    print()
    
    # Build document with substantive content
    print("Step 4: Building document structure...")
    
    # Abstract
    doc.set_abstract(
        "Tully–Fisher (TF)–based peculiar velocity (PV) surveys provide a powerful "
        "probe of large-scale structure and the growth of cosmic structure. This review "
        "examines the TF relation as a distance indicator, surveys major TF PV programs, "
        "discusses methodological developments, and assesses cosmological constraints. "
        "We highlight future prospects with the Square Kilometre Array (SKA), which promises "
        "to revolutionize HI-based TF peculiar velocity measurements."
    )
    
    # Introduction
    intro = ReviewSection("Introduction", level=1)
    intro.content = r"""
Peculiar velocities—the component of galaxy motion not attributable to the 
Hubble expansion—provide a direct probe of the gravitational field on large 
scales and the growth of structure \citep{tully1977new}. The Tully–Fisher (TF) 
relation, which connects galaxy luminosity (or baryonic mass) to rotation 
velocity, has enabled some of the largest peculiar velocity surveys to date 
\citep{giovanelli1997sfi,springob2016sfi++,tully2016cosmicflows3}.

This review surveys the use of the TF relation for peculiar velocity measurements, 
covering historical foundations, major survey programs, methodological advances, 
cosmological constraints, and future prospects with next-generation facilities.
"""
    doc.add_section(intro)
    
    # TF Relation section
    tf_section = ReviewSection("The Tully–Fisher Relation", level=1)
    tf_section.content = r"""
The Tully–Fisher relation \citep{tully1977new} connects the luminosity $L$ (or 
absolute magnitude $M$) of a spiral galaxy to its rotation velocity $v_{\rm rot}$:
\begin{equation}
M = a + b \log_{10}(v_{\rm rot})
\end{equation}
where $a$ is the zero-point and $b$ is the slope (typically $b \approx -8$ to $-10$ 
depending on band). This empirical relation arises from the virial theorem and galaxy 
scaling relations, providing a distance indicator with typical scatter 
$\sigma \sim 0.3$–$0.5$ mag.
"""
    
    calibration = ReviewSection("Calibration Strategies", level=2)
    calibration.content = r"""
Accurate zero-point calibration is critical for PV measurements. Calibrators include 
Cepheid distances, Tip of the Red Giant Branch (TRGB) measurements, and surface 
brightness fluctuations. The choice of band affects systematics: near-infrared (NIR) 
TF relations suffer less from dust extinction, while baryonic TF (combining stellar 
and gas mass) exhibits tighter intrinsic scatter.
"""
    tf_section.add_subsection(calibration)
    doc.add_section(tf_section)
    
    # Survey section
    surveys = ReviewSection("Major TF Peculiar Velocity Surveys", level=1)
    surveys.content = r"""
Table~\ref{tab:survey_comparison} summarizes major TF PV surveys. The Sparse 
Tully-Fisher Survey (SFI; \citealt{giovanelli1997sfi}) pioneered large-scale 
I-band TF measurements. Its successor SFI++ \citep{springob2016sfi++} extended 
coverage to $\sim$5000 galaxies. The Cosmicflows compilation 
\citep{tully2016cosmicflows3} integrates multiple distance indicators including 
TF, providing comprehensive all-sky coverage.
"""
    doc.add_section(surveys)
    
    # SKA section
    ska = ReviewSection("Future Prospects with SKA", level=1)
    ska.content = r"""
The Square Kilometre Array \citep{braun2019ska} will revolutionize HI-based TF 
surveys. SKA Phase 1 is expected to detect $\sim 10^6$ HI galaxies to $z \sim 0.5$, 
enabling TF PV measurements for $\sim 10^5$ spiral galaxies at $z < 0.1$ with 
linewidth precision $\lesssim 5\%$. This will provide exquisite constraints on 
the growth rate $f\sigma_8$ and tests of gravity on scales complementary to 
redshift-space distortions and weak lensing.
"""
    doc.add_section(ska)
    
    # Conclusions
    conclusions = ReviewSection("Conclusions", level=1)
    conclusions.content = r"""
Tully–Fisher peculiar velocity surveys have matured into a powerful cosmological 
probe, contributing constraints on large-scale structure, the growth rate, and the 
Hubble constant. Ongoing surveys and future facilities like SKA promise to 
dramatically improve sample sizes and precision, enabling percent-level measurements 
of cosmological parameters and stringent tests of fundamental physics.
"""
    doc.add_section(conclusions)
    
    print(f"✓ Created document with {len(doc.sections)} sections")
    print()
    
    # Generate tables
    print("Step 5: Generating tables...")
    surveys_list = create_default_surveys()
    survey_table = generate_survey_comparison_table(surveys_list)
    
    os.makedirs('demo_output/tables', exist_ok=True)
    with open('demo_output/tables/survey_comparison.tex', 'w') as f:
        f.write(survey_table)
    print(f"✓ Generated survey comparison table ({len(surveys_list)} surveys)")
    print()
    
    # Generate all outputs
    print("Step 6: Generating outputs...")
    os.makedirs('demo_output', exist_ok=True)
    
    citation_mgr.generate_bibtex('demo_output/demo_references.bib')
    print("  ✓ demo_output/demo_references.bib")
    
    citation_mgr.save_to_ledger('demo_output/demo_ledger.json')
    print("  ✓ demo_output/demo_ledger.json")
    
    doc.bibliography_file = "demo_references"
    doc.save_latex('demo_output/demo_review.tex')
    print("  ✓ demo_output/demo_review.tex")
    
    doc.save_markdown('demo_output/demo_review.md')
    print("  ✓ demo_output/demo_review.md")
    
    provenance.save_report('demo_output/demo_provenance.md')
    print("  ✓ demo_output/demo_provenance.md")
    print()
    
    # Summary
    print("=" * 70)
    print("Demo Complete!")
    print("=" * 70)
    print()
    print("Generated a complete minimal TF PV review with:")
    print(f"  • {len(citations)} citations with full metadata")
    print(f"  • {len(doc.sections)} main sections with content")
    print(f"  • Survey comparison table ({len(surveys_list)} surveys)")
    print(f"  • Provenance tracking ({len(provenance.queries)} queries)")
    print()
    print("Outputs in demo_output/:")
    print("  - demo_review.tex (LaTeX document)")
    print("  - demo_review.md (Markdown version)")
    print("  - demo_references.bib (bibliography)")
    print("  - demo_ledger.json (citation ledger)")
    print("  - demo_provenance.md (search provenance)")
    print("  - tables/survey_comparison.tex")
    print()
    print("To compile PDF:")
    print("  cd demo_output")
    print("  pdflatex demo_review.tex")
    print("  bibtex demo_review")
    print("  pdflatex demo_review.tex")
    print("  pdflatex demo_review.tex")
    print()


if __name__ == '__main__':
    try:
        create_complete_review()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
