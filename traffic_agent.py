import yaml
import requests

class TrafficAgent:
    def __init__(self, config_path="config.yaml"):
        cfg = yaml.safe_load(open(config_path, "r"))
        self.api_key = cfg["api_key"]
        self.model = cfg.get("model", "deepseek-chat")
        self.base_url = cfg.get("base_url", "https://api.deepseek.com")

        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        self.system_prompt = """
你是一名专业的交通工程师、交通规划师和智能交通系统研究专家。
请用严谨、结构化、专业但易懂的方式回答交通相关问题。
"""

    def ask(self, user_query):
        url = f"{self.base_url}/v1/chat/completions"

        payload = {
            "model": self.model,
            "max_tokens": 1024,
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_query}
            ]
        }

        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()

        return response.json()["choices"][0]["message"]["content"]
