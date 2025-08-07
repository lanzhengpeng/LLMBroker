import json,os
def load_json_file(filename: str):
    """
    读取指定路径的 JSON 文件，返回解析后的字典。
    如果文件不存在或解析失败，返回空字典。

    :param filename: JSON 文件名（可以是相对路径或绝对路径）
    :return: dict，JSON 内容
    """
    try:
        path = os.path.abspath(filename)
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"文件 {filename} 未找到。")
    except json.JSONDecodeError:
        print(f"文件 {filename} 不是有效的 JSON 格式。")
    except Exception as e:
        print(f"读取文件 {filename} 时发生错误: {e}")
    return {}