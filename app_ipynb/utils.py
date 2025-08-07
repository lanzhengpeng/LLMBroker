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