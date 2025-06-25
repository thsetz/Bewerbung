#!/usr/bin/env python3
"""
Tests for Documentation Link Validation

Two-phase testing approach:
Phase 1: Extract all links from GitHub Pages documentation and save to index.links
Phase 2: Test reachability of all discovered links and generate detailed report
"""

import os
import sys
import json
import time
import tempfile
import shutil
import pytest
import requests
from pathlib import Path
from urllib.parse import urljoin, urlparse
from typing import List, Dict, Tuple, Set
from dataclasses import dataclass, asdict
from bs4 import BeautifulSoup
import logging
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@dataclass
class LinkTestResult:
    """Result of testing a single link"""
    url: str
    status_code: int
    response_time: float
    error_message: str = ""
    is_reachable: bool = True
    link_type: str = "unknown"  # internal, external, anchor, resource


@dataclass
class LinkAnalysisReport:
    """Complete report of link analysis and testing"""
    total_links: int
    reachable_links: int
    unreachable_links: int
    internal_links: int
    external_links: int
    anchor_links: int
    resource_links: int
    test_duration: float
    results: List[LinkTestResult]


class DocumentationLinkTester:
    """
    Two-phase documentation link testing system:
    
    Phase 1: Link Discovery
    - Fetch GitHub Pages documentation
    - Extract and categorize all links
    - Save to index.links file
    
    Phase 2: Link Validation  
    - Load links from index.links
    - Test reachability of each link
    - Generate comprehensive report
    """
    
    def __init__(self, base_url: str = "https://thsetz.github.io/Bewerbung/", 
                 output_dir: str = None):
        self.base_url = base_url
        self.index_url = urljoin(base_url, "index.html")
        
        # Set up output directory
        self.output_dir = Path(output_dir) if output_dir else Path(".")
        self.links_file = self.output_dir / "index.links"
        self.report_file = self.output_dir / "link_test_report.json"
        
        # Configure logging
        self.logger = self._setup_logging()
        
        # HTTP session configuration
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; DocumentationLinkTester/1.0)'
        })
        
        # Link categorization patterns
        self.internal_patterns = [
            self.base_url,
            "/Bewerbung/",
            "#"  # Anchor links
        ]
        
        # Request configuration
        self.timeout = 10
        self.max_retries = 2
        self.retry_delay = 1
    
    def _setup_logging(self) -> logging.Logger:
        """Set up logging configuration"""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        
        # Create handler if not exists
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    # Phase 1: Link Discovery
    
    def fetch_documentation_page(self) -> str:
        """Fetch the main documentation page HTML content"""
        self.logger.info(f"Fetching documentation from: {self.index_url}")
        
        try:
            response = self.session.get(self.index_url, timeout=self.timeout)
            response.raise_for_status()
            
            self.logger.info(f"Successfully fetched {len(response.text)} characters")
            return response.text
            
        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch documentation: {e}")
            raise
    
    def extract_links_from_html(self, html_content: str) -> List[str]:
        """Extract all links from HTML content"""
        self.logger.info("Extracting links from HTML content")
        
        soup = BeautifulSoup(html_content, 'html.parser')
        links = []
        
        # Extract href attributes from all anchor tags
        for link_tag in soup.find_all('a', href=True):
            href = link_tag['href'].strip()
            if href:
                links.append(href)
        
        # Also check for links in other elements (like area maps)
        for area_tag in soup.find_all('area', href=True):
            href = area_tag['href'].strip()
            if href:
                links.append(href)
        
        self.logger.info(f"Extracted {len(links)} raw links")
        return links
    
    def filter_and_normalize_links(self, raw_links: List[str]) -> List[str]:
        """Filter and normalize extracted links"""
        self.logger.info("Filtering and normalizing links")
        
        normalized_links = []
        seen_links = set()
        
        for link in raw_links:
            # Skip empty links
            if not link.strip():
                continue
            
            # Normalize relative links to absolute URLs
            if link.startswith('/'):
                # Root-relative link
                normalized = urljoin(self.base_url.rstrip('/'), link)
            elif link.startswith('#'):
                # Anchor link - make it relative to index page
                normalized = self.index_url + link
            elif link.startswith('http'):
                # Already absolute
                normalized = link
            else:
                # Relative link
                normalized = urljoin(self.index_url, link)
            
            # Remove duplicates
            if normalized not in seen_links:
                seen_links.add(normalized)
                normalized_links.append(normalized)
        
        self.logger.info(f"Normalized to {len(normalized_links)} unique links")
        return sorted(normalized_links)
    
    def categorize_link(self, url: str) -> str:
        """Categorize a link as internal, external, anchor, or resource"""
        if url.startswith('#') or '#' in url and url.startswith(self.base_url):
            return "anchor"
        elif any(pattern in url for pattern in self.internal_patterns):
            return "internal"
        elif url.startswith('http'):
            return "external"
        else:
            return "resource"
    
    def save_links_to_file(self, links: List[str]) -> None:
        """Save discovered links to index.links file"""
        self.logger.info(f"Saving {len(links)} links to {self.links_file}")
        
        # Create structured data with metadata
        links_data = {
            "metadata": {
                "source_url": self.index_url,
                "extraction_time": datetime.utcnow().isoformat(),
                "total_links": len(links)
            },
            "links": []
        }
        
        for url in links:
            links_data["links"].append({
                "url": url,
                "type": self.categorize_link(url)
            })
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save as JSON for structured access
        with open(self.links_file, 'w', encoding='utf-8') as f:
            json.dump(links_data, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Links saved to {self.links_file}")
    
    def phase1_extract_links(self) -> List[str]:
        """Execute Phase 1: Complete link extraction workflow"""
        self.logger.info("=== PHASE 1: Link Discovery ===")
        
        # Fetch documentation page
        html_content = self.fetch_documentation_page()
        
        # Extract links
        raw_links = self.extract_links_from_html(html_content)
        
        # Normalize and filter
        normalized_links = self.filter_and_normalize_links(raw_links)
        
        # Save to file
        self.save_links_to_file(normalized_links)
        
        self.logger.info(f"Phase 1 completed. Discovered {len(normalized_links)} links")
        return normalized_links
    
    # Phase 2: Link Validation
    
    def load_links_from_file(self) -> List[Dict]:
        """Load links from index.links file"""
        self.logger.info(f"Loading links from {self.links_file}")
        
        if not self.links_file.exists():
            raise FileNotFoundError(f"Links file not found: {self.links_file}")
        
        with open(self.links_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        links = data.get("links", [])
        self.logger.info(f"Loaded {len(links)} links from file")
        return links
    
    def test_single_link(self, url: str, link_type: str) -> LinkTestResult:
        """Test reachability of a single link"""
        start_time = time.time()
        
        try:
            # Special handling for anchor links
            if link_type == "anchor":
                # For anchor links, test the base page
                base_url = url.split('#')[0] if '#' in url else url
                response = self.session.get(base_url, timeout=self.timeout)
            else:
                response = self.session.get(url, timeout=self.timeout, 
                                         allow_redirects=True)
            
            response_time = time.time() - start_time
            
            # Consider successful status codes
            is_reachable = 200 <= response.status_code < 400
            
            return LinkTestResult(
                url=url,
                status_code=response.status_code,
                response_time=response_time,
                is_reachable=is_reachable,
                link_type=link_type
            )
            
        except requests.RequestException as e:
            response_time = time.time() - start_time
            return LinkTestResult(
                url=url,
                status_code=0,
                response_time=response_time,
                error_message=str(e),
                is_reachable=False,
                link_type=link_type
            )
    
    def test_link_with_retry(self, url: str, link_type: str) -> LinkTestResult:
        """Test link with retry logic"""
        for attempt in range(self.max_retries + 1):
            result = self.test_single_link(url, link_type)
            
            if result.is_reachable or attempt == self.max_retries:
                if attempt > 0:
                    self.logger.info(f"Link succeeded on attempt {attempt + 1}: {url}")
                return result
            
            self.logger.warning(f"Retry {attempt + 1}/{self.max_retries} for {url}")
            time.sleep(self.retry_delay)
        
        return result
    
    def test_all_links(self, links_data: List[Dict]) -> List[LinkTestResult]:
        """Test reachability of all links"""
        self.logger.info(f"Testing reachability of {len(links_data)} links")
        
        results = []
        
        for i, link_info in enumerate(links_data, 1):
            url = link_info["url"]
            link_type = link_info["type"]
            
            self.logger.info(f"[{i}/{len(links_data)}] Testing {link_type} link: {url}")
            
            result = self.test_link_with_retry(url, link_type)
            results.append(result)
            
            # Log result
            status_emoji = "✅" if result.is_reachable else "❌"
            self.logger.info(
                f"{status_emoji} {url} - Status: {result.status_code}, "
                f"Time: {result.response_time:.2f}s"
            )
            
            if not result.is_reachable and result.error_message:
                self.logger.warning(f"Error: {result.error_message}")
        
        return results
    
    def generate_analysis_report(self, results: List[LinkTestResult], 
                               test_duration: float) -> LinkAnalysisReport:
        """Generate comprehensive analysis report"""
        # Calculate statistics
        total_links = len(results)
        reachable_links = sum(1 for r in results if r.is_reachable)
        unreachable_links = total_links - reachable_links
        
        # Count by type
        type_counts = {}
        for result in results:
            type_counts[result.link_type] = type_counts.get(result.link_type, 0) + 1
        
        report = LinkAnalysisReport(
            total_links=total_links,
            reachable_links=reachable_links,
            unreachable_links=unreachable_links,
            internal_links=type_counts.get("internal", 0),
            external_links=type_counts.get("external", 0),
            anchor_links=type_counts.get("anchor", 0),
            resource_links=type_counts.get("resource", 0),
            test_duration=test_duration,
            results=results
        )
        
        return report
    
    def save_report(self, report: LinkAnalysisReport) -> None:
        """Save analysis report to JSON file"""
        self.logger.info(f"Saving report to {self.report_file}")
        
        # Convert to JSON-serializable format
        report_data = asdict(report)
        
        with open(self.report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Report saved to {self.report_file}")
    
    def log_summary(self, report: LinkAnalysisReport) -> None:
        """Log comprehensive test summary"""
        self.logger.info("=== LINK VALIDATION SUMMARY ===")
        self.logger.info(f"Total links tested: {report.total_links}")
        self.logger.info(f"Reachable links: {report.reachable_links}")
        self.logger.info(f"Unreachable links: {report.unreachable_links}")
        self.logger.info(f"Success rate: {(report.reachable_links/report.total_links)*100:.1f}%")
        self.logger.info(f"Test duration: {report.test_duration:.2f} seconds")
        
        self.logger.info("\nLink Type Breakdown:")
        self.logger.info(f"  Internal: {report.internal_links}")
        self.logger.info(f"  External: {report.external_links}")
        self.logger.info(f"  Anchors: {report.anchor_links}")
        self.logger.info(f"  Resources: {report.resource_links}")
        
        # Log failed links
        failed_links = [r for r in report.results if not r.is_reachable]
        if failed_links:
            self.logger.warning(f"\nFailed Links ({len(failed_links)}):")
            for result in failed_links:
                self.logger.warning(f"  ❌ {result.url} - {result.error_message or f'Status: {result.status_code}'}")
    
    def phase2_validate_links(self) -> LinkAnalysisReport:
        """Execute Phase 2: Complete link validation workflow"""
        self.logger.info("=== PHASE 2: Link Validation ===")
        
        start_time = time.time()
        
        # Load links from file
        links_data = self.load_links_from_file()
        
        # Test all links
        results = self.test_all_links(links_data)
        
        # Generate report
        test_duration = time.time() - start_time
        report = self.generate_analysis_report(results, test_duration)
        
        # Save and log results
        self.save_report(report)
        self.log_summary(report)
        
        self.logger.info("Phase 2 completed")
        return report
    
    def run_complete_workflow(self) -> LinkAnalysisReport:
        """Execute both phases: discovery and validation"""
        self.logger.info("=== STARTING COMPLETE LINK VALIDATION WORKFLOW ===")
        
        # Phase 1: Extract links
        self.phase1_extract_links()
        
        # Phase 2: Validate links
        report = self.phase2_validate_links()
        
        self.logger.info("=== WORKFLOW COMPLETED ===")
        return report


class TestDocumentationLinks:
    """Test class for documentation link validation"""
    
    def setup_method(self, method):
        """Set up test environment"""
        self.test_dir = Path(tempfile.mkdtemp(prefix=f"link_test_{method.__name__}_"))
        self.tester = DocumentationLinkTester(output_dir=self.test_dir)
    
    def teardown_method(self, method):
        """Clean up test environment"""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def test_phase1_link_extraction(self):
        """Test Phase 1: Link extraction from documentation"""
        links = self.tester.phase1_extract_links()
        
        # Verify links were extracted
        assert len(links) > 0, "No links were extracted from documentation"
        
        # Verify links file was created
        assert self.tester.links_file.exists(), "Links file was not created"
        
        # Verify file structure
        with open(self.tester.links_file, 'r') as f:
            data = json.load(f)
        
        assert "metadata" in data, "Links file missing metadata"
        assert "links" in data, "Links file missing links array"
        assert len(data["links"]) == len(links), "Link count mismatch"
        
        # Verify link categorization
        link_types = {link["type"] for link in data["links"]}
        expected_types = {"internal", "external", "anchor", "resource"}
        assert link_types.issubset(expected_types), f"Unexpected link types: {link_types - expected_types}"
    
    def test_phase2_link_validation(self):
        """Test Phase 2: Link validation (requires Phase 1 first)"""
        # First run Phase 1
        self.tester.phase1_extract_links()
        
        # Then run Phase 2
        report = self.tester.phase2_validate_links()
        
        # Verify report structure
        assert isinstance(report, LinkAnalysisReport), "Invalid report type"
        assert report.total_links > 0, "No links were tested"
        assert len(report.results) == report.total_links, "Result count mismatch"
        
        # Verify report file was created
        assert self.tester.report_file.exists(), "Report file was not created"
        
        # Verify some links are reachable (documentation should have working links)
        success_rate = (report.reachable_links / report.total_links) * 100
        assert success_rate > 50, f"Success rate too low: {success_rate:.1f}%"
    
    def test_complete_workflow(self):
        """Test complete two-phase workflow"""
        # Run complete workflow
        report = self.tester.run_complete_workflow()
        
        # Verify both files were created
        assert self.tester.links_file.exists(), "Links file not created"
        assert self.tester.report_file.exists(), "Report file not created"
        
        # Verify workflow results
        assert isinstance(report, LinkAnalysisReport), "Invalid report type"
        assert report.total_links > 0, "No links processed"
        
        # Verify reasonable success rate for documentation links
        success_rate = (report.reachable_links / report.total_links) * 100
        assert success_rate > 70, f"Documentation success rate too low: {success_rate:.1f}%"


if __name__ == "__main__":
    # Allow direct execution for manual testing
    import argparse
    
    parser = argparse.ArgumentParser(description="Test documentation links")
    parser.add_argument("--phase", choices=["1", "2", "both"], default="both",
                       help="Which phase to run")
    parser.add_argument("--output-dir", default=".",
                       help="Output directory for files")
    
    args = parser.parse_args()
    
    tester = DocumentationLinkTester(output_dir=args.output_dir)
    
    if args.phase == "1":
        tester.phase1_extract_links()
    elif args.phase == "2":
        tester.phase2_validate_links()
    else:
        tester.run_complete_workflow()