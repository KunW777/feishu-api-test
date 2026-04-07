"""
用户相关 API
"""

from api.base import BaseAPI


class UserAPI(BaseAPI):
    """用户 API 封装"""

    def update_user_id(self, user_id: str, new_user_id: str) -> dict:
        """
        更新用户 ID

        :param user_id: 原用户 ID
        :param new_user_id: 新用户 ID
        :return: API 响应
        """
        endpoint = f"/contact/v3/users/{user_id}/user_id"
        data = {
            "new_user_id": new_user_id
        }
        return self.patch(endpoint, data=data)
