#!/usr/bin/env python3
"""
AI Content Generator - Generates intelligent, personalized content for job applications
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
import json
from dataclasses import dataclass, asdict
from enum import Enum


class ContentType(Enum):
    """Types of AI-generated content"""
    EINSTIEGSTEXT = "einstiegstext"
    FACHLICHE_PASSUNG = "fachliche_passung"
    MOTIVATIONSTEXT = "motivationstext"
    MEHRWERT = "mehrwert"
    ABSCHLUSSTEXT = "abschlusstext"
    BERUFSERFAHRUNG = "berufserfahrung_enhanced"
    AUSBILDUNG = "ausbildung_enhanced"
    FACHKENNTNISSE = "fachkenntnisse_enhanced"


@dataclass
class AIContentRequest:
    """Request structure for AI content generation"""
    content_type: ContentType
    job_description: str
    profile_content: str
    company_name: str
    position_title: str
    additional_context: Optional[Dict[str, Any]] = None


@dataclass
class AIContentResponse:
    """Response structure for AI-generated content"""
    content_type: ContentType
    generated_text: str
    confidence: float
    tokens_used: int
    processing_time: float
    metadata: Optional[Dict[str, Any]] = None


class AIContentVariables:
    """Defines all AI-generated content variables used in templates"""
    
    # Cover Letter (Anschreiben) Variables
    COVER_LETTER_VARIABLES = {
        'einstiegstext': {
            'description': 'Personalized opening paragraph for cover letter',
            'example': 'mit großem Interesse habe ich Ihre Stellenausschreibung gelesen und bewerbe mich hiermit um die Position als Senior DevOps Engineer.',
            'max_length': 300,
            'tone': 'professional, enthusiastic'
        },
        'fachliche_passung': {
            'description': 'Match between candidate skills and job requirements',
            'example': 'Meine langjährige Erfahrung in der Automatisierung von CI/CD-Pipelines und Container-Orchestrierung macht mich zum idealen Kandidaten.',
            'max_length': 500,
            'tone': 'confident, specific'
        },
        'motivationstext': {
            'description': 'Motivation and interest in the specific role/company',
            'example': 'Besonders reizt mich die Möglichkeit, innovative Cloud-Lösungen zu entwickeln und dabei modernste DevOps-Praktiken einzusetzen.',
            'max_length': 400,
            'tone': 'passionate, forward-looking'
        },
        'mehrwert': {
            'description': 'Value proposition - what candidate brings to company',
            'example': 'Mit meiner Expertise kann ich Ihre Entwicklungsprozesse optimieren und die Time-to-Market erheblich verkürzen.',
            'max_length': 300,
            'tone': 'value-focused, results-oriented'
        },
        'abschlusstext': {
            'description': 'Professional closing paragraph',
            'example': 'Über die Möglichkeit eines persönlichen Gesprächs würde ich mich sehr freuen.',
            'max_length': 150,
            'tone': 'polite, professional'
        }
    }
    
    # CV (Lebenslauf) Enhancement Variables
    CV_VARIABLES = {
        'berufserfahrung_enhanced': {
            'description': 'Enhanced professional experience tailored to job requirements',
            'example': '**Seit 2020** | Senior DevOps Engineer | TechCorp GmbH\n- Automatisierung von CI/CD-Pipelines mit GitLab CI und Jenkins\n- Container-Orchestrierung mit Kubernetes in AWS-Umgebungen',
            'format': 'markdown',
            'tone': 'achievement-focused, quantified'
        },
        'ausbildung_enhanced': {
            'description': 'Enhanced education section highlighting relevant aspects',
            'example': '**2015-2018** | Master of Science Informatik | TU Berlin\nSchwerpunkt: Software Engineering und Cloud Computing\nMasterarbeit: "Microservices-Architekturen in der Praxis"',
            'format': 'markdown',
            'tone': 'academic, relevant'
        },
        'fachkenntnisse_enhanced': {
            'description': 'Enhanced technical skills organized by relevance to job',
            'example': '**Cloud Platforms:** AWS (Expert), Azure (Advanced), Google Cloud (Intermediate)\n**DevOps Tools:** Docker, Kubernetes, Terraform, Ansible',
            'format': 'markdown',
            'tone': 'technical, categorized'
        }
    }
    
    @classmethod
    def get_all_variables(cls) -> Dict[str, Dict[str, Any]]:
        """Get all AI content variables with their definitions"""
        all_vars = {}
        all_vars.update(cls.COVER_LETTER_VARIABLES)
        all_vars.update(cls.CV_VARIABLES)
        return all_vars
    
    @classmethod
    def get_variable_names(cls) -> List[str]:
        """Get list of all AI content variable names"""
        return list(cls.get_all_variables().keys())
    
    @classmethod
    def get_cover_letter_variables(cls) -> List[str]:
        """Get list of cover letter AI variables"""
        return list(cls.COVER_LETTER_VARIABLES.keys())
    
    @classmethod
    def get_cv_variables(cls) -> List[str]:
        """Get list of CV AI variables"""
        return list(cls.CV_VARIABLES.keys())
    
    @classmethod
    def validate_variable(cls, variable_name: str) -> bool:
        """Check if variable name is a valid AI content variable"""
        return variable_name in cls.get_all_variables()
    
    @classmethod
    def get_variable_info(cls, variable_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific variable"""
        return cls.get_all_variables().get(variable_name)


class AIContentPrompts:
    """Prompt templates for generating different types of content"""
    
    SYSTEM_PROMPT = """Du bist ein Experte für deutsche Bewerbungen und hilfst dabei, personalisierte, professionelle Bewerbungsinhalte zu erstellen. 

Deine Aufgabe ist es, authentische und überzeugende Texte zu schreiben, die:
- Spezifisch auf die Stellenausschreibung eingehen
- Die Qualifikationen des Bewerbers hervorheben
- Einen professionellen, aber natürlichen Ton verwenden
- Deutsche Bewerbungsstandards befolgen
- Konkret und präzise sind (keine Floskeln)

Antworte immer nur mit dem angeforderten Text, ohne zusätzliche Erklärungen."""
    
    PROMPTS = {
        ContentType.EINSTIEGSTEXT: """
Erstelle einen persönlichen Einstiegstext für ein Anschreiben.

STELLENAUSSCHREIBUNG:
{job_description}

PROFIL DES BEWERBERS:
{profile_content}

POSITION: {position_title}
UNTERNEHMEN: {company_name}

Schreibe einen authentischen Einstiegstext (max. 2-3 Sätze), der zeigt:
- Warum diese spezielle Position interessant ist
- Bezug zur konkreten Stellenausschreibung
- Erste Andeutung der Passung

Stil: Professionell, aber persönlich. Keine Standard-Floskeln.
""",
        
        ContentType.FACHLICHE_PASSUNG: """
Erstelle einen Text über die fachliche Passung des Bewerbers zur Stelle.

STELLENAUSSCHREIBUNG:
{job_description}

PROFIL DES BEWERBERS:
{profile_content}

Analysiere die Anforderungen und erstelle einen präzisen Text (max. 3-4 Sätze), der:
- Konkrete Übereinstimmungen zwischen Profil und Anforderungen zeigt
- Spezifische Technologien/Erfahrungen erwähnt
- Quantifizierte Erfahrungen einbaut (Jahre, Projekte, etc.)
- Zeigt, warum der Bewerber ideal geeignet ist

Stil: Selbstbewusst, faktisch, konkret.
""",
        
        ContentType.MOTIVATIONSTEXT: """
Erstelle einen Motivationstext für die spezielle Position und das Unternehmen.

STELLENAUSSCHREIBUNG:
{job_description}

UNTERNEHMEN: {company_name}
POSITION: {position_title}

Schreibe einen authentischen Motivationstext (max. 2-3 Sätze), der:
- Spezifische Aspekte der Position hervorhebt
- Bezug zum Unternehmen/zur Branche zeigt
- Zukunftsorientierte Ziele ausdrückt
- Echte Begeisterung vermittelt

Stil: Enthusiastisch, aber professionell. Kein Marketing-Sprech.
""",
        
        ContentType.MEHRWERT: """
Erstelle einen Text über den Mehrwert, den der Bewerber dem Unternehmen bietet.

STELLENAUSSCHREIBUNG:
{job_description}

PROFIL DES BEWERBERS:
{profile_content}

UNTERNEHMEN: {company_name}

Schreibe einen wertorientierten Text (max. 2-3 Sätze), der:
- Konkrete Ergebnisse/Erfolge des Bewerbers erwähnt
- Direkte Vorteile für das Unternehmen aufzeigt
- Messbare Verbesserungen andeutet
- Problemlösungskompetenz betont

Stil: Ergebnisorientiert, konkret, überzeugend.
""",
        
        ContentType.ABSCHLUSSTEXT: """
Erstelle einen professionellen Abschlusstext für das Anschreiben.

POSITION: {position_title}
UNTERNEHMEN: {company_name}

Schreibe einen höflichen Abschluss (1-2 Sätze), der:
- Interesse an einem Gespräch ausdrückt
- Professionell und respektvoll ist
- Zum Handeln motiviert
- Nicht zu aufdringlich wirkt

Stil: Höflich, professionell, einladend.
"""
    }
    
    @classmethod
    def get_prompt(cls, content_type: ContentType, **kwargs) -> str:
        """Get formatted prompt for specific content type"""
        if content_type not in cls.PROMPTS:
            raise ValueError(f"No prompt defined for content type: {content_type}")
        
        return cls.PROMPTS[content_type].format(**kwargs)
    
    @classmethod
    def get_system_prompt(cls) -> str:
        """Get the system prompt for AI model"""
        return cls.SYSTEM_PROMPT


class ContentCache:
    """Simple cache for generated AI content"""
    
    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(exist_ok=True)
        self.cache_file = self.cache_dir / "ai_content_cache.json"
        self._cache = self._load_cache()
    
    def _load_cache(self) -> Dict[str, Any]:
        """Load cache from file"""
        if self.cache_file.exists():
            try:
                return json.loads(self.cache_file.read_text(encoding='utf-8'))
            except (json.JSONDecodeError, FileNotFoundError):
                return {}
        return {}
    
    def _save_cache(self):
        """Save cache to file"""
        self.cache_file.write_text(
            json.dumps(self._cache, indent=2, ensure_ascii=False), 
            encoding='utf-8'
        )
    
    def _generate_key(self, request: AIContentRequest) -> str:
        """Generate cache key from request"""
        import hashlib
        key_data = f"{request.content_type.value}:{request.job_description[:100]}:{request.profile_content[:100]}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def get(self, request: AIContentRequest) -> Optional[AIContentResponse]:
        """Get cached response"""
        key = self._generate_key(request)
        cached_data = self._cache.get(key)
        if cached_data:
            # Convert string back to enum
            if isinstance(cached_data.get('content_type'), str):
                cached_data['content_type'] = ContentType(cached_data['content_type'])
            return AIContentResponse(**cached_data)
        return None
    
    def set(self, request: AIContentRequest, response: AIContentResponse):
        """Cache response"""
        key = self._generate_key(request)
        # Convert response to dict and handle enum serialization
        response_dict = asdict(response)
        response_dict['content_type'] = response.content_type.value  # Convert enum to string
        self._cache[key] = response_dict
        self._save_cache()
    
    def clear(self):
        """Clear all cached content"""
        self._cache.clear()
        self._save_cache()


def generate_sample_ai_content() -> Dict[str, str]:
    """Generate sample AI content for testing purposes"""
    return {
        'einstiegstext': 'mit großem Interesse habe ich Ihre Stellenausschreibung für die Position als Senior DevOps Engineer gelesen. Die Möglichkeit, bei einem innovativen Unternehmen wie dem Ihren an der Automatisierung cloudbasierter Infrastrukturen mitzuwirken, entspricht genau meinen beruflichen Zielen.',
        
        'fachliche_passung': 'Mit über 7 Jahren Erfahrung in der DevOps-Praxis und meiner Expertise in Kubernetes, Terraform und AWS bringe ich genau die Qualifikationen mit, die Sie suchen. Besonders meine Erfahrung mit MLOps-Plattformen und Infrastructure-as-Code passt perfekt zu Ihren Anforderungen.',
        
        'motivationstext': 'Die Kombination aus technischer Innovation und der Möglichkeit, in einem cross-funktionalen Team an zukunftsweisenden Data Science Plattformen zu arbeiten, begeistert mich besonders. Gerade die Herausforderung, komplexe Automatisierungslösungen zu entwickeln, motiviert mich jeden Tag.',
        
        'mehrwert': 'In meinen bisherigen Projekten konnte ich Deployment-Zeiten um 60% reduzieren und die Systemverfügbarkeit auf 99.9% steigern. Diese Erfahrung würde ich gerne nutzen, um auch Ihre Plattform-Infrastruktur zu optimieren und Ihre Entwicklungsteams noch effizienter zu machen.',
        
        'abschlusstext': 'Über die Möglichkeit, meine Leidenschaft für DevOps-Automatisierung in Ihrem Team einzubringen, würde ich mich in einem persönlichen Gespräch sehr freuen.'
    }