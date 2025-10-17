"""
Query and Provenance Tracker for Literature Search
Manages search queries, inclusion/exclusion decisions, and provenance
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import json


@dataclass
class SearchQuery:
    """Represents a single search query"""
    query_string: str
    database: str
    timestamp: str
    num_results: int = 0
    included_count: int = 0
    excluded_count: int = 0
    notes: str = ""
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class InclusionDecision:
    """Represents an inclusion/exclusion decision for a paper"""
    citekey: str
    title: str
    decision: str  # "included", "excluded", "pending"
    rationale: str
    criteria_met: List[str]
    criteria_failed: List[str]
    timestamp: str
    reviewed_by: str = "automated"
    
    def to_dict(self) -> Dict:
        return asdict(self)


class ProvenanceTracker:
    """Tracks search queries and inclusion decisions"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.queries: List[SearchQuery] = []
        self.decisions: Dict[str, InclusionDecision] = {}
        
    def add_query(self, query: SearchQuery) -> None:
        """Record a search query"""
        self.queries.append(query)
        
    def add_decision(self, decision: InclusionDecision) -> None:
        """Record an inclusion/exclusion decision"""
        self.decisions[decision.citekey] = decision
        
    def generate_markdown_report(self) -> str:
        """Generate a Markdown report of queries and provenance"""
        lines = ["# Literature Search Queries and Provenance"]
        lines.append("")
        lines.append(f"*Generated: {datetime.utcnow().isoformat()}*")
        lines.append("")
        
        # Inclusion/Exclusion Criteria
        lines.append("## Inclusion/Exclusion Criteria")
        lines.append("")
        
        lines.append("### Inclusion Criteria")
        for criterion in self.config['literature_search']['inclusion_criteria']:
            lines.append(f"- {criterion}")
        lines.append("")
        
        lines.append("### Exclusion Criteria")
        for criterion in self.config['literature_search']['exclusion_criteria']:
            lines.append(f"- {criterion}")
        lines.append("")
        
        # Search Queries
        lines.append("## Search Queries")
        lines.append("")
        
        for i, query in enumerate(self.queries, 1):
            lines.append(f"### Query {i}: {query.database}")
            lines.append("")
            lines.append(f"**Query String:** `{query.query_string}`")
            lines.append("")
            lines.append(f"**Timestamp:** {query.timestamp}")
            lines.append("")
            lines.append(f"**Results:** {query.num_results} total, {query.included_count} included, {query.excluded_count} excluded")
            if query.notes:
                lines.append("")
                lines.append(f"**Notes:** {query.notes}")
            lines.append("")
            
        # Inclusion Decisions Summary
        lines.append("## Inclusion Decisions Summary")
        lines.append("")
        
        included = [d for d in self.decisions.values() if d.decision == "included"]
        excluded = [d for d in self.decisions.values() if d.decision == "excluded"]
        pending = [d for d in self.decisions.values() if d.decision == "pending"]
        
        lines.append(f"- **Total Papers Reviewed:** {len(self.decisions)}")
        lines.append(f"- **Included:** {len(included)}")
        lines.append(f"- **Excluded:** {len(excluded)}")
        lines.append(f"- **Pending Review:** {len(pending)}")
        lines.append("")
        
        # Exclusion Reasons
        if excluded:
            lines.append("### Common Exclusion Reasons")
            lines.append("")
            reason_counts = {}
            for decision in excluded:
                if decision.rationale not in reason_counts:
                    reason_counts[decision.rationale] = 0
                reason_counts[decision.rationale] += 1
                
            for reason, count in sorted(reason_counts.items(), key=lambda x: x[1], reverse=True):
                lines.append(f"- {reason}: {count} papers")
            lines.append("")
            
        return "\n".join(lines)
        
    def save_report(self, filepath: str) -> None:
        """Save provenance report to file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.generate_markdown_report())
            
    def save_json(self, filepath: str) -> None:
        """Save queries and decisions to JSON"""
        data = {
            "queries": [q.to_dict() for q in self.queries],
            "decisions": {k: v.to_dict() for k, v in self.decisions.items()}
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
            
    def load_json(self, filepath: str) -> None:
        """Load queries and decisions from JSON"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            self.queries = [SearchQuery(**q) for q in data.get('queries', [])]
            self.decisions = {
                k: InclusionDecision(**v) 
                for k, v in data.get('decisions', {}).items()
            }
        except FileNotFoundError:
            print(f"Provenance file {filepath} not found")


def create_default_queries(config: Dict) -> List[SearchQuery]:
    """Create default ADS search queries from config"""
    queries = []
    timestamp = datetime.utcnow().isoformat()
    
    for query_string in config['literature_search']['ads_queries']:
        query = SearchQuery(
            query_string=query_string,
            database="NASA/ADS",
            timestamp=timestamp,
            notes="Default query from configuration"
        )
        queries.append(query)
        
    return queries
