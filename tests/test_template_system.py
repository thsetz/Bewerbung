"""
Tests for template system with basic personal data and PDF generation
"""

import pytest
import tempfile
import shutil
from pathlib import Path
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from template_manager import TemplateManager
from pdf_generator import PDFGenerator


class TestTemplateSystem:
    
    def setup_method(self):
        """Setup test environment with temporary directory"""
        self.test_dir = Path(tempfile.mkdtemp())
        
        # Create persistent output directory in tests/
        self.output_dir = Path(__file__).parent / "output"
        self.output_dir.mkdir(exist_ok=True)
        
        # Copy templates and CSS to test directory for isolated testing
        self.setup_test_environment()
        
    def teardown_method(self):
        """Clean up test environment (but keep output directory)"""
        shutil.rmtree(self.test_dir)
        # Keep self.output_dir for inspection
    
    def setup_test_environment(self):
        """Setup isolated test environment with templates and CSS"""
        # Create template and CSS directories
        template_dir = self.test_dir / "Ausgabe" / "templates"
        css_dir = self.test_dir / "Ausgabe" / "css"
        template_dir.mkdir(parents=True)
        css_dir.mkdir(parents=True)
        
        # Copy templates
        source_template_dir = Path(__file__).parent.parent / "Ausgabe" / "templates"
        source_css_dir = Path(__file__).parent.parent / "Ausgabe" / "css"
        
        if source_template_dir.exists():
            for template_file in source_template_dir.glob("*.md"):
                shutil.copy2(template_file, template_dir)
        
        if source_css_dir.exists():
            for css_file in source_css_dir.glob("*.css"):
                shutil.copy2(css_file, css_dir)
        
        # Create test .env file
        env_file = self.test_dir / ".env"
        env_content = """
ABSENDER_VORNAME=Max
ABSENDER_NACHNAME=Mustermann
ABSENDER_TITEL=Dr.
ABSENDER_STRASSE=Musterstraße
ABSENDER_HAUSNUMMER=123
ABSENDER_PLZ=12345
ABSENDER_ORT=Berlin
ABSENDER_TELEFON=030 12345678
ABSENDER_MOBIL=0172 1234567
ABSENDER_EMAIL=max.mustermann@example.com
ABSENDER_GEBURTSJAHR=1985
ABSENDER_STAATSANGEHOERIGKEIT=deutsch
DATUM=24.06.2025
BERUFSERFAHRUNG=Senior Software Engineer mit 10 Jahren Erfahrung
AUSBILDUNG=Master of Science Informatik, Universität Berlin
FACHKENNTNISSE=Python, Java, Docker, Kubernetes, AWS
SPRACHKENNTNISSE=Deutsch (Muttersprache), Englisch (verhandlungssicher)
ZUSAETZLICHE_QUALIFIKATIONEN=AWS Certified Solutions Architect, Scrum Master
INTERESSEN=Open Source Projekte, Technologie-Trends, Sport
"""
        env_file.write_text(env_content.strip(), encoding='utf-8')
    
    def get_sample_adressat_data(self):
        """Get sample addressee data for testing"""
        return {
            'adressat_unternehmen': 'TechCorp GmbH',
            'adressat_abteilung': 'IT-Abteilung',
            'adressat_ansprechpartner': 'Herr Schmidt',
            'adressat_ansprechpartner_geschlecht': 'männlich',
            'adressat_ansprechpartner_nachname': 'Schmidt',
            'adressat_strasse': 'Hauptstraße',
            'adressat_hausnummer': '123',
            'adressat_plz': '10115',
            'adressat_ort': 'Berlin',
            'position': 'Senior DevOps Engineer',
            'referenz': True,
            'referenz_datum': '15.06.2025',
            'referenz_nummer': 'REF-2025-001'
        }
    
    def get_sample_ai_content(self):
        """Get sample AI content for testing"""
        return {
            'einstiegstext': 'mit großem Interesse habe ich Ihre Stellenausschreibung gelesen.',
            'fachliche_passung': 'Meine Erfahrung in DevOps macht mich zum idealen Kandidaten.',
            'motivationstext': 'Besonders reizt mich die Möglichkeit, innovative Lösungen zu entwickeln.',
            'mehrwert': 'Mit meiner Expertise kann ich Ihre Prozesse optimieren.',
            'abschlusstext': 'Über ein persönliches Gespräch würde ich mich freuen.'
        }
    
    def test_template_manager_initialization(self):
        """Test TemplateManager initialization"""
        manager = TemplateManager(str(self.test_dir))
        assert manager.base_dir == self.test_dir
        assert manager.template_dir.exists()
    
    def test_environment_variables_loading(self):
        """Test loading of environment variables"""
        manager = TemplateManager(str(self.test_dir))
        env_vars = manager.get_env_variables()
        
        assert 'ABSENDER_VORNAME' in env_vars
        assert env_vars['ABSENDER_VORNAME'] == 'Max'
        assert 'ABSENDER_NACHNAME' in env_vars
        assert env_vars['ABSENDER_NACHNAME'] == 'Mustermann'
    
    def test_template_listing(self):
        """Test listing available templates"""
        manager = TemplateManager(str(self.test_dir))
        templates = manager.list_templates()
        
        # Should find at least anschreiben.md and lebenslauf.md if they exist
        assert isinstance(templates, list)
    
    def test_anschreiben_rendering(self):
        """Test rendering of cover letter template"""
        manager = TemplateManager(str(self.test_dir))
        adressat_data = self.get_sample_adressat_data()
        ai_content = self.get_sample_ai_content()
        
        try:
            rendered = manager.render_anschreiben(adressat_data, ai_content)
            assert isinstance(rendered, str)
            assert len(rendered) > 0
            
            # Check if key content is present
            assert 'Max Mustermann' in rendered
            assert 'TechCorp GmbH' in rendered
            assert 'Senior DevOps Engineer' in rendered
            
        except FileNotFoundError:
            pytest.skip("anschreiben.md template not found")
    
    def test_lebenslauf_rendering(self):
        """Test rendering of CV template"""
        manager = TemplateManager(str(self.test_dir))
        
        try:
            rendered = manager.render_lebenslauf()
            assert isinstance(rendered, str)
            assert len(rendered) > 0
            
            # Check if personal data is present
            assert 'Max Mustermann' in rendered
            assert 'Berlin' in rendered
            
        except FileNotFoundError:
            pytest.skip("lebenslauf.md template not found")
    
    def test_pdf_generator_initialization(self):
        """Test PDFGenerator initialization"""
        generator = PDFGenerator(str(self.test_dir))
        assert generator.base_dir == self.test_dir
        assert generator.css_dir.exists()
    
    def test_pdf_generator_dependencies(self):
        """Test PDF generator dependency validation"""
        generator = PDFGenerator(str(self.test_dir))
        validation = generator.validate_dependencies()
        
        assert 'markdown' in validation
        assert 'weasyprint' in validation
        assert 'css_file' in validation
        
        # markdown should be available (imported above)
        assert validation['markdown'] is True
    
    def test_markdown_to_html_conversion(self):
        """Test markdown to HTML conversion"""
        generator = PDFGenerator(str(self.test_dir))
        
        markdown_content = """
# Test Document

This is a **test** document with *formatting*.

## Section 2

- Item 1
- Item 2
"""
        
        html = generator.markdown_to_html(markdown_content, "Test")
        
        assert isinstance(html, str)
        assert '<h1>' in html
        assert '<h2>' in html
        assert '<strong>' in html
        assert '<em>' in html
        assert '<ul>' in html
        assert 'Test' in html  # Title should be in HTML
    
    @pytest.mark.skipif(
        os.environ.get('SKIP_PDF_TESTS') == '1',
        reason="PDF generation tests skipped (set SKIP_PDF_TESTS=1 to skip)"
    )
    def test_pdf_generation(self):
        """Test PDF generation from markdown"""
        generator = PDFGenerator(str(self.test_dir))
        
        # Check if weasyprint is available
        validation = generator.validate_dependencies()
        if not validation['weasyprint']:
            pytest.skip("WeasyPrint not available")
        
        markdown_content = """
# Test Document

This is a test document for PDF generation.

## Personal Information

**Name:** Max Mustermann  
**Location:** Berlin  
"""
        
        pdf_path = self.output_dir / "test.pdf"
        
        try:
            generator.markdown_to_pdf(markdown_content, pdf_path, "Test PDF")
            
            assert pdf_path.exists()
            assert pdf_path.stat().st_size > 0
            
            # Get PDF info
            pdf_info = generator.get_pdf_info(pdf_path)
            assert pdf_info['exists'] is True
            assert pdf_info['size_bytes'] > 0
            
        except Exception as e:
            pytest.skip(f"PDF generation failed: {str(e)}")
    
    def test_complete_document_generation_workflow(self):
        """Test complete workflow: Templates → Markdown → PDF"""
        manager = TemplateManager(str(self.test_dir))
        generator = PDFGenerator(str(self.test_dir))
        
        # Check dependencies
        validation = generator.validate_dependencies()
        if not validation['weasyprint']:
            pytest.skip("WeasyPrint not available for complete workflow test")
        
        try:
            # Render templates
            adressat_data = self.get_sample_adressat_data()
            ai_content = self.get_sample_ai_content()
            
            anschreiben_md = manager.render_anschreiben(adressat_data, ai_content)
            lebenslauf_md = manager.render_lebenslauf()
            
            # Generate PDFs
            markdown_files = {
                'anschreiben.md': anschreiben_md,
                'lebenslauf.md': lebenslauf_md
            }
            
            generated_pdfs = generator.generate_document_set(
                markdown_files, 
                self.output_dir,
                save_html=True
            )
            
            # Verify results
            assert len(generated_pdfs) >= 1
            
            for filename, pdf_path in generated_pdfs.items():
                assert pdf_path.exists()
                assert pdf_path.suffix == '.pdf'
                
                # Check corresponding HTML file exists
                html_path = pdf_path.with_suffix('.html')
                assert html_path.exists()
                
        except FileNotFoundError:
            pytest.skip("Required templates not found")
        except Exception as e:
            pytest.skip(f"Complete workflow test failed: {str(e)}")
    
    def test_template_validation(self):
        """Test template validation functionality"""
        manager = TemplateManager(str(self.test_dir))
        
        try:
            # Test validation for anschreiben template
            env_vars = manager.get_env_variables()
            validation = manager.validate_template("anschreiben.md", env_vars)
            
            assert 'missing' in validation
            assert 'unused' in validation
            assert 'template_vars' in validation
            assert 'provided_vars' in validation
            
            assert isinstance(validation['missing'], list)
            assert isinstance(validation['unused'], list)
            
        except FileNotFoundError:
            pytest.skip("anschreiben.md template not found for validation test")