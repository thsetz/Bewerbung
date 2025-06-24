#!/usr/bin/env python3
"""
Documentation Generator - Creates comprehensive documentation and regeneration scripts
"""

import os
import json
import subprocess
import platform
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime


class DocumentationGenerator:
    """Generates documentation and regeneration scripts for job application generation"""
    
    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        
    def generate_documentation(self, output_dir: Path, generation_info: Dict[str, Any], 
                             ai_content: Dict[str, str], profile_file: Path, 
                             job_file: Path) -> Dict[str, Path]:
        """Generate complete documentation package"""
        
        generated_docs = {}
        
        # Generate README.md
        readme_path = output_dir / "README.md"
        readme_content = self._generate_readme(generation_info, ai_content, profile_file, job_file)
        readme_path.write_text(readme_content, encoding='utf-8')
        generated_docs['README.md'] = readme_path
        
        # Generate regeneration scripts
        if os.getenv("GENERATE_REGENERATION_SCRIPTS", "true").lower() == "true":
            # Linux/macOS script
            script_sh = output_dir / "regenerate.sh"
            script_content_sh = self._generate_regeneration_script_unix(generation_info)
            script_sh.write_text(script_content_sh, encoding='utf-8')
            script_sh.chmod(0o755)  # Make executable
            generated_docs['regenerate.sh'] = script_sh
            
            # Windows script
            script_bat = output_dir / "regenerate.bat"
            script_content_bat = self._generate_regeneration_script_windows(generation_info)
            script_bat.write_text(script_content_bat, encoding='utf-8')
            generated_docs['regenerate.bat'] = script_bat
        
        return generated_docs
    
    def _generate_readme(self, generation_info: Dict[str, Any], ai_content: Dict[str, str], 
                        profile_file: Path, job_file: Path) -> str:
        """Generate comprehensive README.md content"""
        
        gen_info = generation_info.get("generation_info", {})
        ai_stats = generation_info.get("ai_client_stats", {})
        content_info = generation_info.get("generated_content", {})
        
        # Calculate content statistics
        total_chars = sum(content_info.get(f"{key}_length", 0) for key in ai_content.keys())
        total_words = sum(content_info.get(f"{key}_words", 0) for key in ai_content.keys())
        
        # Get system information
        system_info = self._get_system_info()
        
        readme_content = f"""# Job Application Generation Report

**Generated on:** {gen_info.get('timestamp', 'Unknown')}  
**AI Provider:** {ai_stats.get('provider', 'Unknown')} ({ai_stats.get('model', 'Unknown')})  
**Output Folder:** `{gen_info.get('client_folder', 'Unknown')}`

---

## 📁 Generated Documents

This folder contains a complete German job application generated using AI:

- **📄 anschreiben.md** - Cover letter (Anschreiben)
- **📄 lebenslauf.md** - CV/Resume (Lebenslauf)  
- **📄 anlagen.md** - Attachments list (Anlagen)
- **📁 pdf/** - PDF versions of all documents
- **📊 generation_info.json** - Technical metadata

---

## 🔄 Reproduction Instructions

To regenerate this exact application with the same configuration:

### Quick Start
```bash
# Linux/macOS
./regenerate.sh

# Windows
regenerate.bat
```

### Manual Reproduction
```bash
# Set environment variables
export AI_PROVIDER="{ai_stats.get('provider', 'auto')}"
export OUTPUT_STRUCTURE="by_model"
{self._get_env_vars_for_readme(gen_info)}

# Navigate to project root and run generation
cd {self.base_dir.resolve()}
make generate
```

---

## 📊 Input Files Used

- **Profile:** `{profile_file.name}`
- **Job Description:** `{job_file.name}`
- **Generation Method:** {self._get_generation_method(ai_stats)}

---

## 🤖 AI Content Analysis

| Content Type | Characters | Words | Description |
|--------------|------------|-------|-------------|
{self._generate_content_table(ai_content, content_info)}
| **Total** | **{total_chars:,}** | **{total_words:,}** | **Complete application** |

### Content Quality Indicators
- **AI Provider Available:** {'✅ Yes' if ai_stats.get('available', False) else '❌ No (using fallback)'}
- **Content Cached:** {'✅ Yes (from previous generation)' if self._is_cached_content(ai_stats) else '❌ No (freshly generated)'}
- **Generation Time:** {content_info.get('generation_time', 'Unknown')}

---

## ⚙️ System Requirements

### Required Dependencies
```bash
# Python packages
pip install -r requirements.txt

# System dependencies (for PDF generation)
{self._get_system_dependencies()}
```

### AI Provider Setup
{self._get_ai_provider_setup(ai_stats.get('provider', 'unknown'))}

---

## 🖥️ System Information

- **Operating System:** {system_info.get('os', 'Unknown')}
- **Python Version:** {system_info.get('python_version', 'Unknown')}
- **Generation Host:** {system_info.get('hostname', 'Unknown')}
- **Working Directory:** `{system_info.get('cwd', 'Unknown')}`

---

## 🔧 Troubleshooting

### Common Issues

**AI Provider Not Available**
```bash
# Check AI provider status
make test-providers

# Install missing dependencies
pip install anthropic  # For Claude
# OR install Ollama for local Llama models
```

**PDF Generation Failed**
```bash
# Install system dependencies
# macOS: brew install pango
# Ubuntu: sudo apt-get install libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0
```

**Permission Denied on Scripts**
```bash
# Make regeneration script executable
chmod +x regenerate.sh
```

### Validation
To verify this generation matches the original:
```bash
# Run regeneration test
python tests/test_regeneration.py --target="{gen_info.get('client_folder', 'unknown')}"
```

---

## 📈 Quality Metrics

- **Content Completeness:** {self._calculate_completeness_score(ai_content)}%
- **Template Coverage:** {len(ai_content)}/5 sections generated
- **File Generation:** {'✅ Success' if len(ai_content) > 0 else '❌ Failed'}

---

*Generated by [Bewerbung Generator](https://github.com/thsetz/Bewerbung) v1.0*  
*Documentation auto-generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        return readme_content
    
    def _generate_regeneration_script_unix(self, generation_info: Dict[str, Any]) -> str:
        """Generate Unix/Linux regeneration script"""
        
        gen_info = generation_info.get("generation_info", {})
        ai_stats = generation_info.get("ai_client_stats", {})
        
        script_content = f"""#!/bin/bash
# Auto-generated regeneration script for job application
# Created: {gen_info.get('timestamp', 'Unknown')}
# AI Provider: {ai_stats.get('provider', 'Unknown')} ({ai_stats.get('model', 'Unknown')})

set -e  # Exit on any error

echo "🔄 Regenerating job application with same configuration..."
echo "📊 Original generation: {gen_info.get('timestamp', 'Unknown')}"
echo "🤖 AI Provider: {ai_stats.get('provider', 'Unknown')} ({ai_stats.get('model', 'Unknown')})"

# Color output
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
NC='\\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "Makefile" ] || [ ! -d "src" ]; then
    echo "${{RED}}❌ Error: Not in project root directory${{NC}}"
    echo "Please run this script from the Bewerbung project root"
    exit 1
fi

# Check dependencies
echo "🔍 Checking dependencies..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "${{RED}}❌ Python3 not found${{NC}}"
    exit 1
fi

# Check virtual environment
if [ ! -d ".venv" ]; then
    echo "${{YELLOW}}⚠️  Virtual environment not found, creating one...${{NC}}"
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Set environment variables for exact reproduction
{self._generate_env_vars_section(generation_info)}

# Check AI provider availability
echo "🤖 Checking AI provider availability..."
make test-providers || echo "${{YELLOW}}⚠️  Some AI providers may not be available${{NC}}"

# Run generation
echo "🚀 Starting generation..."
make generate

echo "${{GREEN}}✅ Regeneration completed successfully!${{NC}}"
echo "📁 Check output in: Ausgabe/"
echo "🔍 Compare with original using: python tests/test_regeneration.py"
"""
        
        return script_content
    
    def _generate_regeneration_script_windows(self, generation_info: Dict[str, Any]) -> str:
        """Generate Windows batch regeneration script"""
        
        gen_info = generation_info.get("generation_info", {})
        ai_stats = generation_info.get("ai_client_stats", {})
        
        script_content = f"""@echo off
REM Auto-generated regeneration script for job application
REM Created: {gen_info.get('timestamp', 'Unknown')}
REM AI Provider: {ai_stats.get('provider', 'Unknown')} ({ai_stats.get('model', 'Unknown')})

echo 🔄 Regenerating job application with same configuration...
echo 📊 Original generation: {gen_info.get('timestamp', 'Unknown')}
echo 🤖 AI Provider: {ai_stats.get('provider', 'Unknown')} ({ai_stats.get('model', 'Unknown')})

REM Check if we're in the right directory
if not exist "Makefile" (
    echo ❌ Error: Not in project root directory
    echo Please run this script from the Bewerbung project root
    exit /b 1
)

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found
    exit /b 1
)

REM Check virtual environment
if not exist ".venv" (
    echo ⚠️  Virtual environment not found, creating one...
    python -m venv .venv
)

REM Activate virtual environment
call .venv\\Scripts\\activate.bat

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

REM Set environment variables for exact reproduction
{self._generate_env_vars_section_windows(generation_info)}

REM Run generation
echo 🚀 Starting generation...
make generate

echo ✅ Regeneration completed successfully!
echo 📁 Check output in: Ausgabe/
echo 🔍 Compare with original using: python tests/test_regeneration.py

pause
"""
        
        return script_content
    
    def _generate_env_vars_section(self, generation_info: Dict[str, Any]) -> str:
        """Generate environment variables section for Unix script"""
        ai_stats = generation_info.get("ai_client_stats", {})
        
        env_vars = [
            f'export AI_PROVIDER="{ai_stats.get("provider", "auto")}"',
            'export OUTPUT_STRUCTURE="by_model"',
            'export INCLUDE_GENERATION_METADATA="true"'
        ]
        
        # Add provider-specific variables
        if ai_stats.get("provider") == "llama":
            env_vars.append(f'export LLAMA_MODEL="{ai_stats.get("model", "llama3.2:latest")}"')
        
        return "\n".join(env_vars)
    
    def _generate_env_vars_section_windows(self, generation_info: Dict[str, Any]) -> str:
        """Generate environment variables section for Windows script"""
        ai_stats = generation_info.get("ai_client_stats", {})
        
        env_vars = [
            f'set AI_PROVIDER={ai_stats.get("provider", "auto")}',
            'set OUTPUT_STRUCTURE=by_model',
            'set INCLUDE_GENERATION_METADATA=true'
        ]
        
        # Add provider-specific variables
        if ai_stats.get("provider") == "llama":
            env_vars.append(f'set LLAMA_MODEL={ai_stats.get("model", "llama3.2:latest")}')
        
        return "\n".join(env_vars)
    
    def _generate_content_table(self, ai_content: Dict[str, str], content_info: Dict[str, Any]) -> str:
        """Generate markdown table of content analysis"""
        
        content_descriptions = {
            'einstiegstext': 'Opening paragraph introducing interest',
            'fachliche_passung': 'Technical qualifications and experience',
            'motivationstext': 'Motivation and enthusiasm for role',
            'mehrwert': 'Value proposition and achievements',
            'abschlusstext': 'Professional closing and call to action'
        }
        
        table_rows = []
        for key, content in ai_content.items():
            chars = content_info.get(f"{key}_length", len(content))
            words = content_info.get(f"{key}_words", len(content.split()))
            description = content_descriptions.get(key, 'Generated content section')
            
            table_rows.append(f"| {key.replace('_', ' ').title()} | {chars:,} | {words:,} | {description} |")
        
        return "\n".join(table_rows)
    
    def _get_system_info(self) -> Dict[str, str]:
        """Get system information for documentation"""
        import socket
        import sys
        
        return {
            'os': f"{platform.system()} {platform.release()}",
            'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            'hostname': socket.gethostname(),
            'cwd': str(Path.cwd())
        }
    
    def _get_generation_method(self, ai_stats: Dict[str, Any]) -> str:
        """Determine how content was generated"""
        if not ai_stats.get('available', False):
            return "Sample content (AI not available)"
        elif ai_stats.get('cache_enabled', False):
            return "AI generated (may use cache)"
        else:
            return "AI generated (fresh)"
    
    def _is_cached_content(self, ai_stats: Dict[str, Any]) -> bool:
        """Check if content was likely cached"""
        return ai_stats.get('cache_enabled', False)
    
    def _get_system_dependencies(self) -> str:
        """Get system dependencies based on platform"""
        system = platform.system()
        
        if system == "Darwin":  # macOS
            return "brew install pango"
        elif system == "Linux":
            return "sudo apt-get install libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0"
        else:  # Windows
            return "# Windows: Dependencies included with WeasyPrint"
    
    def _get_ai_provider_setup(self, provider: str) -> str:
        """Get setup instructions for specific AI provider"""
        
        setups = {
            'claude': """**Claude API Setup:**
```bash
# Get API key from https://console.anthropic.com/
# Add to .env.local:
echo "ANTHROPIC_API_KEY=your_api_key_here" >> .env.local
```""",
            
            'llama': """**Ollama Setup:**
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve

# Pull recommended model
ollama pull llama3.2:latest
```""",
            
            'sample': """**Sample Content:**
No additional setup required. Uses built-in sample content."""
        }
        
        return setups.get(provider, "Unknown AI provider")
    
    def _get_env_vars_for_readme(self, gen_info: Dict[str, Any]) -> str:
        """Get environment variables for README reproduction section"""
        env_vars = []
        
        # Add model-specific variables if needed
        model = gen_info.get('ai_model', '')
        if 'llama' in gen_info.get('ai_provider', '').lower():
            env_vars.append(f'export LLAMA_MODEL="{model}"')
        
        if env_vars:
            return "\n".join(env_vars)
        else:
            return "# No additional environment variables needed"
    
    def _calculate_completeness_score(self, ai_content: Dict[str, str]) -> int:
        """Calculate content completeness percentage"""
        expected_sections = ['einstiegstext', 'fachliche_passung', 'motivationstext', 'mehrwert', 'abschlusstext']
        completed_sections = len([key for key in expected_sections if key in ai_content and ai_content[key].strip()])
        
        return int((completed_sections / len(expected_sections)) * 100)