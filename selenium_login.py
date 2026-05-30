from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

# ===== 配置信息 =====
ROUTER_IP = "192.168.31.1"
ROUTER_PASSWORD = "zuiketsu1927"   # 请修改为真实密码

# 指定 chromedriver.exe 的路径（请确认文件存在）
chrome_driver_path = r"C:\Users\35379\router_ai\chromedriver.exe"

# ===== 启动浏览器 =====
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

try:
    # 1. 打开登录页面
    driver.get(f"http://{ROUTER_IP}/cgi-bin/luci/web/home")
    time.sleep(5)  # 等待页面加载

    # 2. 输入密码（根据页面实际 name 属性，常见为 'password'）
    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys(ROUTER_PASSWORD)

    # 3. 点击登录按钮（根据页面实际 type，常见为 'submit'）
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()

    # 4. 等待跳转并获取 stok
    time.sleep(5)
    current_url = driver.current_url
    print(f"登录后 URL: {current_url}")

    if "stok=" in current_url:
        stok = current_url.split("stok=")[1].split("/")[0]
        print(f"✅ 成功获取 stok: {stok}")
        with open("stok.txt", "w") as f:
            f.write(stok)
    else:
        print("❌ 未在 URL 中找到 stok，请检查登录是否成功")

    time.sleep(3)

finally:
    driver.quit()