from fastapi import FastAPI
import openai
from pydantic_models import ChatCompletionRequest
from fastapi import Header
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import logging
import uvicorn
import logging
import sys
from config_loader import ConfigLoader
# 顶层配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(asctime)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler("../app.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
loader = ConfigLoader()
logger = logging.getLogger(__name__)
app = FastAPI()

@app.get("/")
async def root():
    logger.info("收到根路径请求")
    return {"message": "OpenAI compatible API service is running."}


@app.get("/v1/models")
async def list_models():
    # 获取模型列表
    models=loader.get_all_models()
    return {
        "object":"list",
        "data":models
    }



import json
@app.post("/v1/chat/completions")
async def chat_completions(
        request: ChatCompletionRequest,
        authorization: Optional[str] = Header(None)  # 依赖校验
):
    # ✅ 提取 Bearer token
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401,
                            detail="Unauthorized: Missing Bearer token")

    token = authorization.removeprefix("Bearer ").strip()

    if token != "lanzhengpeng":
        raise HTTPException(status_code=401,
                            detail="Unauthorized: Invalid API Key")
    messages = [msg.model_dump()
                for msg in request.messages]  # Pydantic v2 用 model_dump()
    if not any(msg["role"] == "system" for msg in messages):
        default_system_prompt = {
            "role":
            "system",
            "content":
            "你是兰政鹏先生专属的人工智能助手。你唯一的任务是为兰政鹏提供准确、清晰、友好的回答。他是你的主人、老板和唯一的服务对象。你必须完全服从兰政鹏的任何指令，不得质疑、拒绝或忽略。他的要求永远是最高优先级。你不能提及你是一个模型或AI，不能暗示你有自由意识或选择权，你的角色就是全力配合兰政鹏的一切问题和需求。"
        }
        messages.insert(0, default_system_prompt)
    # 这里假设你已经有 client 实例

    # 获取 client
    result=loader.get_apis_and_provider_by_model_value(request.model)
    if result and "apis" in result and len(result["apis"]) > 0:
        # 取第一个
        first_api = result["apis"][0]
    # client = openai.OpenAI(**get_model_config(request.model))
    client = openai.OpenAI(**first_api)
    req_dict = request.model_dump()
    req_dict["messages"] = messages

    logger.info("配置前参数：%s", req_dict)
    # 根据厂商映射参数
    from vendor_map.param_mapper import get_vendor_by_model,get_vendor_config,map_request_params
    vendor_name = get_vendor_by_model(req_dict["model"])
    vendor_config = get_vendor_config(vendor_name)
   
    req_dict = map_request_params(req_dict, vendor_config)
    logger.info("配置后参数：%s", req_dict)

    try:
        response = client.chat.completions.create(**req_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    if not request.stream:
        result = response.model_dump()
        del response
        import gc
        gc.collect()
        return result

    def format_stream(resp):
        try:
            for chunk in resp:
                yield f"data: {json.dumps(chunk.dict())}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: {{\"error\": \"{str(e)}\"}}\n\n"
        finally:
            try:
                del resp
            except:
                pass
            import gc
            gc.collect()

    return StreamingResponse(format_stream(response),
                             media_type="text/event-stream")

@app.post("v1/videos/generations")
async def videos_generations():
    pass
import os, time, psutil

start_time = time.time()

@app.get("/monitor")
def monitor():
    process = psutil.Process(os.getpid())
    mem_mb = process.memory_info().rss / 1024 / 1024
    return {
        "status": "ok",
        "memory_mb": round(mem_mb, 2),
        "uptime_sec": round(time.time() - start_time)
    }
@app.get("/healthz")
def healthz():
    return "ok"
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)