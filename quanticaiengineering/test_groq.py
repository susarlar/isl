"""
Test script to verify Groq API connection and basic functionality.

This script tests:
1. API key authentication
2. Model availability
3. Basic completion generation
4. Streaming responses
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_groq_connection():
    """Test basic Groq API connection."""
    print("=" * 60)
    print("Testing Groq API Connection")
    print("=" * 60)
    print()
    
    # Initialize client
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ Error: GROQ_API_KEY not found in .env file")
        return False
    
    print(f"✓ API Key found: {api_key[:20]}...")
    
    try:
        client = Groq(api_key=api_key)
        print("✓ Groq client initialized")
    except Exception as e:
        print(f"❌ Error initializing client: {e}")
        return False
    
    # Test with a simple query
    print()
    print("Testing completion with streaming...")
    print("-" * 60)
    print("Query: 'Explain what a RAG system is in one sentence.'")
    print("-" * 60)
    print()
    
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "user",
                    "content": "Explain what a RAG (Retrieval-Augmented Generation) system is in one sentence."
                }
            ],
            temperature=1,
            max_completion_tokens=1024,
            top_p=1,
            reasoning_effort="medium",
            stream=True,
            stop=None
        )
        
        print("Response: ", end="", flush=True)
        full_response = ""
        for chunk in completion:
            content = chunk.choices[0].delta.content or ""
            print(content, end="", flush=True)
            full_response += content
        
        print("\n")
        print("✓ Streaming completion successful")
        print(f"✓ Response length: {len(full_response)} characters")
        
    except Exception as e:
        print(f"\n❌ Error during completion: {e}")
        return False
    
    # Test with policy-related query
    print()
    print("Testing policy-related query...")
    print("-" * 60)
    print("Query: 'What are the key components of a good information security policy?'")
    print("-" * 60)
    print()
    
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "user",
                    "content": "List 3 key components that should be in a company information security policy."
                }
            ],
            temperature=0.7,
            max_completion_tokens=512,
            top_p=1,
            reasoning_effort="low",
            stream=True,
            stop=None
        )
        
        print("Response: ", end="", flush=True)
        for chunk in completion:
            content = chunk.choices[0].delta.content or ""
            print(content, end="", flush=True)
        
        print("\n")
        print("✓ Policy query successful")
        
    except Exception as e:
        print(f"\n❌ Error during policy query: {e}")
        return False
    
    print()
    print("=" * 60)
    print("✓ All tests passed!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Install remaining dependencies: pip install -r requirements.txt")
    print("2. Build vector database: python scripts/build_vector_db.py")
    print("3. Start querying: python app/query.py")
    print()
    
    return True


def test_model_availability():
    """Test different Groq models."""
    print()
    print("=" * 60)
    print("Testing Model Availability")
    print("=" * 60)
    print()
    
    api_key = os.getenv("GROQ_API_KEY")
    client = Groq(api_key=api_key)
    
    models_to_test = [
        "openai/gpt-oss-120b",
        "llama-3.1-70b-versatile",
        "llama-3.1-8b-instant",
    ]
    
    available_models = []
    
    for model in models_to_test:
        try:
            print(f"Testing {model}...", end=" ", flush=True)
            completion = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "Hi"}],
                max_completion_tokens=10,
                stream=False
            )
            print("✓ Available")
            available_models.append(model)
        except Exception as e:
            print(f"✗ Not available ({str(e)[:50]}...)")
    
    print()
    print(f"Available models: {len(available_models)}/{len(models_to_test)}")
    for model in available_models:
        print(f"  ✓ {model}")
    print()
    
    return available_models


if __name__ == "__main__":
    print()
    
    # Test basic connection
    success = test_groq_connection()
    
    if success:
        # Test model availability
        try:
            test_model_availability()
        except Exception as e:
            print(f"Warning: Could not test all models: {e}")
    else:
        print()
        print("⚠️  Connection test failed. Please check your API key and try again.")
        sys.exit(1)
