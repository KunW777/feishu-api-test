"""
Token 管理模块
负责获取、缓存和刷新 tenant_access_token
"""

import time
import requests
from config.settings import APP_ID, APP_SECRET, BASE_URL, TOKEN_EXPIRE_BUFFER


class TokenManager:
    """管理飞书 tenant_access_token 的获取和缓存"""

    _instance = None
    _token = None
    _expire_time = 0

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_token(self) -> str:
        """
        获取 tenant_access_token
        如果缓存的 token 有效则直接返回，否则重新获取
        """
        # 检查缓存的 token 是否有效
        if self._token and time.time() < self._expire_time:
            return self._token

        # 重新获取 token
        return self._refresh_token()

    def _refresh_token(self) -> str:
        """调用 API 获取新的 tenant_access_token"""
        url = f"{BASE_URL}/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": APP_ID,
            "app_secret": APP_SECRET
        }

        response = requests.post(url, json=payload)
        result = response.json()

        if result.get("code") != 0:
            raise Exception(f"获取 token 失败: {result}")

        self._token = result["tenant_access_token"]
        # 设置过期时间（提前一段时间刷新，避免临界情况）
        self._expire_time = time.time() + result["expire"] - TOKEN_EXPIRE_BUFFER

        return self._token

    def clear_cache(self):
        """清除缓存的 token"""
        self._token = None
        self._expire_time = 0


# 全局 token 管理器实例
token_manager = TokenManager()
