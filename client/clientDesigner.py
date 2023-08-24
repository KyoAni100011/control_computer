import tkinter as tk
from tkinter import messagebox

class ClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Client")
        self.root.geometry("372x302")

        custom_font = ("Helvetica", 9)

        self.butApp = self.create_button("App Running", custom_font, self.run_app, 93, 64, 145, 63)
        self.butConnect = self.create_button("Kết nối", custom_font, self.connect_server, 244, 27, 100, 23)
        self.txtIP = tk.Entry(self.root)
        self.txtIP.place(x=12, y=29, width=226, height=20)
        self.txtIP.insert(0, "127.0.0.1")
        self.butTat = self.create_button("Tắt\nmáy", custom_font, self.shutdown, 93, 133, 48, 57)
        self.butReg = self.create_button("Sửa registry", custom_font, self.edit_registry, 93, 196, 198, 65)
        self.butExit = self.create_button("Thoát", custom_font, self.exit_app, 297, 196, 47, 65)
        self.butPic = self.create_button("Chụp màn hình", custom_font, self.take_screenshot, 147, 133, 91, 57)
        self.butKeyLock = self.create_button("Keystroke", custom_font, self.keylogger, 244, 64, 100, 126)
        self.butProcess = self.create_button("Process\nRunning", custom_font, self.run_process, 12, 64, 75, 197)

    def create_button(self, text, font, command, x, y, width, height):
        button = tk.Button(self.root, text=text, font=font, command=command, relief=tk.GROOVE)
        button.place(x=x, y=y, width=width, height=height)
        button.bind("<Enter>", self.on_enter)
        button.bind("<Leave>", self.on_leave)
        return button

    def on_enter(self, event):
        event.widget.config(bg="#DDDDDD")  # Change background color on hover

    def on_leave(self, event):
        event.widget.config(bg="SystemButtonFace")  # Reset background color on leave

        

        

  

