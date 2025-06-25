#!/usr/bin/env python3
"""
Test Performance Requirements

Tests for NFR-Perf-1 through NFR-Perf-4 requirements:
- 30-second generation time
- Support for 100+ applications per day
- 10-second AI generation time
- 5-second PDF conversion time
"""

import os
import time
import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add src to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from bewerbung_generator import BewerbungGenerator
from pdf_generator import PDFGenerator
from ai_client_factory import AIClientFactory


class TestPerformanceRequirements:
    
    def setup_method(self):
        """Set up test environment"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.profil_dir = self.test_dir / "profil"
        self.stellen_dir = self.test_dir / "Stellenbeschreibung"
        self.ausgabe_dir = self.test_dir / "Ausgabe"
        
        # Create directories
        self.profil_dir.mkdir(parents=True, exist_ok=True)
        self.stellen_dir.mkdir(parents=True, exist_ok=True)
        self.ausgabe_dir.mkdir(parents=True, exist_ok=True)
        
        # Create test files
        profile_content = "Test profile content"
        job_content = """BWI GmbH
Senior DevOps Engineer (m/w/d)
Reference: 61383
Test job description content for performance testing."""
        
        (self.profil_dir / "20250604_dr_setz.pdf").write_text(profile_content)
        (self.stellen_dir / "20250624_61383_SeniorDevOpsEngineer.txt").write_text(job_content)
        
    def teardown_method(self):
        """Clean up test environment"""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    @pytest.mark.performance
    def test_complete_generation_time_under_30_seconds(self):
        """Test NFR-Perf-1: Complete generation within 30 seconds"""
        generator = BewerbungGenerator(str(self.test_dir))
        
        # Use sample content only for predictable timing
        with patch.dict(os.environ, {'GENERATE_ALL_PROVIDERS': 'false', 'AI_PROVIDER': 'sample'}):
            profile_file = self.profil_dir / "20250604_dr_setz.pdf"
            job_file = self.stellen_dir / "20250624_61383_SeniorDevOpsEngineer.txt"
            
            start_time = time.time()
            
            try:
                # Run complete workflow
                output_dir = generator.create_output_directory(profile_file, job_file)
                markdown_files = generator.generate_application_documents(
                    output_dir, profile_file, job_file, use_cache=False
                )
                pdf_dir = generator.create_pdf_directory(output_dir)
                
                end_time = time.time()
                generation_time = end_time - start_time
                
                # Should complete within 30 seconds (NFR-Perf-1)
                assert generation_time < 30.0, f"Generation took {generation_time:.2f}s, exceeds 30s requirement"
                
                # Log timing for monitoring
                print(f"✅ Complete generation time: {generation_time:.2f}s (target: <30s)")
                
            except Exception as e:
                end_time = time.time()
                generation_time = end_time - start_time
                
                # Even with errors, should fail fast within time limit
                assert generation_time < 30.0, f"Generation failed after {generation_time:.2f}s, exceeds 30s even for failures"
                
                # Re-raise for proper test failure reporting
                raise e
    
    @pytest.mark.performance
    def test_ai_content_generation_time(self):
        """Test NFR-Perf-3: AI content generation within 10 seconds"""
        factory = AIClientFactory(str(self.test_dir))
        
        # Test with sample client (most predictable)
        client = factory._get_fallback_client(use_cache=False)
        
        start_time = time.time()
        
        # Generate AI content
        content = client.generate_all_cover_letter_content(
            job_description="Test job description",
            profile_content="Test profile",
            company_name="Test Company",
            position_title="Test Position"
        )
        
        end_time = time.time()
        ai_generation_time = end_time - start_time
        
        # Should complete within 10 seconds (NFR-Perf-3)
        assert ai_generation_time < 10.0, f"AI generation took {ai_generation_time:.2f}s, exceeds 10s requirement"
        
        # Verify content was generated
        assert isinstance(content, dict)
        assert len(content) > 0
        
        print(f"✅ AI generation time: {ai_generation_time:.2f}s (target: <10s)")
    
    @pytest.mark.performance
    def test_pdf_conversion_time(self):
        """Test NFR-Perf-4: PDF conversion within 5 seconds"""
        pdf_generator = PDFGenerator(str(self.test_dir))
        
        # Create test markdown content
        test_markdown = """# Test Document

## Introduction
This is a test document for PDF generation performance testing.

## Content
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.

### Subsection
More content here to make the document substantial enough for realistic timing.

## Conclusion
End of test document.
"""
        
        output_path = self.test_dir / "test_output.pdf"
        
        start_time = time.time()
        
        try:
            # Convert to PDF
            pdf_generator.markdown_to_pdf(test_markdown, output_path, "Test Document")
            
            end_time = time.time()
            pdf_conversion_time = end_time - start_time
            
            # Should complete within 5 seconds (NFR-Perf-4)
            assert pdf_conversion_time < 5.0, f"PDF conversion took {pdf_conversion_time:.2f}s, exceeds 5s requirement"
            
            # Verify PDF was created
            assert output_path.exists()
            assert output_path.stat().st_size > 0
            
            print(f"✅ PDF conversion time: {pdf_conversion_time:.2f}s (target: <5s)")
            
        except Exception as e:
            end_time = time.time()
            pdf_conversion_time = end_time - start_time
            
            # If WeasyPrint not available, skip this test
            if "WeasyPrint not available" in str(e) or "No module named" in str(e):
                pytest.skip("WeasyPrint not available for PDF generation testing")
            
            # Other failures should still respect timing
            assert pdf_conversion_time < 5.0, f"PDF conversion failed after {pdf_conversion_time:.2f}s"
            raise e
    
    @pytest.mark.performance
    def test_bulk_processing_capability(self):
        """Test NFR-Perf-2: Support for multiple applications (bulk processing simulation)"""
        generator = BewerbungGenerator(str(self.test_dir))
        
        # Create multiple job descriptions for bulk testing
        job_files = []
        for i in range(5):  # Test with 5 applications
            job_content = f"""Company {i+1} GmbH
Test Position {i+1}
Reference: {1000+i}
Job description for position {i+1}."""
            
            job_file = self.stellen_dir / f"20250624_{1000+i}_TestPosition{i+1}.txt"
            job_file.write_text(job_content)
            job_files.append(job_file)
        
        profile_file = self.profil_dir / "20250604_dr_setz.pdf"
        
        # Use sample content for predictable performance
        with patch.dict(os.environ, {'GENERATE_ALL_PROVIDERS': 'false', 'AI_PROVIDER': 'sample'}):
            
            start_time = time.time()
            successful_generations = 0
            
            for job_file in job_files:
                try:
                    output_dir = generator.create_output_directory(profile_file, job_file)
                    markdown_files = generator.generate_application_documents(
                        output_dir, profile_file, job_file, use_cache=False
                    )
                    successful_generations += 1
                    
                except Exception as e:
                    print(f"Failed to generate application for {job_file.name}: {e}")
                    continue
            
            end_time = time.time()
            total_time = end_time - start_time
            
            # Calculate applications per day capability
            if successful_generations > 0:
                avg_time_per_app = total_time / successful_generations
                apps_per_day = (24 * 60 * 60) / avg_time_per_app  # 24 hours in seconds
                
                # Should support 100+ applications per day (NFR-Perf-2)
                assert apps_per_day >= 100, f"Can only process {apps_per_day:.1f} apps/day, need 100+ (avg {avg_time_per_app:.2f}s per app)"
                
                print(f"✅ Bulk processing capability: {apps_per_day:.1f} apps/day (target: 100+)")
                print(f"   Average time per application: {avg_time_per_app:.2f}s")
                print(f"   Successful generations: {successful_generations}/{len(job_files)}")
            else:
                pytest.fail("No successful generations in bulk processing test")
    
    @pytest.mark.performance
    def test_memory_usage_stability(self):
        """Test memory stability during processing - NFR-Perf-2 related"""
        import psutil
        import gc
        
        generator = BewerbungGenerator(str(self.test_dir))
        profile_file = self.profil_dir / "20250604_dr_setz.pdf"
        job_file = self.stellen_dir / "20250624_61383_SeniorDevOpsEngineer.txt"
        
        # Get initial memory usage
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Process multiple applications
        with patch.dict(os.environ, {'GENERATE_ALL_PROVIDERS': 'false', 'AI_PROVIDER': 'sample'}):
            for i in range(3):  # Small number for CI compatibility
                try:
                    output_dir = generator.create_output_directory(profile_file, job_file)
                    # Use unique output directories
                    output_dir = output_dir.parent / f"{output_dir.name}_{i}"
                    output_dir.mkdir(exist_ok=True)
                    
                    markdown_files = generator.generate_application_documents(
                        output_dir, profile_file, job_file, use_cache=False
                    )
                    
                    # Force garbage collection
                    gc.collect()
                    
                except Exception:
                    # Continue with memory test even if generation fails
                    pass
        
        # Check final memory usage
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (less than 100MB for this test)
        assert memory_increase < 100, f"Memory increased by {memory_increase:.1f}MB, possible memory leak"
        
        print(f"✅ Memory usage: {initial_memory:.1f}MB → {final_memory:.1f}MB (+{memory_increase:.1f}MB)")
    
    def test_cache_performance_impact(self):
        """Test performance difference between cached and non-cached generation"""
        factory = AIClientFactory(str(self.test_dir))
        client = factory._get_fallback_client(use_cache=False)
        
        test_params = {
            "job_description": "Test job description",
            "profile_content": "Test profile",
            "company_name": "Test Company",
            "position_title": "Test Position"
        }
        
        # Test without cache (cold start)
        start_time = time.time()
        content1 = client.generate_all_cover_letter_content(**test_params)
        cold_time = time.time() - start_time
        
        # Test with cache (if applicable)
        client_with_cache = factory._get_fallback_client(use_cache=True)
        start_time = time.time()
        content2 = client_with_cache.generate_all_cover_letter_content(**test_params)
        warm_time = time.time() - start_time
        
        print(f"✅ Performance comparison:")
        print(f"   Cold start (no cache): {cold_time:.3f}s")
        print(f"   Warm start (cache): {warm_time:.3f}s")
        
        # Both should be reasonably fast
        assert cold_time < 10.0, f"Cold start too slow: {cold_time:.3f}s"
        assert warm_time < 10.0, f"Warm start too slow: {warm_time:.3f}s"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "performance"])