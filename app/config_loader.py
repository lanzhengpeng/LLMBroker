import sqlite3
import json

class ConfigLoader:
    def __init__(self, db_path='../config/config.db'):
        self.db_path = db_path

    def get_apis_and_provider_by_model_value(self, model_value):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT id, provider_id FROM models WHERE model_value=?", (model_value,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return None

        model_id, provider_id = row

        cursor.execute("SELECT name FROM model_providers WHERE id=?", (provider_id,))
        provider_row = cursor.fetchone()
        provider_name = provider_row[0] if provider_row else None

        cursor.execute("SELECT base_url, api_key FROM model_apis WHERE model_id=? AND enable=1", (model_id,))
        apis = cursor.fetchall()
        conn.close()

        api_list = [{"base_url": base_url, "api_key": api_key} for base_url, api_key in apis]

        return {
            "provider_name": provider_name,
            "apis": api_list
        }

    def get_all_models(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT m.model_name, m.model_value, p.name
            FROM models m
            JOIN model_providers p ON m.provider_id = p.id
        """)
        rows = cursor.fetchall()
        conn.close()

        result = {}
        for model_name, model_value, provider_name in rows:
            result[model_name] = {
                "model_value": model_value,
                "provider_name": provider_name
            }
        return result

if __name__ == "__main__":
    loader = ConfigLoader()

    # 查询单个模型的api和厂商
    result = loader.get_apis_and_provider_by_model_value("ernie-lite-8k")
    if result:
        print("单模型查询结果：")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("未找到对应模型或API")

    # 查询所有模型及厂商
    all_models = loader.get_all_models()
    print("\n所有模型信息：")
    print(json.dumps(all_models, indent=2, ensure_ascii=False))
