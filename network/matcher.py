import json
import os

def load_aliases():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(base_dir, "data", "aliases.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def match_device(target_name, devices):
    aliases = load_aliases()
    target_aliases = aliases.get(target_name, [])
    for device in devices:
        name = device.get("name", "").lower()
        for alias in target_aliases:
            if alias.lower() in name:
                return device
    return None