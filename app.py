from nlp.parser import parse_command
from router.xiaomi import XiaomiRouter
from network.matcher import match_device

def main():
    cmd = input("请输入命令（如：禁用电视上网 / 禁用 AA:BB:CC:DD:EE:FF）: ")
    parsed = parse_command(cmd)
    if not parsed["action"] or not parsed["device"]:
        print("无效命令，请参考: 禁用设备 或 限制设备到5M")
        return

    router = XiaomiRouter()
    try:
        devices = router.get_device_list()
        router.print_devices(devices)

        if parsed["is_mac"]:
            target_mac = parsed["device"]
            target_name = target_mac
        else:
            target = match_device(parsed["device"], devices)
            if not target:
                print(f"未找到设备: {parsed['device']}")
                return
            target_mac = target["mac"]
            target_name = target.get("name", "未知设备")

        if parsed["action"] == "block":
            router.block_device(target_mac)
            print(f"已禁用 {target_name} ({target_mac})")
        elif parsed["action"] == "limit":
            if not parsed["limit"]:
                print("请指定限速值，例如: 限制电视到5M")
                return
            print(f"限速功能需要实现对应的API接口")
        else:
            print("不支持的操作")
    except Exception as e:
        print(f"执行失败: {e}")

if __name__ == "__main__":
    main()