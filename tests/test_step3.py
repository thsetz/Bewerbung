"""
Tests for Step 3: Creating output directory with proper naming pattern
"""

import pytest
import tempfile
import shutil
from pathlib import Path
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from bewerbung_generator import BewerbungGenerator


class TestStep3:
    
    def setup_method(self):
        """Setup test environment with temporary directory"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.ausgabe_dir = self.test_dir / "Ausgabe"
        
    def teardown_method(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir)
    
    def test_extract_file_identifiers(self):
        """Test extracting date and identifier parts from filenames"""
        generator = BewerbungGenerator(str(self.test_dir))
        
        profile_file = Path("20250604_dr_setz.pdf")
        job_file = Path("20250624_61383_SeniorDevOpsEngineer.txt")
        
        profile_date, profile_id, job_date, job_id = generator.extract_file_identifiers(profile_file, job_file)
        
        assert profile_date == "20250604"
        assert profile_id == "dr_setz"
        assert job_date == "20250624"
        assert job_id == "61383_SeniorDevOpsEngineer"
    
    def test_extract_file_identifiers_invalid_profile(self):
        """Test behavior with invalid profile filename"""
        generator = BewerbungGenerator(str(self.test_dir))
        
        profile_file = Path("invalid_profile.pdf")
        job_file = Path("20250624_job.txt")
        
        with pytest.raises(ValueError, match="Invalid profile filename format"):
            generator.extract_file_identifiers(profile_file, job_file)
    
    def test_extract_file_identifiers_invalid_job(self):
        """Test behavior with invalid job filename"""
        generator = BewerbungGenerator(str(self.test_dir))
        
        profile_file = Path("20250604_profile.pdf")
        job_file = Path("invalid_job.txt")
        
        with pytest.raises(ValueError, match="Invalid job filename format"):
            generator.extract_file_identifiers(profile_file, job_file)
    
    def test_create_output_directory_basic(self):
        """Test creating output directory with basic naming"""
        generator = BewerbungGenerator(str(self.test_dir))
        
        profile_file = Path("20250604_dr_setz.pdf")
        job_file = Path("20250624_61383_SeniorDevOpsEngineer.txt")
        
        output_dir = generator.create_output_directory(profile_file, job_file)
        
        expected_name = "20250624_61383_SeniorDevOpsEngineer-20250604_dr_setz"
        expected_path = self.test_dir / "Ausgabe" / expected_name
        
        assert output_dir == expected_path
        assert output_dir.exists()
        assert output_dir.is_dir()
    
    def test_create_output_directory_creates_ausgabe(self):
        """Test that Ausgabe directory is created if it doesn't exist"""
        generator = BewerbungGenerator(str(self.test_dir))
        
        # Ensure Ausgabe directory doesn't exist
        assert not self.ausgabe_dir.exists()
        
        profile_file = Path("20250604_profile.pdf")
        job_file = Path("20250624_job.txt")
        
        output_dir = generator.create_output_directory(profile_file, job_file)
        
        assert self.ausgabe_dir.exists()
        assert output_dir.exists()
    
    def test_create_output_directory_already_exists(self):
        """Test behavior when output directory already exists"""
        generator = BewerbungGenerator(str(self.test_dir))
        
        profile_file = Path("20250604_profile.pdf")
        job_file = Path("20250624_job.txt")
        
        # Create the directory first time
        output_dir1 = generator.create_output_directory(profile_file, job_file)
        
        # Create it again - should not fail
        output_dir2 = generator.create_output_directory(profile_file, job_file)
        
        assert output_dir1 == output_dir2
        assert output_dir1.exists()
    
    def test_create_output_directory_complex_names(self):
        """Test with complex profile and job identifiers"""
        generator = BewerbungGenerator(str(self.test_dir))
        
        profile_file = Path("20250101_john_doe_senior_dev.pdf")
        job_file = Path("20250315_company_xyz_lead_engineer_remote.txt")
        
        output_dir = generator.create_output_directory(profile_file, job_file)
        
        expected_name = "20250315_company_xyz_lead_engineer_remote-20250101_john_doe_senior_dev"
        expected_path = self.test_dir / "Ausgabe" / expected_name
        
        assert output_dir == expected_path
        assert output_dir.exists()