"""
多模型客户端封装，提供统一接口
"""

from typing import Dict, Any, List, Optional
import httpx
import json
from abc import ABC, abstractmethod


class BaseModelClient(ABC):
    """模型客户端基类"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.api_key = config.get("api_key")
        self.base_url = config.get("base_url")
        self.model_name = config.get("model_name")
        
    @abstractmethod
    async def chat_completion(self, messages: List[Dict], **kwargs) -> Dict[str, Any]:
        """聊天完成接口"""
        pass
    
    @abstractmethod
    async def text_completion(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """文本完成接口"""
        pass


class OpenAIClient(BaseModelClient):
    """OpenAI API客户端"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.base_url = self.base_url or "https://api.openai.com/v1"
    
    async def chat_completion(self, messages: List[Dict], **kwargs) -> Dict[str, Any]:
        """OpenAI聊天完成"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model_name,
            "messages": messages,
            **kwargs
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=60.0
            )
            response.raise_for_status()
            return response.json()
    
    async def text_completion(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """OpenAI文本完成"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model_name,
            "prompt": prompt,
            **kwargs
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/completions",
                headers=headers,
                json=data,
                timeout=60.0
            )
            response.raise_for_status()
            return response.json()


class ClaudeClient(BaseModelClient):
    """Anthropic Claude API客户端"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.base_url = self.base_url or "https://api.anthropic.com/v1"
    
    async def chat_completion(self, messages: List[Dict], **kwargs) -> Dict[str, Any]:
        """Claude聊天完成"""
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        # 转换消息格式
        claude_messages = self._convert_messages_to_claude(messages)
        
        data = {
            "model": self.model_name,
            "messages": claude_messages,
            "max_tokens": kwargs.get("max_tokens", 1000),
            **{k: v for k, v in kwargs.items() if k != "max_tokens"}
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/messages",
                headers=headers,
                json=data,
                timeout=60.0
            )
            response.raise_for_status()
            return self._convert_claude_response(response.json())
    
    async def text_completion(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Claude文本完成"""
        # Claude不直接支持text completion，转换为chat completion
        messages = [{"role": "user", "content": prompt}]
        return await self.chat_completion(messages, **kwargs)
    
    def _convert_messages_to_claude(self, messages: List[Dict]) -> List[Dict]:
        """转换消息格式为Claude格式"""
        claude_messages = []
        for msg in messages:
            claude_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        return claude_messages
    
    def _convert_claude_response(self, response: Dict) -> Dict:
        """转换Claude响应为OpenAI格式"""
        return {
            "id": response.get("id", "claude-response"),
            "object": "chat.completion",
            "created": 1234567890,  # 时间戳
            "model": self.model_name,
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": response["content"][0]["text"]
                },
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": response.get("usage", {}).get("input_tokens", 0),
                "completion_tokens": response.get("usage", {}).get("output_tokens", 0),
                "total_tokens": response.get("usage", {}).get("input_tokens", 0) + response.get("usage", {}).get("output_tokens", 0)
            }
        }


class QwenClient(BaseModelClient):
    """阿里云通义千问API客户端"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.base_url = self.base_url or "https://dashscope.aliyuncs.com/api/v1"
    
    async def chat_completion(self, messages: List[Dict], **kwargs) -> Dict[str, Any]:
        """通义千问聊天完成"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model_name,
            "input": {"messages": messages},
            "parameters": kwargs
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/services/aigc/text-generation/generation",
                headers=headers,
                json=data,
                timeout=60.0
            )
            response.raise_for_status()
            return self._convert_qwen_response(response.json())
    
    async def text_completion(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """通义千问文本完成"""
        messages = [{"role": "user", "content": prompt}]
        return await self.chat_completion(messages, **kwargs)
    
    def _convert_qwen_response(self, response: Dict) -> Dict:
        """转换通义千问响应为OpenAI格式"""
        output = response.get("output", {})
        usage = response.get("usage", {})
        
        return {
            "id": response.get("request_id", "qwen-response"),
            "object": "chat.completion",
            "created": 1234567890,
            "model": self.model_name,
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": output.get("text", "")
                },
                "finish_reason": output.get("finish_reason", "stop")
            }],
            "usage": {
                "prompt_tokens": usage.get("input_tokens", 0),
                "completion_tokens": usage.get("output_tokens", 0),
                "total_tokens": usage.get("total_tokens", 0)
            }
        }


class ModelClientManager:
    """模型客户端管理器"""
    
    CLIENT_CLASSES = {
        "openai": OpenAIClient,
        "claude": ClaudeClient,
        "qwen": QwenClient,
    }
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.clients = {}
        self._init_clients()
    
    def _init_clients(self):
        """初始化所有配置的客户端"""
        models = self.config.get("models", {})
        
        for model_alias, model_config in models.items():
            provider = model_config.get("provider")
            if provider in self.CLIENT_CLASSES:
                client_class = self.CLIENT_CLASSES[provider]
                self.clients[model_alias] = client_class(model_config)
    
    def get_client(self, model_alias: str) -> Optional[BaseModelClient]:
        """获取指定模型的客户端"""
        return self.clients.get(model_alias)
    
    def get_available_models(self) -> List[str]:
        """获取所有可用的模型别名"""
        return list(self.clients.keys())
    
    async def chat_completion(self, model_alias: str, messages: List[Dict], **kwargs) -> Dict[str, Any]:
        """通过指定模型进行聊天完成"""
        client = self.get_client(model_alias)
        if not client:
            raise ValueError(f"模型 {model_alias} 不存在")
        
        return await client.chat_completion(messages, **kwargs)
    
    async def text_completion(self, model_alias: str, prompt: str, **kwargs) -> Dict[str, Any]:
        """通过指定模型进行文本完成"""
        client = self.get_client(model_alias)
        if not client:
            raise ValueError(f"模型 {model_alias} 不存在")
        
        return await client.text_completion(prompt, **kwargs)
