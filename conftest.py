"""
项目根级 pytest 配置

本文件只做一件事：注册全项目的命令行参数。

为什么要放在根目录：
pytest 的 pytest_addoption 钩子必须在 pytest 解析命令行之前就被加载。
pytest 加载 conftest.py 的顺序是：从 rootdir 向下扫描，然后从显式传入的
测试路径向上扫描，收集沿途的 conftest.py。如果 pytest_addoption 只放在
子目录（如 tests/api/conftest.py）里，当用户跑 `pytest tests/` 时 pytest
找不到包含该 hook 的 conftest，argparse 会直接把 --user-token 判为
未知参数。

各测试层的 fixture（API 的 token fixture、E2E 的 browser_context_args）
仍保留在各自子目录的 conftest.py 里，只有跨层的 CLI 参数集中在这里。
"""


def pytest_addoption(parser):
    """注册全项目 CLI 参数。

    --user-token:
        user_access_token，供 tests/api/test_wiki.py 中 TestWikiAPIWithUserToken
        需要用户权限的接口测试使用。未传时相关测试会被 pytest.skip。
        获取方式：飞书开放平台 → 应用详情 → API 调试台 → 选择 user_access_token 模式。
    """
    parser.addoption(
        "--user-token",
        action="store",
        default=None,
        help="user_access_token，用于需要用户权限的接口测试",
    )
