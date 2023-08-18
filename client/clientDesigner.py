import tkinter as tk
from tkinter import messagebox

class ClientApp:
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.root.title("Client")
        self.root.geometry("372x402")

        self.txtIP = tk.Entry(root)
        self.txtIP.insert(0, "127.0.0.1")
        self.txtIP.pack(padx=10, pady=10)

        self.butConnect = tk.Button(root, text="Kết nối", command=self.connect_server)
        self.butConnect.pack(padx=10, pady=10)

        self.butApp = tk.Button(root, text="App Running", command=self.run_app)
        self.butApp.pack(padx=10, pady=10)

        self.butProcess = tk.Button(root, text="Process Running", command=self.run_process)
        self.butProcess.pack(padx=10, pady=10)

        self.butTat = tk.Button(root, text="Tắt máy", command=self.shutdown)
        self.butTat.pack(padx=10, pady=10)

        self.butReg = tk.Button(root, text="Sửa registry", command=self.edit_registry)
        self.butReg.pack(padx=10, pady=10)

        self.butExit = tk.Button(root, text="Thoát", command=root.destroy)
        self.butExit.pack(padx=10, pady=10)

        self.butPic = tk.Button(root, text="Chụp màn hình", command=self.take_screenshot)
        self.butPic.pack(padx=10, pady=10)

        self.butKeyLock = tk.Button(root, text="Keystroke", command=self.keylogger)
        self.butKeyLock.pack(padx=10, pady=10)

  

