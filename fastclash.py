import wx
import wx.grid as gridlib
import wx.adv
import os
import sys
import ctypes
import datetime
import psutil
import requests
import re
import threading
import base64
import io
from concurrent.futures import ThreadPoolExecutor

# ========== fastclash.py code refactored into a Panel ==========

CONFIG_FILE = "config.txt"
logo_base64_data = "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"


def get_logo_bitmap():
    """解码Base64数据并返回一个 wx.Bitmap 对象"""
    try:
        image_data = base64.b64decode(logo_base64_data)
        stream = io.BytesIO(image_data)
        image = wx.Image(stream)
        bitmap = wx.Bitmap(image)
        return bitmap
    except Exception as e:
        print(f"从Base64加载图片失败: {e}")
        return wx.Bitmap(32, 32) # 返回一个空Bitmap以防程序崩溃

def get_logo_icon():
    """从Bitmap创建并返回一个 wx.Icon 对象"""
    icon = wx.Icon()
    icon.CopyFromBitmap(get_logo_bitmap())
    return icon


class FastClashPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.file_picker1 = wx.FilePickerCtrl(self, message="选择程序 (exe)")
        self.dir_picker = wx.DirPickerCtrl(self, message="选择文件夹")
        self.url_text_ctrl = wx.TextCtrl(self, style=wx.TE_MULTILINE, size=(300, 25))

        # 程序
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(wx.StaticText(self, label="主程序:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        hbox1.Add(self.file_picker1, 1, wx.EXPAND | wx.ALL, 5)
        vbox.Add(hbox1, 0, wx.EXPAND)

        # 配置文件夹
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add(wx.StaticText(self, label="配置文件夹:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        hbox2.Add(self.dir_picker, 1, wx.EXPAND | wx.ALL, 5)
        vbox.Add(hbox2, 0, wx.EXPAND)

        # 输入网址
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3.Add(wx.StaticText(self, label="输入网址:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        hbox3.Add(self.url_text_ctrl, 1, wx.EXPAND | wx.ALL, 5)
        download_btn = wx.Button(self, label="下载文件")

        hbox3.Add(download_btn, 0, wx.ALL, 5)
        vbox.Add(hbox3, 0, wx.EXPAND)


        # Main buttons
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        run_btn = wx.Button(self, label="运行程序")
        kill_btn = wx.Button(self, label="结束程序")
        proxy_on_btn = wx.Button(self, label="打开代理")
        proxy_off_btn = wx.Button(self, label="关闭代理")
        button_height = 50
        run_btn.SetMinSize((-1, button_height))
        kill_btn.SetMinSize((-1, button_height))
        proxy_on_btn.SetMinSize((-1, button_height))
        proxy_off_btn.SetMinSize((-1, button_height))
        btn_sizer.Add(run_btn, 0, wx.ALL, 5)
        btn_sizer.Add(kill_btn, 0, wx.ALL, 5)
        btn_sizer.Add(proxy_on_btn, 0, wx.ALL, 5)
        btn_sizer.Add(proxy_off_btn, 0, wx.ALL, 5)
        vbox.Add(btn_sizer, 0, wx.CENTER)


        self.other_file_picker1 = wx.FilePickerCtrl(self, message="选择程序 (exe)")
        self.other_file_picker2 = wx.FilePickerCtrl(self, message="选择配置 (config)")
        self.other_url_text_ctrl = wx.TextCtrl(self, style=wx.TE_MULTILINE, size=(300, 25))

        # 程序选择
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        hbox4.Add(wx.StaticText(self, label="次程序"), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        hbox4.Add(self.other_file_picker1, 1, wx.EXPAND)
        vbox.Add(hbox4, 0, wx.EXPAND | wx.ALL, 5)

        # 配置文件夹
        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        hbox5.Add(wx.StaticText(self, label="配置文件"), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        hbox5.Add(self.other_file_picker2, 1, wx.EXPAND)
        vbox.Add(hbox5, 0, wx.EXPAND | wx.ALL, 5)

        # 输入网址
        hbox6 = wx.BoxSizer(wx.HORIZONTAL)
        hbox6.Add(wx.StaticText(self, label="运行命令"), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        hbox6.Add(self.other_url_text_ctrl, 1, wx.EXPAND)
        vbox.Add(hbox6, 0, wx.EXPAND | wx.ALL, 5)


        # Log box
        self.log = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        vbox.Add(wx.StaticText(self, label="运行日志:"), 0, wx.ALL, 5)
        vbox.Add(self.log, 1, wx.EXPAND | wx.ALL, 5)

        # Program status
        self.status_text = wx.StaticText(self, label="主程序状态: 停止运行", style=wx.ALIGN_CENTER)
        vbox.Add(self.status_text, 0, wx.CENTER)

        self.status_text2 = wx.StaticText(self, label="次程序状态: 停止运行", style=wx.ALIGN_CENTER)
        vbox.Add(self.status_text2, 0, wx.CENTER)
       
        self.SetSizer(vbox)

        # Event bindings
        self.file_picker1.Bind(wx.EVT_FILEPICKER_CHANGED, self.on_path_change)
        self.dir_picker.Bind(wx.EVT_DIRPICKER_CHANGED, self.on_path_change)
        self.url_text_ctrl.Bind(wx.EVT_TEXT, self.on_path_change)
        self.other_file_picker1.Bind(wx.EVT_FILEPICKER_CHANGED, self.on_path_change)
        self.other_file_picker2.Bind(wx.EVT_FILEPICKER_CHANGED, self.on_path_change)
        self.other_url_text_ctrl.Bind(wx.EVT_TEXT, self.on_path_change)        
        
        run_btn.Bind(wx.EVT_BUTTON, self.on_run)
        kill_btn.Bind(wx.EVT_BUTTON, self.on_kill)
        proxy_on_btn.Bind(wx.EVT_BUTTON, self.on_proxy_on)
        proxy_off_btn.Bind(wx.EVT_BUTTON, self.on_proxy_off)
        download_btn.Bind(wx.EVT_BUTTON, self.on_download)

        self.load_config()
        self.auto_run()

        # Timer to check program status
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)
        self.timer.Start(1000)

    def on_timer(self, event):
        program = self.file_picker1.GetPath()
        program2 = self.other_file_picker1.GetPath()
        if self.is_program_running(program):
            self.status_text.SetForegroundColour(wx.BLUE)
            self.status_text.SetLabel("主程序状态: 正在运行")
        else:
            self.status_text.SetForegroundColour(wx.RED)
            self.status_text.SetLabel("主程序状态: 停止运行")
        
        if self.is_program_running(program2):
            self.status_text2.SetForegroundColour(wx.BLUE)
            self.status_text2.SetLabel("次程序状态: 正在运行")
        else:
            self.status_text2.SetForegroundColour(wx.RED)
            self.status_text2.SetLabel("次程序状态: 停止运行")


    def on_path_change(self, event):
        program = self.file_picker1.GetPath()
        folder = self.dir_picker.GetPath()
        url = self.url_text_ctrl.GetValue()
        program2 = self.other_file_picker1.GetPath()
        config2 = self.other_file_picker2.GetPath()
        configrun2 = self.other_url_text_ctrl.GetValue()
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                lines = f.read().splitlines()
                secret = lines[6] if len(lines) > 6 else ""
                testurl = lines[7] if len(lines) > 7 else ""
        except (IOError, IndexError):
            secret = ""
            testurl= ""
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            f.write(f"{program}\n{folder}\n{url}\n{program2}\n{config2}\n{configrun2}\n{secret}\n{testurl}\n")

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                lines = f.read().splitlines()
                if len(lines) > 0 and os.path.exists(lines[0]):
                    self.file_picker1.SetPath(lines[0])
                if len(lines) > 1 and os.path.exists(lines[1]):
                    self.dir_picker.SetPath(lines[1])
                if len(lines) > 2 :
                    self.url_text_ctrl.SetValue(lines[2])
                if len(lines) > 3 and os.path.exists(lines[3]):
                    self.other_file_picker1.SetPath(lines[3])
                if len(lines) > 4 and os.path.exists(lines[4]):
                    self.other_file_picker2.SetPath(lines[4])           
                if len(lines) > 5 :
                    self.other_url_text_ctrl.SetValue(lines[5])

    def log_message(self, msg):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log.AppendText(f"[{timestamp}] {msg}\n")

    def is_program_running(self, program_path):
        exe_name = os.path.basename(program_path).lower()
        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name'] and proc.info['name'].lower() == exe_name:
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return False

    def run_program(self):
        program = self.file_picker1.GetPath()
        folder = self.dir_picker.GetPath()
        if not os.path.exists(program) or not os.path.exists(folder):
            self.log_message("程序路径或文件夹无效，未执行。")
            return
        if self.is_program_running(program):
            self.log_message("程序已经在运行，未再次启动。")
            return
        try:
            params = f'-d "{folder}"'
            ctypes.windll.shell32.ShellExecuteW(None, "open", program, params, None, 0)
            self.log_message(f"已启动: {program} {params}")
        except Exception as e:
            self.log_message(f"{program}启动失败: {e}")
        
        program2 = self.other_file_picker1.GetPath()
        config2 = self.other_file_picker2.GetPath()
        configrun2 = self.other_url_text_ctrl.GetValue()
        if not os.path.exists(program2) or not os.path.exists(folder):
            self.log_message("程序路径或文件夹无效，未执行。")
            return
        if self.is_program_running(program2):
            self.log_message("程序已经在运行，未再次启动。")
            return
        try:
            params2 = f' {configrun2} {config2}'
            ctypes.windll.shell32.ShellExecuteW(None, "open", program2, params2, None, 0)
            self.log_message(f"已启动: {program2} {params2}")
        except Exception as e:
            self.log_message(f"{program2}启动失败: {e}")
        

    def on_run(self, event):
        self.run_program()

    def auto_run(self):
        self.run_program()

    def on_kill(self, event):
        program = self.file_picker1.GetPath()
        program2 = self.other_file_picker1.GetPath()
        
        if not os.path.exists(program):
            self.log_message("未选择有效的程序，无法结束。")
            return
        exe_name = os.path.basename(program).lower()
        killed = False
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'] and proc.info['name'].lower() == exe_name:
                    proc.kill()
                    killed = True
                    self.log_message(f"已结束进程: {exe_name} (PID {proc.info['pid']})")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        if not killed:
            self.log_message(f"未发现正在运行的 {exe_name} 进程。")
            
        if not os.path.exists(program2):
            self.log_message("未选择有效的程序，无法结束。")
            return
        exe_name = os.path.basename(program2).lower()
        killed = False
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'] and proc.info['name'].lower() == exe_name:
                    proc.kill()
                    killed = True
                    self.log_message(f"已结束进程: {exe_name} (PID {proc.info['pid']})")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        if not killed:
            self.log_message(f"未发现正在运行的 {exe_name} 进程。")
            
        self.update_program_status()

    def update_program_status(self):
        program = self.file_picker1.GetPath()
        if self.is_program_running(program):
            self.status_text.SetForegroundColour(wx.BLUE)
            self.status_text.SetLabel("程序状态: 正在运行")
        else:
            self.status_text.SetForegroundColour(wx.RED)
            self.status_text.SetLabel("程序状态: 停止运行")
            
        program2 = self.other_file_picker1.GetPath()
        if self.is_program_running(program2):
            self.status_text2.SetForegroundColour(wx.BLUE)
            self.status_text2.SetLabel("程序状态: 正在运行")
        else:
            self.status_text2.SetForegroundColour(wx.RED)
            self.status_text2.SetLabel("程序状态: 停止运行")        

    def on_proxy_on(self, event):
        try:
            os.system('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings" /v ProxyEnable /t REG_DWORD /d 1 /f')
            os.system('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings" /v ProxyServer /t REG_SZ /d 127.0.0.1:7892 /f')
            self.log_message("代理已打开: 127.0.0.1:7892")
        except Exception as e:
            self.log_message(f"代理开启失败: {e}")

    def on_proxy_off(self, event):
        try:
            os.system('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings" /v ProxyEnable /t REG_DWORD /d 0 /f')
            self.log_message("代理已关闭")
        except Exception as e:
            self.log_message(f"代理关闭失败: {e}")

    def on_download(self, event):
        url = self.url_text_ctrl.GetValue()
        folder = self.dir_picker.GetPath()
        if not url or not folder:
            self.log_message("错误：请填写网址和选择文件夹")
            return
        try:
            file_name = "config.yaml"
            file_path = os.path.join(folder, file_name)
            response = requests.get(url)
            response.raise_for_status()
            with open(file_path, 'wb') as f:
                f.write(response.content)
            self.log_message(f"文件已下载并保存到: {file_path}")
        except requests.exceptions.RequestException as e:
            self.log_message(f"下载失败: {e}")

# ========== webtest.py code refactored into a Panel ==========

CLASH_API = "http://127.0.0.1:9090"

def clash_get(path, secret=None):
    url = f"{CLASH_API}{path}"
    headers = {"Authorization": f"Bearer {secret}"} if secret else {}
    res = requests.get(url, headers=headers, timeout=10)
    res.raise_for_status()
    return res.json()

def clash_put(path, data=None, secret=None):
    url = f"{CLASH_API}{path}"
    headers = {"Authorization": f"Bearer {secret}"} if secret else {}
    res = requests.put(url, headers=headers, json=data)
    res.raise_for_status()
    try:
        return res.json()
    except ValueError:
        return {}
        
def clash_patch(path, data=None, secret=None):
    url = f"{CLASH_API}{path}"
    headers = {"Authorization": f"Bearer {secret}"} if secret else {}
    res = requests.patch(url, headers=headers, json=data)
    res.raise_for_status()
    try:
        return res.json()
    except ValueError:
        return {}

def clash_close_all_connections(secret=None):
    """Closes all active connections via the Clash API."""
    url = f"{CLASH_API}/connections"
    headers = {"Authorization": f"Bearer {secret}"} if secret else {}
    res = requests.delete(url, headers=headers)
    res.raise_for_status()
    return res

class WebTestPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # 面板密码
        hbox_secret = wx.BoxSizer(wx.HORIZONTAL)
        hbox_secret.Add(wx.StaticText(self, label="面板密码:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.clash_secret_text_ctrl = wx.TextCtrl(self)
        self.clash_secret_text_ctrl.Bind(wx.EVT_TEXT, self.on_path_change)
        hbox_secret.Add(self.clash_secret_text_ctrl, 1, wx.EXPAND | wx.ALL, 5)
        vbox.Add(hbox_secret, 0, wx.EXPAND)

        # 测试url
        hbox_testurl = wx.BoxSizer(wx.HORIZONTAL)
        hbox_testurl.Add(wx.StaticText(self, label="测试url:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.clash_testurl_text_ctrl = wx.TextCtrl(self)
        self.clash_testurl_text_ctrl.Bind(wx.EVT_TEXT, self.on_path_change)
        hbox_testurl.Add(self.clash_testurl_text_ctrl, 1, wx.EXPAND | wx.ALL, 5)
        vbox.Add(hbox_testurl, 0, wx.EXPAND)
        
        # New: Proxy Group Selector
        hbox_selector = wx.BoxSizer(wx.HORIZONTAL)
        hbox_selector.Add(wx.StaticText(self, label="选择代理组:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 5)
        self.proxy_group_choice = wx.Choice(self, choices=[])
        self.proxy_group_choice.Bind(wx.EVT_CHOICE, self.on_group_select)
        hbox_selector.Add(self.proxy_group_choice, 1, wx.EXPAND | wx.ALL, 5)
        vbox.Add(hbox_selector, 0, wx.EXPAND)

        # New: Proxy Mode Selector
        hbox_mode = wx.BoxSizer(wx.HORIZONTAL)
        hbox_mode.Add(wx.StaticText(self, label="选择代理模式:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 5)
        self.mode_choice = wx.Choice(self, choices=["全局", "规则", "直连"])
        self.mode_choice.Bind(wx.EVT_CHOICE, self.on_mode_select)
        hbox_mode.Add(self.mode_choice, 1, wx.EXPAND | wx.ALL, 5)
        vbox.Add(hbox_mode, 0, wx.EXPAND)

        # Buttons
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.refresh_btn = wx.Button(self, label="刷新节点列表")
        self.delay_btn = wx.Button(self, label="刷新延迟")
        self.refresh_btn.SetMinSize((-1, 50))
        self.delay_btn.SetMinSize((-1, 50))
        btn_sizer.Add(self.refresh_btn, 0, wx.ALL, 5)
        btn_sizer.Add(self.delay_btn, 0, wx.ALL, 5)
        vbox.Add(btn_sizer, 0, wx.EXPAND)

        # Grid
        self.grid = gridlib.Grid(self)
        self.grid.CreateGrid(0, 2)
        self.grid.SetColLabelValue(0, "节点")
        self.grid.SetColLabelValue(1, "延迟(ms)")
        self.grid.SetRowLabelSize(0)  # Hide the row label column
        
        self.grid.EnableEditing(False)
        
        vbox.Add(self.grid, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(vbox)

        # Setup thread pool for delay checks
        self.executor = ThreadPoolExecutor(max_workers=5)

        self.proxy_data = {}
        self.current_group_name = ""
        
        self.load_secret_from_config()

        # Start the initial refresh in a separate thread
        threading.Thread(target=self._initial_setup).start()
        # 绑定刷新/延迟按钮事件 与 表格双击事件（用于切换节点）
        self.refresh_btn.Bind(wx.EVT_BUTTON, self.on_refresh)
        self.delay_btn.Bind(wx.EVT_BUTTON, self.on_delay)
        self.grid.Bind(gridlib.EVT_GRID_CELL_LEFT_DCLICK, self.on_select_node)


    def on_path_change(self, event):
        """Save secret to config.txt when the text box changes"""
        secret = self.clash_secret_text_ctrl.GetValue()
        testurl = self.clash_testurl_text_ctrl.GetValue()
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                lines = f.read().splitlines()
                program = lines[0] if len(lines) > 0 else ""
                folder = lines[1] if len(lines) > 1 else ""
                url = lines[2] if len(lines) > 2 else ""
                program2 = lines[3] if len(lines) > 3 else ""
                config2 = lines[4] if len(lines) > 4 else ""
                configrun2 = lines[5] if len(lines) > 5 else ""
        except (IOError, IndexError):
            program = ""
            folder = ""
            url = ""
            program2 = ""
            config2 = ""
            configrun2 = ""
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            f.write(f"{program}\n{folder}\n{url}\n{program2}\n{config2}\n{configrun2}\n{secret}\n{testurl}\n")

    def load_secret_from_config(self):
        """Load secret from config.txt on startup"""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    lines = f.read().splitlines()
                    if len(lines) > 6:
                        self.clash_secret_text_ctrl.SetValue(lines[6])
                    if len(lines) > 7:
                        self.clash_testurl_text_ctrl.SetValue(lines[7])
            except (IOError, IndexError):
                pass


                
    def _initial_setup(self):
        """Initial setup: fetch proxies and current mode."""
        self._fetch_proxies_in_background()
        self._fetch_mode_in_background()

    def on_group_select(self, event):
        """Handle the change of proxy group selector"""
        self.current_group_name = self.proxy_group_choice.GetString(self.proxy_group_choice.GetSelection())
        self.executor_wait_counter = 0  # Reset the counter
        self.delay_btn.Enable()  # Immediately re-enable the button
        wx.CallAfter(self._update_ui_with_nodes)



    def on_mode_select(self, event):
        """Handle the change of proxy mode selector"""
        secret = self.clash_secret_text_ctrl.GetValue()
        selected_mode_zh = self.mode_choice.GetString(self.mode_choice.GetSelection())
        mode_map = {"全局": "Global", "规则": "Rule", "直连": "Direct"}
        mode_en = mode_map.get(selected_mode_zh, "Rule")
        
        try:
            clash_patch("/configs", {"mode": mode_en}, secret)
            clash_close_all_connections(secret)
            self.log_message(f"代理模式已切换为: {selected_mode_zh}")
        except requests.exceptions.RequestException as e:
            if e.response.status_code == 401:
                self.log_message("切换代理模式失败: 认证失败，请检查面板密码是否正确。")
            else:
                self.log_message(f"切换代理模式失败: {e}")

    def on_refresh(self, event=None):
        """Handle the refresh button click by starting a background thread."""
        self.refresh_btn.Disable()
        threading.Thread(target=self._fetch_proxies_in_background).start()

    def _fetch_proxies_in_background(self):
        """Fetch all proxies from Clash API in a background thread."""
        secret = self.clash_secret_text_ctrl.GetValue()
        try:
            data = clash_get("/proxies", secret)
            self.proxy_data = data["proxies"]
            
            # Find all selector groups
            group_names = [name for name, info in self.proxy_data.items() if info["type"] == "Selector"]
            
            wx.CallAfter(self._update_ui_with_groups, group_names)

        except requests.exceptions.RequestException as e:
            # On failure, clear proxy data and UI, then re-enable the button
            self.proxy_data = {}
            wx.CallAfter(self._update_ui_with_groups, [])
            if e.response and e.response.status_code == 401:
                wx.CallAfter(self.log_message, "获取节点失败: 认证失败，请检查面板密码是否正确。")
            else:
                wx.CallAfter(self.log_message, f"获取节点失败: {e}")
            wx.CallAfter(self.refresh_btn.Enable)

    def _fetch_mode_in_background(self):
        """Fetch the current mode from Clash API in a background thread."""
        secret = self.clash_secret_text_ctrl.GetValue()
        try:
            data = clash_get("/configs", secret)
            current_mode_en = data.get("mode", "Rule")
            mode_map_rev = {"Global": "全局", "Rule": "规则", "Direct": "直连"}
            current_mode_zh = mode_map_rev.get(current_mode_en, "规则")
            wx.CallAfter(self.mode_choice.SetStringSelection, current_mode_zh)
        except requests.exceptions.RequestException as e:
            if e.response.status_code == 401:
                wx.CallAfter(self.log_message, "获取代理模式失败: 认证失败，请检查面板密码是否正确。")
            else:
                wx.CallAfter(self.log_message, f"获取代理模式失败: {e}")

    def _update_ui_with_groups(self, group_names):
        """Update the proxy group dropdown. Must be called from the main thread."""
        self.proxy_group_choice.SetItems(group_names)
        
        # Select the PROXY group by default if it exists, otherwise select the first one
        if "PROXY" in group_names:
            self.proxy_group_choice.SetStringSelection("PROXY")
            self.current_group_name = "PROXY"
        elif group_names:
            self.proxy_group_choice.SetSelection(0)
            self.current_group_name = group_names[0]
        else:
            self.current_group_name = ""
            self.proxy_group_choice.SetSelection(wx.NOT_FOUND) # Fix: Set to no selection if no groups
            
        # Now update the grid with the selected group's nodes
        self._update_ui_with_nodes()
        self.refresh_btn.Enable()
        self.log_message("节点列表和代理组列表刷新成功")
        

    def _update_ui_with_nodes(self):
        """Update the UI grid with the fetched nodes of the current group. Must be called from the main thread."""
        self.grid.ClearGrid()
        if self.grid.GetNumberRows() > 0:
            self.grid.DeleteRows(0, self.grid.GetNumberRows())

        if not self.current_group_name or self.current_group_name not in self.proxy_data:
            return

        group = self.proxy_data[self.current_group_name]
        current_node = group.get("now", "")
        nodes = group.get("all", [])

        for i, node in enumerate(nodes):
            self.grid.AppendRows(1)
            self.grid.SetCellValue(i, 0, node)
            self.grid.SetCellValue(i, 1, "")
            if node == current_node:
                self.grid.SetCellTextColour(i, 0, wx.BLUE)
                self.grid.SetCellFont(i, 0, wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))
                self.grid.SetCellTextColour(i, 1, wx.BLUE)
                self.grid.SetCellFont(i, 1, wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        
        self.grid.AutoSizeColumns()

    def on_delay(self, event):
        """用线程刷新所有节点的延迟"""
        self.delay_btn.Disable()
        self.log_message("开始测试所有节点延迟...")
        self.executor_wait_counter = 0  # Reset the counter
        if self.grid.GetNumberRows() == 0:
            self.delay_btn.Enable()
            self.log_message("没有节点可供测试。")
            return
            
        for row in range(self.grid.GetNumberRows()):
            node_name = self.grid.GetCellValue(row, 0)
            self.grid.SetCellValue(row, 1, "正在测试...")
        wx.Yield()  # Add this line to force UI refresh
        
        for row in range(self.grid.GetNumberRows()):
            node_name = self.grid.GetCellValue(row, 0)
            self.executor.submit(self._check_node_delay, row, node_name)
    
    def _check_node_delay(self, row, node_name):
        """Background task for a single delay check"""
        secret = self.clash_secret_text_ctrl.GetValue()
        testurl = self.clash_testurl_text_ctrl.GetValue()
        url = f"/proxies/{node_name}/delay?timeout=5000&url={testurl}"
        try:
            delay_info = clash_get(url, secret)
            delay = delay_info.get("delay", -1)
            delay_str = str(delay) if delay >= 0 else "超时"
        except requests.exceptions.Timeout:
            delay_str = "超时"
        except requests.exceptions.RequestException:
            delay_str = "请求错误"
        except Exception:
            delay_str = "未知错误"
        
        wx.CallAfter(self.update_grid_delay, row, delay_str)
        # Use a counter to track completion and re-enable the button
        wx.CallAfter(self.increment_counter)


    def update_grid_delay(self, row, delay_str):
        """Updates a single cell in the grid"""
        if row < self.grid.GetNumberRows():
            self.grid.SetCellValue(row, 1, delay_str)
        else:
            pass

    def increment_counter(self):
        """Increments the counter and checks if all tasks are complete."""
        self.executor_wait_counter += 1
        if self.executor_wait_counter >= self.grid.GetNumberRows() and self.grid.GetNumberRows() > 0:
            self.delay_btn.Enable()
    
    def on_select_node(self, event):
        """双击节点 -> 切换"""
        row = event.GetRow()
        node_name = self.grid.GetCellValue(row, 0)
        secret = self.clash_secret_text_ctrl.GetValue()
        group_name = self.current_group_name

        if not group_name:
            self.log_message("未选择代理组。")
            return

        try:
            # Switch node and close old connections
            clash_put(f"/proxies/{group_name}", {"name": node_name}, secret)
            clash_close_all_connections(secret)
            self.log_message(f"已切换 {group_name} -> {node_name} 并关闭旧连接")

            # Manually update the 'now' field in the local proxy data to reflect the change
            if group_name in self.proxy_data:
                self.proxy_data[group_name]["now"] = node_name

            # Refresh the grid using the updated local data. This only affects the table.
            self._update_ui_with_nodes()

        except requests.exceptions.RequestException as e:
            # Improved error handling
            if hasattr(e, 'response') and e.response is not None and e.response.status_code == 401:
                self.log_message("切换节点失败: 认证失败，请检查面板密码是否正确。")
            else:
                self.log_message(f"切换节点失败: {e}")

    def log_message(self, msg):
        parent_frame = self.GetParent().GetParent()
        if hasattr(parent_frame, 'fastclash_panel'):
            parent_frame.fastclash_panel.log_message(msg)
        else:
            print(msg)



# ========== New Combined Main Frame ==========

class MyTaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame):
        super().__init__()
        self.frame = frame  # 保存主窗口引用

        # 设置任务栏图标
        self.icon = get_logo_icon()
        self.SetIcon(self.icon, "fastclash")

        # 左键点击显示窗口
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_click)

    def CreatePopupMenu(self):
        # 创建右键菜单
        menu = wx.Menu()

        show_item = menu.Append(wx.ID_ANY, "显示窗口")
        self.Bind(wx.EVT_MENU, self.on_show, show_item)

        exit_item = menu.Append(wx.ID_EXIT, "退出")
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)

        return menu

    def restore_frame(self):
        """恢复窗口"""
        if not self.frame.IsShown():
            self.frame.Show()
        if self.frame.IsIconized():
            self.frame.Iconize(False)  # 取消最小化
        self.frame.Raise()  # 窗口置顶

    def on_left_click(self, event):
        """左键点击图标：显示主窗口"""
        self.restore_frame()

    def on_show(self, event):
        """右键菜单 - 显示"""
        self.restore_frame()

    def on_exit(self, event):
        """右键菜单 - 退出"""
        self.frame.Destroy()
        wx.GetApp().ExitMainLoop()


class CombinedFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="fastclash", size=(600, 550))

        self.SetIcon(get_logo_icon())

        splitter = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE)

        self.fastclash_panel = FastClashPanel(splitter)
        self.webtest_panel = WebTestPanel(splitter)

        splitter.SplitVertically(self.fastclash_panel, self.webtest_panel)
        splitter.SetSashPosition(340)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(splitter, 1, wx.EXPAND | wx.ALL, 0)
        self.SetSizer(sizer)

        # 绑定关闭事件：隐藏到后台
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_close(self, event):
        """点 X 时隐藏，而不是退出"""
        self.Hide()


class MyApp(wx.App):
    def OnInit(self):
        frame = CombinedFrame()
        frame.taskbar_icon = MyTaskBarIcon(frame)

        # 启动时不显示窗口（最小化到托盘）
        frame.Hide()

        return True


if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()