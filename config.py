import json
import os
from mirouterpy import MiWiFi

class XiaomiAuth:
    def __init__(self, host="192.168.31.1", password=""):
        self.host = host
        self.password = password
        self.router = MiWiFi(host)
        self.stok = None
        self.session = None   # mirouterpy 内部有 session，但我们保持接口一致

    def get_session(self):
        # 如果 mirouterpy 的 session 需要暴露，可以这样：
        if not self.session:
            self.session = self.router.session  # mirouterpy 内部 session 属性名可能需要确认
        return self.session

    def login(self):
        try:
            if self.router.login(self.password):
                self.stok = self.router.token
                print(f"✅ 自动登录成功，stok: {self.stok}")
                return True
            else:
                print("❌ mirouterpy 登录失败，请检查密码")
                return False
        except Exception as e:
            print(f"❌ 登录异常: {e}")
            return False

    def set_manual_stok(self, stok):
        self.stok = stok
        print(f"已使用手动配置的 stok: {self.stok}")

    def get_stok(self):
        if not self.stok:
            raise Exception("尚未登录")
        return self.stok

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
            host = cfg.get("ROUTER_HOST", "192.168.31.1")
            password = cfg.get("ROUTER_PASSWORD", "")
            manual_stok = cfg.get("MANUAL_STOK", None)
            return host, password, manual_stok
    else:
        default_cfg = {
            "ROUTER_HOST": "192.168.31.1",
            "ROUTER_PASSWORD": "zuiketsu1927",
            "MANUAL_STOK": None
        }
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(default_cfg, f, indent=4)
        print("已生成 config.json 模板，请填写密码后重新运行。")
        exit(0)

ROUTER_HOST, ROUTER_PASSWORD, MANUAL_STOK = load_config()
auth = XiaomiAuth(host=ROUTER_HOST, password=ROUTER_PASSWORD)

if MANUAL_STOK:
    auth.set_manual_stok(MANUAL_STOK)