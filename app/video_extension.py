import requests

class VideoGenerations:
    def __init__(self, client):
        self.client = client

    def __call__(self, model: str, prompt: str, quality: str = "quality",
                 with_audio: bool = True, size: str = "1920x1080", fps: int = 30,
                 image_url: str = None):  # ✅ 新增参数 image_url
        url = f"{self.client.base_url}/videos/generations"
        headers = {
            "Authorization": f"Bearer {self.client.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model,
            "prompt": prompt,
            "quality": quality,
            "with_audio": with_audio,
            "size": size,
            "fps": fps
        }
        if image_url:  # ✅ 可选添加
            payload["image_url"] = image_url

        response = requests.post(url, json=payload, headers=headers)
        return response.json()

class VideoNamespace:
    def __init__(self, client):
        self.generations = VideoGenerations(client)
