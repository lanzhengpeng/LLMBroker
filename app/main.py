"""
FastAPI 应用入口和路由定义
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Dict, Any
import json

from .config import load_and_validate_config as load_config
from .proxy import LLMProxy
from .clients import ModelClientManager

app = FastAPI(
    title="LLMBroker",
    description="统一多个LLM模型的API代理服务",
    version="1.0.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局变量
config = None
llm_proxy = None
client_manager = None


@app.on_event("startup")
async def startup_event():
    """应用启动时初始化配置和服务"""
    global config, llm_proxy, client_manager
    
    try:
        config = load_config()
        client_manager = ModelClientManager(config)
        llm_proxy = LLMProxy(config, client_manager)
        print("LLMBroker 服务启动成功!")
    except Exception as e:
        print(f"服务启动失败: {e}")
        raise


@app.get("/")
async def root():
    """根路径，返回服务信息"""
    return {
        "service": "LLMBroker",
        "version": "1.0.0",
        "description": "LLM模型代理服务",
        "status": "running"
    }


@app.get("/models")
async def list_models():
    """获取所有可用的模型列表"""
    try:
        models = client_manager.get_available_models()
        return {"models": models}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    """
    统一的聊天完成接口
    兼容OpenAI API格式
    """
    try:
        # 获取请求体
        body = await request.json()
        
        # 通过代理处理请求
        response = await llm_proxy.handle_chat_request(body)
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/completions")
async def completions(request: Request):
    """
    文本完成接口
    兼容OpenAI API格式
    """
    try:
        # 获取请求体
        body = await request.json()
        
        # 通过代理处理请求
        response = await llm_proxy.handle_completion_request(body)
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy", "timestamp": "2025-08-07"}


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
