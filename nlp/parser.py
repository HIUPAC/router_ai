import re

def parse_command(text):
    result = {"action": None, "device": None, "limit": None, "is_mac": False}
    text_lower = text.lower()

    if re.search(r'禁用|禁止|拉黑|屏蔽', text_lower):
        result["action"] = "block"
    elif re.search(r'限制|限速', text_lower):
        result["action"] = "limit"
    else:
        return result

    mac_pattern = r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})'
    mac_match = re.search(mac_pattern, text, re.IGNORECASE)
    if mac_match:
        result["device"] = mac_match.group(0).upper()
        result["is_mac"] = True
        return result

    device_keywords = ["电视", "电脑", "手机", "ipad"]
    for keyword in device_keywords:
        if keyword in text_lower:
            result["device"] = keyword
            break

    if result["action"] == "limit" and not result["is_mac"]:
        speed_match = re.search(r'(\d+)m', text_lower)
        if speed_match:
            result["limit"] = int(speed_match.group(1))

    return result