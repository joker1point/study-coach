import requests
import json

# 测试非流式调用
def test_chat():
    print("测试非流式调用...")
    url = "http://localhost:8700/api/model/chat"
    payload = {
        "prompt": "你好，简单介绍一下你自己",
        "model": "qwen:0.5b-chat",
        "max_tokens": 500,
        "temp": 0.7
    }
    try:
        response = requests.post(url, json=payload, timeout=60)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"成功: {result['success']}")
            print(f"内容: {result['content']}")
            print(f"耗时: {result['time_cost']}秒")
        else:
            print(f"请求失败: {response.text}")
    except Exception as e:
        print(f"请求异常: {str(e)}")
    print()

# 测试流式调用
def test_chat_stream():
    print("测试流式调用...")
    url = "http://localhost:8700/api/model/chat/stream"
    payload = {
        "prompt": "你好，简单介绍一下你自己",
        "model": "qwen:0.5b-chat"
    }
    try:
        response = requests.post(url, json=payload, stream=True, timeout=60)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            print("流式输出内容:")
            full_content = ""
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    if "content" in chunk and chunk["content"]:
                        content = chunk["content"]
                        full_content += content
                        print(content, end="", flush=True)
                    if chunk.get("done", False):
                        break
            print()
            print(f"完整内容: {full_content}")
        else:
            print(f"请求失败: {response.text}")
    except Exception as e:
        print(f"请求异常: {str(e)}")
    print()

if __name__ == "__main__":
    print("=== 测试Ollama OpenAI兼容接口 ===")
    test_chat()
    test_chat_stream()
    print("=== 测试完成 ===")
