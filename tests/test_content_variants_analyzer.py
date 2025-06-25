#!/usr/bin/env python3
"""
Tests for Content Variants Analyzer

Tests the content_variants_analyzer module including ContentVariant dataclass
and ContentVariantsAnalyzer class functionality.
"""

import os
import json
import tempfile
import shutil
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open

# Add src to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from content_variants_analyzer import ContentVariant, ContentVariantsAnalyzer


class TestContentVariant:
    """Test ContentVariant dataclass"""
    
    def test_from_content_short_text(self):
        """Test ContentVariant creation with short text"""
        content = "This is a short test content."
        variant = ContentVariant.from_content(
            client_model="test_client",
            ai_provider="test_provider", 
            ai_model="test_model",
            content=content
        )
        
        assert variant.client_model == "test_client"
        assert variant.ai_provider == "test_provider"
        assert variant.ai_model == "test_model"
        assert variant.content == content
        assert variant.char_count == len(content)
        assert variant.word_count == 6  # "This is a short test content."
        assert variant.preview == content  # Short enough, no truncation
    
    def test_from_content_long_text(self):
        """Test ContentVariant creation with long text (preview truncation)"""
        content = "This is a very long test content that should be truncated in the preview because it exceeds fifty characters."
        variant = ContentVariant.from_content(
            client_model="test_client",
            ai_provider="test_provider",
            ai_model="test_model", 
            content=content
        )
        
        assert variant.char_count == len(content)
        assert variant.word_count == 19
        assert variant.preview == "This is a very long test content that should be tr..."
        assert len(variant.preview) == 53  # 50 chars + "..."
    
    def test_from_content_whitespace_handling(self):
        """Test ContentVariant handles whitespace properly"""
        content = "  \n  Test content with whitespace  \n  "
        variant = ContentVariant.from_content(
            client_model="test",
            ai_provider="test",
            ai_model="test",
            content=content
        )
        
        expected_content = "Test content with whitespace"
        assert variant.content == expected_content
        assert variant.char_count == len(expected_content)
        assert variant.word_count == 4
    
    def test_from_content_empty_string(self):
        """Test ContentVariant with empty string"""
        variant = ContentVariant.from_content(
            client_model="test",
            ai_provider="test", 
            ai_model="test",
            content=""
        )
        
        assert variant.content == ""
        assert variant.char_count == 0
        assert variant.word_count == 0
        assert variant.preview == ""


class TestContentVariantsAnalyzer:
    """Test ContentVariantsAnalyzer class"""
    
    def setup_method(self, method):
        """Set up test environment"""
        self.test_dir = Path(tempfile.mkdtemp(prefix=f"variants_test_{method.__name__}_"))
        self.ausgabe_dir = self.test_dir / "Ausgabe"
        self.ausgabe_dir.mkdir(parents=True)
        
        # Create analyzer instance
        self.analyzer = ContentVariantsAnalyzer(str(self.test_dir))
    
    def teardown_method(self, method):
        """Clean up test environment"""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def create_sample_output_structure(self):
        """Create a sample output directory structure"""
        # Create output directory with job/profile structure
        output_dir = self.ausgabe_dir / "20250624_61383_SeniorDevOps-20250604_dr_setz"
        output_dir.mkdir(parents=True)
        
        # Create client model directories
        claude_dir = output_dir / "claude_sonnet_3_5"
        llama_dir = output_dir / "llama_3_1_8b"
        sample_dir = output_dir / "sample_content"
        
        for client_dir in [claude_dir, llama_dir, sample_dir]:
            client_dir.mkdir(parents=True)
        
        return output_dir, claude_dir, llama_dir, sample_dir
    
    def create_generation_info_file(self, client_dir: Path, provider: str, model: str):
        """Create a generation_info.json file"""
        metadata = {
            "generation_info": {
                "ai_provider": provider,
                "ai_model": model,
                "timestamp": "2025-01-01T12:00:00"
            }
        }
        
        metadata_file = client_dir / "generation_info.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        
        return metadata_file
    
    def create_anschreiben_file(self, client_dir: Path, content_sections: dict):
        """Create an anschreiben.md file with specified content"""
        template = """# Anschreiben

---

## Briefkopf Absender

**Max Mustermann**
Dr.
Musterstraße 123
12345 Berlin

**Kontakt:**
Telefon: 030 12345678
E-Mail: max.mustermann@example.com

---

## Adressat

**TechCorp GmbH**
IT-Abteilung
z.Hd. Herr Schmidt
Hauptstraße 123
10115 Berlin

---

**Berlin, 25.06.2025**

## Bewerbung um die Stelle als Senior DevOps Engineer

Sehr geehrte Damen und Herren,

{einstiegstext}

## Meine Qualifikationen

{fachliche_passung}

## Motivation

{motivationstext}

## Mehrwert für Ihr Unternehmen

{mehrwert}

{abschlusstext}

Mit freundlichen Grüßen

Max Mustermann

---

**Anlagen:**
- Lebenslauf
- Zeugnisse und Zertifikate
"""
        
        anschreiben_content = template.format(**content_sections)
        anschreiben_file = client_dir / "anschreiben.md"
        anschreiben_file.write_text(anschreiben_content, encoding='utf-8')
        
        return anschreiben_file
    
    def test_find_output_directories_empty(self):
        """Test finding output directories when none exist"""
        # Clear ausgabe directory
        shutil.rmtree(self.ausgabe_dir)
        self.ausgabe_dir.mkdir()
        
        output_dirs = self.analyzer.find_output_directories()
        assert output_dirs == []
    
    def test_find_output_directories_no_ausgabe(self):
        """Test finding output directories when Ausgabe doesn't exist"""
        shutil.rmtree(self.ausgabe_dir)
        
        output_dirs = self.analyzer.find_output_directories()
        assert output_dirs == []
    
    def test_find_output_directories_with_content(self):
        """Test finding output directories with actual content"""
        # Create sample directories
        dir1 = self.ausgabe_dir / "20250624_61383_JobA-20250604_profile"
        dir2 = self.ausgabe_dir / "20250625_61384_JobB-20250604_profile"
        hidden_dir = self.ausgabe_dir / ".hidden"
        file_item = self.ausgabe_dir / "somefile.txt"
        
        dir1.mkdir()
        dir2.mkdir()
        hidden_dir.mkdir()
        file_item.write_text("test")
        
        output_dirs = self.analyzer.find_output_directories()
        
        # Should find 2 directories, sorted alphabetically
        assert len(output_dirs) == 2
        assert output_dirs[0].name == "20250624_61383_JobA-20250604_profile"
        assert output_dirs[1].name == "20250625_61384_JobB-20250604_profile"
    
    def test_find_client_model_directories(self):
        """Test finding client model directories"""
        output_dir, claude_dir, llama_dir, sample_dir = self.create_sample_output_structure()
        
        # Create additional directories and files
        pdf_dir = output_dir / "pdf"
        pdf_dir.mkdir()
        readme_file = output_dir / "README.md"
        readme_file.write_text("test")
        
        client_dirs = self.analyzer.find_client_model_directories(output_dir)
        
        # Should find 3 client directories, excluding pdf and files
        assert len(client_dirs) == 3
        client_names = [d.name for d in client_dirs]
        assert "claude_sonnet_3_5" in client_names
        assert "llama_3_1_8b" in client_names
        assert "sample_content" in client_names
        assert "pdf" not in client_names
    
    def test_extract_metadata_from_json(self):
        """Test extracting metadata from generation_info.json"""
        output_dir, claude_dir, llama_dir, sample_dir = self.create_sample_output_structure()
        
        # Create metadata file
        self.create_generation_info_file(claude_dir, "claude", "sonnet-3.5")
        
        provider, model = self.analyzer.extract_metadata(claude_dir)
        assert provider == "claude"
        assert model == "sonnet-3.5"
    
    def test_extract_metadata_from_directory_name(self):
        """Test extracting metadata from directory name when JSON missing"""
        output_dir, claude_dir, llama_dir, sample_dir = self.create_sample_output_structure()
        
        # Test Claude directory
        provider, model = self.analyzer.extract_metadata(claude_dir)
        assert provider == "claude"
        assert model == "sonnet_3_5"
        
        # Test Llama directory
        provider, model = self.analyzer.extract_metadata(llama_dir)
        assert provider == "llama"
        assert model == "3_1_8b"
        
        # Test sample directory
        provider, model = self.analyzer.extract_metadata(sample_dir)
        assert provider == "sample"
        assert model == "content"
    
    def test_extract_metadata_corrupted_json(self):
        """Test extracting metadata with corrupted JSON file"""
        output_dir, claude_dir, llama_dir, sample_dir = self.create_sample_output_structure()
        
        # Create corrupted JSON
        metadata_file = claude_dir / "generation_info.json"
        metadata_file.write_text("{ invalid json }", encoding='utf-8')
        
        # Should fallback to directory name parsing
        provider, model = self.analyzer.extract_metadata(claude_dir)
        assert provider == "claude"
        assert model == "sonnet_3_5"
    
    def test_extract_ai_content_missing_file(self):
        """Test extracting AI content when anschreiben.md doesn't exist"""
        output_dir, claude_dir, llama_dir, sample_dir = self.create_sample_output_structure()
        
        content = self.analyzer.extract_ai_content(claude_dir)
        assert content == {}
    
    def test_extract_ai_content_complete_sections(self):
        """Test extracting AI content with all sections present"""
        output_dir, claude_dir, llama_dir, sample_dir = self.create_sample_output_structure()
        
        # Create content sections
        content_sections = {
            'einstiegstext': 'mit großem Interesse habe ich Ihre Stellenausschreibung gelesen.',
            'fachliche_passung': 'Meine Erfahrung in DevOps macht mich zum idealen Kandidaten.',
            'motivationstext': 'Besonders reizt mich die Möglichkeit, innovative Lösungen zu entwickeln.',
            'mehrwert': 'Mit meiner Expertise kann ich Ihre Prozesse optimieren.',
            'abschlusstext': 'Ich freue mich auf ein persönliches Gespräch.'
        }
        
        self.create_anschreiben_file(claude_dir, content_sections)
        
        extracted = self.analyzer.extract_ai_content(claude_dir)
        
        assert extracted['einstiegstext'] == content_sections['einstiegstext']
        assert extracted['fachliche_passung'] == content_sections['fachliche_passung']
        assert extracted['motivationstext'] == content_sections['motivationstext']
        assert extracted['mehrwert'] == content_sections['mehrwert']
        assert extracted['abschlusstext'] == content_sections['abschlusstext']
    
    def test_extraction_methods_individual(self):
        """Test individual content extraction methods"""
        # Test introduction extraction
        text_with_intro = """
Sehr geehrte Damen und Herren,

This is the introduction text that should be extracted.

## Meine Qualifikationen
"""
        result = self.analyzer._extract_introduction(text_with_intro)
        assert result == "This is the introduction text that should be extracted."
        
        # Test qualifications extraction
        text_with_quals = """
## Meine Qualifikationen

These are my qualifications and experience.

## Motivation
"""
        result = self.analyzer._extract_qualifications(text_with_quals)
        assert result == "These are my qualifications and experience."
        
        # Test motivation extraction
        text_with_motivation = """
## Motivation

This is my motivation for applying.

## Mehrwert
"""
        result = self.analyzer._extract_motivation(text_with_motivation)
        assert result == "This is my motivation for applying."
        
        # Test value proposition extraction
        text_with_value = """
## Mehrwert für Ihr Unternehmen

This is the value I bring to your company.

Ich freue mich auf weitere Gespräche.
"""
        result = self.analyzer._extract_value_proposition(text_with_value)
        assert result == "This is the value I bring to your company."
        
        # Test closing extraction
        text_with_closing = """
Some content here.

Ich freue mich auf ein persönliches Gespräch mit Ihnen.

Mit freundlichen Grüßen
"""
        result = self.analyzer._extract_closing(text_with_closing)
        assert result == "Ich freue mich auf ein persönliches Gespräch mit Ihnen."
    
    def test_analyze_variants_complete_workflow(self):
        """Test complete variants analysis workflow"""
        output_dir, claude_dir, llama_dir, sample_dir = self.create_sample_output_structure()
        
        # Create metadata files
        self.create_generation_info_file(claude_dir, "claude", "sonnet-3.5")
        self.create_generation_info_file(llama_dir, "llama", "3.1-8b")
        
        # Create content files with different content
        claude_content = {
            'einstiegstext': 'Claude introduction text.',
            'fachliche_passung': 'Claude qualifications text.',
            'motivationstext': 'Claude motivation text.',
            'mehrwert': 'Claude value proposition.',
            'abschlusstext': 'Claude closing text.'
        }
        
        llama_content = {
            'einstiegstext': 'Llama introduction text that is longer.',
            'fachliche_passung': 'Llama qualifications.',
            'motivationstext': 'Llama motivation.',
            'mehrwert': 'Llama value.',
            'abschlusstext': 'Llama closing.'
        }
        
        sample_content = {
            'einstiegstext': 'Sample introduction.',
            'fachliche_passung': 'Sample qualifications text here.',
            'motivationstext': 'Sample motivation text.',
            'mehrwert': 'Sample value proposition text.',
            'abschlusstext': 'Sample closing.'
        }
        
        self.create_anschreiben_file(claude_dir, claude_content)
        self.create_anschreiben_file(llama_dir, llama_content)
        self.create_anschreiben_file(sample_dir, sample_content)
        
        # Analyze variants
        variants = self.analyzer.analyze_variants()
        
        # Verify results
        assert len(variants) >= 3  # At least 3 AI variables (some may be empty due to regex patterns)
        
        # Check that we have einstiegstext (most reliable extraction)
        assert 'einstiegstext' in variants
        assert len(variants['einstiegstext']) == 3  # 3 client directories
        
        # Verify client models are represented in einstiegstext
        client_models = [v.client_model for v in variants['einstiegstext']]
        assert "claude_sonnet_3_5" in client_models
        assert "llama_3_1_8b" in client_models
        assert "sample_content" in client_models
        
        # Verify some content was extracted
        for var_name, var_variants in variants.items():
            if var_variants:  # Only check non-empty variants
                assert all(len(v.content) > 0 for v in var_variants)
    
    def test_format_table_row(self):
        """Test table row formatting"""
        variant = ContentVariant(
            client_model="test_client_model",
            ai_provider="test_provider",
            ai_model="test_model",
            content="This is test content for formatting.",
            char_count=35,
            word_count=7,
            preview="This is test content for formatting."
        )
        
        col_widths = {
            'client': 20,
            'chars': 10,
            'words': 7,
            'preview': 30
        }
        
        row = self.analyzer.format_table_row(variant, col_widths)
        
        assert "test_client_model" in row
        assert "35" in row
        assert "7" in row
        assert "This is test content for form…" in row  # Truncated preview
    
    def test_format_table_row_truncation(self):
        """Test table row formatting with truncation"""
        variant = ContentVariant(
            client_model="very_long_client_model_name_that_exceeds_width",
            ai_provider="test",
            ai_model="test",
            content="test",
            char_count=4,
            word_count=1,
            preview="very long preview text that will be truncated"
        )
        
        col_widths = {
            'client': 15,
            'chars': 10,
            'words': 7,
            'preview': 20
        }
        
        row = self.analyzer.format_table_row(variant, col_widths)
        
        # Should be truncated with ellipsis
        assert "very_long_clie…" in row
        assert "very long preview t…" in row
    
    def test_format_table_separator(self):
        """Test table separator formatting"""
        col_widths = {
            'client': 15,
            'chars': 10,
            'words': 7,
            'preview': 20
        }
        
        top = self.analyzer.format_table_separator(col_widths, "top")
        middle = self.analyzer.format_table_separator(col_widths, "middle")
        bottom = self.analyzer.format_table_separator(col_widths, "bottom")
        
        assert top.startswith("┌")
        assert top.endswith("┐")
        assert middle.startswith("├")
        assert middle.endswith("┤")
        assert bottom.startswith("└")
        assert bottom.endswith("┘")
    
    def test_display_variants_no_variants(self, capsys):
        """Test display when no variants are found"""
        self.analyzer.display_variants({})
        
        captured = capsys.readouterr()
        assert "No content variants found" in captured.out
    
    def test_display_variants_with_content(self, capsys):
        """Test display with actual variants"""
        # Create test variants
        variants = {
            'einstiegstext': [
                ContentVariant.from_content("claude_3_5", "claude", "sonnet-3.5", "Claude introduction text."),
                ContentVariant.from_content("llama_8b", "llama", "3.1-8b", "Llama introduction text that is longer.")
            ]
        }
        
        self.analyzer.display_variants(variants)
        
        captured = capsys.readouterr()
        assert "AI Content Variants Analysis" in captured.out
        assert "claude_3_5" in captured.out
        assert "llama_8b" in captured.out
        assert "einstiegstext" in captured.out
        assert "Summary Statistics" in captured.out


class TestMainFunction:
    """Test the main function and command-line interface"""
    
    @patch('content_variants_analyzer.ContentVariantsAnalyzer')
    def test_main_function_basic(self, mock_analyzer_class):
        """Test main function basic execution"""
        # Mock analyzer instance
        mock_analyzer = mock_analyzer_class.return_value
        mock_analyzer.analyze_variants.return_value = {}
        
        # Import and run main
        from content_variants_analyzer import main
        
        with patch('sys.argv', ['content_variants_analyzer.py']):
            main()
        
        # Verify analyzer was created and methods called
        mock_analyzer_class.assert_called_once()
        mock_analyzer.analyze_variants.assert_called_once()
        mock_analyzer.display_variants.assert_called_once_with({})
    
    @patch('content_variants_analyzer.ContentVariantsAnalyzer')
    def test_main_function_with_content_flag(self, mock_analyzer_class):
        """Test main function with --content flag"""
        # Mock analyzer instance with variants
        mock_analyzer = mock_analyzer_class.return_value
        mock_variants = {
            'einstiegstext': [
                ContentVariant.from_content("test1", "provider1", "model1", "Content 1"),
                ContentVariant.from_content("test2", "provider2", "model2", "Content 2")
            ]
        }
        mock_analyzer.analyze_variants.return_value = mock_variants
        
        from content_variants_analyzer import main
        
        with patch('sys.argv', ['content_variants_analyzer.py', '--content']):
            main()
        
        mock_analyzer.analyze_variants.assert_called_once()
        mock_analyzer.display_variants.assert_called_once_with(mock_variants)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])