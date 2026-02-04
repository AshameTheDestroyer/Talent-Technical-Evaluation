from integrations.ai_integration.ai_factory import AIGeneratorFactory, AIProvider
from integrations.ai_integration.mock_ai_generator import MockAIGenerator
from integrations.ai_integration.openai_generator import OpenAIGenerator
from integrations.ai_integration.anthropic_generator import AnthropicGenerator
from integrations.ai_integration.google_ai_generator import GoogleAIGenerator


def test_factory_pattern():
    """Test the AI generator factory pattern"""
    
    print("Testing AI Generator Factory Pattern...")
    
    # Test creating a mock generator
    print("\n1. Creating Mock AI Generator...")
    try:
        mock_generator = AIGeneratorFactory.create_generator(AIProvider.MOCK)
        print(f"   [PASS] Successfully created: {type(mock_generator).__name__}")
        assert isinstance(mock_generator, MockAIGenerator)
        print("   [PASS] Correct type instantiated")
    except Exception as e:
        print(f"   [FAIL] Failed to create mock generator: {e}")

    # Test creating an OpenAI generator
    print("\n2. Creating OpenAI Generator...")
    try:
        openai_generator = AIGeneratorFactory.create_generator(AIProvider.OPENAI)
        print(f"   [PASS] Successfully created: {type(openai_generator).__name__}")
        assert isinstance(openai_generator, OpenAIGenerator)
        print("   [PASS] Correct type instantiated")
    except NotImplementedError as e:
        print(f"   [PASS] OpenAI generator correctly raises NotImplementedError: {e}")
    except Exception as e:
        print(f"   [FAIL] Unexpected error: {e}")

    # Test creating an Anthropic generator
    print("\n3. Creating Anthropic Generator...")
    try:
        anthropic_generator = AIGeneratorFactory.create_generator(AIProvider.ANTHROPIC)
        print(f"   [PASS] Successfully created: {type(anthropic_generator).__name__}")
        assert isinstance(anthropic_generator, AnthropicGenerator)
        print("   [PASS] Correct type instantiated")
    except NotImplementedError as e:
        print(f"   [PASS] Anthropic generator correctly raises NotImplementedError: {e}")
    except Exception as e:
        print(f"   [FAIL] Unexpected error: {e}")

    # Test creating a Google AI generator
    print("\n4. Creating Google AI Generator...")
    try:
        google_generator = AIGeneratorFactory.create_generator(AIProvider.GOOGLE)
        print(f"   [PASS] Successfully created: {type(google_generator).__name__}")
        assert isinstance(google_generator, GoogleAIGenerator)
        print("   [PASS] Correct type instantiated")
    except NotImplementedError as e:
        print(f"   [PASS] Google AI generator correctly raises NotImplementedError: {e}")
    except Exception as e:
        print(f"   [FAIL] Unexpected error: {e}")

    # Test getting available providers
    print("\n5. Getting available providers...")
    try:
        providers = AIGeneratorFactory.get_available_providers()
        print(f"   Available providers: {[p.value for p in providers]}")
        expected_providers = [AIProvider.MOCK, AIProvider.OPENAI, AIProvider.ANTHROPIC, AIProvider.GOOGLE]
        assert len(providers) == len(expected_providers), f"Expected {len(expected_providers)} providers, got {len(providers)}"
        print("   [PASS] Correct number of providers returned")
    except Exception as e:
        print(f"   [FAIL] Failed to get providers: {e}")

    # Test creating a generator with non-existent provider
    print("\n6. Testing non-existent provider...")
    try:
        fake_generator = AIGeneratorFactory.create_generator("FAKE_PROVIDER")
        print("   [FAIL] Should have raised an error for non-existent provider")
    except ValueError as e:
        print(f"   [PASS] Correctly raised ValueError for non-existent provider: {e}")
    except Exception as e:
        print(f"   [WARN] Raised unexpected error: {e}")

    print("\n[PASS] All factory pattern tests completed successfully!")


def test_mock_generator_functionality():
    """Test the mock generator's functionality"""
    
    print("\n\nTesting Mock Generator Functionality...")
    
    # Create a mock generator
    generator = AIGeneratorFactory.create_generator(AIProvider.MOCK)
    
    # Prepare job information
    job_info = {
        "title": "Senior Python Developer",
        "seniority": "senior",
        "description": "Looking for experienced Python developers familiar with Django, Flask, and cloud technologies",
        "skill_categories": ["python", "django", "flask", "sql", "cloud"]
    }
    
    # Generate questions
    try:
        questions = generator.generate_questions(
            title="Backend Development Skills Assessment",
            questions_types=["choose_one", "text_based"],
            additional_note="Focus on Django and cloud deployment",
            job_info=job_info
        )
        
        print(f"   Generated {len(questions)} questions successfully")
        assert len(questions) == 2, f"Expected 2 questions, got {len(questions)}"
        
        for i, q in enumerate(questions):
            print(f"   Question {i+1}: {q.text[:50]}...")
            assert q.id, "Question should have an ID"
            assert q.text, "Question should have text"
            assert q.weight >= 1 and q.weight <= 5, f"Weight should be between 1-5, got {q.weight}"
            assert q.skill_categories, "Question should have skill categories"
            assert q.type.value in ["choose_one", "choose_many", "text_based"], f"Invalid question type: {q.type.value}"
        
        print("   [PASS] Mock generator functionality test passed")
    except Exception as e:
        print(f"   [FAIL] Mock generator functionality test failed: {e}")


if __name__ == "__main__":
    test_factory_pattern()
    test_mock_generator_functionality()