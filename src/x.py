from llama_api_client import LlamaAPIClient

from ai_content_generator import (
    AIContentRequest, AIContentResponse, ContentType, 
    ContentCache, generate_sample_ai_content
)


print("Hello AI")

client = LlamaAPIClient("..")