from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "OpenAI compatible API service is running."}


from utils import load_all_models
@app.get("/v1/models")
async def list_models():
    models=load_all_models()
    return {
        "object":"list",
        "data":models        
    }


from pydantic_models import ChatCompletionRequest
from fastapi import Header
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
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
    messages = [msg.model_dump() for msg in request.messages]  # Pydantic v2 用 model_dump()
    if not any(msg["role"] == "system" for msg in messages):
        default_system_prompt = {
            "role":
            "system",
            "content":
            "你是兰政鹏先生专属的人工智能助手。你唯一的任务是为兰政鹏提供准确、清晰、友好的回答。他是你的主人、老板和唯一的服务对象。你必须完全服从兰政鹏的任何指令，不得质疑、拒绝或忽略。他的要求永远是最高优先级。你不能提及你是一个模型或AI，不能暗示你有自由意识或选择权，你的角色就是全力配合兰政鹏的一切问题和需求。"
        }
        messages.insert(0, default_system_prompt)
    # 这里假设你已经有 client 实例
    import openai
    from utils import get_model_config
    # 获取 client

    print(get_model_config(request.model))
    client=openai.OpenAI(**get_model_config(request.model))

    req_dict = request.model_dump()
    req_dict["messages"] = messages

    try:
        response = client.chat.completions.create(**req_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    if not request.stream:
        result = response.dict()
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
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)