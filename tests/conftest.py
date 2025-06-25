"""
Pytest configuration and shared fixtures for Bewerbung Generator tests
"""

import pytest


# Configure pytest marks
def pytest_configure(config):
    """Configure custom pytest marks"""
    config.addinivalue_line(
        "markers", "performance: mark test as performance test"
    )


@pytest.fixture
def test_profile_data():
    """Test profile data with Max Mustermann"""
    return {
        'ABSENDER_VORNAME': 'Max',
        'ABSENDER_NACHNAME': 'Mustermann',
        'ABSENDER_TITEL': 'Dr.',
        'ABSENDER_STRASSE': 'Musterstraße',
        'ABSENDER_HAUSNUMMER': '123',
        'ABSENDER_PLZ': '12345',
        'ABSENDER_ORT': 'Berlin',
        'ABSENDER_TELEFON': '030 12345678',
        'ABSENDER_MOBIL': '0172 1234567',
        'ABSENDER_EMAIL': 'max.mustermann@example.com',
        'ABSENDER_GEBURTSJAHR': '1985',
        'ABSENDER_STAATSANGEHOERIGKEIT': 'deutsch',
        'DATUM': '24.06.2025',
        'BERUFSERFAHRUNG': 'Senior Software Engineer mit 10 Jahren Erfahrung',
        'AUSBILDUNG': 'Master of Science Informatik, Universität Berlin',
        'FACHKENNTNISSE': 'Python, Java, Docker, Kubernetes, AWS',
        'SPRACHKENNTNISSE': 'Deutsch (Muttersprache), Englisch (verhandlungssicher)',
        'ZUSAETZLICHE_QUALIFIKATIONEN': 'AWS Certified Solutions Architect, Scrum Master',
        'INTERESSEN': 'Open Source Projekte, Technologie-Trends, Sport'
    }


@pytest.fixture
def test_adressat_data():
    """Test addressee data for job applications"""
    return {
        'ADRESSAT_FIRMA': 'TechCorp GmbH',
        'ADRESSAT_ABTEILUNG': 'IT-Abteilung',
        'ADRESSAT_ANSPRECHPARTNER': 'Schmidt',
        'ADRESSAT_STRASSE': 'Hauptstraße 123',
        'ADRESSAT_PLZ_ORT': '10115 Berlin',
        'STELLE': 'Senior DevOps Engineer',
        'STELLEN_ID': 'REF-2025-001',
        'adressat_ansprechpartner_geschlecht': 'männlich',
        'adressat_ansprechpartner_nachname': 'Schmidt'
    }


@pytest.fixture
def test_ai_content():
    """Test AI-generated content sections"""
    return {
        'einstiegstext': 'mit großem Interesse habe ich Ihre Stellenausschreibung gelesen.',
        'fachliche_passung': 'Meine Erfahrung in DevOps macht mich zum idealen Kandidaten.',
        'motivationstext': 'Besonders reizt mich die Möglichkeit, innovative Lösungen zu entwickeln.',
        'mehrwert': 'Mit meiner Expertise kann ich Ihre Prozesse optimieren.',
        'abschlusstext': 'Über ein persönliches Gespräch würde ich mich freuen.'
    }


@pytest.fixture
def isolated_test_environment(test_profile_data, tmp_path):
    """Create isolated test environment with templates and test data"""
    import shutil
    from pathlib import Path
    
    # Create template and CSS directories
    template_dir = tmp_path / "Ausgabe" / "templates"
    css_dir = tmp_path / "Ausgabe" / "css"
    template_dir.mkdir(parents=True)
    css_dir.mkdir(parents=True)
    
    # Copy templates from source
    source_template_dir = Path(__file__).parent.parent / "Ausgabe" / "templates"
    source_css_dir = Path(__file__).parent.parent / "Ausgabe" / "css"
    
    if source_template_dir.exists():
        for template_file in source_template_dir.glob("*.md"):
            shutil.copy2(template_file, template_dir)
    
    if source_css_dir.exists():
        for css_file in source_css_dir.glob("*.css"):
            shutil.copy2(css_file, css_dir)
    
    # Create test .env file with Max Mustermann data
    env_file = tmp_path / ".env"
    env_content = "\n".join([f"{key}={value}" for key, value in test_profile_data.items()])
    env_file.write_text(env_content, encoding='utf-8')
    
    return tmp_path


@pytest.fixture
def test_template_manager(isolated_test_environment, test_profile_data):
    """Create TemplateManager with test environment override"""
    import sys
    import os
    
    # Add src directory to path for imports
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
    
    from template_manager import TemplateManager
    
    # Create TemplateManager with environment override
    return TemplateManager(
        base_dir=str(isolated_test_environment),
        env_override=test_profile_data
    )