小米路由器自动禁用设备工具
使用 Playwright 自动化登录小米路由器管理界面，自动提取 stok 并调用接口禁用指定 MAC 地址的设备，无需手动复制 stok，无需处理复杂的登录加密。

✨ 功能特点
自动打开浏览器并登录路由器管理后台

通过网络请求拦截自动获取 stok（会话令牌）

一键禁用指定 MAC 地址的设备（加入黑名单）

支持后台静默运行（可选无头模式）

完全本地运行，无需第三方云服务

📋 环境要求
Windows / macOS / Linux

Python 3.8 或更高版本

小米路由器（已测试：小米路由器 4A 千兆版，固件版本 1.0.34）

路由器管理密码

🚀 安装步骤
1. 安装 Python 依赖
bash
pip install playwright
playwright install chromium
首次安装会自动下载 Chromium 浏览器（约 150MB），只需一次。

2. 下载脚本
将以下代码保存为 auto_block.py（完整代码见下文）。

📝 完整代码
python
from playwright.sync_api import sync_playwright, Playwright
import time
from urllib.parse import quote

def auto_block_device(playwright: Playwright, mac_address: str, password: str) -> None:
    browser = playwright.chromium.launch(headless=False)  # 设为 True 可隐藏窗口
    context = browser.new_context()
    page = context.new_page()

    stok = None

    # 拦截登录响应，提取 token (stok)
    def handle_response(response):
        nonlocal stok
        if "/api/xqsystem/login" in response.url:
            try:
                data = response.json()
                if data.get("code") == 0:
                    stok = data.get("token")
                    print(f"[捕获] stok = {stok}")
            except:
                pass

    page.on("response", handle_response)

    # 1. 自动登录
    print("正在登录路由器...")
    page.goto("http://192.168.31.1/cgi-bin/luci/web/home")
    page.get_by_role("textbox", name="请输入路由器管理密码").click()
    page.get_by_role("textbox", name="请输入路由器管理密码").fill(password)
    page.locator("#btnRtSubmit").click()

    # 等待 stok 获取成功
    for _ in range(30):
        if stok:
            break
        time.sleep(0.5)
    else:
        print("❌ 登录失败：未能获取 stok")
        browser.close()
        return

    print(f"✅ 登录成功，stok = {stok}")

    # 2. 禁用设备
    encoded_mac = quote(mac_address)
    block_url = f"http://192.168.31.1/cgi-bin/luci;stok={stok}/api/xqsystem/set_mac_filter?mac={encoded_mac}&wan=1"
    print(f"正在禁用设备 {mac_address} ...")
    page.goto(block_url)

    time.sleep(2)
    body_text = page.text_content("body")
    print(f"服务器返回: {body_text}")

    if "code" in body_text and "0" in body_text:
        print("✅ 设备已成功禁用！")
    else:
        print("⚠️ 禁用结果未知，请手动检查路由器后台")

    time.sleep(3)
    browser.close()

if __name__ == "__main__":
    print("=== 小米路由器自动禁用设备工具 ===\n")
    mac = input("请输入要禁用的设备 MAC 地址: ").strip()
    pwd = input("请输入路由器管理密码: ").strip()
    if not mac or not pwd:
        print("MAC 地址和密码不能为空")
    else:
        with sync_playwright() as playwright:
            auto_block_device(playwright, mac, pwd)
🖥️ 使用方法
打开终端（CMD / PowerShell / Terminal），进入脚本所在目录。

运行命令：

bash
python auto_block.py
按提示输入：

设备 MAC 地址（例如 7E:82:64:7E:8A:7C，字母大写）

路由器管理密码

程序会自动打开浏览器 → 登录 → 获取 stok → 禁用设备。

看到 ✅ 设备已成功禁用！ 表示操作完成。

🔧 常见问题
Q1: 登录后提示“未能获取 stok”
请检查密码是否正确。

部分路由器固件的登录接口路径不同。打开浏览器开发者工具（F12）→ Network，登录后找到名为 login 的请求，查看其 URL 是否包含 /api/xqsystem/login。如果不包含，修改代码中 if "/api/xqsystem/login" in response.url 的关键词。

Q2: 禁用不生效
尝试将 wan=1 改为 wan=0（某些固件使用 0 表示禁用）。

确保输入的 MAC 地址格式正确（例如 AA:BB:CC:DD:EE:FF，冒号英文半角，字母大写）。

Q3: 浏览器窗口一闪而过，看不到过程
将 headless=False 改为 headless=True 可后台运行；若想观察，保持 False 并适当增加 time.sleep() 时间。

Q4: 如何获取设备的 MAC 地址？
在路由器后台「设备管理」页面查看。

或者使用手机/电脑的网络连接详情查看（Wi-Fi 设置 → 高级 → MAC 地址）。

Q5: 能否禁用多个设备？
可以。获取 stok 后，对每个 MAC 地址循环调用 page.goto(block_url) 即可。可将代码稍作修改，支持列表输入。

📌 注意事项
本工具仅用于合法管理您自己的家庭网络，请勿用于非法用途。

路由器固件更新后，登录接口可能变化，届时可能需要重新调整拦截条件。

建议在电脑通过有线连接路由器的情况下运行，避免 Wi-Fi 不稳定导致登录失败。

🤝 贡献与支持
如果遇到问题或有改进建议，欢迎提交 Issue 或 Pull Request。