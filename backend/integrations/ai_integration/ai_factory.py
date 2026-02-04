from enum import Enum
from typing import Dict, Type
from integrations.ai_integration.ai_generator_interface import AIGeneratorInterface
from integrations.ai_integration.mock_ai_generator import MockAIGenerator
from integrations.ai_integration.openai_generator import OpenAIGenerator
from integrations.ai_integration.anthropic_generator import AnthropicGenerator
from integrations.ai_integration.google_ai_generator import GoogleAIGenerator


class AIProvider(Enum):
    """
    Enum representing different AI providers that can be used.
    """
    MOCK = "mock"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"


class AIGeneratorFactory:
    """
    Factory class for creating AI generator instances.
    Allows for easy addition of new AI providers without changing existing code.
    """
    
    _providers: Dict[AIProvider, Type[AIGeneratorInterface]] = {}
    
    @classmethod
    def register_provider(cls, provider: AIProvider, generator_class: Type[AIGeneratorInterface]):
        """
        Register a new AI provider with the factory.
        
        Args:
            provider: The AI provider enum value
            generator_class: The class that implements AIGeneratorInterface
        """
        cls._providers[provider] = generator_class
    
    @classmethod
    def create_generator(cls, provider: AIProvider) -> AIGeneratorInterface:
        """
        Create an instance of the specified AI generator.
        
        Args:
            provider: The AI provider to instantiate
            
        Returns:
            An instance of the requested AI generator
            
        Raises:
            ValueError: If the provider is not registered
        """
        if provider not in cls._providers:
            raise ValueError(f"AI provider {provider} is not registered")
        
        generator_class = cls._providers[provider]
        return generator_class()
    
    @classmethod
    def get_available_providers(cls) -> list:
        """
        Get a list of available AI providers.
        
        Returns:
            List of available AI providers
        """
        return list(cls._providers.keys())


# Register all available providers
AIGeneratorFactory.register_provider(AIProvider.MOCK, MockAIGenerator)
AIGeneratorFactory.register_provider(AIProvider.OPENAI, OpenAIGenerator)
AIGeneratorFactory.register_provider(AIProvider.ANTHROPIC, AnthropicGenerator)
AIGeneratorFactory.register_provider(AIProvider.GOOGLE, GoogleAIGenerator)


# Optional: Create a default provider
DEFAULT_PROVIDER = AIProvider.MOCK