#!/usr/bin/env python3
"""
AI Client Factory - Creates and manages different AI clients with fallback logic
"""

import os
from typing import Optional, List
from dotenv import load_dotenv

from base_ai_client import BaseAIClient, AIProviderError


class AIClientFactory:
    """Factory for creating AI clients with automatic provider selection and fallback"""
    
    def __init__(self, base_dir: str = "."):
        self.base_dir = base_dir
        
        # Load environment variables
        load_dotenv()
        
        # Configuration
        self.preferred_provider = os.getenv("AI_PROVIDER", "auto").lower()
        self.enable_fallback = os.getenv("AI_ENABLE_FALLBACK", "true").lower() == "true"
        
    def create_client(self, use_cache: bool = True) -> BaseAIClient:
        """
        Create an AI client based on configuration and availability
        
        Provider selection logic:
        1. If AI_PROVIDER is set to specific provider, try that first
        2. If "auto" or not set, try providers in order: Llama -> Claude -> Sample
        3. If fallback is enabled, continue down the chain until one works
        4. If no providers work, return a mock client with sample content
        """
        
        if self.preferred_provider == "claude":
            return self._try_claude_client(use_cache) or self._get_fallback_client(use_cache)
        elif self.preferred_provider == "llama":
            return self._try_llama_client(use_cache) or self._get_fallback_client(use_cache)
        elif self.preferred_provider == "auto":
            return self._get_auto_client(use_cache)
        else:
            print(f"⚠️  Unknown AI provider '{self.preferred_provider}', using auto selection")
            return self._get_auto_client(use_cache)
    
    def _get_auto_client(self, use_cache: bool) -> BaseAIClient:
        """Auto-select the best available client"""
        
        # Try Llama first (local, free)
        client = self._try_llama_client(use_cache)
        if client and client.is_available():
            print(f"🦙 Using Llama client ({client.model_name})")
            return client
        
        # Fall back to Claude (cloud, paid)
        client = self._try_claude_client(use_cache)
        if client and client.is_available():
            print(f"🤖 Using Claude client")
            return client
        
        # Final fallback to sample content
        print("⚠️  No AI providers available, using sample content")
        return self._get_fallback_client(use_cache)
    
    def _try_llama_client(self, use_cache: bool) -> Optional[BaseAIClient]:
        """Try to create a Llama client"""
        try:
            from llama_api_client import LlamaAPIClient
            client = LlamaAPIClient(self.base_dir, use_cache)
            return client if client.is_available() else None
        except ImportError as e:
            print(f"⚠️  Llama client not available: {e}")
            return None
        except Exception as e:
            print(f"⚠️  Error initializing Llama client: {e}")
            return None
    
    def _try_claude_client(self, use_cache: bool) -> Optional[BaseAIClient]:
        """Try to create a Claude client"""
        try:
            from claude_api_client import ClaudeAPIClient
            client = ClaudeAPIClient(self.base_dir, use_cache)
            return client if client.is_available() else None
        except ImportError as e:
            print(f"⚠️  Claude client not available: {e}")
            return None
        except Exception as e:
            print(f"⚠️  Error initializing Claude client: {e}")
            return None
    
    def _get_fallback_client(self, use_cache: bool) -> BaseAIClient:
        """Get fallback client that always works (sample content)"""
        return SampleAIClient(self.base_dir, use_cache)
    
    def get_available_providers(self) -> List[str]:
        """Get list of available AI providers"""
        providers = []
        
        if self._try_llama_client(False):
            providers.append("llama")
        
        if self._try_claude_client(False):
            providers.append("claude")
        
        providers.append("sample")  # Always available
        
        return providers
    
    def test_all_providers(self) -> dict:
        """Test all available providers and return status"""
        results = {}
        
        # Test Llama
        llama_client = self._try_llama_client(False)
        if llama_client:
            results["llama"] = {
                "available": llama_client.is_available(),
                "test_passed": llama_client.test_content_generation() if llama_client.is_available() else False
            }
        else:
            results["llama"] = {"available": False, "test_passed": False}
        
        # Test Claude
        claude_client = self._try_claude_client(False)
        if claude_client:
            results["claude"] = {
                "available": claude_client.is_available(),
                "test_passed": claude_client.test_content_generation() if claude_client.is_available() else False
            }
        else:
            results["claude"] = {"available": False, "test_passed": False}
        
        # Sample is always available
        sample_client = self._get_fallback_client(False)
        results["sample"] = {
            "available": True,
            "test_passed": sample_client.test_content_generation()
        }
        
        return results


class SampleAIClient(BaseAIClient):
    """Fallback AI client that provides sample content"""
    
    def __init__(self, base_dir: str = ".", use_cache: bool = True):
        super().__init__(base_dir, use_cache)
        self.available = True  # Always available
    
    def is_available(self) -> bool:
        """Sample client is always available"""
        return True
    
    def generate_content(self, request):
        """Generate sample content"""
        import time
        from ai_content_generator import generate_sample_ai_content, AIContentResponse
        
        start_time = time.time()
        sample_content = generate_sample_ai_content()
        content_key = request.content_type.value
        
        generated_text = sample_content.get(content_key, f"Sample {content_key} content")
        
        return AIContentResponse(
            content_type=request.content_type,
            generated_text=generated_text,
            confidence=0.5,
            tokens_used=0,
            processing_time=time.time() - start_time,
            metadata={'source': 'sample_content', 'provider': 'sample'}
        )
    
    def generate_all_cover_letter_content(self, job_description: str, profile_content: str, 
                                        company_name: str, position_title: str) -> dict:
        """Generate sample cover letter content"""
        from ai_content_generator import generate_sample_ai_content
        return generate_sample_ai_content()
    
    def extract_company_and_position(self, job_description: str) -> dict:
        """Extract basic company and position info"""
        # Try to parse structured header first
        try:
            from claude_api_client import ClaudeAPIClient
            claude_client = ClaudeAPIClient()
            return claude_client._parse_adressat_line(job_description)
        except:
            return {
                'company_name': 'Beispiel Unternehmen',
                'position_title': 'Position'
            }
    
    def get_provider_name(self) -> str:
        """Get provider name"""
        return "sample"
    
    def get_model_name(self) -> str:
        """Get model name"""
        return "content"