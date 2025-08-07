# config.py
from enum import Enum

class ModelProvider(str, Enum):
    zhipu = "zhipu"
    xunfei = "xunfei"
    baidu = "baidu"


MODEL_CONFIG = {
    ModelProvider.zhipu: {
        "glm-4.5-flash": {
            "api_key": "2df10bf298af4748bf01864a3b8a0ba1.4UOCbHoDgewtC8QA",
            "base_url": "https://open.bigmodel.cn/api/paas/v4"
        },
        "glm-4-flash": {
            "api_key": "2df10bf298af4748bf01864a3b8a0ba1.4UOCbHoDgewtC8QA",
            "base_url": "https://open.bigmodel.cn/api/paas/v4"
        },
        "GLM-Z1-Flash": {
            "api_key": "2df10bf298af4748bf01864a3b8a0ba1.4UOCbHoDgewtC8QA",
            "base_url": "https://open.bigmodel.cn/api/paas/v4"
        },
        "GLM-4.1V-Thinking-Flash": {
            "api_key": "2df10bf298af4748bf01864a3b8a0ba1.4UOCbHoDgewtC8QA",
            "base_url": "https://open.bigmodel.cn/api/paas/v4"
        },
        "GLM-4V-Flash": {
            "api_key": "2df10bf298af4748bf01864a3b8a0ba1.4UOCbHoDgewtC8QA",
            "base_url": "https://open.bigmodel.cn/api/paas/v4"
        },
        "Cogview-3-Flash": {
            "api_key": "2df10bf298af4748bf01864a3b8a0ba1.4UOCbHoDgewtC8QA",
            "base_url": "https://open.bigmodel.cn/api/paas/v4"
        },
        "CogVideoX-Flash": {
            "api_key": "2df10bf298af4748bf01864a3b8a0ba1.4UOCbHoDgewtC8QA",
            "base_url": "https://open.bigmodel.cn/api/paas/v4"
        },
    },
    ModelProvider.xunfei: {
        "Lite": {
            "api_key": "LbxeRlvDbLwsJLxZQCYb:dZnLgkSFYmIQRzqDIkhw",
            "base_url": "https://spark-api-open.xf-yun.com/v1"
        }
    },
    ModelProvider.baidu: {
        "ERNIE-Speed-128K": {
            "api_key":
            "bce-v3/ALTAK-4KyFUYBYZMuf8s3bxg2nO/5852d9dd9a49dccc9234f0907a1b53645456469c",
            "base_url": "https://qianfan.baidubce.com/v2"
        },
        "ERNIE-Speed-8K": {
            "api_key":
            "bce-v3/ALTAK-4KyFUYBYZMuf8s3bxg2nO/5852d9dd9a49dccc9234f0907a1b53645456469c",
            "base_url": "https://qianfan.baidubce.com/v2"
        },
        "ERNIE-Lite": {
            "api_key":
            "bce-v3/ALTAK-4KyFUYBYZMuf8s3bxg2nO/5852d9dd9a49dccc9234f0907a1b53645456469c",
            "base_url": "https://qianfan.baidubce.com/v2"
        },
        "ERNIE-Tiny": {
            "api_key":
            "bce-v3/ALTAK-4KyFUYBYZMuf8s3bxg2nO/5852d9dd9a49dccc9234f0907a1b53645456469c",
            "base_url": "https://qianfan.baidubce.com/v2"
        }
    }
}
