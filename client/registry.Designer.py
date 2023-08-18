import tkinter as tk
from tkinter import ttk

class RegistryEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Registry Editor")
        
        self.txtReg = tk.Text(self, height=5, width=40)
        self.txtReg.insert(tk.END, "Nội dung")
        self.txtReg.pack()
        
        self.butSend = tk.Button(self, text="Gởi nội dung", command=self.butSend_Click)
        self.butSend.pack()
        
        self.butBro = tk.Button(self, text="Browser...", command=self.butBro_Click)
        self.butBro.pack()
        
        self.txtBro = tk.Entry(self)
        self.txtBro.insert(0, "Đường dẫn ...")
        self.txtBro.pack()
        
        self.groupBox1 = ttk.LabelFrame(self, text="Sửa giá trị trực tiếp")
        self.groupBox1.pack()
        
        self.button1 = tk.Button(self.groupBox1, text="Gởi", command=self.button1_Click)
        self.button1.pack()
        
        self.opApp = ttk.Combobox(self.groupBox1, values=["Get value", "Set value", "Delete value", "Create key", "Delete key"])
        self.opApp.set("Chọn chức năng")
        self.opApp.pack()
        
        self.txtKQ = tk.Text(self.groupBox1, height=5, width=40)
        self.txtKQ.pack()
        
        self.txtLink = tk.Entry(self.groupBox1)
        self.txtLink.insert(0, "Đường dẫn")
        self.txtLink.pack()
        
        self.txtValue = tk.Entry(self.groupBox1)
        self.txtValue.insert(0, "Value")
        self.txtValue.pack()
        
        self.txtNameValue = tk.Entry(self.groupBox1)
        self.txtNameValue.insert(0, "Name value")
        self.txtNameValue.pack()
        
        self.opTypeValue = ttk.Combobox(self.groupBox1, values=["String", "Binary", "DWORD", "QWORD", "Multi-String", "Expandable String"])
        self.opTypeValue.set("Kiểu dữ liệu")
        self.opTypeValue.pack()
        
        self.butXoa = tk.Button(self.groupBox1, text="Xóa", command=self.butXoa_Click)
        self.butXoa.pack()
        
        self.protocol("WM_DELETE_WINDOW", self.registry_closing)
        
    def butSend_Click(self):
        # Xử lý sự kiện khi nút Gởi nội dung được nhấn
        pass
    
    def butBro_Click(self):
        # Xử lý sự kiện khi nút Browser được nhấn
        pass
    
    def button1_Click(self):
        # Xử lý sự kiện khi nút Gởi được nhấn trong groupBox1
        pass
    
    def butXoa_Click(self):
        # Xử lý sự kiện khi nút Xóa được nhấn
        pass
    
    def registry_closing(self):
        # Xử lý sự kiện khi cửa sổ đóng
        self.destroy()

if __name__ == "__main__":
    app = RegistryEditor()
    app.mainloop()
