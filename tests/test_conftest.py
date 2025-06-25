"""
Test the conftest.py fixtures
"""

def test_profile_data_fixture(test_profile_data):
    """Test that the profile data fixture works"""
    assert test_profile_data['ABSENDER_VORNAME'] == 'Max'
    assert test_profile_data['ABSENDER_NACHNAME'] == 'Mustermann'
    assert test_profile_data['ABSENDER_TITEL'] == 'Dr.'
    assert test_profile_data['ABSENDER_EMAIL'] == 'max.mustermann@example.com'


def test_adressat_data_fixture(test_adressat_data):
    """Test that the addressee data fixture works"""
    assert test_adressat_data['ADRESSAT_FIRMA'] == 'TechCorp GmbH'
    assert test_adressat_data['ADRESSAT_ANSPRECHPARTNER'] == 'Schmidt'
    assert test_adressat_data['STELLE'] == 'Senior DevOps Engineer'


def test_ai_content_fixture(test_ai_content):
    """Test that the AI content fixture works"""
    assert 'einstiegstext' in test_ai_content
    assert 'fachliche_passung' in test_ai_content
    assert 'motivationstext' in test_ai_content
    assert 'mehrwert' in test_ai_content
    assert 'abschlusstext' in test_ai_content
    assert 'großem Interesse' in test_ai_content['einstiegstext']


def test_isolated_environment_fixture(isolated_test_environment):
    """Test that the isolated test environment fixture works"""
    assert isolated_test_environment.exists()
    assert (isolated_test_environment / "Ausgabe" / "templates").exists()
    assert (isolated_test_environment / ".env").exists()
    
    # Check that test data is in .env file
    env_content = (isolated_test_environment / ".env").read_text()
    assert "ABSENDER_VORNAME=Max" in env_content
    assert "ABSENDER_NACHNAME=Mustermann" in env_content


def test_template_manager_fixture(test_template_manager):
    """Test that the template manager fixture works with environment override"""
    assert test_template_manager is not None
    
    # Test that environment variables are properly overridden
    env_vars = test_template_manager.get_env_variables()
    assert env_vars['ABSENDER_VORNAME'] == 'Max'
    assert env_vars['ABSENDER_NACHNAME'] == 'Mustermann'
    assert env_vars['ABSENDER_EMAIL'] == 'max.mustermann@example.com'