"""
Simple Groq API test - Minimal example
"""

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Initialize client from environment variable
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

print("Testing Groq API...")
print("=" * 60)
print()

# Create a streaming completion
completion = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {
            "role": "user",
            "content": "What is a Retrieval-Augmented Generation (RAG) system? Explain in 2-3 sentences."
        }
    ],
    temperature=1,
    max_completion_tokens=8192,
    top_p=1,
    reasoning_effort="medium",
    stream=True,
    stop=None
)

print("Response:")
print("-" * 60)
for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")

print("\n" + "=" * 60)
print("\n✓ Groq API test successful!")
