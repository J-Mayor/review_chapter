#!/usr/bin/env python3
"""
Test suite for TF PV Literature Review System
Run all tests to verify system functionality
"""

import os
import sys
from pathlib import Path


def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    try:
        import citation_manager
        import review_generator
        import provenance_tracker
        import survey_tables
        print("  ✓ All modules import successfully")
        return True
    except ImportError as e:
        print(f"  ✗ Import error: {e}")
        return False


def test_config():
    """Test configuration loading"""
    print("Testing configuration...")
    try:
        from review_generator import load_config
        config = load_config('config.yaml')
        
        # Check required keys
        assert 'review' in config
        assert 'authors' in config
        assert 'outputs' in config
        assert 'literature_search' in config
        
        print("  ✓ Configuration loaded successfully")
        print(f"    Title: {config['review']['title']}")
        print(f"    Venue: {config['review']['target_venue']}")
        return True
    except Exception as e:
        print(f"  ✗ Configuration error: {e}")
        return False


def test_citation_manager():
    """Test citation manager functionality"""
    print("Testing citation manager...")
    try:
        from citation_manager import CitationManager, Citation
        from review_generator import load_config
        
        config = load_config('config.yaml')
        manager = CitationManager(config)
        
        # Create test citation
        citation = Citation(
            citekey="test2025paper",
            title="Test Paper",
            authors=["Test Author"],
            year=2025,
            journal="Test Journal"
        )
        
        # Add citation
        manager.add_citation(citation)
        assert len(manager.citations) == 1
        
        # Test deduplication
        duplicate = Citation(
            citekey="test2025duplicate",
            title="Test Paper",  # Same title
            authors=["Test Author"],
            year=2025,
            journal="Test Journal"
        )
        manager.add_citation(duplicate)
        duplicates = manager.deduplicate_citations()
        assert len(duplicates) > 0
        
        print("  ✓ Citation manager working correctly")
        return True
    except Exception as e:
        print(f"  ✗ Citation manager error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_review_generator():
    """Test review document generator"""
    print("Testing review generator...")
    try:
        from review_generator import ReviewDocument, ReviewSection
        from review_generator import load_config
        
        config = load_config('config.yaml')
        doc = ReviewDocument(config)
        
        # Create outline
        doc.create_default_outline()
        assert len(doc.sections) > 0
        
        # Test section creation
        section = ReviewSection("Test Section", level=1)
        section.content = "Test content"
        doc.add_section(section)
        
        # Test LaTeX generation
        latex = doc.to_latex()
        assert "\\documentclass" in latex
        assert "Test Section" in latex
        
        # Test Markdown generation
        md = doc.to_markdown()
        assert "# Test Section" in md
        
        print("  ✓ Review generator working correctly")
        print(f"    Generated {len(doc.sections)} sections")
        return True
    except Exception as e:
        print(f"  ✗ Review generator error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_provenance_tracker():
    """Test provenance tracking"""
    print("Testing provenance tracker...")
    try:
        from provenance_tracker import ProvenanceTracker, SearchQuery, InclusionDecision
        from review_generator import load_config
        from datetime import datetime
        
        config = load_config('config.yaml')
        tracker = ProvenanceTracker(config)
        
        # Add query
        query = SearchQuery(
            query_string="test query",
            database="NASA/ADS",
            timestamp=datetime.utcnow().isoformat(),
            num_results=10
        )
        tracker.add_query(query)
        assert len(tracker.queries) == 1
        
        # Add decision
        decision = InclusionDecision(
            citekey="test2025paper",
            title="Test Paper",
            decision="included",
            rationale="Test rationale",
            criteria_met=["test"],
            criteria_failed=[],
            timestamp=datetime.utcnow().isoformat()
        )
        tracker.add_decision(decision)
        assert len(tracker.decisions) == 1
        
        # Test report generation
        report = tracker.generate_markdown_report()
        assert "test query" in report
        
        print("  ✓ Provenance tracker working correctly")
        return True
    except Exception as e:
        print(f"  ✗ Provenance tracker error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_survey_tables():
    """Test survey table generation"""
    print("Testing survey tables...")
    try:
        from survey_tables import create_default_surveys, generate_survey_comparison_table
        
        surveys = create_default_surveys()
        assert len(surveys) > 0
        
        table = generate_survey_comparison_table(surveys)
        assert "\\begin{table" in table
        assert "SFI" in table or "Cosmicflows" in table
        
        print(f"  ✓ Survey tables working correctly")
        print(f"    Generated table for {len(surveys)} surveys")
        return True
    except Exception as e:
        print(f"  ✗ Survey tables error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_main_script():
    """Test main orchestration script"""
    print("Testing main script...")
    try:
        from main import ReviewOrchestrator
        
        orchestrator = ReviewOrchestrator('config.yaml')
        
        # Check components are initialized
        assert orchestrator.citation_manager is not None
        assert orchestrator.review_doc is not None
        assert orchestrator.provenance_tracker is not None
        
        print("  ✓ Main script working correctly")
        return True
    except Exception as e:
        print(f"  ✗ Main script error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_file_generation():
    """Test that files can be generated"""
    print("Testing file generation...")
    try:
        # Clean up test files
        test_files = [
            'test_review.tex',
            'test_review.md',
            'test_references.bib',
            'test_ledger.json'
        ]
        for f in test_files:
            if Path(f).exists():
                os.remove(f)
        
        from citation_manager import CitationManager, Citation
        from review_generator import ReviewDocument, load_config
        
        config = load_config('config.yaml')
        
        # Generate documents
        doc = ReviewDocument(config)
        doc.create_default_outline()
        doc.set_abstract("Test abstract")
        doc.save_latex('test_review.tex')
        doc.save_markdown('test_review.md')
        
        # Generate bibliography
        manager = CitationManager(config)
        citation = Citation(
            citekey="test2025",
            title="Test",
            authors=["Author"],
            year=2025
        )
        manager.add_citation(citation)
        manager.generate_bibtex('test_references.bib')
        manager.save_to_ledger('test_ledger.json')
        
        # Check files exist
        for f in test_files:
            assert Path(f).exists(), f"File {f} was not created"
        
        print("  ✓ File generation working correctly")
        
        # Clean up
        for f in test_files:
            if Path(f).exists():
                os.remove(f)
        
        return True
    except Exception as e:
        print(f"  ✗ File generation error: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("TF PV Literature Review System - Test Suite")
    print("=" * 60)
    print()
    
    tests = [
        ("Imports", test_imports),
        ("Configuration", test_config),
        ("Citation Manager", test_citation_manager),
        ("Review Generator", test_review_generator),
        ("Provenance Tracker", test_provenance_tracker),
        ("Survey Tables", test_survey_tables),
        ("Main Script", test_main_script),
        ("File Generation", test_file_generation),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"  ✗ Unexpected error in {name}: {e}")
            results.append((name, False))
        print()
    
    # Summary
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print()
    print(f"Total: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print()
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed")
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
