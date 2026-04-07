"""
API 基础请求封装
提供统一的请求方法，自动处理 token 和错误
"""

import requests
from config.settings import BASE_URL
from utils.token_manager import token_manager


class BaseAPI:
    """API 请求基类"""

    def __init__(self):
        self.base_url = BASE_URL

    def _get_headers(self) -> dict:
        """获取请求头，包含 token"""
        token = token_manager.get_token()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    def get(self, endpoint: str, params: dict = None) -> dict:
        """发送 GET 请求"""
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=self._get_headers(), params=params)
        return self._handle_response(response)

    def post(self, endpoint: str, data: dict = None) -> dict:
        """发送 POST 请求"""
        url = f"{self.base_url}{endpoint}"
        response = requests.post(url, headers=self._get_headers(), json=data)
        return self._handle_response(response)

    def put(self, endpoint: str, data: dict = None) -> dict:
        """发送 PUT 请求"""
        url = f"{self.base_url}{endpoint}"
        response = requests.put(url, headers=self._get_headers(), json=data)
        return self._handle_response(response)

    def patch(self, endpoint: str, data: dict = None) -> dict:
        """发送 PATCH 请求"""
        url = f"{self.base_url}{endpoint}"
        response = requests.patch(url, headers=self._get_headers(), json=data)
        return self._handle_response(response)

    def delete(self, endpoint: str, params: dict = None) -> dict:
        """发送 DELETE 请求"""
        url = f"{self.base_url}{endpoint}"
        response = requests.delete(url, headers=self._get_headers(), params=params)
        return self._handle_response(response)

    def _handle_response(self, response: requests.Response) -> dict:
        """处理响应，统一错误处理"""
        result = response.json()
        if result.get("code") != 0:
            raise Exception(f"API 请求失败: {result}")
        return result
