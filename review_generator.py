"""
Review Document Generator for TF PV Literature Review
Generates LaTeX and Markdown versions of the review
"""

from typing import Dict, List, Optional
from datetime import datetime
import yaml


class ReviewSection:
    """Represents a section of the review document"""
    
    def __init__(self, title: str, level: int = 1, content: str = ""):
        self.title = title
        self.level = level  # 1=section, 2=subsection, 3=subsubsection
        self.content = content
        self.subsections: List['ReviewSection'] = []
        
    def add_subsection(self, subsection: 'ReviewSection') -> None:
        """Add a subsection"""
        self.subsections.append(subsection)
        
    def to_latex(self) -> str:
        """Convert section to LaTeX"""
        section_commands = {1: "section", 2: "subsection", 3: "subsubsection"}
        cmd = section_commands.get(self.level, "paragraph")
        
        lines = [f"\\{cmd}{{{self.title}}}"]
        if self.content:
            lines.append("")
            lines.append(self.content)
            
        for subsection in self.subsections:
            lines.append("")
            lines.append(subsection.to_latex())
            
        return "\n".join(lines)
        
    def to_markdown(self) -> str:
        """Convert section to Markdown"""
        header = "#" * self.level
        lines = [f"{header} {self.title}"]
        if self.content:
            lines.append("")
            lines.append(self.content)
            
        for subsection in self.subsections:
            lines.append("")
            lines.append(subsection.to_markdown())
            
        return "\n".join(lines)


class ReviewDocument:
    """Main review document class"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.title = config['review']['title']
        self.short_title = config['review']['short_title']
        self.authors = config['authors']
        self.affiliations = config['affiliations']
        self.abstract = ""
        self.sections: List[ReviewSection] = []
        self.bibliography_file = config['outputs']['bibliography']
        
    def set_abstract(self, abstract: str) -> None:
        """Set the abstract"""
        self.abstract = abstract
        
    def add_section(self, section: ReviewSection) -> None:
        """Add a top-level section"""
        self.sections.append(section)
        
    def create_default_outline(self) -> None:
        """Create the default outline structure for TF PV review"""
        
        # Introduction
        intro = ReviewSection("Introduction and Historical Context", level=1)
        intro.content = """The measurement of peculiar velocities—deviations from the smooth Hubble flow—provides a direct probe of the growth of cosmic structure and the underlying gravitational dynamics. Among distance indicator methods, the Tully–Fisher (TF) relation \\citep{tully1977new} has proven to be a powerful tool for peculiar velocity (PV) surveys, linking galaxy rotation velocities to their intrinsic luminosities or baryonic masses."""
        
        intro.add_subsection(ReviewSection("Scope and Objectives", level=2, 
            content="This review comprehensively surveys the use of the Tully–Fisher relation for peculiar velocity measurements and cosmological applications."))
        intro.add_subsection(ReviewSection("Historical Development", level=2,
            content="The TF relation was first established in 1977, and has since undergone continuous refinement."))
        
        self.add_section(intro)
        
        # TF Relation
        tf_section = ReviewSection("The Tully–Fisher Relation as a Distance and Velocity Probe", level=1)
        tf_section.content = """The Tully–Fisher relation provides a fundamental correlation between galaxy luminosity and rotation velocity, serving as a distance indicator and enabling peculiar velocity measurements."""
        
        tf_section.add_subsection(ReviewSection("Physical Basis and Calibration", level=2,
            content="The TF relation arises from the virial theorem and galaxy scaling relations."))
        tf_section.add_subsection(ReviewSection("Optical, NIR, and Baryonic Variants", level=2,
            content="Different wavelength bands and the baryonic TF relation offer complementary advantages."))
        tf_section.add_subsection(ReviewSection("Systematic Uncertainties", level=2,
            content="Key systematics include Malmquist bias, selection effects, inclination corrections, and extinction."))
        
        self.add_section(tf_section)
        
        # Survey Landscape
        survey_section = ReviewSection("Survey Landscape for TF Peculiar Velocities", level=1)
        survey_section.content = """A rich history of TF-based peculiar velocity surveys has accumulated over several decades."""
        
        survey_section.add_subsection(ReviewSection("Major Surveys and Catalogs", level=2,
            content="Key surveys include SFI/SFI++, Cosmicflows series, 2MTF, 6dFGSv, HIPASS, and ALFALFA."))
        survey_section.add_subsection(ReviewSection("Survey Characteristics and Comparison", level=2,
            content="Table~\\ref{tab:survey_comparison} summarizes key characteristics."))
        
        self.add_section(survey_section)
        
        # Methods
        methods_section = ReviewSection("Methodological Foundations", level=1)
        methods_section.content = """Extracting cosmological constraints from peculiar velocities requires careful statistical modeling."""
        
        methods_section.add_subsection(ReviewSection("Peculiar Velocity Statistics in Linear Theory", level=2,
            content="The peculiar velocity field is related to the matter density field and the growth rate."))
        methods_section.add_subsection(ReviewSection("Velocity Field Reconstruction", level=2,
            content="POTENT, Wiener filtering, and constrained realizations enable full-field reconstruction."))
        methods_section.add_subsection(ReviewSection("Bias Corrections and Hierarchical Modeling", level=2,
            content="Modern approaches use hierarchical Bayesian methods to account for selection effects."))
        
        self.add_section(methods_section)
        
        # Cosmological Results
        results_section = ReviewSection("Cosmological Results from TF Peculiar Velocities", level=1)
        results_section.content = """TF PV surveys have yielded important constraints on cosmological parameters."""
        
        results_section.add_subsection(ReviewSection("Growth Rate and $f\\sigma_8$ Constraints", level=2,
            content="Peculiar velocities directly probe the growth rate of structure."))
        results_section.add_subsection(ReviewSection("Hubble Constant and Distance Scale", level=2,
            content="TF surveys contribute to $H_0$ measurements and cross-checks."))
        results_section.add_subsection(ReviewSection("Bulk Flows and Large-Scale Structure", level=2,
            content="Measurements of coherent bulk flows test homogeneity and isotropy."))
        
        self.add_section(results_section)
        
        # Simulations
        sims_section = ReviewSection("Simulations and Mocks for TF Peculiar Velocities", level=1)
        sims_section.content = """Realistic simulations are essential for validation and forecast."""
        
        sims_section.add_subsection(ReviewSection("N-body and Hydrodynamic Mocks", level=2,
            content="Simulations provide controlled environments for testing methods."))
        sims_section.add_subsection(ReviewSection("Survey Realism and Selection Functions", level=2,
            content="Mock catalogs must incorporate realistic observational effects."))
        
        self.add_section(sims_section)
        
        # SKA Forecasts
        ska_section = ReviewSection("SKA Era Forecasts and Prospects", level=1)
        ska_section.content = """The Square Kilometre Array and its precursors promise transformative HI-based TF peculiar velocity surveys."""
        
        ska_section.add_subsection(ReviewSection("SKA1-MID and SKA1-SUR Capabilities", level=2,
            content="SKA Phase 1 will enable deep HI surveys with precise linewidth measurements."))
        ska_section.add_subsection(ReviewSection("Precursors and Pathfinders", level=2,
            content="ASKAP, MeerKAT, and APERTIF are already demonstrating HI TF capabilities."))
        ska_section.add_subsection(ReviewSection("Forecast Assumptions and Systematics Budgets", level=2,
            content="Forecasts depend on survey strategy, linewidth precision, and systematics control."))
        ska_section.add_subsection(ReviewSection("Multi-Probe Synergies", level=2,
            content="SKA TF PV will complement Euclid, LSST, DESI, and CMB experiments."))
        
        self.add_section(ska_section)
        
        # Comparison with other probes
        comparison_section = ReviewSection("Comparison with Other PV Probes", level=1)
        comparison_section.content = """TF is one of several PV methods, each with distinct advantages."""
        
        comparison_section.add_subsection(ReviewSection("Fundamental Plane Peculiar Velocities", level=2,
            content="The FP offers an alternative distance indicator for early-type galaxies."))
        comparison_section.add_subsection(ReviewSection("Type Ia Supernovae Peculiar Velocities", level=2,
            content="SNe Ia provide precise distances but sparser sampling."))
        
        self.add_section(comparison_section)
        
        # Future Directions
        future_section = ReviewSection("Open Problems and Future Directions", level=1)
        future_section.content = """Several challenges and opportunities remain for TF PV science."""
        
        future_section.add_subsection(ReviewSection("Outstanding Systematics", level=2,
            content="Key challenges include calibration uncertainties and selection biases."))
        future_section.add_subsection(ReviewSection("Theoretical Developments", level=2,
            content="Advances in modeling and simulation will improve interpretation."))
        future_section.add_subsection(ReviewSection("Observational Opportunities", level=2,
            content="Future facilities and surveys offer exciting prospects."))
        
        self.add_section(future_section)
        
        # Conclusions
        conclusions = ReviewSection("Conclusions", level=1)
        conclusions.content = """Tully–Fisher peculiar velocity surveys have matured into a powerful cosmological probe, with the SKA era promising transformative advances."""
        
        self.add_section(conclusions)
        
    def to_latex(self) -> str:
        """Generate full LaTeX document"""
        lines = []
        
        # Preamble
        doc_class = self.config['latex']['document_class']
        class_opts = self.config['latex']['class_options']
        lines.append(f"\\documentclass[{class_opts}]{{{doc_class}}}")
        lines.append("\\usepackage{aaskaiid}")
        lines.append("")
        
        # Title and authors
        lines.append(f"\\title{{{self.title}}}")
        lines.append(f"\\ShortTitle{{{self.short_title}}}")
        lines.append("")
        
        for i, author in enumerate(self.authors):
            affil_str = ",".join(map(str, author['affiliations']))
            lines.append(f"\\author[{affil_str}]{{{author['name']}}}")
            if i == 0:
                # Use first author for short name
                lines.append(f"\\ShortName{{{author['name']} et al.}}")
                
        lines.append("")
        
        # Affiliations
        for affil in self.affiliations:
            lines.append(f"\\affiliation[{affil['id']}]{{{affil['name']}}}")
            
        for author in self.authors:
            if 'email' in author:
                lines.append(f"\\emailAdd{{{author['email']}}}")
                
        lines.append("")
        
        # Abstract
        lines.append(f"\\abstract{{{self.abstract}}}")
        lines.append("")
        
        # Begin document
        lines.append("\\begin{document}")
        lines.append("\\maketitle")
        lines.append("")
        
        # Sections
        for section in self.sections:
            lines.append(section.to_latex())
            lines.append("")
            
        # Bibliography
        bib_style = self.config['latex']['bibliography_style']
        bib_file = self.bibliography_file.replace('.bib', '')
        lines.append(f"\\bibliographystyle{{{bib_style}}}")
        lines.append(f"\\bibliography{{{bib_file}}}")
        lines.append("")
        
        lines.append("\\end{document}")
        
        return "\n".join(lines)
        
    def to_markdown(self) -> str:
        """Generate full Markdown document"""
        lines = []
        
        # Title and metadata
        lines.append(f"# {self.title}")
        lines.append("")
        
        # Authors
        author_names = [a['name'] for a in self.authors]
        lines.append(", ".join(author_names))
        lines.append("")
        
        # Affiliations
        for affil in self.affiliations:
            lines.append(f"{affil['id']}. {affil['name']}")
        lines.append("")
        
        # Abstract
        lines.append("## Abstract")
        lines.append("")
        lines.append(self.abstract)
        lines.append("")
        
        # Sections
        for section in self.sections:
            lines.append(section.to_markdown())
            lines.append("")
            
        return "\n".join(lines)
        
    def save_latex(self, filepath: str) -> None:
        """Save LaTeX document to file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.to_latex())
            
    def save_markdown(self, filepath: str) -> None:
        """Save Markdown document to file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.to_markdown())


def load_config(config_path: str) -> Dict:
    """Load configuration from YAML file"""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)
