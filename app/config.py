"""
配置文件加载和管理
"""

import yaml
import json
import os
from typing import Dict, Any
from pathlib import Path


def load_config(config_path: str = None) -> Dict[str, Any]:
    """
    加载配置文件
    支持YAML和JSON格式
    """
    if config_path is None:
        # 默认配置文件路径
        base_dir = Path(__file__).parent.parent
        config_path = base_dir / "config.yaml"
    
    config_path = Path(config_path)
    
    if not config_path.exists():
        raise FileNotFoundError(f"配置文件不存在: {config_path}")
    
    # 根据文件扩展名选择加载方式
    if config_path.suffix.lower() in ['.yaml', '.yml']:
        return load_yaml_config(config_path)
    elif config_path.suffix.lower() == '.json':
        return load_json_config(config_path)
    else:
        raise ValueError(f"不支持的配置文件格式: {config_path.suffix}")


def load_yaml_config(config_path: Path) -> Dict[str, Any]:
    """加载YAML配置文件"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return config
    except yaml.YAMLError as e:
        raise ValueError(f"YAML配置文件解析错误: {e}")
    except Exception as e:
        raise ValueError(f"配置文件读取错误: {e}")


def load_json_config(config_path: Path) -> Dict[str, Any]:
    """加载JSON配置文件"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON配置文件解析错误: {e}")
    except Exception as e:
        raise ValueError(f"配置文件读取错误: {e}")


def get_default_config() -> Dict[str, Any]:
    """获取默认配置"""
    return {
        "server": {
            "host": "0.0.0.0",
            "port": 8000,
            "reload": True,
            "log_level": "info"
        },
        "models": {
            "gpt-3.5-turbo": {
                "provider": "openai",
                "model_name": "gpt-3.5-turbo",
                "api_key": "${OPENAI_API_KEY}",
                "base_url": "https://api.openai.com/v1",
                "default_params": {
                    "temperature": 0.7,
                    "max_tokens": 1000
                }
            },
            "gpt-4": {
                "provider": "openai",
                "model_name": "gpt-4",
                "api_key": "${OPENAI_API_KEY}",
                "base_url": "https://api.openai.com/v1",
                "default_params": {
                    "temperature": 0.7,
                    "max_tokens": 1000
                }
            },
            "claude-3": {
                "provider": "claude",
                "model_name": "claude-3-sonnet-20240229",
                "api_key": "${ANTHROPIC_API_KEY}",
                "base_url": "https://api.anthropic.com/v1",
                "default_params": {
                    "temperature": 0.7,
                    "max_tokens": 1000
                }
            },
            "qwen": {
                "provider": "qwen",
                "model_name": "qwen-turbo",
                "api_key": "${DASHSCOPE_API_KEY}",
                "base_url": "https://dashscope.aliyuncs.com/api/v1",
                "default_params": {
                    "temperature": 0.7,
                    "max_tokens": 1000
                }
            }
        },
        "proxy": {
            "default_model": "gpt-3.5-turbo",
            "enable_parameter_injection": True,
            "enable_request_logging": True,
            "timeout": 60
        }
    }


def resolve_env_variables(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    解析配置中的环境变量
    格式: ${ENV_VAR_NAME}
    """
    def resolve_value(value):
        if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
            env_var = value[2:-1]  # 去掉 ${ 和 }
            return os.environ.get(env_var, value)
        elif isinstance(value, dict):
            return {k: resolve_value(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [resolve_value(item) for item in value]
        else:
            return value
    
    return resolve_value(config)


def validate_config(config: Dict[str, Any]) -> bool:
    """验证配置文件的有效性"""
    required_sections = ["models", "server", "proxy"]
    
    for section in required_sections:
        if section not in config:
            raise ValueError(f"配置文件缺少必需的节点: {section}")
    
    # 验证模型配置
    models = config.get("models", {})
    if not models:
        raise ValueError("配置文件中没有定义任何模型")
    
    for model_alias, model_config in models.items():
        required_model_fields = ["provider", "model_name", "api_key"]
        for field in required_model_fields:
            if field not in model_config:
                raise ValueError(f"模型 {model_alias} 缺少必需字段: {field}")
    
    return True


def load_and_validate_config(config_path: str = None) -> Dict[str, Any]:
    """加载并验证配置文件"""
    try:
        config = load_config(config_path)
    except FileNotFoundError:
        print("未找到配置文件，使用默认配置")
        config = get_default_config()
    
    # 解析环境变量
    config = resolve_env_variables(config)
    
    # 验证配置
    validate_config(config)
    
    return config
