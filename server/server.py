import os
import socket
import subprocess
import threading
from io import BytesIO
from PIL import Image, ImageTk
import pygetwindow as gw
import ctypes
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import winreg
import keyboard
import mss
import win32gui
import win32process
import psutil
import appstart
import win32api
import win32con
from serverDesigner import ServerApp
import multiprocessing

class ServerFunc(ServerApp):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.recording = False
        self.recorded_keys = []
        

    def receive_signal(self):
        try:
            return self.nr.readline().strip()
        except Exception:
            return "QUIT"

    def shutdown(self):
        subprocess.Popen(["shutdown", "-s"])

    def base_registry_key(self, link):
        a = None
        if '\\' in link:
            root_key = link.split('\\')[0].upper()
            if root_key == "HKEY_CLASSES_ROOT":
                a = winreg.HKEY_CLASSES_ROOT
            elif root_key == "HKEY_CURRENT_USER":
                a = winreg.HKEY_CURRENT_USER
            elif root_key == "HKEY_LOCAL_MACHINE":
                a = winreg.HKEY_LOCAL_MACHINE
            elif root_key == "HKEY_USERS":
                a = winreg.HKEY_USERS
            elif root_key == "HKEY_CURRENT_CONFIG":
                a = winreg.HKEY_CURRENT_CONFIG
        return a

    def get_value(self, a, link, value_name):
        try:
            a = a.OpenSubKey(link)
        except Exception:
            return "Lỗi"

        try:
            op = a.GetValue(value_name)
        except Exception:
            return "Lỗi"

        if op is not None:
            if a.GetValueKind(value_name) == winreg.REG_MULTI_SZ:
                s = " ".join(op)
            elif a.GetValueKind(value_name) == winreg.REG_BINARY:
                s = " ".join([str(byte) for byte in op])
            else:
                s = str(op)
            return s
        else:
            return "Lỗi"

    def set_value(self, a, link, value_name, value, type_value):
        try:
            a = a.OpenSubKey(link, True)
        except Exception:
            return "Lỗi"
        
        if a is not None:
            kind = None
            if type_value == "String":
                kind = winreg.REG_SZ
            elif type_value == "Binary":
                kind = winreg.REG_BINARY
            elif type_value == "DWORD":
                kind = winreg.REG_DWORD
            elif type_value == "QWORD":
                kind = winreg.REG_QWORD
            elif type_value == "Multi-String":
                kind = winreg.REG_MULTI_SZ
            elif type_value == "Expandable String":
                kind = winreg.REG_EXPAND_SZ
            else:
                return "Lỗi"
            
            v = value
            try:
                a.SetValue(value_name, v, kind)
            except Exception:
                return "Lỗi"
            
            return "Set value thành công"
        else:
            return "Lỗi"

    def delete_value(self, a, link, value_name):
        try:
            a = a.OpenSubKey(link, True)
        except Exception:
            return "Lỗi"
        
        if a is not None:
            try:
                a.DeleteValue(value_name)
            except Exception:
                return "Lỗi"
            
            return "Xóa value thành công"
        else:
            return "Lỗi"

    def delete_key(self, a, link):
        try:
            a.DeleteSubKey(link)
        except Exception:
            return "Lỗi"
        return "Xóa key thành công"

    def registry(self):
        s = ""
        with open("fileReg.reg", "w") as fs:
            pass
        
        while True:
            s = self.receive_signal()
            if s == "REG":
                data = self.nr.read(5000).decode()
                with open("fileReg.reg", "w") as fin:
                    fin.write(data)
                s = os.path.join(os.path.dirname(__file__), "fileReg.reg")
                try:
                    subprocess.run(["regedit.exe", "/s", s], timeout=20)
                    self.nw.write("Sửa thành công\n")
                except Exception:
                    self.nw.write("Sửa thất bại\n")
                self.nw.flush()
            elif s == "QUIT":
                return

    def take_pic(self):
        ss = ""
        
        while True:
            ss = self.receive_signal()
            if ss == "TAKE":
                with mss.mss() as sct:
                    screenshot = sct.shot()
                    with open(screenshot, "rb") as image_file:
                        image_data = image_file.read()
                        print(image_data)
                        s = str(len(image_data))
                        self.nw.write(s + "\n")
                        self.nw.flush()
                        self.client.sendall(image_data)
            elif ss == "QUIT":
                return

    def hook_key(self, event_queue):
        print("Hooking keys")
        self.recording = True
        self.recorded_keys = []
        keyboard.on_press(self.record_key, event_queue)

    def unhook(self, event_queue):
        print("Unhooking keys")
        self.recording = False
        keyboard.unhook_all()
        event_queue.put(None)  # Send a signal to stop the process

    def record_key(self, event, event_queue=None):
        if self.recording:
            self.recorded_keys.append(event.name)
            if event_queue:
                event_queue.put(event.name)  # Send the recorded key to the queue

    def key_log(self):
        event_queue = multiprocessing.Queue()
        process = multiprocessing.Process(target=self.process_keys, args=(event_queue,))
        process.start()
        while True:
            s = self.receive_signal()  # Implement receive_signal function
            if s == "PRINT":
                self.print_keys()  # Implement print_keys function
            elif s == "HOOK":
                self.hook_key(event_queue)  # Implement hook_key function
            elif s == "UNHOOK":
                self.unhook(event_queue)  # Implement unhook function
            elif s == "QUIT":
                process.terminate()  # Terminate the process
                break

    def process_keys(self, event_queue):
        while True:
            key = event_queue.get()
            if key is None:  # Received a stop signal
                break
            print("Received key:", key)

    def get_process_info_from_pid(self, pid):
        try:
            process = psutil.Process(pid)
            return {
                "name": process.name().split(".exe")[0],
                "pid": process.pid,
                "num_threads": process.num_threads()
            }
        except psutil.NoSuchProcess:
            return None

    def application(self):
        ss = ""
        while True:
            ss = self.receive_signal()
            if ss == "XEM":
                running_apps = set()
                u = ""

                # Lấy danh sách cửa sổ đang chạy
                for window in gw.getWindowsWithTitle(''):
                    if window.isMinimized or not window.visible:
                        continue

                    # Lấy thông tin tiến trình tương ứng với cửa sổ
                    pid = ctypes.c_ulong(0)
                    ctypes.windll.user32.GetWindowThreadProcessId(window._hWnd, ctypes.byref(pid))
                    
                    process_info = self.get_process_info_from_pid(pid.value)
                    if process_info:
                        running_apps.add((process_info["name"], process_info["pid"], process_info["num_threads"]))

                u = str(len(running_apps))
                self.nw.write(u + "\n")
                self.nw.flush()

                for app_info in running_apps:
                    print(app_info)
                    try:
                        process_name = app_info[0]
                        process_id = app_info[1]
                        process_thread_count = app_info[2]
                        u = process_name
                        self.nw.write(u + "\n")
                        self.nw.flush()
                        u = str(process_id)
                        self.nw.write(u + "\n")
                        self.nw.flush()
                        u = str(process_thread_count)
                        self.nw.write(u + "\n")
                        self.nw.flush()
                    except Exception:
                        pass
            elif ss == "KILL":
                    ss = self.receive_signal()
                    if ss == "QUIT":
                        break
                    elif ss == "KILLID":
                        u = self.nr.readline().strip()
                        test2 = False
                        if u:
                            try:
                                process_id = int(u)
                                os.kill(process_id, 9)
                                self.nw.write("Da diet process\n")
                            except Exception:
                                self.nw.write("Loi\n")
                            self.nw.flush()
        
            elif ss == "START":
                    ss = self.receive_signal()
                    if ss == "STARTID":
                        u = self.nr.readline().strip()
                        print(u)
                        if u:
                            try:
                                u = u + ".exe"  # Thêm đuôi ".exe" vào tên tệp tin
                                subprocess.Popen([u])
                                self.nw.write("Process da duoc bat\n")
                                self.nw.flush()
                            except Exception as e:
                                self.nw.write("Loi: {}\n".format(str(e)))
                                self.nw.flush()
                    
            elif ss == "QUIT":
                return
                break

    def process(self):
        ss = ""
        while True:
            ss = self.receive_signal()
            if ss == "XEM":
                processes = []
                for process in psutil.process_iter():
                    processes.append(process)
                u = str(len(processes))
                self.nw.write(u + "\n")
                self.nw.flush()
                for p in processes:
                    print(p)
                    try:
                        process_name = p.name()
                        process_id = p.pid
                        process_thread_count = p.num_threads()
                        u = process_name
                        self.nw.write(u + "\n")
                        self.nw.flush()
                        u = str(process_id)
                        self.nw.write(u + "\n")
                        self.nw.flush()
                        u = str(process_thread_count)
                        self.nw.write(u + "\n")
                        self.nw.flush()
                    except Exception:
                        pass

            elif ss == "KILL":
                    ss = self.receive_signal()
                    if ss == "QUIT":
                        break
                    elif ss == "KILLID":
                        u = self.nr.readline().strip()
                        test2 = False
                        if u:
                            try:
                                process_id = int(u)
                                os.kill(process_id, 9)
                                self.nw.write("Da diet process\n")
                            except Exception:
                                self.nw.write("Loi\n")
                            self.nw.flush()
        
            elif ss == "START":
                    ss = self.receive_signal()
                    if ss == "STARTID":
                        u = self.nr.readline().strip()
                        print(u)
                        if u:
                            try:
                                u = u + ".exe"  # Thêm đuôi ".exe" vào tên tệp tin
                                subprocess.Popen([u])
                                self.nw.write("Process da duoc bat\n")
                                self.nw.flush()
                            except Exception as e:
                                self.nw.write("Loi: {}\n".format(str(e)))
                                self.nw.flush()

            elif ss == "QUIT":
                return
                break

    def start_server(self):
        ip = ("127.0.0.1", 5656)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ip)
        self.server.listen(100)
        print("Listening to client ...")
        self.client, _ = self.server.accept()
        self.ns = self.client.makefile('rw')
        self.nr = self.ns
        self.nw = self.ns
        s = ""
        while True:
            s = self.receive_signal()
            print(s)
            if s == "KEYLOG":
                self.key_log()
            # elif s == "SHUTDOWN":
            #     self.shutdown()
            # elif s == "REGISTRY":
            #     self.registry()
            if s == "TAKEPIC":
                self.take_pic()
            elif s == "PROCESS":
                self.process()
            elif s == "APPLICATION":
                self.application()
            elif s == "QUIT":
                break
        
        self.client.close()
        self.server.close()
  
if __name__ == "__main__":
    root = tk.Tk()
    app = ServerFunc(root)
    root.mainloop()
