import json,os
MODEL_DIR = "../models"  # 模型配置文件夹路径
def load_all_models():
    models = []
    # 遍历文件夹下所有 .json 文件
    for filename in os.listdir(MODEL_DIR):
        if filename.endswith(".json"):
            filepath = os.path.join(MODEL_DIR, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # 如果 JSON 是列表，就extend，如果是单个字典，就append
                    if isinstance(data, list):
                        models.extend(data)
                    elif isinstance(data, dict):
                        models.append(data)
            except Exception as e:
                print(f"加载模型文件出错: {filepath}，错误：{e}")
    return models


from config import MODEL_CONFIG


def get_model_config(model_name: str):
    for provider_models in MODEL_CONFIG.values():
        if model_name in provider_models:
            return provider_models[model_name]
    raise ValueError(f"Model config for {model_name} not found.")

import json
from typing import Optional

_model_to_vendor_cache = {}
_is_loaded = False
_default_mapping_file = "../models/model_name.json"

def _load_model_vendor_mapping(mapping_file: str = _default_mapping_file) -> None:
    global _model_to_vendor_cache, _is_loaded
    with open(mapping_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    _model_to_vendor_cache = {}
    for vendor, models in data.items():
        for _, internal_model in models.items():
            _model_to_vendor_cache[internal_model.lower()] = vendor.lower()
    _is_loaded = True

def get_vendor_by_model(model_name: str) -> Optional[str]:
    """
    根据模型名返回厂商名（小写），找不到返回 None。
    第一次调用时会自动加载默认配置文件 model_name.json。
    """
    global _is_loaded
    if not _is_loaded:
        _load_model_vendor_mapping()
    if not model_name:
        return None
    return _model_to_vendor_cache.get(model_name.lower())
