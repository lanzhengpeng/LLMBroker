import json
from typing import Optional
import yaml
import os
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


_config_cache = None
_default_yaml_path = os.path.join(os.path.dirname(__file__), "../../config/vendor_config.yaml")

def _load_vendor_config(yaml_path: str = _default_yaml_path):
    global _config_cache
    with open(yaml_path, 'r', encoding='utf-8') as f:
        _config_cache = yaml.safe_load(f)

def get_vendor_config(vendor_name: str):
    if _config_cache is None:
        _load_vendor_config()
    vendors = _config_cache.get("vendors", {})
    vendor_conf =  vendors.get(vendor_name, {
        "rename_params": {},
        "remove_params": [],
        "extra_params": {}
    })
    return vendor_conf

def map_request_params(req_dict: dict, vendor_config: dict) -> dict:
    mapped = req_dict.copy()

    # 参数重命名
    rename_map = vendor_config.get("rename_params", {})
    for old_key, new_key in rename_map.items():
        if old_key in mapped:
            mapped[new_key] = mapped.pop(old_key)

    for param in vendor_config.get("remove_params", []):
        if param in mapped:
            mapped.pop(param)

    # 删除所有值为 None 的参数
    keys_to_del = [k for k, v in mapped.items() if v is None]
    for k in keys_to_del:
        mapped.pop(k)

    mapped['extra_body'] = vendor_config.get("extra_params", {})

    return mapped
