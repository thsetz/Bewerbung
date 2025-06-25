#!/usr/bin/env python3
"""
Bewerbung Generator - German Job Application Generation System

A comprehensive system for generating personalized German job applications (Bewerbungen)
using AI-powered content generation. Supports multiple AI providers (Claude, Llama) 
and generates complete application packages including cover letters, CVs, and attachments.

Key Features:
- Multi-provider AI content generation (Claude API, Ollama/Llama, sample content)
- Automated document generation (Markdown and PDF)
- Template-based content rendering
- Comprehensive documentation generation
- Content variants analysis across different AI models
- Robust caching and performance optimization

Main Components:
- BewerbungGenerator: Core application generation workflow
- DocumentationGenerator: README and regeneration script creation
- TemplateManager: Jinja2-based template rendering
- AIClientFactory: Multi-provider AI client management
- ContentVariantsAnalyzer: Analysis of AI-generated content variations
"""

# Version information
__version__ = "1.0.4"
__author__ = "Bewerbung Generator Project"
__description__ = "German Job Application Generation System with AI Support"

# Import main classes for easy access
# Note: Due to current import structure in modules, imports are done conditionally
try:
    from .bewerbung_generator import BewerbungGenerator
except ImportError:
    BewerbungGenerator = None

try:
    from .documentation_generator import DocumentationGenerator  
except ImportError:
    DocumentationGenerator = None

try:
    from .template_manager import TemplateManager
except ImportError:
    TemplateManager = None

try:
    from .ai_client_factory import AIClientFactory
except ImportError:
    AIClientFactory = None

try:
    from .content_variants_analyzer import ContentVariantsAnalyzer, ContentVariant
except ImportError:
    ContentVariantsAnalyzer = None
    ContentVariant = None

try:
    from .pdf_generator import PDFGenerator
except ImportError:
    PDFGenerator = None

# Import AI clients
try:
    from .claude_api_client import ClaudeAPIClient
except ImportError:
    ClaudeAPIClient = None

try:
    from .llama_api_client import LlamaAPIClient
except ImportError:
    LlamaAPIClient = None

try:
    from .base_ai_client import BaseAIClient
except ImportError:
    BaseAIClient = None

def get_version() -> str:
    """
    Get the current version of the Bewerbung Generator package.
    
    Returns:
        str: Version string in semantic versioning format (MAJOR.MINOR.PATCH)
        
    Example:
        >>> from src import get_version
        >>> print(f"Bewerbung Generator v{get_version()}")
        Bewerbung Generator v1.0.0
    """
    return __version__

def get_package_info() -> dict:
    """
    Get comprehensive package information.
    
    Returns:
        dict: Package metadata including version, author, and description
        
    Example:
        >>> from src import get_package_info
        >>> info = get_package_info()
        >>> print(f"{info['description']} v{info['version']}")
        German Job Application Generation System with AI Support v1.0.0
    """
    return {
        "name": "bewerbung-generator",
        "version": __version__,
        "author": __author__,
        "description": __description__,
        "main_classes": [
            "BewerbungGenerator",
            "DocumentationGenerator", 
            "TemplateManager",
            "AIClientFactory",
            "ContentVariantsAnalyzer",
            "PDFGenerator"
        ]
    }

# Package-level constants
DEFAULT_PROFILE_DIR = "profil"
DEFAULT_JOB_DIR = "Stellenbeschreibung"
DEFAULT_OUTPUT_DIR = "Ausgabe"
DEFAULT_TEMPLATES_DIR = "templates"

# Export main components
__all__ = [
    # Version functions
    "get_version",
    "get_package_info",
    
    # Main classes
    "BewerbungGenerator",
    "DocumentationGenerator",
    "TemplateManager", 
    "AIClientFactory",
    "ContentVariantsAnalyzer",
    "ContentVariant",
    "PDFGenerator",
    
    # AI clients
    "ClaudeAPIClient",
    "LlamaAPIClient", 
    "BaseAIClient",
    
    # Constants
    "DEFAULT_PROFILE_DIR",
    "DEFAULT_JOB_DIR",
    "DEFAULT_OUTPUT_DIR",
    "DEFAULT_TEMPLATES_DIR",
    
    # Package metadata
    "__version__",
    "__author__",
    "__description__"
]