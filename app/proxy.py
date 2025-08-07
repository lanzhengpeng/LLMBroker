"""
代理逻辑处理模块
负责参数注入、请求转发和响应处理
"""

from typing import Dict, Any, List, Optional
import logging
import time
from datetime import datetime

from .clients import ModelClientManager
from .utils import merge_parameters, extract_model_from_request, log_request


class LLMProxy:
    """LLM代理服务核心类"""
    
    def __init__(self, config: Dict[str, Any], client_manager: ModelClientManager):
        self.config = config
        self.client_manager = client_manager
        self.proxy_config = config.get("proxy", {})
        self.default_model = self.proxy_config.get("default_model", "gpt-3.5-turbo")
        self.enable_logging = self.proxy_config.get("enable_request_logging", True)
        self.enable_param_injection = self.proxy_config.get("enable_parameter_injection", True)
        
        # 设置日志
        if self.enable_logging:
            logging.basicConfig(level=logging.INFO)
            self.logger = logging.getLogger(__name__)
    
    async def handle_chat_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理聊天完成请求
        """
        start_time = time.time()
        
        try:
            # 提取模型名称
            model_alias = extract_model_from_request(request, self.default_model)
            
            # 获取消息
            messages = request.get("messages", [])
            if not messages:
                raise ValueError("请求中缺少messages字段")
            
            # 参数注入和合并
            merged_params = self._inject_and_merge_parameters(model_alias, request)
            
            # 记录请求日志
            if self.enable_logging:
                log_request(self.logger, "chat_completion", model_alias, request)
            
            # 调用模型客户端
            response = await self.client_manager.chat_completion(
                model_alias, messages, **merged_params
            )
            
            # 后处理响应
            processed_response = self._post_process_response(response, model_alias, start_time)
            
            return processed_response
        
        except Exception as e:
            # 错误处理
            return self._create_error_response(str(e), start_time)
    
    async def handle_completion_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理文本完成请求
        """
        start_time = time.time()
        
        try:
            # 提取模型名称
            model_alias = extract_model_from_request(request, self.default_model)
            
            # 获取提示词
            prompt = request.get("prompt", "")
            if not prompt:
                raise ValueError("请求中缺少prompt字段")
            
            # 参数注入和合并
            merged_params = self._inject_and_merge_parameters(model_alias, request)
            
            # 记录请求日志
            if self.enable_logging:
                log_request(self.logger, "text_completion", model_alias, request)
            
            # 调用模型客户端
            response = await self.client_manager.text_completion(
                model_alias, prompt, **merged_params
            )
            
            # 后处理响应
            processed_response = self._post_process_response(response, model_alias, start_time)
            
            return processed_response
        
        except Exception as e:
            # 错误处理
            return self._create_error_response(str(e), start_time)
    
    def _inject_and_merge_parameters(self, model_alias: str, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        参数注入和合并
        """
        if not self.enable_param_injection:
            # 如果禁用参数注入，直接返回请求中的参数
            return self._extract_request_parameters(request)
        
        # 获取模型的默认参数
        model_config = self.config.get("models", {}).get(model_alias, {})
        default_params = model_config.get("default_params", {})
        
        # 获取请求中的参数
        request_params = self._extract_request_parameters(request)
        
        # 合并参数（请求参数优先级更高）
        merged_params = merge_parameters(default_params, request_params)
        
        return merged_params
    
    def _extract_request_parameters(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        从请求中提取参数
        """
        # 排除不应该传递给模型API的字段
        excluded_fields = {
            "model", "messages", "prompt", "stream"  # 这些字段由代理处理
        }
        
        params = {}
        for key, value in request.items():
            if key not in excluded_fields:
                params[key] = value
        
        return params
    
    def _post_process_response(self, response: Dict[str, Any], model_alias: str, start_time: float) -> Dict[str, Any]:
        """
        后处理响应
        """
        # 添加代理信息
        if "x-proxy-info" not in response:
            response["x-proxy-info"] = {
                "proxy": "LLMBroker",
                "model_alias": model_alias,
                "processing_time": time.time() - start_time,
                "timestamp": datetime.utcnow().isoformat()
            }
        
        # 记录响应日志
        if self.enable_logging:
            self.logger.info(f"响应成功 - 模型: {model_alias}, 耗时: {time.time() - start_time:.2f}s")
        
        return response
    
    def _create_error_response(self, error_message: str, start_time: float) -> Dict[str, Any]:
        """
        创建错误响应
        """
        return {
            "error": {
                "message": error_message,
                "type": "proxy_error",
                "code": "internal_error"
            },
            "x-proxy-info": {
                "proxy": "LLMBroker",
                "processing_time": time.time() - start_time,
                "timestamp": datetime.utcnow().isoformat(),
                "status": "error"
            }
        }
    
    def get_available_models(self) -> List[str]:
        """获取所有可用模型"""
        return self.client_manager.get_available_models()
    
    def get_model_config(self, model_alias: str) -> Optional[Dict[str, Any]]:
        """获取指定模型的配置"""
        return self.config.get("models", {}).get(model_alias)
