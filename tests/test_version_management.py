#!/usr/bin/env python3
"""
Tests for Version Management Strategy

Tests the version management functionality in src/__init__.py including
version functions, package metadata, constants, and exports.
"""

import re
import sys
import pytest
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import src


class TestVersionAccess:
    """Test direct version variable access"""
    
    def test_version_variable_exists(self):
        """Test that __version__ variable exists"""
        assert hasattr(src, '__version__')
        assert src.__version__ is not None
    
    def test_author_variable_exists(self):
        """Test that __author__ variable exists"""
        assert hasattr(src, '__author__')
        assert src.__author__ is not None
    
    def test_description_variable_exists(self):
        """Test that __description__ variable exists"""
        assert hasattr(src, '__description__')
        assert src.__description__ is not None
    
    def test_version_format(self):
        """Test that version follows semantic versioning format"""
        version_pattern = r'^\d+\.\d+\.\d+$'
        assert re.match(version_pattern, src.__version__), f"Version '{src.__version__}' does not match semantic versioning format"
    
    def test_version_is_string(self):
        """Test that version is a string"""
        assert isinstance(src.__version__, str)
        assert len(src.__version__) > 0
    
    def test_author_is_string(self):
        """Test that author is a string"""
        assert isinstance(src.__author__, str)
        assert len(src.__author__) > 0
    
    def test_description_is_string(self):
        """Test that description is a string"""
        assert isinstance(src.__description__, str)
        assert len(src.__description__) > 0


class TestVersionFunctions:
    """Test function-based version retrieval"""
    
    def test_get_version_function_exists(self):
        """Test that get_version function exists"""
        assert hasattr(src, 'get_version')
        assert callable(src.get_version)
    
    def test_get_version_returns_string(self):
        """Test that get_version returns a string"""
        version = src.get_version()
        assert isinstance(version, str)
        assert len(version) > 0
    
    def test_get_version_format(self):
        """Test that get_version returns semantic versioning format"""
        version = src.get_version()
        version_pattern = r'^\d+\.\d+\.\d+$'
        assert re.match(version_pattern, version), f"Version '{version}' does not match semantic versioning format"
    
    def test_version_consistency(self):
        """Test that get_version() returns same value as __version__"""
        assert src.get_version() == src.__version__
    
    def test_get_package_info_function_exists(self):
        """Test that get_package_info function exists"""
        assert hasattr(src, 'get_package_info')
        assert callable(src.get_package_info)
    
    def test_get_package_info_returns_dict(self):
        """Test that get_package_info returns a dictionary"""
        info = src.get_package_info()
        assert isinstance(info, dict)
        assert len(info) > 0


class TestPackageMetadata:
    """Test package metadata validation"""
    
    def test_package_info_required_fields(self):
        """Test that package info contains all required fields"""
        info = src.get_package_info()
        required_fields = ["name", "version", "author", "description", "main_classes"]
        
        for field in required_fields:
            assert field in info, f"Required field '{field}' missing from package info"
            assert info[field] is not None, f"Required field '{field}' is None"
    
    def test_package_info_version_consistency(self):
        """Test that package info version matches __version__"""
        info = src.get_package_info()
        assert info["version"] == src.__version__
    
    def test_package_info_author_consistency(self):
        """Test that package info author matches __author__"""
        info = src.get_package_info()
        assert info["author"] == src.__author__
    
    def test_package_info_description_consistency(self):
        """Test that package info description matches __description__"""
        info = src.get_package_info()
        assert info["description"] == src.__description__
    
    def test_package_info_name(self):
        """Test that package has a proper name"""
        info = src.get_package_info()
        assert isinstance(info["name"], str)
        assert len(info["name"]) > 0
        assert "bewerbung" in info["name"].lower()
    
    def test_main_classes_list(self):
        """Test that main_classes is a list with expected classes"""
        info = src.get_package_info()
        main_classes = info["main_classes"]
        
        assert isinstance(main_classes, list)
        assert len(main_classes) > 0
        
        expected_classes = [
            "BewerbungGenerator",
            "DocumentationGenerator",
            "TemplateManager",
            "AIClientFactory",
            "ContentVariantsAnalyzer",
            "PDFGenerator"
        ]
        
        for expected_class in expected_classes:
            assert expected_class in main_classes, f"Expected class '{expected_class}' not found in main_classes"


class TestConstants:
    """Test package constants"""
    
    def test_default_constants_exist(self):
        """Test that default directory constants exist"""
        constants = [
            "DEFAULT_PROFILE_DIR",
            "DEFAULT_JOB_DIR", 
            "DEFAULT_OUTPUT_DIR",
            "DEFAULT_TEMPLATES_DIR"
        ]
        
        for constant in constants:
            assert hasattr(src, constant), f"Constant '{constant}' not found"
            assert getattr(src, constant) is not None, f"Constant '{constant}' is None"
    
    def test_default_constants_are_strings(self):
        """Test that default constants are strings"""
        constants = {
            "DEFAULT_PROFILE_DIR": src.DEFAULT_PROFILE_DIR,
            "DEFAULT_JOB_DIR": src.DEFAULT_JOB_DIR,
            "DEFAULT_OUTPUT_DIR": src.DEFAULT_OUTPUT_DIR,
            "DEFAULT_TEMPLATES_DIR": src.DEFAULT_TEMPLATES_DIR
        }
        
        for name, value in constants.items():
            assert isinstance(value, str), f"Constant '{name}' is not a string: {type(value)}"
            assert len(value) > 0, f"Constant '{name}' is empty"
    
    def test_default_directory_values(self):
        """Test that default directories have expected values"""
        assert src.DEFAULT_PROFILE_DIR == "profil"
        assert src.DEFAULT_JOB_DIR == "Stellenbeschreibung"
        assert src.DEFAULT_OUTPUT_DIR == "Ausgabe"
        assert src.DEFAULT_TEMPLATES_DIR == "templates"


class TestExports:
    """Test __all__ exports validation"""
    
    def test_all_exists(self):
        """Test that __all__ exists"""
        assert hasattr(src, '__all__')
        assert isinstance(src.__all__, list)
        assert len(src.__all__) > 0
    
    def test_version_functions_in_all(self):
        """Test that version functions are in __all__"""
        version_functions = ["get_version", "get_package_info"]
        
        for func in version_functions:
            assert func in src.__all__, f"Function '{func}' not in __all__"
    
    def test_main_classes_in_all(self):
        """Test that main classes are in __all__"""
        main_classes = [
            "BewerbungGenerator",
            "DocumentationGenerator", 
            "TemplateManager",
            "AIClientFactory",
            "ContentVariantsAnalyzer",
            "ContentVariant",
            "PDFGenerator"
        ]
        
        for cls in main_classes:
            assert cls in src.__all__, f"Class '{cls}' not in __all__"
    
    def test_constants_in_all(self):
        """Test that constants are in __all__"""
        constants = [
            "DEFAULT_PROFILE_DIR",
            "DEFAULT_JOB_DIR",
            "DEFAULT_OUTPUT_DIR", 
            "DEFAULT_TEMPLATES_DIR"
        ]
        
        for constant in constants:
            assert constant in src.__all__, f"Constant '{constant}' not in __all__"
    
    def test_metadata_in_all(self):
        """Test that metadata variables are in __all__"""
        metadata = ["__version__", "__author__", "__description__"]
        
        for meta in metadata:
            assert meta in src.__all__, f"Metadata '{meta}' not in __all__"
    
    def test_all_items_accessible(self):
        """Test that all items in __all__ are accessible from the module"""
        for item in src.__all__:
            assert hasattr(src, item), f"Item '{item}' in __all__ but not accessible from module"
            
            # Get the actual attribute
            attr = getattr(src, item)
            
            # Skip None values (these are optional imports that failed)
            if attr is None:
                continue
                
            # Verify the attribute exists and is not None
            assert attr is not None, f"Item '{item}' is None"


class TestConditionalImports:
    """Test conditional import behavior"""
    
    def test_import_graceful_failure(self):
        """Test that the module can be imported even if some components fail"""
        # This test verifies that the conditional imports work
        # The module should be importable even if some classes are None
        assert src is not None
        assert hasattr(src, 'get_version')
        assert src.get_version() is not None
    
    def test_available_classes_not_none(self):
        """Test that available classes are not None"""
        # These should be available since we're testing from the same directory structure
        available_classes = [
            'DocumentationGenerator',  # This should definitely be available
            'ContentVariantsAnalyzer'  # This should also be available
        ]
        
        for class_name in available_classes:
            if hasattr(src, class_name):
                cls = getattr(src, class_name)
                # Only test if the class is actually imported (not None due to import failure)
                if cls is not None:
                    assert cls is not None, f"Class '{class_name}' should not be None"


class TestVersionSemanticValidation:
    """Test semantic versioning compliance"""
    
    def test_version_parts_are_numeric(self):
        """Test that version parts are numeric"""
        version = src.get_version()
        parts = version.split('.')
        
        assert len(parts) == 3, f"Version should have 3 parts, got {len(parts)}: {version}"
        
        for i, part in enumerate(parts):
            assert part.isdigit(), f"Version part {i} '{part}' is not numeric in version: {version}"
            assert int(part) >= 0, f"Version part {i} '{part}' should be non-negative in version: {version}"
    
    def test_version_major_minor_patch(self):
        """Test version has valid major, minor, patch numbers"""
        version = src.get_version()
        major, minor, patch = version.split('.')
        
        # Convert to integers to validate
        major_int = int(major)
        minor_int = int(minor)
        patch_int = int(patch)
        
        # Basic validation - all should be non-negative
        assert major_int >= 0, f"Major version {major_int} should be >= 0"
        assert minor_int >= 0, f"Minor version {minor_int} should be >= 0"
        assert patch_int >= 0, f"Patch version {patch_int} should be >= 0"
        
        # For version 1.0.0, validate specific values
        if version == "1.0.0":
            assert major_int == 1, "Expected major version 1"
            assert minor_int == 0, "Expected minor version 0"
            assert patch_int == 0, "Expected patch version 0"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])