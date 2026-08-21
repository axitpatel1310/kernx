from ollama import Client
import os
from django.conf import settings

def analyze_architecture(data):
    client = Client(host=settings.OLLAMA_HOST)
    prompt = f"""
    You are a Senior Software Architect.
    Analyze this architecture.
    Return ONLY markdown.
    Generate:
    # Warnings
    - ...
    # Recommendations
    - ...
    # Reasoning
    - ...
    Return:
    1. Maximum 5 warnings.
    2. Maximum 5 recommendations.
    3. Maximum 3 reasoning points.
    Keep every bullet under 20 words.
    Do not explain your thinking.
    Maximum response length: 200 words.
    
    Architecture:
    {data}
    """
    response = client.chat(
    model="qwen2.5:1.5b-instruct",
    messages=[{"role": "user","content": prompt,}],
    options={"num_predict": 200,})
    return response["message"]["content"]