"""
工具函数模块
"""

from typing import Dict, Any, Optional
import json
import logging
from datetime import datetime


def merge_parameters(default_params: Dict[str, Any], request_params: Dict[str, Any]) -> Dict[str, Any]:
    """
    合并默认参数和请求参数
    请求参数优先级更高
    """
    merged = default_params.copy()
    merged.update(request_params)
    return merged


def extract_model_from_request(request: Dict[str, Any], default_model: str) -> str:
    """
    从请求中提取模型名称
    如果没有指定模型，使用默认模型
    """
    return request.get("model", default_model)


def log_request(logger: logging.Logger, request_type: str, model_alias: str, request: Dict[str, Any]):
    """
    记录请求日志
    """
    # 构建日志信息，隐藏敏感信息
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "request_type": request_type,
        "model_alias": model_alias,
        "request_size": len(json.dumps(request)),
    }
    
    # 如果是聊天请求，记录消息数量
    if request_type == "chat_completion" and "messages" in request:
        log_data["message_count"] = len(request["messages"])
    
    # 如果是文本完成请求，记录提示词长度
    if request_type == "text_completion" and "prompt" in request:
        log_data["prompt_length"] = len(request["prompt"])
    
    logger.info(f"处理请求: {json.dumps(log_data, ensure_ascii=False)}")


def sanitize_response(response: Dict[str, Any]) -> Dict[str, Any]:
    """
    清理响应数据，移除敏感信息
    """
    # 创建响应副本
    sanitized = response.copy()
    
    # 移除可能的敏感字段
    sensitive_fields = ["api_key", "authorization", "x-api-key"]
    
    def remove_sensitive_fields(obj):
        if isinstance(obj, dict):
            return {k: remove_sensitive_fields(v) for k, v in obj.items() 
                   if k.lower() not in sensitive_fields}
        elif isinstance(obj, list):
            return [remove_sensitive_fields(item) for item in obj]
        else:
            return obj
    
    return remove_sensitive_fields(sanitized)


def validate_chat_messages(messages: list) -> bool:
    """
    验证聊天消息格式
    """
    if not isinstance(messages, list):
        return False
    
    for message in messages:
        if not isinstance(message, dict):
            return False
        
        if "role" not in message or "content" not in message:
            return False
        
        if message["role"] not in ["system", "user", "assistant"]:
            return False
    
    return True


def validate_completion_prompt(prompt: str) -> bool:
    """
    验证文本完成提示词格式
    """
    return isinstance(prompt, str) and len(prompt.strip()) > 0


def format_error_response(error_message: str, error_type: str = "validation_error") -> Dict[str, Any]:
    """
    格式化错误响应
    """
    return {
        "error": {
            "message": error_message,
            "type": error_type,
            "code": error_type.upper(),
            "timestamp": datetime.utcnow().isoformat()
        }
    }


def calculate_token_usage(text: str, approximate: bool = True) -> int:
    """
    估算文本的token使用量
    这是一个近似计算，实际使用量可能有差异
    """
    if approximate:
        # 简单估算：英文大约4个字符=1个token，中文大约1.5个字符=1个token
        # 这里使用简化的平均值：3个字符=1个token
        return len(text) // 3
    else:
        # 更精确的计算需要使用tiktoken等库
        # 这里暂时返回简单估算
        return len(text) // 3


def mask_api_key(api_key: str) -> str:
    """
    掩码API密钥，只显示前4位和后4位
    """
    if not api_key or len(api_key) < 8:
        return "****"
    
    return f"{api_key[:4]}{'*' * (len(api_key) - 8)}{api_key[-4:]}"


def get_timestamp() -> str:
    """
    获取当前时间戳（ISO格式）
    """
    return datetime.utcnow().isoformat()


def deep_merge_dict(base_dict: Dict[str, Any], update_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    深度合并字典
    """
    result = base_dict.copy()
    
    for key, value in update_dict.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge_dict(result[key], value)
        else:
            result[key] = value
    
    return result


def extract_model_provider(model_alias: str, config: Dict[str, Any]) -> Optional[str]:
    """
    从配置中提取模型的提供商信息
    """
    models = config.get("models", {})
    model_config = models.get(model_alias, {})
    return model_config.get("provider")


def validate_model_config(model_config: Dict[str, Any]) -> tuple[bool, str]:
    """
    验证模型配置的有效性
    返回 (是否有效, 错误信息)
    """
    required_fields = ["provider", "model_name", "api_key"]
    
    for field in required_fields:
        if field not in model_config:
            return False, f"缺少必需字段: {field}"
        
        if not model_config[field]:
            return False, f"字段 {field} 不能为空"
    
    # 验证提供商是否支持
    supported_providers = ["openai", "claude", "qwen"]
    if model_config["provider"] not in supported_providers:
        return False, f"不支持的提供商: {model_config['provider']}"
    
    return True, ""


def format_model_info(model_alias: str, model_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    格式化模型信息用于显示
    """
    return {
        "alias": model_alias,
        "provider": model_config.get("provider"),
        "model_name": model_config.get("model_name"),
        "base_url": model_config.get("base_url"),
        "api_key_masked": mask_api_key(model_config.get("api_key", "")),
        "default_params": model_config.get("default_params", {})
    }
