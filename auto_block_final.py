from playwright.sync_api import sync_playwright, Playwright
import time
from urllib.parse import quote


def auto_block_device(playwright: Playwright, mac_address: str, password: str) -> None:
    browser = playwright.chromium.launch(headless=False)  # 显示浏览器窗口，便于观察
    context = browser.new_context()
    page = context.new_page()

    # ---------- 1. 自动登录 ----------
    print("正在登录路由器...")
    page.goto("http://192.168.31.1/cgi-bin/luci/web/home")
    page.get_by_role("textbox", name="请输入路由器管理密码").click()
    page.get_by_role("textbox", name="请输入路由器管理密码").fill(password)
    page.locator("#btnRtSubmit").click()

    # 等待登录完成，直到 URL 中包含 stok（最多等待 15 秒）
    print("等待登录完成并获取 stok...")
    stok = None
    for i in range(30):
        time.sleep(0.5)
        current_url = page.url
        if "stok=" in current_url:
            stok = current_url.split("stok=")[1].split("/")[0]
            break
    if not stok:
        print("❌ 登录失败：未检测到 stok，请检查密码或页面是否正常跳转。")
        browser.close()
        return

    print(f"✅ 登录成功，stok = {stok}")

    # ---------- 2. 构造禁用设备的 URL ----------
    encoded_mac = quote(mac_address)  # 对 MAC 地址进行 URL 编码（冒号转成 %3A）
    # 注意：根据您之前成功禁用的经验，使用 wan=1 表示加入黑名单（禁用）
    # 如果无效，可尝试 wan=0
    block_url = f"http://192.168.31.1/cgi-bin/luci;stok={stok}/api/xqsystem/set_mac_filter?mac={encoded_mac}&wan=1"
    print(f"正在禁用设备 {mac_address} ...")

    # 直接在当前浏览器会话中访问该 URL（保持登录状态）
    page.goto(block_url)

    # 等待页面返回结果（通常返回 JSON 文本）
    time.sleep(2)
    body_text = page.text_content("body")
    print(f"服务器返回内容: {body_text}")

    # 简单判断是否成功（返回的 JSON 中通常包含 "code":0）
    if "code" in body_text and "0" in body_text:
        print("✅ 设备已成功禁用！")
    else:
        print("⚠️ 禁用结果未知，请登录路由器后台手动确认。")

    # 保持浏览器窗口几秒钟，方便查看结果，然后关闭
    print("5 秒后关闭浏览器...")
    time.sleep(5)
    browser.close()


# ---------- 主程序 ----------
if __name__ == "__main__":
    print("=== 小米路由器自动禁用设备工具 ===\n")
    mac = input("请输入要禁用的设备 MAC 地址（例如 7E:82:64:7E:8A:7C）: ").strip()
    pwd = input("请输入路由器管理密码: ").strip()
    if not mac or not pwd:
        print("MAC 地址和密码不能为空")
    else:
        with sync_playwright() as playwright:
            auto_block_device(playwright, mac, pwd)