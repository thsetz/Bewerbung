"""
Tests for Step 2: Reading newest job description from Stellenbeschreibung/ directory
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


class TestStep2:
    
    def setup_method(self):
        """Setup test environment with temporary directory"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.stellenbeschreibung_dir = self.test_dir / "Stellenbeschreibung"
        self.stellenbeschreibung_dir.mkdir(parents=True)
        
    def teardown_method(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir)
    
    def test_read_newest_job_description_single_file(self):
        """Test reading job description when only one file exists"""
        # Create a single job description file
        job_file = self.stellenbeschreibung_dir / "20250624_61383_SeniorDevOpsEngineer.txt"
        job_file.write_text("Test job description")
        
        generator = BewerbungGenerator(str(self.test_dir))
        result = generator.read_newest_job_description()
        
        assert result is not None
        assert result.name == "20250624_61383_SeniorDevOpsEngineer.txt"
    
    def test_read_newest_job_description_multiple_files(self):
        """Test reading newest job description when multiple files exist"""
        # Create multiple job description files with different dates
        old_job = self.stellenbeschreibung_dir / "20250601_old_job.txt"
        new_job = self.stellenbeschreibung_dir / "20250630_new_job.txt"
        middle_job = self.stellenbeschreibung_dir / "20250615_middle_job.txt"
        
        old_job.write_text("Old job description")
        new_job.write_text("New job description")
        middle_job.write_text("Middle job description")
        
        generator = BewerbungGenerator(str(self.test_dir))
        result = generator.read_newest_job_description()
        
        assert result is not None
        assert result.name == "20250630_new_job.txt"
    
    def test_read_newest_job_description_no_files(self):
        """Test behavior when no job description files exist"""
        generator = BewerbungGenerator(str(self.test_dir))
        result = generator.read_newest_job_description()
        
        assert result is None
    
    def test_read_newest_job_description_no_directory(self):
        """Test behavior when Stellenbeschreibung directory doesn't exist"""
        # Remove the Stellenbeschreibung directory
        shutil.rmtree(self.stellenbeschreibung_dir)
        
        generator = BewerbungGenerator(str(self.test_dir))
        result = generator.read_newest_job_description()
        
        assert result is None
    
    def test_read_newest_job_description_wrong_format(self):
        """Test that files not matching date pattern are ignored"""
        # Create files with wrong naming pattern
        wrong_file1 = self.stellenbeschreibung_dir / "job.txt"
        wrong_file2 = self.stellenbeschreibung_dir / "2025_job.txt"
        correct_file = self.stellenbeschreibung_dir / "20250624_correct_job.txt"
        
        wrong_file1.write_text("Wrong format job")
        wrong_file2.write_text("Another wrong format job")
        correct_file.write_text("Correct format job")
        
        generator = BewerbungGenerator(str(self.test_dir))
        result = generator.read_newest_job_description()
        
        assert result is not None
        assert result.name == "20250624_correct_job.txt"
    
    def test_read_newest_job_description_non_txt_ignored(self):
        """Test that non-TXT files are ignored"""
        # Create files with different extensions
        pdf_file = self.stellenbeschreibung_dir / "20250624_job.pdf"
        txt_file = self.stellenbeschreibung_dir / "20250625_job.txt"
        
        pdf_file.write_text("PDF job description")
        txt_file.write_text("TXT job description")
        
        generator = BewerbungGenerator(str(self.test_dir))
        result = generator.read_newest_job_description()
        
        assert result is not None
        assert result.name == "20250625_job.txt"