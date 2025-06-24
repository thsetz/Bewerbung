"""
Tests for Step 1: Reading newest profile file from profil/ directory
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


class TestStep1:
    
    def setup_method(self):
        """Setup test environment with temporary directory"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.profil_dir = self.test_dir / "profil"
        self.profil_dir.mkdir(parents=True)
        
    def teardown_method(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir)
    
    def test_read_newest_profile_single_file(self):
        """Test reading profile when only one file exists"""
        # Create a single profile file
        profile_file = self.profil_dir / "20250604_dr_setz.pdf"
        profile_file.touch()
        
        generator = BewerbungGenerator(str(self.test_dir))
        result = generator.read_newest_profile()
        
        assert result is not None
        assert result.name == "20250604_dr_setz.pdf"
    
    def test_read_newest_profile_multiple_files(self):
        """Test reading newest profile when multiple files exist"""
        # Create multiple profile files with different dates
        old_profile = self.profil_dir / "20250601_old_profile.pdf"
        new_profile = self.profil_dir / "20250610_new_profile.pdf"
        middle_profile = self.profil_dir / "20250605_middle_profile.pdf"
        
        old_profile.touch()
        new_profile.touch()
        middle_profile.touch()
        
        generator = BewerbungGenerator(str(self.test_dir))
        result = generator.read_newest_profile()
        
        assert result is not None
        assert result.name == "20250610_new_profile.pdf"
    
    def test_read_newest_profile_no_files(self):
        """Test behavior when no profile files exist"""
        generator = BewerbungGenerator(str(self.test_dir))
        result = generator.read_newest_profile()
        
        assert result is None
    
    def test_read_newest_profile_no_directory(self):
        """Test behavior when profil directory doesn't exist"""
        # Remove the profil directory
        shutil.rmtree(self.profil_dir)
        
        generator = BewerbungGenerator(str(self.test_dir))
        result = generator.read_newest_profile()
        
        assert result is None
    
    def test_read_newest_profile_wrong_format(self):
        """Test that files not matching date pattern are ignored"""
        # Create files with wrong naming pattern
        wrong_file1 = self.profil_dir / "profile.pdf"
        wrong_file2 = self.profil_dir / "2025_profile.pdf"
        correct_file = self.profil_dir / "20250604_correct.pdf"
        
        wrong_file1.touch()
        wrong_file2.touch()
        correct_file.touch()
        
        generator = BewerbungGenerator(str(self.test_dir))
        result = generator.read_newest_profile()
        
        assert result is not None
        assert result.name == "20250604_correct.pdf"
    
    def test_read_newest_profile_non_pdf_ignored(self):
        """Test that non-PDF files are ignored"""
        # Create files with different extensions
        txt_file = self.profil_dir / "20250604_profile.txt"
        pdf_file = self.profil_dir / "20250605_profile.pdf"
        
        txt_file.touch()
        pdf_file.touch()
        
        generator = BewerbungGenerator(str(self.test_dir))
        result = generator.read_newest_profile()
        
        assert result is not None
        assert result.name == "20250605_profile.pdf"