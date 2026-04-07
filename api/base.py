"""
API 基础请求封装
提供统一的请求方法，自动处理 token 和错误
"""

import requests
from config.settings import BASE_URL
from utils.token_manager import token_manager


class BaseAPI:
    """API 请求基类"""

    def __init__(self, user_token: str = None):
        """
        初始化 API 客户端
        
        :param user_token: user_access_token（可选），用于需要用户权限的接口
        """
        self.base_url = BASE_URL
        self.user_token = user_token

    def _get_headers(self) -> dict:
        """获取请求头，包含 token"""
        # 优先使用 user_token，否则使用 tenant_access_token
        token = self.user_token if self.user_token else token_manager.get_token()
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
        """处理响应，返回结果（包含成功和失败）"""
        # 尝试解析 JSON
        try:
            result = response.json()
        except Exception:
            # 非 JSON 响应（如 404 页面）
            result = {
                "code": response.status_code,
                "msg": response.text,
                "http_status": response.status_code
            }
        return result
