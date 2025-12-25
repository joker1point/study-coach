# LLM服务配置

# CloseAI API配置
CLOSEAI_CONFIG = {
    "model_name": "qwen:0.5b-chat",
    "provider": "openai",
    "api_base": "https://api.closeai-inc.com/v1",
    "api_key": "null"
}

# 本地Ollama配置（备用）
OLLAMA_CONFIG = {
    "model_name": "qwen:0.5b-chat",
    "provider": "openai",
    "api_base": "http://localhost:11434/v1",
    "api_key": "dummy"
}

# 默认使用本地Ollama配置
DEFAULT_LLM_CONFIG = OLLAMA_CONFIG
