"""
Survey Table Generator for TF PV Review
Generates LaTeX tables summarizing major TF PV surveys
"""

from typing import List, Dict


class Survey:
    """Represents a TF PV survey"""
    
    def __init__(self, name: str, year: int, **kwargs):
        self.name = name
        self.year = year
        self.reference = kwargs.get('reference', '')
        self.sample_size = kwargs.get('sample_size', 'N/A')
        self.bands = kwargs.get('bands', 'N/A')
        self.depth = kwargs.get('depth', 'N/A')
        self.sky_coverage = kwargs.get('sky_coverage', 'N/A')
        self.velocity_measure = kwargs.get('velocity_measure', 'HI linewidth')
        self.calibration = kwargs.get('calibration', 'N/A')
        self.notes = kwargs.get('notes', '')


def create_default_surveys() -> List[Survey]:
    """Create list of major TF PV surveys"""
    surveys = [
        Survey(
            name="SFI",
            year=1997,
            reference="\\citet{giovanelli1997sfi}",
            sample_size="~1300",
            bands="I-band",
            depth="cz < 6000 km/s",
            sky_coverage="High Galactic latitude",
            velocity_measure="HI linewidth (W₂₀)",
            calibration="Cepheid distances",
            notes="Sparse Tully-Fisher survey"
        ),
        Survey(
            name="SFI++",
            year=2016,
            reference="\\citet{springob2016sfi++}",
            sample_size="~4800",
            bands="I-band",
            depth="cz < 15000 km/s",
            sky_coverage="All-sky (|b| > 15°)",
            velocity_measure="HI linewidth (W₂₀)",
            calibration="Multi-step calibration",
            notes="Extension of SFI to larger volume"
        ),
        Survey(
            name="2MTF",
            year=2012,
            reference="\\citet{hong2012tf}",
            sample_size="~2000",
            bands="J, H, K (2MASS)",
            depth="cz < 10000 km/s",
            sky_coverage="Southern hemisphere",
            velocity_measure="HI linewidth",
            calibration="NIR Tully-Fisher",
            notes="Near-infrared survey"
        ),
        Survey(
            name="Cosmicflows-3",
            year=2016,
            reference="\\citet{tully2016cosmicflows3}",
            sample_size="~18000 distances",
            bands="Multi-band compilation",
            depth="cz < 30000 km/s",
            sky_coverage="All-sky",
            velocity_measure="Multiple methods",
            calibration="Unified framework",
            notes="Compilation including TF, FP, SNe Ia"
        ),
        Survey(
            name="6dFGSv",
            year=2012,
            reference="\\citet{springob20126dfgsv}",
            sample_size="~8500 (FP)",
            bands="K-band",
            depth="cz < 16000 km/s",
            sky_coverage="Southern hemisphere",
            velocity_measure="Velocity dispersion (FP)",
            calibration="Local calibrators",
            notes="Includes FP and some TF"
        ),
        Survey(
            name="HIPASS TF",
            year=2006,
            reference="\\citet{koribalski2004hipass}",
            sample_size="~4300 HI detections",
            bands="Optical + HI",
            depth="cz < 12700 km/s",
            sky_coverage="Southern hemisphere",
            velocity_measure="HI linewidth (W₅₀)",
            calibration="Local TF calibration",
            notes="Blind HI survey"
        ),
        Survey(
            name="ALFALFA",
            year=2011,
            reference="\\citet{haynes2011alfalfa}",
            sample_size="~31000 HI sources",
            bands="Optical + HI",
            depth="cz < 18000 km/s",
            sky_coverage="7000 deg² (North)",
            velocity_measure="HI linewidth (W₅₀)",
            calibration="Various optical surveys",
            notes="Large HI survey, TF subset analyzed"
        ),
    ]
    return surveys


def generate_survey_comparison_table(surveys: List[Survey]) -> str:
    """Generate LaTeX table comparing surveys"""
    
    lines = [
        "\\begin{table*}",
        "\\centering",
        "\\caption{Major Tully–Fisher and Related Peculiar Velocity Surveys}",
        "\\label{tab:survey_comparison}",
        "\\begin{tabular}{llcccll}",
        "\\hline",
        "Survey & Year & Sample Size & Bands & Depth & Velocity & Reference \\\\",
        "       &      &             &       & (km/s) & Measure  &           \\\\",
        "\\hline"
    ]
    
    for survey in sorted(surveys, key=lambda s: s.year):
        row = f"{survey.name} & {survey.year} & {survey.sample_size} & " \
              f"{survey.bands} & {survey.depth} & {survey.velocity_measure} & " \
              f"{survey.reference} \\\\"
        lines.append(row)
    
    lines.extend([
        "\\hline",
        "\\end{tabular}",
        "\\tablecomments{Summary of major TF-based and related peculiar velocity surveys. ",
        "Sample sizes refer to galaxies with TF or FP distance estimates. Velocity measures ",
        "indicate the primary observable used (HI linewidth W₂₀ or W₅₀, or velocity dispersion for FP). ",
        "Depths are approximate maximum recession velocities.}",
        "\\end{table*}"
    ])
    
    return "\n".join(lines)


def generate_ska_forecast_table() -> str:
    """Generate table of SKA forecast parameters"""
    
    lines = [
        "\\begin{table}",
        "\\centering",
        "\\caption{SKA HI TF Survey Forecast Parameters}",
        "\\label{tab:ska_forecast}",
        "\\begin{tabular}{lcc}",
        "\\hline",
        "Parameter & SKA1-MID & SKA1-SUR \\\\",
        "\\hline",
        "Frequency range (GHz) & 0.35--1.05 & 0.35--3.05 \\\\",
        "Angular resolution (arcsec) & $\\sim$1 & $\\sim$1 \\\\",
        "HI detection threshold & $\\sim$10⁸ M$_\\odot$ & $\\sim$10⁸ M$_\\odot$ \\\\",
        "Expected HI galaxies & $\\sim$10⁶ & $\\sim$10⁶ \\\\",
        "Redshift range (HI) & 0--0.5 & 0--0.5 \\\\",
        "Linewidth precision & $<$5\\% & $<$5\\% \\\\",
        "TF sample (z<0.1) & $\\sim$10⁵ & $\\sim$10⁵ \\\\",
        "PV precision (km/s) & $\\sim$50 & $\\sim$50 \\\\",
        "\\hline",
        "\\end{tabular}",
        "\\tablecomments{Forecast parameters for HI-based TF peculiar velocity surveys ",
        "with SKA Phase 1. Linewidth precision and PV precision depend on galaxy properties, ",
        "S/N, and inclination. Estimates assume median conditions and conservative systematics budgets.}",
        "\\end{table}"
    ]
    
    return "\n".join(lines)


def generate_method_comparison_table() -> str:
    """Generate table comparing PV methods"""
    
    lines = [
        "\\begin{table*}",
        "\\centering",
        "\\caption{Comparison of Peculiar Velocity Methods}",
        "\\label{tab:method_comparison}",
        "\\begin{tabular}{lccccl}",
        "\\hline",
        "Method & Galaxy Type & Precision & Systematics & Depth & Advantages/Disadvantages \\\\",
        "       &             & (\\%)      & Level       & (Mpc)  &                          \\\\",
        "\\hline",
        "TF (optical) & Spirals & 15--25 & Medium & 150 & Large samples; dust, morphology \\\\",
        "TF (NIR) & Spirals & 10--20 & Medium-Low & 150 & Less extinction; calibration \\\\",
        "TF (HI) & Spirals & 15--25 & Medium & 200+ & Direct kinematics; HI mass limit \\\\",
        "Baryonic TF & Spirals & 10--15 & Low & 150 & Tight relation; gas+stars needed \\\\",
        "FP & Early-type & 10--20 & Medium & 200 & Complementary sample; velocity dispersion \\\\",
        "SNe Ia & All types & 5--10 & Low & 500+ & High precision; sparse sampling \\\\",
        "\\hline",
        "\\end{tabular}",
        "\\tablecomments{Comparison of major peculiar velocity methods. Precision refers to ",
        "typical fractional distance uncertainty per galaxy. Systematics level is qualitative. ",
        "Depth indicates typical maximum distance with current samples.}",
        "\\end{table*}"
    ]
    
    return "\n".join(lines)


def save_all_tables(output_dir: str = "tables") -> None:
    """Generate and save all standard tables"""
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    # Survey comparison table
    surveys = create_default_surveys()
    table1 = generate_survey_comparison_table(surveys)
    with open(f"{output_dir}/survey_comparison.tex", 'w') as f:
        f.write(table1)
    print(f"Generated {output_dir}/survey_comparison.tex")
    
    # SKA forecast table
    table2 = generate_ska_forecast_table()
    with open(f"{output_dir}/ska_forecast.tex", 'w') as f:
        f.write(table2)
    print(f"Generated {output_dir}/ska_forecast.tex")
    
    # Method comparison table
    table3 = generate_method_comparison_table()
    with open(f"{output_dir}/method_comparison.tex", 'w') as f:
        f.write(table3)
    print(f"Generated {output_dir}/method_comparison.tex")


if __name__ == '__main__':
    save_all_tables()
