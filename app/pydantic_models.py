from typing import Union, List, Any
from pydantic import BaseModel, Field
from typing import Literal
class Message(BaseModel):
    role: Literal["system", "user", "assistant"] = Field(..., description="消息角色")
    content: Union[str, List[Any]] = Field(..., description="消息内容，字符串或JSON列表")


from typing import List, Literal, Optional, Union, Dict
from pydantic import BaseModel, Field
class ChatCompletionRequest(BaseModel):
    model: str = Field(..., description="模型，必填")
    messages: List[Message] = Field(..., description="消息列表，必填")
    temperature: Optional[float] = Field(1.0, ge=0, le=2, description="温度")
    top_p: Optional[float] = Field(1.0, ge=0, le=1, description="核采样")
    n: Optional[int] = Field(1, ge=1, description="生成数量")
    stream: Optional[bool] = Field(False, description="流式输出")
    stop: Optional[Union[str, List[str]]] = Field(None, description="停止序列")
    max_tokens: Optional[int] = Field(None, ge=1, description="最大令牌数")
    presence_penalty: Optional[float] = Field(0.0, description="存在惩罚")
    frequency_penalty: Optional[float] = Field(0.0, description="频率惩罚")
    logit_bias: Optional[Dict[str, float]] = Field(None, description="逻辑偏置")
    user: Optional[str] = Field(None, description="用户标识")
    tools: Optional[List[Any]] = Field(None, description="工具列表")
    tool_choice: Optional[Union[str, Dict[str, Any]]] = Field(None, description="工具选择")
    response_format: Optional[Dict[str, Any]] = Field(None, description="响应格式")