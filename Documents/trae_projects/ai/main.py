from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from model_router import model_router

# 创建FastAPI应用
app = FastAPI(
    title="本地Ollama模型API",
    description="提供本地Ollama大语言模型的API接口",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制为特定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载模型路由
app.include_router(model_router)

# 根路由
@app.get("/")
def read_root():
    return {
        "message": "本地Ollama模型API服务已启动",
        "docs": "/docs",
        "redoc": "/redoc"
    }

# 健康检查路由
@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8700, reload=True)