import tkinter as tk
from tkinter import Button

class ServerApp:
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.root.title("Server")

        self.button1 = Button(self.root, text="Mở server", command=self.start_server)
        self.button1.pack(padx=10, pady=10)

    def open_server(self):
        # Thêm mã lệnh mở server vào đây
        pass
