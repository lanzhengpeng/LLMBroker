# config.py
from enum import Enum

class ModelProvider(str, Enum):
    zhipu = "zhipu"
    xunfei = "xunfei"
    baidu = "baidu"



from json_utils import load_json_file
config = load_json_file("../models/model_name.json")
MODEL_CONFIG = {
    ModelProvider.zhipu: {
        config.get("zhipu").get("GLM-4.5-Flash"): {
            "api_key": "2df10bf298af4748bf01864a3b8a0ba1.4UOCbHoDgewtC8QA",
            "base_url": "https://open.bigmodel.cn/api/paas/v4"
        },
        config.get("zhipu").get("GLM-4-Flash"): {
            "api_key": "2df10bf298af4748bf01864a3b8a0ba1.4UOCbHoDgewtC8QA",
            "base_url": "https://open.bigmodel.cn/api/paas/v4"
        },
        config.get("zhipu").get("GLM-Z1-Flash"): {
            "api_key": "2df10bf298af4748bf01864a3b8a0ba1.4UOCbHoDgewtC8QA",
            "base_url": "https://open.bigmodel.cn/api/paas/v4"
        },
        config.get("zhipu").get("GLM-4.1V-Thinking-Flash"): {
            "api_key": "2df10bf298af4748bf01864a3b8a0ba1.4UOCbHoDgewtC8QA",
            "base_url": "https://open.bigmodel.cn/api/paas/v4"
        },
        config.get("zhipu").get("GLM-4V-Flash"): {
            "api_key": "2df10bf298af4748bf01864a3b8a0ba1.4UOCbHoDgewtC8QA",
            "base_url": "https://open.bigmodel.cn/api/paas/v4"
        },
        config.get("zhipu").get("Cogview-3-Flash"): {
            "api_key": "dc4846b5f53145028b3d6c0784b1e04d.EY7MtneUU8aRlcbk",
            "base_url": "https://open.bigmodel.cn/api/paas/v4"
        },
        config.get("zhipu").get("CogVideoX-Flash"): {
            "api_key": "2df10bf298af4748bf01864a3b8a0ba1.4UOCbHoDgewtC8QA",
            "base_url": "https://open.bigmodel.cn/api/paas/v4"
        },
    },
    ModelProvider.xunfei: {
        config.get("xunfei").get("Spark-Lite"): {
            "api_key": "LbxeRlvDbLwsJLxZQCYb:dZnLgkSFYmIQRzqDIkhw",
            "base_url": "https://spark-api-open.xf-yun.com/v1"
        }
    },
    ModelProvider.baidu: {
        config.get("baidu").get("ERNIE-Speed-128K"): {
            "api_key":
            "bce-v3/ALTAK-4KyFUYBYZMuf8s3bxg2nO/5852d9dd9a49dccc9234f0907a1b53645456469c",
            "base_url": "https://qianfan.baidubce.com/v2"
        },
        config.get("baidu").get("ERNIE-Speed-8K"): {
            "api_key":
            "bce-v3/ALTAK-4KyFUYBYZMuf8s3bxg2nO/5852d9dd9a49dccc9234f0907a1b53645456469c",
            "base_url": "https://qianfan.baidubce.com/v2"
        },
        config.get("baidu").get("ERNIE-Lite-8K"): {
            "api_key":
            "bce-v3/ALTAK-4KyFUYBYZMuf8s3bxg2nO/5852d9dd9a49dccc9234f0907a1b53645456469c",
            "base_url": "https://qianfan.baidubce.com/v2"
        },
        config.get("baidu").get("ERNIE-Tiny-8K"): {
            "api_key":
            "bce-v3/ALTAK-4KyFUYBYZMuf8s3bxg2nO/5852d9dd9a49dccc9234f0907a1b53645456469c",
            "base_url": "https://qianfan.baidubce.com/v2"
        }
    }
}
