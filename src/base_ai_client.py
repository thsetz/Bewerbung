#!/usr/bin/env python3
"""
Base AI Client - Abstract interface for different AI providers
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from ai_content_generator import AIContentRequest, AIContentResponse


class BaseAIClient(ABC):
    """Abstract base class for AI content generation clients"""
    
    def __init__(self, base_dir: str = "."):
        self.base_dir = base_dir
        self.available = False
        
    @abstractmethod
    def is_available(self) -> bool:
        """Check if AI client is available and configured"""
        pass
    
    @abstractmethod
    def generate_content(self, request: AIContentRequest) -> AIContentResponse:
        """Generate AI content for the given request"""
        pass
    
    @abstractmethod
    def generate_all_cover_letter_content(self, job_description: str, profile_content: str, 
                                        company_name: str, position_title: str) -> Dict[str, str]:
        """Generate all cover letter content variables at once"""
        pass
    
    @abstractmethod
    def extract_company_and_position(self, job_description: str) -> Dict[str, str]:
        """Extract company name and position title from job description"""
        pass
    
    def get_provider_name(self) -> str:
        """Get the name of the AI provider"""
        return self.__class__.__name__.replace('APIClient', '').replace('Client', '').lower()
    
    @abstractmethod
    def get_model_name(self) -> str:
        """Get the specific model name (e.g., 'sonnet-4', '3.2-3b', 'content')"""
        pass
    
    def get_client_model_folder(self) -> str:
        """Get formatted folder name for client and model"""
        provider = self.get_provider_name()
        model = self.get_model_name()
        
        # Sanitize folder name
        folder_name = f"{provider}_{model}"
        # Replace problematic characters for filesystem
        folder_name = folder_name.replace(':', '-').replace('/', '-').replace('\\', '-')
        folder_name = folder_name.replace(' ', '_').replace('.', '-')
        
        return folder_name
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get usage statistics"""
        return {
            'provider': self.get_provider_name(),
            'model': self.get_model_name(),
            'folder': self.get_client_model_folder(),
            'available': self.is_available()
        }
    
    def test_content_generation(self) -> bool:
        """Test content generation with sample data"""
        try:
            from ai_content_generator import ContentType
            
            test_request = AIContentRequest(
                content_type=ContentType.EINSTIEGSTEXT,
                job_description="Wir suchen einen DevOps Engineer für unser innovatives Team.",
                profile_content="Erfahrener DevOps Engineer mit 5 Jahren Kubernetes-Erfahrung.",
                company_name="TechCorp",
                position_title="DevOps Engineer"
            )
            
            response = self.generate_content(test_request)
            print(f"✓ {self.get_provider_name()} test successful: {response.generated_text[:100]}...")
            return True
        except Exception as e:
            print(f"✗ {self.get_provider_name()} test failed: {e}")
            return False


class AIProviderError(Exception):
    """Exception raised when AI provider is not available or configured incorrectly"""
    pass


class AIContentError(Exception):
    """Exception raised when AI content generation fails"""
    pass