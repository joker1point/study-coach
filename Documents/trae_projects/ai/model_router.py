from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import StreamingResponse
from openai import OpenAI
import json
import asyncio
import time

# 路由配置
model_router = APIRouter(prefix="/api/model", tags=["本地模型"])

# 全局Ollama客户端（使用OpenAI兼容接口）
class OllamaClient:
    def __init__(self, host="http://localhost:11434", default_model="qwen:7b"):
        self.host = host
        self.default_model = default_model
        self.client = OpenAI(
            base_url=f"{self.host}/v1",
            api_key="xx"  # Ollama兼容接口不需要真实API密钥，任意字符串即可
        )
        if not self._check_service():
            raise RuntimeError("Ollama服务未启动，请检查11434端口")

    def _check_service(self) -> bool:
        """检查服务可用性"""
        try:
            # 使用OpenAI兼容接口的models端点检查服务状态
            self.client.models.list(timeout=5)
            return True
        except:
            return False

    def chat(self, prompt: str, model=None, max_tokens=1024, temp=0.7):
        """普通调用（非流式） - 返回与OpenAI API兼容的格式"""
        model = model or self.default_model
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temp,
                stream=False
            )
            # 返回与OpenAI API兼容的格式
            current_time = int(time.time())
            return {
                "choices": [
                    {
                        "message": {
                            "content": response.choices[0].message.content.strip(),
                            "role": "assistant"
                        },
                        "finish_reason": "stop",
                        "index": 0
                    }
                ],
                "created": current_time,
                "id": f"chatcmpl-{str(current_time)}",
                "model": model,
                "object": "chat.completion",
                "usage": {
                    "completion_tokens": len(response.choices[0].message.content),
                    "prompt_tokens": len(prompt),
                    "total_tokens": len(prompt) + len(response.choices[0].message.content)
                }
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"调用失败：{str(e)}")

    def chat_stream(self, prompt: str, model=None, max_tokens=1024, temp=0.7):
        """流式调用（同步）"""
        model = model or self.default_model
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temp,
                stream=True
            )
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    yield json.dumps({
                        "choices": [{
                            "delta": {
                                "content": chunk.choices[0].delta.content
                            },
                            "finish_reason": None,
                            "index": 0
                        }],
                        "created": int(time.time()),
                        "id": f"chatcmpl-{str(time.time())}-stream",
                        "model": model,
                        "object": "chat.completion.chunk"
                    }, ensure_ascii=False) + "\n"
            yield json.dumps({
                "choices": [{
                    "delta": {},
                    "finish_reason": "stop",
                    "index": 0
                }],
                "created": int(time.time()),
                "id": f"chatcmpl-{str(time.time())}-stream",
                "model": model,
                "object": "chat.completion.chunk"
            }, ensure_ascii=False) + "\n"
        except Exception as e:
            yield json.dumps({
                "error": {
                    "message": str(e),
                    "type": "server_error"
                },
                "object": "error"
            }, ensure_ascii=False) + "\n"

# 初始化（替换为你的本地模型名）
ollama_client = OllamaClient(default_model="qwen:0.5b-chat")

# 接口定义
@model_router.post("/chat")
def model_chat(
    prompt: str = Body(..., description="用户输入"),
    model: str = Body(None),
    max_tokens: int = Body(1024, ge=1),
    temp: float = Body(0.7, ge=0.0, le=1.0)
):
    return ollama_client.chat(prompt, model, max_tokens, temp)

@model_router.post("/chat/stream")
def model_chat_stream(prompt: str = Body(...), model: str = Body(None)):
    return StreamingResponse(ollama_client.chat_stream(prompt, model), media_type="application/x-ndjson")