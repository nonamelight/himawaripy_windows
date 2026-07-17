import os
import json
import sys
import appdirs

def load_config():
    config_dir = appdirs.user_config_dir(appname="himawaripy", appauthor=False)
    config_file = os.path.join(config_dir, "config.json")
    default_config = {"interval": 10, "scale": 100, "history_offset": 0, "run_at_startup": True}
    
    if os.path.exists(config_file):
        try:
            with open(config_file, "r") as f:
                data = json.load(f)
                default_config.update(data)
        except Exception:
            pass
    return default_config

def save_config(config):
    config_dir = appdirs.user_config_dir(appname="himawaripy", appauthor=False)
    os.makedirs(config_dir, exist_ok=True)
    config_file = os.path.join(config_dir, "config.json")
    try:
        with open(config_file, "w") as f:
            json.dump(config, f)
    except Exception:
        pass

def set_startup(enable):
    if sys.platform != "win32":
        return
    try:
        import winreg
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS)
        if enable:
            executable = sys.executable
            if executable.lower().endswith("python.exe"):
                executable = executable[:-10] + "pythonw.exe"
            cmd = f'"{executable}" -m himawaripy'
            winreg.SetValueEx(key, "HimawariPy", 0, winreg.REG_SZ, cmd)
        else:
            try:
                winreg.DeleteValue(key, "HimawariPy")
            except FileNotFoundError:
                pass
        winreg.CloseKey(key)
    except Exception as e:
        print("Failed to modify startup registry:", e)
