"""
Citation Manager for TF PV Literature Review
Handles ADS/arXiv queries, BibTeX generation, and citation verification
"""

import json
import requests
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import re


@dataclass
class Citation:
    """Represents a single bibliographic entry with verification state"""
    citekey: str
    title: str
    authors: List[str]
    year: int
    journal: Optional[str] = None
    ads_bibcode: Optional[str] = None
    doi: Optional[str] = None
    arxiv_id: Optional[str] = None
    ads_url: Optional[str] = None
    publisher_url: Optional[str] = None
    last_verified: Optional[str] = None
    http_status_ads: Optional[int] = None
    http_status_doi: Optional[int] = None
    crossref_match: bool = False
    ads_match: bool = False
    notes: str = ""
    bibtex_entry: str = ""
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Citation':
        """Create Citation from dictionary"""
        return cls(**data)


class CitationManager:
    """Manages citations, verification, and BibTeX generation"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.citations: Dict[str, Citation] = {}
        self.ads_token = None  # ADS API token (set via environment)
        self.verification_timeout = config.get('citations', {}).get('verification_timeout_seconds', 10)
        self.max_retries = config.get('citations', {}).get('max_verification_retries', 3)
        
    def add_citation(self, citation: Citation) -> None:
        """Add a citation to the manager"""
        self.citations[citation.citekey] = citation
        
    def load_from_ledger(self, filepath: str) -> None:
        """Load citations from JSON ledger"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for entry in data:
                    citation = Citation.from_dict(entry)
                    self.citations[citation.citekey] = citation
        except FileNotFoundError:
            print(f"Ledger file {filepath} not found, starting fresh")
            
    def save_to_ledger(self, filepath: str) -> None:
        """Save citations to JSON ledger"""
        data = [citation.to_dict() for citation in self.citations.values()]
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
    def generate_bibtex(self, filepath: str) -> None:
        """Generate BibTeX file from all citations"""
        with open(filepath, 'w', encoding='utf-8') as f:
            for citation in sorted(self.citations.values(), key=lambda x: (x.year, x.citekey)):
                if citation.bibtex_entry:
                    f.write(citation.bibtex_entry + "\n\n")
                else:
                    # Generate basic BibTeX if not provided
                    f.write(self._generate_basic_bibtex(citation) + "\n\n")
                    
    def _generate_basic_bibtex(self, citation: Citation) -> str:
        """Generate basic BibTeX entry from citation metadata"""
        entry_type = "article" if citation.journal else "misc"
        
        lines = [f"@{entry_type}{{{citation.citekey},"]
        lines.append(f'  title={{{citation.title}}},')
        lines.append(f'  author={{{" and ".join(citation.authors)}}},')
        lines.append(f'  year={{{citation.year}}},')
        
        if citation.journal:
            lines.append(f'  journal={{{citation.journal}}},')
        if citation.doi:
            lines.append(f'  doi={{{citation.doi}}},')
        if citation.arxiv_id:
            lines.append(f'  eprint={{{citation.arxiv_id}}},')
            lines.append(f'  archivePrefix={{arXiv}},')
        if citation.ads_bibcode:
            lines.append(f'  adsurl={{{citation.ads_url or "https://ui.adsabs.harvard.edu/abs/" + citation.ads_bibcode}}},')
        if citation.publisher_url:
            lines.append(f'  url={{{citation.publisher_url}}},')
            
        lines.append("}")
        return "\n".join(lines)
        
    def verify_url(self, url: str) -> Tuple[bool, int]:
        """Verify that a URL resolves successfully"""
        for attempt in range(self.max_retries):
            try:
                response = requests.head(url, timeout=self.verification_timeout, allow_redirects=True)
                return (response.status_code == 200, response.status_code)
            except requests.RequestException as e:
                if attempt == self.max_retries - 1:
                    return (False, 0)
                time.sleep(1)
        return (False, 0)
        
    def verify_citation(self, citekey: str) -> Dict[str, bool]:
        """Verify a single citation's URLs and metadata"""
        citation = self.citations.get(citekey)
        if not citation:
            return {"error": "Citation not found"}
            
        results = {
            "ads_url_valid": False,
            "doi_url_valid": False,
            "metadata_complete": False
        }
        
        # Verify ADS URL
        if citation.ads_url:
            valid, status = self.verify_url(citation.ads_url)
            results["ads_url_valid"] = valid
            citation.http_status_ads = status
            
        # Verify DOI URL
        if citation.doi:
            doi_url = f"https://doi.org/{citation.doi}"
            valid, status = self.verify_url(doi_url)
            results["doi_url_valid"] = valid
            citation.http_status_doi = status
            citation.publisher_url = doi_url
            
        # Check metadata completeness
        results["metadata_complete"] = all([
            citation.title,
            citation.authors,
            citation.year,
            citation.citekey
        ])
        
        citation.last_verified = datetime.utcnow().isoformat()
        return results
        
    def verify_all_citations(self) -> Dict[str, Dict]:
        """Verify all citations in the manager"""
        results = {}
        for citekey in self.citations:
            print(f"Verifying {citekey}...")
            results[citekey] = self.verify_citation(citekey)
            time.sleep(0.5)  # Rate limiting
        return results
        
    def get_verification_report(self) -> Dict:
        """Generate a verification status report"""
        total = len(self.citations)
        verified = sum(1 for c in self.citations.values() if c.last_verified)
        ads_valid = sum(1 for c in self.citations.values() if c.http_status_ads == 200)
        doi_valid = sum(1 for c in self.citations.values() if c.http_status_doi == 200)
        
        return {
            "total_citations": total,
            "verified_count": verified,
            "ads_urls_valid": ads_valid,
            "doi_urls_valid": doi_valid,
            "verification_percentage": (verified / total * 100) if total > 0 else 0
        }
        
    def search_ads(self, query: str, max_results: int = 50) -> List[Dict]:
        """
        Search NASA/ADS for papers (requires ADS API token)
        Returns list of paper metadata dictionaries
        """
        # Placeholder - requires ADS API token
        # In real implementation, would use ads Python package or direct API calls
        print(f"ADS search query: {query}")
        print("Note: ADS API token required for actual search")
        return []
        
    def import_from_ads_bibcode(self, bibcode: str) -> Optional[Citation]:
        """Import citation from ADS bibcode"""
        # Placeholder - requires ADS API
        print(f"Importing from ADS bibcode: {bibcode}")
        return None
        
    def deduplicate_citations(self) -> List[str]:
        """
        Find and remove duplicate citations
        Returns list of removed citekeys
        """
        seen = {}
        duplicates = []
        
        for citekey, citation in list(self.citations.items()):
            # Create key from title and year
            key = (citation.title.lower().strip(), citation.year)
            
            if key in seen:
                # Keep the one with more complete metadata
                existing = self.citations[seen[key]]
                if self._citation_completeness(citation) > self._citation_completeness(existing):
                    # Replace existing with new one
                    duplicates.append(seen[key])
                    del self.citations[seen[key]]
                    seen[key] = citekey
                else:
                    duplicates.append(citekey)
                    del self.citations[citekey]
            else:
                seen[key] = citekey
                
        return duplicates
        
    def _citation_completeness(self, citation: Citation) -> int:
        """Calculate completeness score for a citation"""
        score = 0
        if citation.ads_bibcode:
            score += 3
        if citation.doi:
            score += 2
        if citation.arxiv_id:
            score += 1
        if citation.journal:
            score += 1
        if citation.bibtex_entry:
            score += 2
        return score


def create_citation_from_bibtex(bibtex_entry: str) -> Optional[Citation]:
    """Parse a BibTeX entry and create a Citation object"""
    # Simple parser - in production would use a proper BibTeX library
    lines = bibtex_entry.strip().split('\n')
    if not lines:
        return None
        
    # Extract citekey
    match = re.match(r'@\w+\{([^,]+),', lines[0])
    if not match:
        return None
    citekey = match.group(1)
    
    # Extract fields
    title = ""
    authors = []
    year = 0
    journal = None
    doi = None
    arxiv_id = None
    
    for line in lines[1:]:
        line = line.strip().rstrip(',')
        if '=' in line:
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip().strip('{}').strip('"')
            
            if key == 'title':
                title = value
            elif key == 'author':
                authors = [a.strip() for a in value.split(' and ')]
            elif key == 'year':
                try:
                    year = int(value)
                except ValueError:
                    pass
            elif key == 'journal':
                journal = value
            elif key == 'doi':
                doi = value
            elif key == 'eprint':
                arxiv_id = value
                
    if not all([citekey, title, authors, year]):
        return None
        
    return Citation(
        citekey=citekey,
        title=title,
        authors=authors,
        year=year,
        journal=journal,
        doi=doi,
        arxiv_id=arxiv_id,
        bibtex_entry=bibtex_entry
    )
