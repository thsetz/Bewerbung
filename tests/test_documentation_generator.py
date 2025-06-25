#!/usr/bin/env python3
"""
Tests for Documentation Generator

Tests the documentation_generator module including DocumentationGenerator class
and all its methods for README generation, script creation, and system analysis.
"""

import os
import json
import tempfile
import shutil
import platform
import socket
import sys
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from documentation_generator import DocumentationGenerator


class TestDocumentationGenerator:
    """Test DocumentationGenerator class"""
    
    def setup_method(self, method):
        """Set up test environment"""
        self.test_dir = Path(tempfile.mkdtemp(prefix=f"docgen_test_{method.__name__}_"))
        self.generator = DocumentationGenerator(str(self.test_dir))
    
    def teardown_method(self, method):
        """Clean up test environment"""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def create_sample_generation_info(self) -> dict:
        """Create sample generation info data"""
        return {
            "generation_info": {
                "timestamp": "2025-01-01T12:00:00",
                "client_folder": "20250101_12345_JobTitle-20250101_profile",
                "ai_provider": "claude",
                "ai_model": "sonnet-3.5"
            },
            "ai_client_stats": {
                "provider": "claude",
                "model": "sonnet-3.5",
                "available": True,
                "cache_enabled": False
            },
            "generated_content": {
                "einstiegstext_length": 150,
                "einstiegstext_words": 25,
                "fachliche_passung_length": 200,
                "fachliche_passung_words": 35,
                "motivationstext_length": 100,
                "motivationstext_words": 18,
                "mehrwert_length": 180,
                "mehrwert_words": 30,
                "abschlusstext_length": 80,
                "abschlusstext_words": 15,
                "generation_time": "2.5s"
            }
        }
    
    def create_sample_ai_content(self) -> dict:
        """Create sample AI content"""
        return {
            "einstiegstext": "Mit großem Interesse habe ich Ihre Stellenausschreibung gelesen und bewerbe mich hiermit um die Position.",
            "fachliche_passung": "Meine langjährige Erfahrung in der Softwareentwicklung und DevOps macht mich zum idealen Kandidaten für diese Position.",
            "motivationstext": "Besonders reizt mich die Möglichkeit, innovative Lösungen zu entwickeln und mein Wissen zu erweitern.",
            "mehrwert": "Mit meiner Expertise in Cloud-Technologien kann ich Ihre Entwicklungsprozesse optimieren und die Effizienz steigern.",
            "abschlusstext": "Ich freue mich auf ein persönliches Gespräch und die Möglichkeit, mich näher vorstellen zu können."
        }
    
    def test_init_default_base_dir(self):
        """Test DocumentationGenerator initialization with default base directory"""
        generator = DocumentationGenerator()
        assert generator.base_dir == Path(".")
    
    def test_init_custom_base_dir(self):
        """Test DocumentationGenerator initialization with custom base directory"""
        custom_dir = "/custom/path"
        generator = DocumentationGenerator(custom_dir)
        assert generator.base_dir == Path(custom_dir)
    
    def test_init_with_test_dir(self):
        """Test initialization with test directory"""
        assert self.generator.base_dir == self.test_dir


class TestGenerateDocumentation:
    """Test generate_documentation method"""
    
    def setup_method(self, method):
        """Set up test environment"""
        self.test_dir = Path(tempfile.mkdtemp(prefix=f"docgen_test_{method.__name__}_"))
        self.output_dir = self.test_dir / "output"
        self.output_dir.mkdir(parents=True)
        self.generator = DocumentationGenerator(str(self.test_dir))
        
        # Create sample files
        self.profile_file = self.test_dir / "profile.pdf"
        self.profile_file.write_text("sample profile")
        self.job_file = self.test_dir / "job.txt"
        self.job_file.write_text("sample job description")
    
    def teardown_method(self, method):
        """Clean up test environment"""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def test_generate_documentation_complete(self):
        """Test complete documentation generation"""
        generation_info = {
            "generation_info": {
                "timestamp": "2025-01-01T12:00:00",
                "client_folder": "test_output",
                "ai_provider": "claude",
                "ai_model": "sonnet-3.5"
            },
            "ai_client_stats": {
                "provider": "claude",
                "model": "sonnet-3.5",
                "available": True
            },
            "generated_content": {
                "einstiegstext_length": 100,
                "einstiegstext_words": 20,
                "generation_time": "1.5s"
            }
        }
        
        ai_content = {
            "einstiegstext": "Sample introduction text",
            "fachliche_passung": "Sample qualifications text"
        }
        
        # Mock environment variable
        with patch.dict(os.environ, {"GENERATE_REGENERATION_SCRIPTS": "true"}):
            result = self.generator.generate_documentation(
                output_dir=self.output_dir,
                generation_info=generation_info,
                ai_content=ai_content,
                profile_file=self.profile_file,
                job_file=self.job_file
            )
        
        # Verify returned paths
        assert "README.md" in result
        assert "regenerate.sh" in result
        assert "regenerate.bat" in result
        
        # Verify files were created
        assert (self.output_dir / "README.md").exists()
        assert (self.output_dir / "regenerate.sh").exists()
        assert (self.output_dir / "regenerate.bat").exists()
        
        # Verify script permissions
        sh_stat = (self.output_dir / "regenerate.sh").stat()
        assert sh_stat.st_mode & 0o755  # Executable permissions
    
    def test_generate_documentation_no_scripts(self):
        """Test documentation generation without regeneration scripts"""
        generation_info = {"generation_info": {}, "ai_client_stats": {}}
        ai_content = {"einstiegstext": "test"}
        
        with patch.dict(os.environ, {"GENERATE_REGENERATION_SCRIPTS": "false"}):
            result = self.generator.generate_documentation(
                output_dir=self.output_dir,
                generation_info=generation_info,
                ai_content=ai_content,
                profile_file=self.profile_file,
                job_file=self.job_file
            )
        
        # Should only have README
        assert "README.md" in result
        assert "regenerate.sh" not in result
        assert "regenerate.bat" not in result
        
        assert (self.output_dir / "README.md").exists()
        assert not (self.output_dir / "regenerate.sh").exists()
        assert not (self.output_dir / "regenerate.bat").exists()
    
    def test_generate_documentation_default_env(self):
        """Test documentation generation with default environment settings"""
        generation_info = {"generation_info": {}, "ai_client_stats": {}}
        ai_content = {}
        
        # Clear environment variable
        with patch.dict(os.environ, {}, clear=True):
            result = self.generator.generate_documentation(
                output_dir=self.output_dir,
                generation_info=generation_info,
                ai_content=ai_content,
                profile_file=self.profile_file,
                job_file=self.job_file
            )
        
        # Should generate scripts by default (true)
        assert "regenerate.sh" in result
        assert "regenerate.bat" in result


class TestGenerateReadme:
    """Test _generate_readme method"""
    
    def setup_method(self, method):
        """Set up test environment"""
        self.test_dir = Path(tempfile.mkdtemp(prefix=f"readme_test_{method.__name__}_"))
        self.generator = DocumentationGenerator(str(self.test_dir))
        
        self.profile_file = self.test_dir / "20250101_profile.pdf"
        self.job_file = self.test_dir / "20250101_job.txt"
        self.profile_file.write_text("test")
        self.job_file.write_text("test")
    
    def teardown_method(self, method):
        """Clean up test environment"""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    @patch('documentation_generator.DocumentationGenerator._get_system_info')
    def test_generate_readme_basic(self, mock_system_info):
        """Test basic README generation"""
        mock_system_info.return_value = {
            'os': 'Linux 5.4.0',
            'python_version': '3.9.0',
            'hostname': 'test-host',
            'cwd': '/test/path'
        }
        
        generation_info = {
            "generation_info": {
                "timestamp": "2025-01-01T12:00:00",
                "client_folder": "test_folder",
                "ai_provider": "claude",
                "ai_model": "sonnet-3.5"
            },
            "ai_client_stats": {
                "provider": "claude",
                "model": "sonnet-3.5",
                "available": True,
                "cache_enabled": False
            },
            "generated_content": {
                "einstiegstext_length": 100,
                "einstiegstext_words": 20,
                "generation_time": "1.5s"
            }
        }
        
        ai_content = {
            "einstiegstext": "Sample introduction",
            "fachliche_passung": "Sample qualifications"
        }
        
        readme = self.generator._generate_readme(
            generation_info, ai_content, self.profile_file, self.job_file
        )
        
        # Verify README contains expected sections
        assert "# Job Application Generation Report" in readme
        assert "Generated on:" in readme
        assert "AI Provider:" in readme
        assert "claude" in readme
        assert "sonnet-3.5" in readme
        assert "📁 Generated Documents" in readme
        assert "🔄 Reproduction Instructions" in readme
        assert "📊 Input Files Used" in readme
        assert "🤖 AI Content Analysis" in readme
        assert "⚙️ System Requirements" in readme
        assert "🖥️ System Information" in readme
        assert "🔧 Troubleshooting" in readme
        assert "📈 Quality Metrics" in readme
        assert "test-host" in readme  # hostname from mocked system info
    
    @patch('documentation_generator.DocumentationGenerator._get_system_info')
    def test_generate_readme_with_missing_data(self, mock_system_info):
        """Test README generation with missing/empty data"""
        mock_system_info.return_value = {
            'os': 'Unknown',
            'python_version': 'Unknown',
            'hostname': 'Unknown',
            'cwd': 'Unknown'
        }
        
        generation_info = {}
        ai_content = {}
        
        readme = self.generator._generate_readme(
            generation_info, ai_content, self.profile_file, self.job_file
        )
        
        # Should handle missing data gracefully
        assert "**Generated on:** Unknown" in readme
        assert "**AI Provider:** Unknown (Unknown)" in readme
        assert "| **Total** | **0** | **0** |" in readme  # Zero content stats
    
    @patch('documentation_generator.datetime')
    @patch('documentation_generator.DocumentationGenerator._get_system_info')
    def test_generate_readme_timestamp(self, mock_system_info, mock_datetime):
        """Test README generation includes current timestamp"""
        mock_system_info.return_value = {'os': 'Test', 'python_version': '3.9', 'hostname': 'test', 'cwd': '/test'}
        
        # Mock datetime.now()
        mock_now = MagicMock()
        mock_now.strftime.return_value = "2025-01-01 12:00:00"
        mock_datetime.now.return_value = mock_now
        
        generation_info = {"generation_info": {}, "ai_client_stats": {}}
        ai_content = {}
        
        readme = self.generator._generate_readme(
            generation_info, ai_content, self.profile_file, self.job_file
        )
        
        assert "Documentation auto-generated on 2025-01-01 12:00:00" in readme


class TestRegenerationScripts:
    """Test regeneration script generation methods"""
    
    def setup_method(self, method):
        """Set up test environment"""
        self.generator = DocumentationGenerator()
    
    def test_generate_regeneration_script_unix(self):
        """Test Unix regeneration script generation"""
        generation_info = {
            "generation_info": {
                "timestamp": "2025-01-01T12:00:00",
                "ai_provider": "claude",
                "ai_model": "sonnet-3.5"
            },
            "ai_client_stats": {
                "provider": "claude",
                "model": "sonnet-3.5"
            }
        }
        
        script = self.generator._generate_regeneration_script_unix(generation_info)
        
        # Verify script content
        assert "#!/bin/bash" in script
        assert "Auto-generated regeneration script" in script
        assert "2025-01-01T12:00:00" in script
        assert "claude" in script
        assert "sonnet-3.5" in script
        assert "set -e" in script  # Error handling
        assert "source .venv/bin/activate" in script
        assert "pip install -r requirements.txt" in script
        assert "make generate" in script
        assert "export AI_PROVIDER=\"claude\"" in script
        assert "export OUTPUT_STRUCTURE=\"by_model\"" in script
    
    def test_generate_regeneration_script_windows(self):
        """Test Windows regeneration script generation"""
        generation_info = {
            "generation_info": {
                "timestamp": "2025-01-01T12:00:00",
                "ai_provider": "llama", 
                "ai_model": "3.1-8b"
            },
            "ai_client_stats": {
                "provider": "llama",
                "model": "3.1-8b"
            }
        }
        
        script = self.generator._generate_regeneration_script_windows(generation_info)
        
        # Verify script content
        assert "@echo off" in script
        assert "Auto-generated regeneration script" in script
        assert "2025-01-01T12:00:00" in script
        assert "llama" in script
        assert "3.1-8b" in script
        assert "call .venv\\Scripts\\activate.bat" in script
        assert "pip install -r requirements.txt" in script
        assert "make generate" in script
        assert "set AI_PROVIDER=llama" in script
        assert "set OUTPUT_STRUCTURE=by_model" in script
        assert "pause" in script
    
    def test_generate_env_vars_section_claude(self):
        """Test environment variables section for Claude"""
        generation_info = {
            "generation_info": {
                "ai_provider": "claude",
                "ai_model": "sonnet-3.5"
            }
        }
        
        env_vars = self.generator._generate_env_vars_section(generation_info)
        
        assert 'export AI_PROVIDER="claude"' in env_vars
        assert 'export OUTPUT_STRUCTURE="by_model"' in env_vars
        assert 'export INCLUDE_GENERATION_METADATA="true"' in env_vars
        # Should not have LLAMA_MODEL for Claude
        assert "LLAMA_MODEL" not in env_vars
    
    def test_generate_env_vars_section_llama(self):
        """Test environment variables section for Llama"""
        generation_info = {
            "generation_info": {
                "ai_provider": "llama",
                "ai_model": "3.1-8b"
            }
        }
        
        env_vars = self.generator._generate_env_vars_section(generation_info)
        
        assert 'export AI_PROVIDER="llama"' in env_vars
        assert 'export LLAMA_MODEL="3.1-8b"' in env_vars
    
    def test_generate_env_vars_section_windows_llama(self):
        """Test Windows environment variables section for Llama"""
        generation_info = {
            "generation_info": {
                "ai_provider": "llama",
                "ai_model": "3.1-8b"
            }
        }
        
        env_vars = self.generator._generate_env_vars_section_windows(generation_info)
        
        assert "set AI_PROVIDER=llama" in env_vars
        assert "set LLAMA_MODEL=3.1-8b" in env_vars
        assert "set OUTPUT_STRUCTURE=by_model" in env_vars


class TestSystemInformation:
    """Test system information gathering methods"""
    
    def setup_method(self, method):
        """Set up test environment"""
        self.generator = DocumentationGenerator()
    
    @patch('socket.gethostname')
    @patch('sys.version_info')
    @patch('platform.system')
    @patch('platform.release')
    @patch('pathlib.Path.cwd')
    def test_get_system_info(self, mock_cwd, mock_release, mock_system, mock_version, mock_hostname):
        """Test system information gathering"""
        mock_hostname.return_value = "test-host"
        mock_version.major = 3
        mock_version.minor = 9
        mock_version.micro = 0
        mock_system.return_value = "Linux"
        mock_release.return_value = "5.4.0"
        mock_cwd.return_value = Path("/test/path")
        
        info = self.generator._get_system_info()
        
        assert info['os'] == "Linux 5.4.0"
        assert info['python_version'] == "3.9.0"
        assert info['hostname'] == "test-host"
        assert info['cwd'] == "/test/path"
    
    @patch('documentation_generator.platform.system')
    def test_get_system_dependencies_macos(self, mock_system):
        """Test system dependencies for macOS"""
        mock_system.return_value = "Darwin"
        
        deps = self.generator._get_system_dependencies()
        assert deps == "brew install pango"
    
    @patch('documentation_generator.platform.system')
    def test_get_system_dependencies_linux(self, mock_system):
        """Test system dependencies for Linux"""
        mock_system.return_value = "Linux"
        
        deps = self.generator._get_system_dependencies()
        assert deps == "sudo apt-get install libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0"
    
    @patch('documentation_generator.platform.system')
    def test_get_system_dependencies_windows(self, mock_system):
        """Test system dependencies for Windows"""
        mock_system.return_value = "Windows"
        
        deps = self.generator._get_system_dependencies()
        assert deps == "# Windows: Dependencies included with WeasyPrint"
    
    def test_get_ai_provider_setup_claude(self):
        """Test AI provider setup instructions for Claude"""
        setup = self.generator._get_ai_provider_setup("claude")
        
        assert "Claude API Setup:" in setup
        assert "console.anthropic.com" in setup
        assert "ANTHROPIC_API_KEY" in setup
        assert ".env.local" in setup
    
    def test_get_ai_provider_setup_llama(self):
        """Test AI provider setup instructions for Llama"""
        setup = self.generator._get_ai_provider_setup("llama")
        
        assert "Ollama Setup:" in setup
        assert "ollama.ai/install.sh" in setup
        assert "ollama serve" in setup
        assert "ollama pull llama3.2:latest" in setup
    
    def test_get_ai_provider_setup_sample(self):
        """Test AI provider setup instructions for sample content"""
        setup = self.generator._get_ai_provider_setup("sample")
        
        assert "Sample Content:" in setup
        assert "No additional setup required" in setup
    
    def test_get_ai_provider_setup_unknown(self):
        """Test AI provider setup instructions for unknown provider"""
        setup = self.generator._get_ai_provider_setup("unknown_provider")
        
        assert setup == "Unknown AI provider"


class TestContentAnalysis:
    """Test content analysis and utility methods"""
    
    def setup_method(self, method):
        """Set up test environment"""
        self.generator = DocumentationGenerator()
    
    def test_generate_content_table(self):
        """Test content table generation"""
        ai_content = {
            "einstiegstext": "Sample introduction text",
            "fachliche_passung": "Sample qualifications text",
            "motivationstext": "Sample motivation text"
        }
        
        content_info = {
            "einstiegstext_length": 100,
            "einstiegstext_words": 20,
            "fachliche_passung_length": 150,
            "fachliche_passung_words": 25,
            "motivationstext_length": 80,
            "motivationstext_words": 15
        }
        
        table = self.generator._generate_content_table(ai_content, content_info)
        
        # Verify table format
        assert "| Einstiegstext | 100 | 20 | Opening paragraph introducing interest |" in table
        assert "| Fachliche Passung | 150 | 25 | Technical qualifications and experience |" in table
        assert "| Motivationstext | 80 | 15 | Motivation and enthusiasm for role |" in table
    
    def test_generate_content_table_missing_stats(self):
        """Test content table generation with missing statistics"""
        ai_content = {
            "einstiegstext": "Sample text",
            "mehrwert": "Value proposition text"
        }
        
        content_info = {}  # No statistics provided
        
        table = self.generator._generate_content_table(ai_content, content_info)
        
        # Should calculate stats from content
        assert "| Einstiegstext | 11 | 2 |" in table  # len("Sample text") = 11, 2 words
        assert "| Mehrwert | 22 | 3 |" in table  # len("Value proposition text") = 22, 3 words
    
    def test_calculate_completeness_score_full(self):
        """Test completeness score calculation with all sections"""
        ai_content = {
            "einstiegstext": "Introduction",
            "fachliche_passung": "Qualifications", 
            "motivationstext": "Motivation",
            "mehrwert": "Value",
            "abschlusstext": "Closing"
        }
        
        score = self.generator._calculate_completeness_score(ai_content)
        assert score == 100
    
    def test_calculate_completeness_score_partial(self):
        """Test completeness score calculation with partial sections"""
        ai_content = {
            "einstiegstext": "Introduction",
            "motivationstext": "Motivation",
            "abschlusstext": ""  # Empty content should not count
        }
        
        score = self.generator._calculate_completeness_score(ai_content)
        assert score == 40  # 2 out of 5 sections = 40%
    
    def test_calculate_completeness_score_empty(self):
        """Test completeness score calculation with empty content"""
        ai_content = {}
        
        score = self.generator._calculate_completeness_score(ai_content)
        assert score == 0
    
    def test_get_generation_method_ai_available(self):
        """Test generation method determination when AI is available"""
        ai_stats = {"available": True, "cache_enabled": False}
        method = self.generator._get_generation_method(ai_stats)
        assert method == "AI generated (fresh)"
        
        ai_stats = {"available": True, "cache_enabled": True}
        method = self.generator._get_generation_method(ai_stats)
        assert method == "AI generated (may use cache)"
    
    def test_get_generation_method_ai_unavailable(self):
        """Test generation method determination when AI is unavailable"""
        ai_stats = {"available": False}
        method = self.generator._get_generation_method(ai_stats)
        assert method == "Sample content (AI not available)"
    
    def test_is_cached_content(self):
        """Test cached content detection"""
        assert self.generator._is_cached_content({"cache_enabled": True}) == True
        assert self.generator._is_cached_content({"cache_enabled": False}) == False
        assert self.generator._is_cached_content({}) == False
    
    def test_get_env_vars_for_readme_llama(self):
        """Test environment variables for README with Llama"""
        gen_info = {
            "ai_provider": "llama", 
            "ai_model": "3.1-8b"
        }
        
        env_vars = self.generator._get_env_vars_for_readme(gen_info)
        assert 'export LLAMA_MODEL="3.1-8b"' in env_vars
    
    def test_get_env_vars_for_readme_claude(self):
        """Test environment variables for README with Claude"""
        gen_info = {
            "ai_provider": "claude",
            "ai_model": "sonnet-3.5"
        }
        
        env_vars = self.generator._get_env_vars_for_readme(gen_info)
        assert env_vars == "# No additional environment variables needed"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])