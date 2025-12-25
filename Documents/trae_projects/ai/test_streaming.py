# Test script for LLM streaming output
# This script directly tests the streaming functionality of the LLM provider

from openagents.lms.providers import OpenAIProvider

async def test_streaming():
    # 直接设置API密钥（移除中文引号）
    api_key = "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"
    
    # 初始化OpenAI提供商
    provider = OpenAIProvider(model_name="gpt-3.5-turbo", api_key=api_key)
    
    # Test streaming output
    print("Testing streaming output...")
    print("=" * 50)
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is OpenAgents? Please explain in detail."}
    ]
    
    try:
        # Call chat_completion with stream=True
        response = await provider.chat_completion(messages, stream=True)
        
        # If streaming is supported, response should have __aiter__ method
        if hasattr(response, '__aiter__'):
            print("✓ Streaming response received. Processing chunks...")
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
        else:
            print("✗ Streaming not supported or response is not a stream")
            print(f"Response type: {type(response)}")
            
    except Exception as e:
        print(f"✗ Error during streaming test: {e}")
        import traceback
        traceback.print_exc()

# Run the test
if __name__ == "__main__":
    import asyncio
    asyncio.run(test_streaming())
