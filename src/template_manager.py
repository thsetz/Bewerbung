#!/usr/bin/env python3
"""
Template Manager - Handles Jinja2 template rendering for application documents
"""

import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from jinja2 import Environment, FileSystemLoader, Template, TemplateNotFound
from dotenv import load_dotenv
import re


class TemplateManager:
    def __init__(self, base_dir: str = ".", env_override: Optional[Dict[str, str]] = None):
        self.base_dir = Path(base_dir)
        self.template_dir = self.base_dir / "Ausgabe" / "templates"
        self.env_file = self.base_dir / ".env"
        self.env_override = env_override or {}
        
        # Load environment variables
        load_dotenv(self.env_file)
        
        # Initialize Jinja2 environment
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            trim_blocks=True,
            lstrip_blocks=True
        )
    
    def get_env_variables(self) -> Dict[str, str]:
        """
        Load all environment variables with ABSENDER_ prefix and general variables
        Keep uppercase naming to match .env file
        """
        variables = {}
        
        # Start with environment variables
        for key, value in os.environ.items():
            if (key.startswith('ABSENDER_') or 
                key.startswith('ADRESSAT_') or 
                key in ['DATUM', 'BERUFSERFAHRUNG', 'AUSBILDUNG', 
                        'FACHKENNTNISSE', 'SPRACHKENNTNISSE', 
                        'ZUSAETZLICHE_QUALIFIKATIONEN', 'INTERESSEN',
                        'STELLE', 'STELLEN_ID']):
                # Keep uppercase for global .env variables
                variables[key] = value
        
        # Override with test data if provided (for testing)
        variables.update(self.env_override)
        
        return variables
    
    def get_template_variables(self, template_name: str) -> List[str]:
        """
        Extract all variables used in a template
        """
        try:
            # Read template file directly to get source content
            template_path = self.template_dir / template_name
            if not template_path.exists():
                print(f"Template {template_name} not found")
                return []
            
            template_source = template_path.read_text(encoding='utf-8')
            
            # Find all {{ variable }} patterns (both uppercase and lowercase)
            variable_pattern = r'\{\{\s*([A-Za-z_][A-Za-z0-9_]*)\s*\}\}'
            variables = re.findall(variable_pattern, template_source)
            return list(set(variables))
        except Exception as e:
            print(f"Error reading template {template_name}: {e}")
            return []
    
    def validate_template(self, template_name: str, variables: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Validate template against provided variables
        Returns dict with 'missing' and 'unused' variable lists
        """
        template_vars = set(self.get_template_variables(template_name))
        provided_vars = set(variables.keys())
        
        missing = list(template_vars - provided_vars)
        unused = list(provided_vars - template_vars)
        
        return {
            'missing': missing,
            'unused': unused,
            'template_vars': list(template_vars),
            'provided_vars': list(provided_vars)
        }
    
    def render_template(self, template_name: str, additional_vars: Optional[Dict[str, Any]] = None) -> str:
        """
        Render a template with environment variables and additional variables
        """
        # Get base variables from .env (uppercase)
        variables = self.get_env_variables()
        
        # Add additional variables if provided (lowercase for dynamic content)
        if additional_vars:
            variables.update(additional_vars)
        
        try:
            template = self.jinja_env.get_template(template_name)
            return template.render(**variables)
        except TemplateNotFound:
            raise FileNotFoundError(f"Template {template_name} not found in {self.template_dir}")
        except Exception as e:
            raise RuntimeError(f"Error rendering template {template_name}: {str(e)}")
    
    def render_anschreiben(self, adressat_vars: Dict[str, Any], ai_content: Optional[Dict[str, Any]] = None) -> str:
        """
        Render cover letter template with addressee and AI-generated content
        adressat_vars: lowercase variables for dynamic content
        ai_content: lowercase variables for AI-generated content
        """
        additional_vars = {}
        
        # Map lowercase adressat variables to uppercase template variables
        variable_mapping = {
            'adressat_unternehmen': 'ADRESSAT_FIRMA',
            'adressat_abteilung': 'ADRESSAT_ABTEILUNG', 
            'adressat_ansprechpartner': 'ADRESSAT_ANSPRECHPARTNER',
            'adressat_strasse': 'ADRESSAT_STRASSE',
            'adressat_hausnummer': 'ADRESSAT_HAUSNUMMER',
            'adressat_plz': 'ADRESSAT_PLZ',
            'adressat_ort': 'ADRESSAT_ORT',
            'position': 'STELLE',
            'referenz_nummer': 'STELLEN_ID'
        }
        
        # Transform adressat variables using mapping
        for key, value in adressat_vars.items():
            if key in variable_mapping:
                additional_vars[variable_mapping[key]] = value
            else:
                additional_vars[key] = value
        
        # Handle combined PLZ_ORT for template
        if 'adressat_plz' in adressat_vars and 'adressat_ort' in adressat_vars:
            additional_vars['ADRESSAT_PLZ_ORT'] = f"{adressat_vars['adressat_plz']} {adressat_vars['adressat_ort']}"
        
        if ai_content:
            additional_vars.update(ai_content)
        
        return self.render_template("anschreiben.md", additional_vars)
    
    def render_lebenslauf(self, ai_content: Optional[Dict[str, Any]] = None) -> str:
        """
        Render CV template with AI-generated content
        ai_content: lowercase variables for AI-generated content
        """
        additional_vars = ai_content or {}
        return self.render_template("lebenslauf.md", additional_vars)
    
    def save_rendered_template(self, content: str, output_path: Path) -> None:
        """
        Save rendered template content to file
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding='utf-8')
        print(f"Saved rendered template to: {output_path}")
    
    def list_templates(self) -> List[str]:
        """
        List all available templates
        """
        if not self.template_dir.exists():
            return []
        
        templates = []
        for file_path in self.template_dir.glob("*.md"):
            templates.append(file_path.name)
        
        return templates
    
    def template_info(self, template_name: str) -> Dict[str, Any]:
        """
        Get information about a template including required variables
        """
        variables = self.get_template_variables(template_name)
        env_vars = self.get_env_variables()
        validation = self.validate_template(template_name, env_vars)
        
        # Separate uppercase (global .env) and lowercase (dynamic) variables
        uppercase_vars = [v for v in variables if v.isupper()]
        lowercase_vars = [v for v in variables if not v.isupper()]
        
        return {
            'name': template_name,
            'all_variables': variables,
            'global_variables': uppercase_vars,
            'dynamic_variables': lowercase_vars,
            'validation': validation,
            'exists': (self.template_dir / template_name).exists()
        }