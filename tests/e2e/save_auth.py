"""
手动登录飞书并保存登录态到 auth_state.json

运行方式：
    python tests/e2e/save_auth.py

这是一次性操作：保存后，所有 E2E 测试都会自动使用此文件复用登录态。
auth_state.json 在 .gitignore 中被排除，不会被提交到仓库——每个开发者
clone 后需要自行运行本脚本完成登录。

飞书 session 过期后（通常几天到几周），重新运行本脚本即可刷新。
"""
from pathlib import Path

from playwright.sync_api import sync_playwright

# auth_state.json 与本脚本同目录，便于 conftest.py 定位
AUTH_FILE = Path(__file__).parent / "auth_state.json"
FEISHU_URL = "https://ucnzz0zt5wpo.feishu.cn/"


def main() -> None:
    with sync_playwright() as p:
        # 必须 headless=False，让用户能看到登录页并完成扫码/账号密码
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(FEISHU_URL)

        print("=" * 60)
        print("请在打开的浏览器中完成飞书登录（扫码或账号密码都行）")
        print("登录成功后，回到此终端按 Enter 键保存登录态")
        print("=" * 60)
        input("按 Enter 继续... ")

        context.storage_state(path=str(AUTH_FILE))
        print(f"\n✅ 登录态已保存到：{AUTH_FILE}")
        print("现在可以运行：pytest tests/e2e/ -v -s")

        browser.close()


if __name__ == "__main__":
    main()
