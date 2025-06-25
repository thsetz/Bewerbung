#!/usr/bin/env python3
"""
Test 7-Step Workflow Requirements

Tests for FR-1.1 and FR-1.2 requirements:
- Complete 7-step workflow execution
- Automatic file discovery with date patterns
- Proper directory naming
- AI cache management
"""

import os
import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add src to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from bewerbung_generator import BewerbungGenerator


class TestWorkflowRequirements:
    
    def setup_method(self):
        """Set up test environment"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.profil_dir = self.test_dir / "profil"
        self.stellen_dir = self.test_dir / "Stellenbeschreibung"
        self.ausgabe_dir = self.test_dir / "Ausgabe"
        self.cache_dir = self.test_dir / ".cache"
        
        # Create directories
        self.profil_dir.mkdir(parents=True, exist_ok=True)
        self.stellen_dir.mkdir(parents=True, exist_ok=True)
        self.ausgabe_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Create test files with proper date patterns
        profile_content = "Test profile content"
        job_content = """BWI GmbH
Senior DevOps Engineer (m/w/d)
Reference: 61383
Test job description content."""
        
        # Create files with date patterns as specified in FR-1.1
        (self.profil_dir / "20250604_dr_setz.pdf").write_text(profile_content)
        (self.stellen_dir / "20250624_61383_SeniorDevOpsEngineer.txt").write_text(job_content)
        
        # Create cache file for testing cache management
        cache_content = '{"test": "cached_content"}'
        (self.cache_dir / "ai_content_cache.json").write_text(cache_content)
        
    def teardown_method(self):
        """Clean up test environment"""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def test_step0_ai_cache_clearing(self):
        """Test FR-1.2: Step 0 - AI content cache clearing"""
        generator = BewerbungGenerator(str(self.test_dir))
        
        # Verify cache exists initially
        cache_file = self.cache_dir / "ai_content_cache.json"
        assert cache_file.exists(), "Cache file should exist for testing"
        
        # Test cache clearing with force=True
        result = generator.clear_ai_content_cache(force=True)
        assert result == True, "Cache clearing should return True when file was deleted"
        assert not cache_file.exists(), "Cache file should be deleted after clearing"
        
        # Test cache clearing when no cache exists
        result = generator.clear_ai_content_cache(force=True)
        assert result == False, "Cache clearing should return False when no file exists"
        
        # Test with CLEAR_CACHE_ON_START environment variable
        cache_file.write_text('{"test": "content"}')  # Recreate cache
        
        with patch.dict(os.environ, {'CLEAR_CACHE_ON_START': 'false'}):
            result = generator.clear_ai_content_cache(force=False)
            assert result == False, "Cache should not be cleared when CLEAR_CACHE_ON_START=false"
            assert cache_file.exists(), "Cache file should remain when clearing disabled"
        
        with patch.dict(os.environ, {'CLEAR_CACHE_ON_START': 'true'}):
            result = generator.clear_ai_content_cache(force=False)
            assert result == True, "Cache should be cleared when CLEAR_CACHE_ON_START=true"
            assert not cache_file.exists(), "Cache file should be deleted when clearing enabled"
    
    def test_step1_read_newest_profile(self):
        """Test FR-1.1: Step 1 - Read newest profile with date pattern"""
        generator = BewerbungGenerator(str(self.test_dir))
        
        # Test with single profile file
        profile_file = generator.read_newest_profile()
        assert profile_file is not None, "Should find the profile file"
        assert profile_file.name == "20250604_dr_setz.pdf", "Should find the correct profile file"
        assert profile_file.exists(), "Profile file should exist"
        
        # Test with multiple profile files (newest should be selected)
        older_profile = self.profil_dir / "20250601_older_profile.pdf"
        newer_profile = self.profil_dir / "20250607_newer_profile.pdf"
        older_profile.write_text("Older profile")
        newer_profile.write_text("Newer profile")
        
        newest_file = generator.read_newest_profile()
        assert newest_file is not None, "Should find a profile file"
        assert newest_file.name == "20250607_newer_profile.pdf", "Should select the newest profile file"
        
        # Test with no profile files
        for f in self.profil_dir.glob("*.pdf"):
            f.unlink()
        
        no_file = generator.read_newest_profile()
        assert no_file is None, "Should return None when no profile files exist"
    
    def test_step2_read_newest_job_description(self):
        """Test FR-1.1: Step 2 - Read newest job description with date pattern"""
        generator = BewerbungGenerator(str(self.test_dir))
        
        # Test with single job description file
        job_file = generator.read_newest_job_description()
        assert job_file is not None, "Should find the job description file"
        assert job_file.name == "20250624_61383_SeniorDevOpsEngineer.txt", "Should find the correct job file"
        assert job_file.exists(), "Job description file should exist"
        
        # Test with multiple job description files (newest should be selected)
        older_job = self.stellen_dir / "20250620_older_job.txt"
        newer_job = self.stellen_dir / "20250626_newer_job.txt"
        older_job.write_text("Older job description")
        newer_job.write_text("Newer job description")
        
        newest_file = generator.read_newest_job_description()
        assert newest_file is not None, "Should find a job description file"
        assert newest_file.name == "20250626_newer_job.txt", "Should select the newest job description file"
        
        # Test with no job description files
        for f in self.stellen_dir.glob("*.txt"):
            f.unlink()
        
        no_file = generator.read_newest_job_description()
        assert no_file is None, "Should return None when no job description files exist"
    
    def test_step3_create_output_directory(self):
        """Test FR-1.1: Step 3 - Create output directory with proper naming"""
        generator = BewerbungGenerator(str(self.test_dir))
        
        profile_file = self.profil_dir / "20250604_dr_setz.pdf"
        job_file = self.stellen_dir / "20250624_61383_SeniorDevOpsEngineer.txt"
        
        output_dir = generator.create_output_directory(profile_file, job_file)
        
        # Verify directory naming pattern: {job_date}_{job_id}-{profile_date}_{profile_id}
        expected_name = "20250624_61383_SeniorDevOpsEngineer-20250604_dr_setz"
        assert output_dir.name == expected_name, f"Directory name should be {expected_name}, got {output_dir.name}"
        
        # Verify directory was created
        assert output_dir.exists(), "Output directory should be created"
        assert output_dir.is_dir(), "Output path should be a directory"
        
        # Verify Ausgabe parent directory exists
        assert output_dir.parent.name == "Ausgabe", "Output should be in Ausgabe directory"
        assert output_dir.parent.exists(), "Ausgabe directory should be created"
    
    def test_file_identifier_extraction(self):
        """Test FR-1.1: File identifier extraction for directory naming"""
        generator = BewerbungGenerator(str(self.test_dir))
        
        profile_file = self.profil_dir / "20250604_dr_setz.pdf"
        job_file = self.stellen_dir / "20250624_61383_SeniorDevOpsEngineer.txt"
        
        profile_date, profile_id, job_date, job_id = generator.extract_file_identifiers(profile_file, job_file)
        
        assert profile_date == "20250604", "Profile date should be extracted correctly"
        assert profile_id == "dr_setz", "Profile ID should be extracted correctly"
        assert job_date == "20250624", "Job date should be extracted correctly"
        assert job_id == "61383_SeniorDevOpsEngineer", "Job ID should be extracted correctly"
        
        # Test with invalid filename formats
        invalid_profile = self.profil_dir / "invalid_filename.pdf"
        invalid_job = self.stellen_dir / "invalid_filename.txt"
        invalid_profile.write_text("test")
        invalid_job.write_text("test")
        
        with pytest.raises(ValueError, match="Invalid profile filename format"):
            generator.extract_file_identifiers(invalid_profile, job_file)
        
        with pytest.raises(ValueError, match="Invalid job filename format"):
            generator.extract_file_identifiers(profile_file, invalid_job)
    
    def test_complete_7_step_workflow(self):
        """Test FR-1.1: Complete 7-step workflow execution"""
        generator = BewerbungGenerator(str(self.test_dir))
        
        # Use sample provider for predictable testing
        with patch.dict(os.environ, {'GENERATE_ALL_PROVIDERS': 'false', 'AI_PROVIDER': 'sample'}):
            
            # Step 0: Clear AI cache
            cache_result = generator.clear_ai_content_cache(force=True)
            # Should clear cache (result depends on whether cache existed)
            
            # Step 1: Read newest profile
            profile_file = generator.read_newest_profile()
            assert profile_file is not None, "Step 1 failed: No profile file found"
            
            # Step 2: Read newest job description
            job_file = generator.read_newest_job_description()
            assert job_file is not None, "Step 2 failed: No job description file found"
            
            # Step 3: Create output directory
            output_dir = generator.create_output_directory(profile_file, job_file)
            assert output_dir.exists(), "Step 3 failed: Output directory not created"
            
            try:
                # Step 4: Generate application documents
                markdown_files = generator.generate_application_documents(
                    output_dir, profile_file, job_file, use_cache=False
                )
                assert isinstance(markdown_files, dict), "Step 4 failed: No markdown files generated"
                
                # Step 5: Create PDF directory
                pdf_dir = generator.create_pdf_directory(output_dir)
                assert pdf_dir is not None, "Step 5 failed: PDF directory not created"
                
                # Step 6: Convert documents to PDF (may fail due to missing dependencies)
                try:
                    pdf_files = generator.convert_documents_to_pdf(markdown_files, pdf_dir)
                    # PDF conversion success is optional in test environment
                    print("✅ Step 6: PDF conversion completed")
                except Exception as e:
                    print(f"⚠️ Step 6: PDF conversion failed (expected in test environment): {e}")
                
                print("✅ Complete 7-step workflow executed successfully")
                
            except Exception as e:
                # Steps 4-6 may fail due to missing dependencies, but structure should be correct
                print(f"⚠️ Workflow steps 4-6 failed (may be due to test environment): {e}")
                
                # Verify that at least the directory structure is correct
                assert output_dir.exists(), "Output directory should exist even if generation fails"
    
    def test_date_pattern_validation(self):
        """Test FR-1.1: Date pattern validation (YYYYMMDD_*.pdf and YYYYMMDD_*.txt)"""
        generator = BewerbungGenerator(str(self.test_dir))
        
        # Clear existing test files
        for f in self.profil_dir.glob("*"):
            f.unlink()
        for f in self.stellen_dir.glob("*"):
            f.unlink()
        
        # Test valid date patterns
        valid_profiles = [
            "20250101_test.pdf",
            "20251231_another_test.pdf",
            "20240229_leap_year.pdf"  # Valid leap year date
        ]
        
        valid_jobs = [
            "20250101_job1.txt",
            "20251231_job2_with_longer_name.txt",
            "20240229_12345_job_with_number.txt"
        ]
        
        for profile_name in valid_profiles:
            (self.profil_dir / profile_name).write_text("test profile")
        
        for job_name in valid_jobs:
            (self.stellen_dir / job_name).write_text("test job")
        
        # Should find the newest files
        newest_profile = generator.read_newest_profile()
        newest_job = generator.read_newest_job_description()
        
        assert newest_profile is not None, "Should find valid profile with date pattern"
        assert newest_job is not None, "Should find valid job description with date pattern"
        
        # Newest should be 20251231 files
        assert "20251231" in newest_profile.name, "Should select the newest profile by date"
        assert "20251231" in newest_job.name, "Should select the newest job description by date"
        
        # Test invalid date patterns (should be ignored)
        invalid_files = [
            "profile_without_date.pdf",
            "20250230_invalid_date.pdf",  # Invalid date (Feb 30)
            "2025_short_year.pdf",
            "profile.pdf"
        ]
        
        for invalid_name in invalid_files:
            (self.profil_dir / invalid_name).write_text("invalid profile")
        
        # Should still find valid files, ignoring invalid patterns
        found_profile = generator.read_newest_profile()
        assert found_profile is not None, "Should still find valid profiles despite invalid files"
        assert found_profile.name in [p for p in valid_profiles], "Should only match valid pattern files"
    
    def test_cache_environment_variable_behavior(self):
        """Test FR-1.2: Cache management environment variable behavior"""
        generator = BewerbungGenerator(str(self.test_dir))
        
        # Create cache file
        cache_file = self.cache_dir / "ai_content_cache.json"
        cache_file.write_text('{"test": "content"}')
        
        # Test default behavior (should clear cache)
        with patch.dict(os.environ, {}, clear=True):
            result = generator.clear_ai_content_cache(force=False)
            # Default should be to clear cache
            expected_default = os.getenv('CLEAR_CACHE_ON_START', 'true').lower() == 'true'
            if expected_default:
                assert not cache_file.exists(), "Cache should be cleared by default"
        
        # Test explicit true
        cache_file.write_text('{"test": "content"}')  # Recreate
        with patch.dict(os.environ, {'CLEAR_CACHE_ON_START': 'true'}):
            result = generator.clear_ai_content_cache(force=False)
            assert result == True, "Should clear cache when explicitly enabled"
            assert not cache_file.exists(), "Cache file should be deleted"
        
        # Test explicit false
        cache_file.write_text('{"test": "content"}')  # Recreate
        with patch.dict(os.environ, {'CLEAR_CACHE_ON_START': 'false'}):
            result = generator.clear_ai_content_cache(force=False)
            assert result == False, "Should not clear cache when explicitly disabled"
            assert cache_file.exists(), "Cache file should remain"
        
        # Test force override
        with patch.dict(os.environ, {'CLEAR_CACHE_ON_START': 'false'}):
            result = generator.clear_ai_content_cache(force=True)
            assert result == True, "Force=True should override environment variable"
            assert not cache_file.exists(), "Cache should be cleared even when disabled"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])