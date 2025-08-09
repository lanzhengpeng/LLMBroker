import sqlite3
import gc  # 垃圾回收模块

class ConfigLoader:
    def __init__(self, db_path='../config/config.db'):
        # 使用 SQLite URI 只读模式，避免写缓存和锁
        self.db_path = f'file:{db_path}?mode=ro'

    def get_apis_and_provider_by_model_value(self, model_value):
        conn = None
        try:
            conn = sqlite3.connect(self.db_path, uri=True)
            cursor = conn.cursor()

            cursor.execute("SELECT id, provider_id FROM models WHERE model_value=?", (model_value,))
            row = cursor.fetchone()
            if not row:
                return None
            model_id, provider_id = row

            cursor.execute("SELECT name FROM model_providers WHERE id=?", (provider_id,))
            provider_row = cursor.fetchone()
            provider_name = provider_row[0] if provider_row else None

            cursor.execute("SELECT base_url, api_key FROM model_apis WHERE model_id=? AND enable=1", (model_id,))
            apis = cursor.fetchall()
            api_list = [{"base_url": base_url, "api_key": api_key} for base_url, api_key in apis]

            return {
                "provider_name": provider_name,
                "apis": api_list
            }
        except Exception as e:
            print(f"数据库查询异常: {e}")
            return None
        finally:
            if conn:
                conn.close()
                del conn  # 删除引用
                gc.collect()  # 显式触发垃圾回收

    def get_all_models(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_path, uri=True)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT m.model_value, m.model_name, p.name as provider_name
                FROM models m
                LEFT JOIN model_providers p ON m.provider_id = p.id
            """)
            rows = cursor.fetchall()
            models = [
                {"model_value": mv, "model_name": mn, "provider_name": pn}
                for mv, mn, pn in rows
            ]
            return models
        except Exception as e:
            print(f"数据库查询异常: {e}")
            return []
        finally:
            if conn:
                conn.close()
                del conn  # 删除引用
                gc.collect()  # 显式触发垃圾回收
