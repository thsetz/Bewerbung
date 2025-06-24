#!/usr/bin/env python3
"""
Llama API Client - Integrates with Ollama for local AI content generation
"""

import os
import time
import json
import requests
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Base AI Client
from base_ai_client import BaseAIClient, AIProviderError, AIContentError

# AI Content Generator imports
from ai_content_generator import (
    AIContentRequest, AIContentResponse, ContentType, 
    ContentCache, generate_sample_ai_content
)


class LlamaAPIClient(BaseAIClient):
    """Client for generating content using Ollama (local Llama models)"""
    
    def __init__(self, base_dir: str = ".", use_cache: bool = True):
        super().__init__(base_dir, use_cache)
        self.base_dir = Path(base_dir)
        
        # Load environment variables (try local first, then default)
        local_env = self.base_dir / ".env.local"
        default_env = self.base_dir / ".env"
        
        if local_env.exists():
            load_dotenv(local_env)
        else:
            load_dotenv(default_env)
        
        # Ollama configuration
        self.ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.model_name = os.getenv("LLAMA_MODEL", "llama3.2:3b")  # Default to 3B model
        self.temperature = float(os.getenv("LLAMA_TEMPERATURE", "0.3"))
        self.max_tokens = int(os.getenv("LLAMA_MAX_TOKENS", "1000"))
        
        # Initialize cache
        if use_cache:
            cache_dir = self.base_dir / ".cache"
            self.cache = ContentCache(cache_dir)
        else:
            self.cache = None
        
        # Check availability
        self._check_ollama_availability()
    
    def _check_ollama_availability(self):
        """Check if Ollama is running and model is available"""
        try:
            # Check if Ollama is running
            response = requests.get(f"{self.ollama_host}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_names = [model.get('name', '') for model in models]
                
                if self.model_name in model_names:
                    self.available = True
                    print(f"✅ Ollama client initialized with model {self.model_name}")
                else:
                    print(f"❌ Model {self.model_name} not found in Ollama")
                    print(f"   Available models: {', '.join(model_names) if model_names else 'None'}")
                    print(f"   Install with: ollama pull {self.model_name}")
            else:
                print(f"❌ Ollama not responding at {self.ollama_host}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Ollama not available: {e}")
            print(f"   Start Ollama with: ollama serve")
            print(f"   Install model with: ollama pull {self.model_name}")
    
    def is_available(self) -> bool:
        """Check if Ollama is available and configured"""
        return self.available
    
    def get_model_name(self) -> str:
        """Get the specific Llama model name"""
        if hasattr(self, 'model_name') and self.model_name:
            # Extract clean model name
            # e.g., "llama3.2:3b" -> "3-2-3b", "llama3.2:latest" -> "3-2-latest"
            model = self.model_name
            if model.startswith('llama'):
                model = model.replace('llama', '')
            # Replace dots and colons with dashes for filesystem compatibility
            model = model.replace('.', '-').replace(':', '-')
            return model.strip('-')
        return 'unknown'
    
    def generate_content(self, request: AIContentRequest) -> AIContentResponse:
        """Generate AI content using Ollama"""
        start_time = time.time()
        
        # Check cache first
        if self.cache:
            cached_response = self.cache.get(request)
            if cached_response:
                print(f"Using cached content for {request.content_type.value}")
                return cached_response
        
        # Generate content
        if not self.available:
            print(f"Ollama not available, using sample content for {request.content_type.value}")
            return self._generate_sample_response(request, start_time)
        
        try:
            # Generate prompt adapted for Llama
            prompt = self._get_llama_prompt(
                request.content_type,
                job_description=request.job_description,
                profile_content=request.profile_content,
                company_name=request.company_name,
                position_title=request.position_title
            )
            
            # Call Ollama API
            response = requests.post(
                f"{self.ollama_host}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": self.temperature,
                        "num_predict": self.max_tokens
                    }
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                generated_text = result.get('response', '').strip()
                
                # Create response object
                ai_response = AIContentResponse(
                    content_type=request.content_type,
                    generated_text=generated_text,
                    confidence=0.8,  # Llama generally good confidence
                    tokens_used=len(generated_text.split()),  # Approximate token count
                    processing_time=time.time() - start_time,
                    metadata={
                        'model': self.model_name,
                        'provider': 'ollama'
                    }
                )
                
                # Cache the response
                if self.cache:
                    self.cache.set(request, ai_response)
                
                print(f"Generated {request.content_type.value} content with Ollama ({ai_response.tokens_used} tokens)")
                return ai_response
            else:
                raise AIContentError(f"Ollama API error: {response.status_code}")
                
        except Exception as e:
            print(f"Error generating content with Ollama: {e}")
            return self._generate_sample_response(request, start_time)
    
    def _get_llama_prompt(self, content_type: ContentType, **kwargs) -> str:
        """Get Llama-optimized prompt for specific content type"""
        
        # Llama instruction format: <|begin_of_text|><|start_header_id|>system<|end_header_id|>...
        system_prompt = """Du bist ein erfahrener Bewerbungsberater für den deutschen Arbeitsmarkt. 
Schreibe professionelle, authentische Bewerbungstexte in deutscher Sprache. 
Verwende einen überzeugenden aber nicht übertriebenen Stil."""
        
        prompts = {
            ContentType.EINSTIEGSTEXT: f"""
<|begin_of_text|><|start_header_id|>system<|end_header_id|>
{system_prompt}
<|end_header_id|><|start_header_id|>user<|end_header_id|>

Schreibe einen überzeugenden Einstiegstext für ein Anschreiben.

STELLENAUSSCHREIBUNG:
{kwargs.get('job_description', '')}

BEWERBER-PROFIL:
{kwargs.get('profile_content', '')}

UNTERNEHMEN: {kwargs.get('company_name', '')}
POSITION: {kwargs.get('position_title', '')}

Schreibe 2-3 Sätze, die:
- Interesse an der Position zeigen
- Bezug zur Stellenausschreibung herstellen
- Erste Qualifikationen andeuten
- Professionell und authentisch wirken

Antworte nur mit dem Text, ohne Erklärungen.
<|end_header_id|><|start_header_id|>assistant<|end_header_id|>
""",
            
            ContentType.FACHLICHE_PASSUNG: f"""
<|begin_of_text|><|start_header_id|>system<|end_header_id|>
{system_prompt}
<|end_header_id|><|start_header_id|>user<|end_header_id|>

Schreibe einen Text über die fachliche Passung des Bewerbers zur Position.

STELLENAUSSCHREIBUNG:
{kwargs.get('job_description', '')}

BEWERBER-PROFIL:
{kwargs.get('profile_content', '')}

Schreibe 2-3 Sätze, die:
- Konkrete Qualifikationen des Bewerbers hervorheben
- Bezug zu den geforderten Fähigkeiten herstellen
- Berufserfahrung erwähnen
- Fachliche Expertise demonstrieren

Antworte nur mit dem Text, ohne Erklärungen.
<|end_header_id|><|start_header_id|>assistant<|end_header_id|>
""",
            
            ContentType.MOTIVATIONSTEXT: f"""
<|begin_of_text|><|start_header_id|>system<|end_header_id|>
{system_prompt}
<|end_header_id|><|start_header_id|>user<|end_header_id|>

Schreibe einen authentischen Motivationstext.

STELLENAUSSCHREIBUNG:
{kwargs.get('job_description', '')}

UNTERNEHMEN: {kwargs.get('company_name', '')}
POSITION: {kwargs.get('position_title', '')}

Schreibe 2-3 Sätze, die:
- Echte Begeisterung für die Position zeigen
- Bezug zum Unternehmen/zur Branche herstellen
- Zukunftsorientierte Ziele ausdrücken
- Authentisch und überzeugend wirken

Antworte nur mit dem Text, ohne Erklärungen.
<|end_header_id|><|start_header_id|>assistant<|end_header_id|>
""",
            
            ContentType.MEHRWERT: f"""
<|begin_of_text|><|start_header_id|>system<|end_header_id|>
{system_prompt}
<|end_header_id|><|start_header_id|>user<|end_header_id|>

Schreibe einen Text über den Mehrwert des Bewerbers für das Unternehmen.

STELLENAUSSCHREIBUNG:
{kwargs.get('job_description', '')}

BEWERBER-PROFIL:
{kwargs.get('profile_content', '')}

UNTERNEHMEN: {kwargs.get('company_name', '')}

Schreibe 2-3 Sätze, die:
- Konkrete Erfolge/Ergebnisse erwähnen
- Direkte Vorteile für das Unternehmen aufzeigen
- Messbare Verbesserungen andeuten
- Problemlösungskompetenz betonen

Antworte nur mit dem Text, ohne Erklärungen.
<|end_header_id|><|start_header_id|>assistant<|end_header_id|>
""",
            
            ContentType.ABSCHLUSSTEXT: f"""
<|begin_of_text|><|start_header_id|>system<|end_header_id|>
{system_prompt}
<|end_header_id|><|start_header_id|>user<|end_header_id|>

Schreibe einen professionellen Abschlusstext für das Anschreiben.

POSITION: {kwargs.get('position_title', '')}
UNTERNEHMEN: {kwargs.get('company_name', '')}

Schreibe 1-2 Sätze, die:
- Interesse an einem Gespräch ausdrücken
- Professionell und respektvoll sind
- Zum Handeln motivieren
- Nicht aufdringlich wirken

Antworte nur mit dem Text, ohne Erklärungen.
<|end_header_id|><|start_header_id|>assistant<|end_header_id|>
"""
        }
        
        return prompts.get(content_type, prompts[ContentType.EINSTIEGSTEXT])
    
    def _generate_sample_response(self, request: AIContentRequest, start_time: float) -> AIContentResponse:
        """Generate sample response when Ollama is not available"""
        sample_content = generate_sample_ai_content()
        content_key = request.content_type.value
        
        generated_text = sample_content.get(content_key, f"Sample {content_key} content")
        
        return AIContentResponse(
            content_type=request.content_type,
            generated_text=generated_text,
            confidence=0.5,  # Lower confidence for sample content
            tokens_used=0,
            processing_time=time.time() - start_time,
            metadata={'source': 'sample_content', 'provider': 'ollama_fallback'}
        )
    
    def generate_all_cover_letter_content(self, job_description: str, profile_content: str, 
                                        company_name: str, position_title: str) -> Dict[str, str]:
        """Generate all cover letter content variables at once"""
        content_types = [
            ContentType.EINSTIEGSTEXT,
            ContentType.FACHLICHE_PASSUNG,
            ContentType.MOTIVATIONSTEXT,
            ContentType.MEHRWERT,
            ContentType.ABSCHLUSSTEXT
        ]
        
        results = {}
        for content_type in content_types:
            request = AIContentRequest(
                content_type=content_type,
                job_description=job_description,
                profile_content=profile_content,
                company_name=company_name,
                position_title=position_title
            )
            
            response = self.generate_content(request)
            results[content_type.value] = response.generated_text
        
        return results
    
    def extract_company_and_position(self, job_description: str) -> Dict[str, str]:
        """Extract company name and position title from job description"""
        # First try to parse structured header (same as Claude client)
        from claude_api_client import ClaudeAPIClient
        claude_client = ClaudeAPIClient()
        adressat_info = claude_client._parse_adressat_line(job_description)
        
        if adressat_info['company_name'] != 'Unternehmen':
            # If we found structured data, try to extract position with Llama
            if self.available:
                position = self._extract_position_with_llama(job_description)
                adressat_info['position_title'] = position
            return adressat_info
        
        # Fall back to Llama extraction if available
        if not self.available:
            return {
                'company_name': 'Unternehmen',
                'position_title': 'Position'
            }
        
        try:
            extraction_prompt = f"""
<|begin_of_text|><|start_header_id|>system<|end_header_id|>
Du bist ein Experte für die Analyse von Stellenausschreibungen.
<|end_header_id|><|start_header_id|>user<|end_header_id|>

Extrahiere aus der folgenden Stellenausschreibung:
1. Den Unternehmensnamen
2. Die genaue Positionsbezeichnung

STELLENAUSSCHREIBUNG:
{job_description}

Antworte im Format:
Unternehmen: [Name]
Position: [Bezeichnung]
<|end_header_id|><|start_header_id|>assistant<|end_header_id|>
"""
            
            response = requests.post(
                f"{self.ollama_host}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": extraction_prompt,
                    "stream": False,
                    "options": {"temperature": 0.1, "num_predict": 100}
                },
                timeout=30
            )
            
            if response.status_code == 200:
                content = response.json().get('response', '').strip()
                
                # Parse response
                company_name = "Unternehmen"
                position_title = "Position"
                
                for line in content.split('\n'):
                    if line.startswith('Unternehmen:'):
                        company_name = line.replace('Unternehmen:', '').strip()
                    elif line.startswith('Position:'):
                        position_title = line.replace('Position:', '').strip()
                
                return {
                    'company_name': company_name,
                    'position_title': position_title
                }
                
        except Exception as e:
            print(f"Error extracting company/position with Llama: {e}")
        
        return {
            'company_name': 'Unternehmen',
            'position_title': 'Position'
        }
    
    def _extract_position_with_llama(self, job_description: str) -> str:
        """Extract just the position title using Llama"""
        if not self.available:
            return 'Position'
        
        try:
            extraction_prompt = f"""
<|begin_of_text|><|start_header_id|>system<|end_header_id|>
Du extrahierst Positionsbezeichnungen aus Stellenausschreibungen.
<|end_header_id|><|start_header_id|>user<|end_header_id|>

Extrahiere aus der folgenden Stellenausschreibung nur die genaue Positionsbezeichnung.

STELLENAUSSCHREIBUNG:
{job_description}

Antworte nur mit der Positionsbezeichnung, ohne weitere Erklärungen.
<|end_header_id|><|start_header_id|>assistant<|end_header_id|>
"""
            
            response = requests.post(
                f"{self.ollama_host}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": extraction_prompt,
                    "stream": False,
                    "options": {"temperature": 0.1, "num_predict": 50}
                },
                timeout=20
            )
            
            if response.status_code == 200:
                return response.json().get('response', '').strip()
                
        except Exception as e:
            print(f"Error extracting position with Llama: {e}")
        
        return 'Position'
    
    def get_available_models(self) -> list:
        """Get list of available Ollama models"""
        try:
            response = requests.get(f"{self.ollama_host}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                return [model.get('name', '') for model in models]
        except Exception:
            pass
        return []
    
    def install_model(self, model_name: str = None) -> bool:
        """Install/pull a model in Ollama"""
        model = model_name or self.model_name
        try:
            print(f"Installing model {model}...")
            response = requests.post(
                f"{self.ollama_host}/api/pull",
                json={"name": model},
                timeout=300  # 5 minutes for model download
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Error installing model {model}: {e}")
            return False