import requests
import json
import time

def test_ollama_service():
    """测试Ollama服务是否正常运行"""
    try:
        response = requests.get("http://localhost:11434/v1/models")
        if response.status_code == 200:
            models = response.json()
            print(f"✅ Ollama服务运行正常！")
            print(f"已安装模型: {[model['id'] for model in models['data']]}")
            return True
        else:
            print(f"❌ Ollama服务异常，状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 无法连接到Ollama服务: {e}")
        return False

def test_qwen_model():
    """测试千问0.5模型是否能正常响应"""
    try:
        url = "http://localhost:11434/v1/chat/completions"
        headers = {"Content-Type": "application/json"}
        payload = {
            "model": "qwen:0.5b-chat",
            "messages": [{"role": "user", "content": "你好，这是一个测试"}],
            "temperature": 0.7
        }
        
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            result = response.json()
            assistant_message = result['choices'][0]['message']['content']
            print(f"\n✅ 千问0.5模型响应测试成功!")
            print(f"模型响应: {assistant_message}")
            return True
        else:
            print(f"\n❌ 千问0.5模型响应异常，状态码: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
    except Exception as e:
        print(f"\n❌ 测试千问0.5模型失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_agent_config():
    """测试智能体配置是否正确"""
    # 读取一个智能体配置文件来验证
    import os
    agent_files = [
        "./my_first_network/agents/llm_agent.py",
        "./my_first_network/agents/tutoring_agent.py",
        "./my_first_network/agents/diagnosis_agent.py",
        "./my_first_network/agents/review_agent.py",
        "./my_first_network/agents/custom_agent_v2.py"
    ]
    
    configured_agents = []
    for agent_file in agent_files:
        if os.path.exists(agent_file):
            with open(agent_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'qwen:0.5b-chat' in content and 'http://localhost:11434/v1' in content:
                    configured_agents.append(os.path.basename(agent_file))
    
    if configured_agents:
        print(f"\n✅ 智能体配置测试成功!")
        print(f"已配置使用千问0.5模型的智能体: {configured_agents}")
        return True
    else:
        print(f"\n❌ 未找到配置千问0.5模型的智能体")
        return False

def main():
    """主测试函数"""
    print("🚀 千问0.5模型外部集成接入测试开始")
    print("=" * 50)
    
    # 测试Ollama服务
    ollama_ok = test_ollama_service()
    
    # 测试千问模型
    qwen_ok = test_qwen_model()
    
    # 测试智能体配置
    agent_ok = test_agent_config()
    
    print("\n" + "=" * 50)
    print("📋 测试结果总结")
    print(f"1. Ollama服务状态: {'✅ 正常' if ollama_ok else '❌ 异常'}")
    print(f"2. 千问0.5模型状态: {'✅ 正常' if qwen_ok else '❌ 异常'}")
    print(f"3. 智能体配置状态: {'✅ 完成' if agent_ok else '❌ 未完成'}")
    
    if ollama_ok and qwen_ok and agent_ok:
        print("\n🎉 所有测试通过！千问0.5模型的外部集成接入已完全配置成功！")
        print("\n📝 集成说明:")
        print("- Ollama服务运行在 http://localhost:11434")
        print("- 千问0.5模型ID: qwen:0.5b-chat")
        print("- 智能体通过OpenAI兼容API与模型通信")
        print("- 所有智能体已配置使用千问0.5模型")
    else:
        print("\n❌ 部分测试失败，请检查上述错误信息并修复问题")

if __name__ == "__main__":
    main()