# Test script for LLM streaming output
# This script tests streaming functionality with both OpenAI and local Ollama models

import asyncio
from openagents.lms.providers import OpenAIProvider, SimpleGenericProvider

async def test_streaming_with_provider(provider, provider_name):
    # Test streaming output
    print(f"\n=== Testing streaming output with {provider_name} ===")
    print("=" * 50)
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is OpenAgents? Please explain briefly."}
    ]
    
    try:
        # Call chat_completion with stream=True
        response = await provider.chat_completion(messages, stream=True)
        
        # If streaming is supported, response should have __aiter__ method
        if hasattr(response, '__aiter__'):
            print(f"✓ Streaming response received from {provider_name}. Processing chunks...")
            print("\nResponse:")
            print("-" * 30)
            
            full_response = ""
            async for chunk in response:
                # Process the chunk based on OpenAI's streaming format
                if hasattr(chunk, 'choices') and chunk.choices:
                    for choice in chunk.choices:
                        if hasattr(choice, 'delta') and hasattr(choice.delta, 'content') and choice.delta.content:
                            content = choice.delta.content
                            print(content, end="", flush=True)
                            full_response += content
            
            print("\n" + "-" * 30)
            print(f"\n✓ Streaming completed. Total response length: {len(full_response)} characters")
            return True
        else:
            print(f"✗ Streaming not supported or response is not a stream from {provider_name}")
            print(f"Response type: {type(response)}")
            return False
            
    except Exception as e:
        print(f"✗ Error during streaming test with {provider_name}: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    print("OpenAgents Streaming Output Test")
    print("=" * 50)
    
    # Test with local Ollama model
    print("\n1. Testing with local Ollama model (recommended for offline testing)")
    ollama_provider = SimpleGenericProvider(
        model_name="qwen:0.5b-chat",
        api_base="http://localhost:11434/v1",
        api_key="dummy"  # Ollama doesn't require a real API key
    )
    ollama_success = await test_streaming_with_provider(ollama_provider, "Ollama")
    
    # Test with OpenAI using provided API key
    print("\n2. Testing with OpenAI (using provided API key)")
    try:
        # Use the API key provided by the user
        openai_api_key = "sk-JYboHoX9v6bsIr0ZND31tSTi6JcOV0D9AZ1Pws4zA3UCqlvY"
        openai_provider = OpenAIProvider(model_name="gpt-3.5-turbo", api_key=openai_api_key)
        openai_success = await test_streaming_with_provider(openai_provider, "OpenAI")
    except Exception as e:
        print(f"✗ Failed to initialize OpenAI provider: {e}")
        openai_success = False
    
    print("\n" + "=" * 50)
    print("Test Results Summary:")
    print(f"- Ollama streaming: {'SUCCESS' if ollama_success else 'FAILED'}")
    print(f"- OpenAI streaming: {'SUCCESS' if openai_success else 'FAILED'}")
    
    if ollama_success or openai_success:
        print("\n✓ Streaming output functionality is working!")
    else:
        print("\n✗ Streaming output functionality is not working with any tested provider")

# Run the test
if __name__ == "__main__":
    asyncio.run(main())
