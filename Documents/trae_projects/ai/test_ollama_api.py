import requests
import json

# 测试普通调用
def test_chat():
    print("=== 测试普通调用 ===")
    url = "http://localhost:8700/api/model/chat"
    data = {
        "prompt": "什么是OpenAgents？",
        "model": "qwen:0.5b-chat",
        "max_tokens": 512,
        "temp": 0.7
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        result = response.json()
        print(f"内容: {result.get('choices', [{}])[0].get('message', {}).get('content')}")
    else:
        print(f"调用失败: {response.status_code} - {response.text}")

# 测试流式调用
def test_chat_stream():
    print("\n=== 测试流式调用 ===")
    url = "http://localhost:8700/api/model/chat/stream"
    data = {
        "prompt": "请简单介绍一下FastAPI",
        "model": "qwen:0.5b-chat"
    }
    response = requests.post(url, json=data, stream=True)
    if response.status_code == 200:
        print("流式响应:")
        for line in response.iter_lines():
            if line:
                chunk = json.loads(line)
                print(chunk.get('choices', [{}])[0].get('delta', {}).get('content', ''), end='')
                if chunk.get('done'):
                    print()
                    break
    else:
        print(f"调用失败: {response.status_code} - {response.text}")

if __name__ == "__main__":
    test_chat()
    test_chat_stream()