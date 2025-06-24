#!/usr/bin/env python3
"""
Claude API Client - Integrates with Anthropic's Claude API for intelligent content generation
"""

import os
import time
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# AI Content Generator imports
from ai_content_generator import (
    AIContentRequest, AIContentResponse, ContentType, 
    AIContentPrompts, ContentCache, generate_sample_ai_content
)

# Anthropic API client with error handling
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    print("Anthropic package not available. Install with: pip install anthropic")
    ANTHROPIC_AVAILABLE = False
    anthropic = None


class ClaudeAPIClient:
    """Client for generating content using Claude API"""
    
    def __init__(self, base_dir: str = ".", use_cache: bool = True):
        self.base_dir = Path(base_dir)
        
        # Load environment variables (try local first, then default)
        local_env = self.base_dir / ".env.local"
        default_env = self.base_dir / ".env"
        
        if local_env.exists():
            load_dotenv(local_env)
            print("Using local .env.local file")
        else:
            load_dotenv(default_env)
        
        # Initialize API client
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        self.client = None
        self.available = False
        
        # Validate API key format
        if not ANTHROPIC_AVAILABLE:
            print("❌ Anthropic package not available. Install with: pip install anthropic")
        elif not self.api_key:
            print("❌ ANTHROPIC_API_KEY not found in environment variables")
            print("   Create a .env.local file with: ANTHROPIC_API_KEY=your_actual_key")
        elif self.api_key == "your_api_key_here":
            print("❌ ANTHROPIC_API_KEY is still set to placeholder value")
            print("   Update .env.local with your actual API key from https://console.anthropic.com/")
        elif not self.api_key.startswith("sk-"):
            print("❌ ANTHROPIC_API_KEY appears to be invalid (should start with 'sk-')")
        else:
            try:
                self.client = anthropic.Anthropic(api_key=self.api_key)
                self.available = True
                print("✅ Claude API client initialized successfully")
            except Exception as e:
                print(f"❌ Failed to initialize Claude API client: {e}")
                print("   Check if your API key is valid and has sufficient credits")
        
        # Initialize cache
        self.use_cache = use_cache
        if use_cache:
            cache_dir = self.base_dir / ".cache"
            self.cache = ContentCache(cache_dir)
        else:
            self.cache = None
        
        # API configuration
        self.model = "claude-3-5-sonnet-20241022"
        self.max_tokens = 1000
        self.temperature = 0.3
    
    def is_available(self) -> bool:
        """Check if Claude API is available and configured"""
        return self.available
    
    def generate_content(self, request: AIContentRequest) -> AIContentResponse:
        """
        Generate AI content for the given request
        """
        start_time = time.time()
        
        # Check cache first
        if self.cache:
            cached_response = self.cache.get(request)
            if cached_response:
                print(f"Using cached content for {request.content_type.value}")
                return cached_response
        
        # Generate content
        if not self.available:
            print(f"Claude API not available, using sample content for {request.content_type.value}")
            return self._generate_sample_response(request, start_time)
        
        try:
            # Generate prompt
            prompt = AIContentPrompts.get_prompt(
                request.content_type,
                job_description=request.job_description,
                profile_content=request.profile_content,
                company_name=request.company_name,
                position_title=request.position_title
            )
            
            # Call Claude API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system=AIContentPrompts.get_system_prompt(),
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            # Extract content
            generated_text = response.content[0].text.strip()
            
            # Create response object
            ai_response = AIContentResponse(
                content_type=request.content_type,
                generated_text=generated_text,
                confidence=0.9,  # Claude generally high confidence
                tokens_used=response.usage.input_tokens + response.usage.output_tokens,
                processing_time=time.time() - start_time,
                metadata={
                    'model': self.model,
                    'input_tokens': response.usage.input_tokens,
                    'output_tokens': response.usage.output_tokens
                }
            )
            
            # Cache the response
            if self.cache:
                self.cache.set(request, ai_response)
            
            print(f"Generated {request.content_type.value} content ({ai_response.tokens_used} tokens)")
            return ai_response
            
        except Exception as e:
            print(f"Error generating content with Claude API: {e}")
            return self._generate_sample_response(request, start_time)
    
    def _generate_sample_response(self, request: AIContentRequest, start_time: float) -> AIContentResponse:
        """Generate sample response when API is not available"""
        sample_content = generate_sample_ai_content()
        content_key = request.content_type.value
        
        generated_text = sample_content.get(content_key, f"Sample {content_key} content")
        
        return AIContentResponse(
            content_type=request.content_type,
            generated_text=generated_text,
            confidence=0.5,  # Lower confidence for sample content
            tokens_used=0,
            processing_time=time.time() - start_time,
            metadata={'source': 'sample_content'}
        )
    
    def generate_all_cover_letter_content(self, job_description: str, profile_content: str, 
                                        company_name: str, position_title: str) -> Dict[str, str]:
        """
        Generate all cover letter content variables at once
        """
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
        """
        Extract company name and position title from job description
        First tries to parse Adressat line, then falls back to Claude API
        """
        # First try to parse Adressat line directly
        adressat_info = self._parse_adressat_line(job_description)
        if adressat_info['company_name'] != 'Unternehmen':
            # Try to extract position from filename or use Claude API
            if self.available:
                position = self._extract_position_with_claude(job_description)
                adressat_info['position_title'] = position
            return adressat_info
        
        # Fall back to Claude API extraction
        if not self.available:
            return {
                'company_name': 'Unternehmen',
                'position_title': 'Position'
            }
        
        extraction_prompt = f"""
Extrahiere aus der folgenden Stellenausschreibung:
1. Den Unternehmensnamen
2. Die genaue Positionsbezeichnung

STELLENAUSSCHREIBUNG:
{job_description}

Antworte im Format:
Unternehmen: [Name]
Position: [Bezeichnung]
"""
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=200,
                temperature=0.1,
                messages=[{
                    "role": "user",
                    "content": extraction_prompt
                }]
            )
            
            content = response.content[0].text.strip()
            
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
            print(f"Error extracting company/position: {e}")
            return {
                'company_name': 'Unternehmen',
                'position_title': 'Position'
            }
    
    def _parse_adressat_line(self, job_description: str) -> Dict[str, str]:
        """
        Parse structured job description header
        Expected format:
        Adressat: BWI GmbH Auf dem Steinbüchel 22 53340 Meckenheim Deutschland
        Stelle: Senior DevOps Engineer (m/w/d)
        Stellen-ID: 61383
        """
        lines = job_description.strip().split('\n')
        
        result = {
            'company_name': 'Unternehmen',
            'position_title': 'Position',
            'adressat_firma': 'Unternehmen',
            'adressat_strasse': 'Straße',
            'adressat_plz_ort': 'PLZ Ort',
            'adressat_land': 'Deutschland',
            'stelle': 'Position',
            'stellen_id': ''
        }
        
        for line in lines:
            line = line.strip()
            
            # Parse Adressat line
            if line.startswith('Adressat:'):
                adressat_text = line.replace('Adressat:', '').strip()
                
                # Parse the address components
                parts = adressat_text.split()
                
                if len(parts) >= 4:
                    # Find postal code (5 digits)
                    plz_index = -1
                    for i, part in enumerate(parts):
                        if part.isdigit() and len(part) == 5:
                            plz_index = i
                            break
                    
                    if plz_index > 0:
                        # Company name: everything before street address
                        # Look for typical German company suffixes
                        company_end = 1
                        for i, part in enumerate(parts[:plz_index-1]):
                            if part.lower() in ['gmbh', 'ag', 'kg', 'co.', 'co', 'ohg', 'mbh']:
                                company_end = i + 1
                                break
                        
                        company_name = ' '.join(parts[:company_end])
                        street = ' '.join(parts[company_end:plz_index])
                        plz = parts[plz_index]
                        city = ' '.join(parts[plz_index+1:-1]) if len(parts) > plz_index + 2 else parts[plz_index+1]
                        country = parts[-1] if len(parts) > plz_index + 2 else 'Deutschland'
                        
                        result.update({
                            'company_name': company_name,
                            'adressat_firma': company_name,
                            'adressat_strasse': street,
                            'adressat_plz_ort': f"{plz} {city}",
                            'adressat_land': country
                        })
            
            # Parse Stelle line
            elif line.startswith('Stelle:'):
                stelle = line.replace('Stelle:', '').strip()
                result.update({
                    'position_title': stelle,
                    'stelle': stelle
                })
            
            # Parse Stellen-ID line
            elif line.startswith('Stellen-ID:'):
                stellen_id = line.replace('Stellen-ID:', '').strip()
                result['stellen_id'] = stellen_id
        
        return result
    
    def _extract_position_with_claude(self, job_description: str) -> str:
        """Extract just the position title using Claude API"""
        if not self.available:
            return 'Position'
        
        try:
            extraction_prompt = f"""
Extrahiere aus der folgenden Stellenausschreibung nur die genaue Positionsbezeichnung.

STELLENAUSSCHREIBUNG:
{job_description}

Antworte nur mit der Positionsbezeichnung, ohne weitere Erklärungen.
"""
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=50,
                temperature=0.1,
                messages=[{
                    "role": "user",
                    "content": extraction_prompt
                }]
            )
            
            return response.content[0].text.strip()
            
        except Exception as e:
            print(f"Error extracting position: {e}")
            return 'Position'
    
    def validate_api_key(self) -> bool:
        """
        Validate API key by making a simple test request
        """
        if not self.available:
            return False
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=10,
                messages=[{
                    "role": "user",
                    "content": "Test"
                }]
            )
            return True
        except Exception as e:
            print(f"API key validation failed: {e}")
            return False
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """
        Get usage statistics from cache
        """
        if not self.cache:
            return {'cache_enabled': False}
        
        stats = {
            'cache_enabled': True,
            'cached_items': len(self.cache._cache),
            'api_available': self.available
        }
        
        if self.cache._cache:
            total_tokens = sum(
                item.get('tokens_used', 0) 
                for item in self.cache._cache.values()
            )
            stats['total_tokens_cached'] = total_tokens
        
        return stats
    
    def clear_cache(self):
        """Clear the content cache"""
        if self.cache:
            self.cache.clear()
            print("Content cache cleared")
    
    def test_content_generation(self) -> bool:
        """
        Test content generation with sample data
        """
        print("Testing Claude API content generation...")
        
        test_request = AIContentRequest(
            content_type=ContentType.EINSTIEGSTEXT,
            job_description="Wir suchen einen DevOps Engineer für unser innovatives Team.",
            profile_content="Erfahrener DevOps Engineer mit 5 Jahren Kubernetes-Erfahrung.",
            company_name="TechCorp",
            position_title="DevOps Engineer"
        )
        
        try:
            response = self.generate_content(test_request)
            print(f"✓ Test successful: {response.generated_text[:100]}...")
            return True
        except Exception as e:
            print(f"✗ Test failed: {e}")
            return False