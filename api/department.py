"""
部门相关 API
"""

from api.base import BaseAPI


class DepartmentAPI(BaseAPI):
    """部门 API 封装"""

    def update_user_id(self, user_id: str, new_user_id: str) -> dict:
        """
        更新用户 ID

        :param user_id: 原用户 ID
        :param new_user_id: 新用户 ID
        :return: API 响应
        """
        endpoint = "/user/v1/users/user_id"
        data = {
            "user_id": user_id,
            "new_user_id": new_user_id
        }
        return self.patch(endpoint, data=data)
