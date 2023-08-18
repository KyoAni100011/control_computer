import tkinter as tk

class Start(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Start")

        self.butStart = tk.Button(self, text="Start", command=self.butStart_Click)
        self.butStart.pack()

        self.txtID = tk.Entry(self)
        self.txtID.insert(0, "Nhập tên")
        self.txtID.pack()

        self.protocol("WM_DELETE_WINDOW", self.start_closing)
    