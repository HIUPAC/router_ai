import json
import requests
from urllib.parse import quote
from config import auth, ROUTER_HOST


class XiaomiRouter:
    def __init__(self):
        self.session = auth.get_session()
        self.stok = None

    def ensure_login(self):
        if not auth.stok:
            if not auth.login():
                raise Exception("登录失败，请检查密码和网络")
        self.stok = auth.stok
        return True

    def get_device_list(self):
        self.ensure_login()
        url = f"http://{ROUTER_HOST}/cgi-bin/luci;stok={self.stok}/api/misystem/devicelist"
        resp = self.session.get(url)
        data = resp.json()
        return data.get("list", [])

    def print_devices(self, devices):
        print("\n当前在线设备:\n")
        for idx, dev in enumerate(devices, 1):
            print(f"[{idx}] 名称: {dev.get('name')} | IP: {dev.get('ip')} | MAC: {dev.get('mac')}")

    def block_device(self, mac):
        self.ensure_login()
        encoded_mac = quote(mac)
        url = f"http://{ROUTER_HOST}/cgi-bin/luci;stok={self.stok}/api/xqsystem/set_mac_filter?mac={encoded_mac}&wan=1"
        print(f"\n请求禁用设备 {mac} ...")
        resp = self.session.get(url)
        print(f"响应: {resp.text}")
        return resp.json()