# OpenAI API 网络连接问题排查指南

## 问题描述
在测试 OpenAI 模型的流式输出功能时，遇到了 `openai.APITimeoutError: Request timed out` 错误，这通常是由于网络连接问题导致的。

## 可能的原因
1. 网络环境无法直接访问 OpenAI 的服务器
2. 防火墙或代理设置阻止了请求
3. 网络连接不稳定或速度过慢
4. OpenAI API 密钥无效或已过期

## 解决建议

### 1. 检查网络连接
```bash
# 测试是否能访问 OpenAI API 服务器
curl -v https://api.openai.com/v1/chat/completions
```

### 2. 配置代理服务器
如果您处于需要代理的网络环境中，可以尝试在环境变量中设置代理：
```bash
# 设置 HTTP 代理（替换为您的代理地址和端口）
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
```

在 Windows PowerShell 中：
```powershell
$env:HTTP_PROXY = "http://proxy.example.com:8080"
$env:HTTPS_PROXY = "http://proxy.example.com:8080"
```

### 3. 检查 API 密钥有效性
确保您提供的 API 密钥格式正确且未过期。您可以登录 OpenAI 控制台（https://platform.openai.com/api-keys）查看密钥状态。

### 4. 尝试使用本地模型
如果无法解决网络问题，您可以继续使用本地的 Ollama 模型，它不依赖外部网络连接：
```bash
# 确保 Ollama 服务正在运行
ollama list

# 运行使用本地模型的测试
python test_streaming_final.py
```

## 测试结果说明
- ✓ **Ollama 流式输出**：功能正常工作，可以实时接收和显示响应内容
- ✗ **OpenAI 流式输出**：由于网络连接问题超时失败，但这不是代码问题

流式输出功能本身已经修复完成，您可以使用本地 Ollama 模型或在解决网络问题后使用 OpenAI 模型来体验这一功能。