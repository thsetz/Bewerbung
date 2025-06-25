"""
Fixed template system tests using conftest fixtures
"""

import sys
import os
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from template_manager import TemplateManager
from pdf_generator import PDFGenerator


def test_template_manager_initialization(test_template_manager):
    """Test template manager initialization with environment override"""
    assert test_template_manager is not None


def test_anschreiben_rendering_with_fixtures(test_template_manager, test_adressat_data, test_ai_content):
    """Test rendering of cover letter template using fixtures"""
    rendered = test_template_manager.render_anschreiben(test_adressat_data, test_ai_content)
    assert isinstance(rendered, str)
    assert len(rendered) > 0
    
    # Check if key content from fixtures is present
    assert 'Max Mustermann' in rendered  # From test_profile_data
    assert 'TechCorp GmbH' in rendered   # From test_adressat_data
    assert 'Senior DevOps Engineer' in rendered  # From test_adressat_data
    assert 'großem Interesse' in rendered  # From test_ai_content


def test_lebenslauf_rendering_with_fixtures(test_template_manager):
    """Test rendering of CV template using fixtures"""
    rendered = test_template_manager.render_lebenslauf()
    assert isinstance(rendered, str)
    assert len(rendered) > 0
    
    # Check if personal data from fixtures is present
    assert 'Max Mustermann' in rendered
    assert 'Berlin' in rendered  # From test_profile_data
    assert 'max.mustermann@example.com' in rendered  # From test_profile_data