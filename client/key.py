from keylogDesigner import KeylogApp
import tkinter as tk

class Key(KeylogApp):
    def __init__(self, nw, nr, ns):
        super().__init__()
        self.nw = nw
        self.nr = nr
        self.ns = ns

    def send_hook(self):
        s = "HOOK"
        self.nw.write(s + "\n")

    def send_unhook(self):
        s = "UNHOOK"
        self.nw.write(s + "\n")

    def send_print(self):
        s = "PRINT"
        self.nw.write(s + "\n")
        # data = self.nr.read(5000)
        # s = data.decode()
        # self.txtKQ.insert(tk.END, s)

    def on_closing(self):
        s = "QUIT"
        self.nw.write(s + "\n")
        self.nw.flush()
        self.destroy()

    def clear_text(self):
        self.txtKQ.config(state='normal')
        self.txtKQ.delete('1.0', tk.END)
        self.txtKQ.config(state='disabled')