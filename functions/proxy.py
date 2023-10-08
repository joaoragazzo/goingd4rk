import winreg
import requests
import json
import win32serviceutil


class Proxy:

    def __init__(self):
        self.reg_path = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
        self.value_name = "ProxyEnable"
        self.key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.reg_path, 0, winreg.KEY_READ | winreg.KEY_WRITE)
        self.current_value, _ = winreg.QueryValueEx(self.key, self.value_name)

    def change_proxy_state(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.reg_path, 0, winreg.KEY_READ | winreg.KEY_WRITE)
            self.current_value, _ = winreg.QueryValueEx(key, self.value_name)
            new_value = 1 if self.current_value == 0 else 0
            winreg.SetValueEx(key, self.value_name, 0, winreg.REG_DWORD, new_value)
            winreg.CloseKey(key)

            return self.get_identity()

        except Exception as e:
            print(f"Erro ao alterar a configuração do proxy: {e}")

    def new_location(self):
        if self.current_value:
            self.change_proxy_state()
            win32serviceutil.RestartService("tor")
            self.change_proxy_state()
        else:
            win32serviceutil.RestartService("tor")

    def get_identity(self):
        res = requests.get("http://ip-api.com/json/").json()
        return res
