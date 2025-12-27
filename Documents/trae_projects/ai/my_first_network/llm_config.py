# LLM服务配置
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 统一大模型接口网关配置
UNIFIED_GATEWAY_CONFIG = {
    "model_name": os.getenv("LLM_MODEL_NAME", "gpt-4o-mini"),
    "provider": os.getenv("LLM_PROVIDER", "openai"),
    "api_base": os.getenv("LLM_API_BASE", "http://205.185.126.106:3000/v1"),
    "api_key": os.getenv("LLM_API_KEY", "")
}

# 本地Ollama配置（备用）
OLLAMA_CONFIG = {
    "model_name": os.getenv("OLLAMA_MODEL_NAME", "qwen:0.5b-chat"),
    "provider": os.getenv("OLLAMA_PROVIDER", "openai"),
    "api_base": os.getenv("OLLAMA_API_BASE", "http://localhost:11434/v1"),
    "api_key": os.getenv("OLLAMA_API_KEY", "dummy")
}

# 默认使用统一大模型接口网关
DEFAULT_LLM_CONFIG = UNIFIED_GATEWAY_CONFIG

# 验证API密钥是否存在
if not UNIFIED_GATEWAY_CONFIG["api_key"]:
    print("⚠️ 警告：未设置LLM_API_KEY环境变量，可能导致API调用失败")
    print("请设置环境变量或在.env文件中配置API密钥")
