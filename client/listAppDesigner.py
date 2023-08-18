import tkinter as tk
from tkinter import ttk
import threading

class ApplicationList(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("App Viewer")
        self.geometry("800x300")
        
        self.configure(bg="white")
        
        self.header_frame = ttk.Frame(self)
        self.header_frame.pack(pady=10)
        
        self.button1 = ttk.Button(self.header_frame, text="Kill", command=self.button2_Click)
        self.button1.grid(row=0, column=0, padx=10)
        
        self.button2 = ttk.Button(self.header_frame, text="Xem", command=self.button1_Click)
        self.button2.grid(row=0, column=1, padx=10)
        
        self.button3 = ttk.Button(self.header_frame, text="Start", command=self.button3_Click)
        self.button3.grid(row=0, column=2, padx=10)
        
        self.button4 = ttk.Button(self.header_frame, text="Xóa", command=self.button4_Click)
        self.button4.grid(row=0, column=3, padx=10)
        
        self.listView1 = ttk.Treeview(self, columns=("Name Process", "ID Process", "Count Thread"), show="headings")
        self.listView1.heading("Name Process", text="Tên Process", command=lambda: self.sort_name("Name Process"))
        self.listView1.heading("ID Process", text="ID Process")
        self.listView1.heading("Count Thread", text="Số luồng")
        self.listView1.pack(padx=10, pady=10, fill="both", expand=True)

        # Create a vertical scrollbar within the Treeview
        self.scrollbar = ttk.Scrollbar(self.listView1, orient="vertical", command=self.listView1.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.listView1.configure(yscrollcommand=self.scrollbar.set)
        
        self.protocol("WM_DELETE_WINDOW", self.listApp_closing)

   
    def sort_name(self, column):
        if hasattr(self, "sorting_thread") and self.sorting_thread.is_alive():
            return

        self.sorting_thread = threading.Thread(target=self.perform_sorting, args=(column,))
        self.sorting_thread.start()

    def perform_sorting(self, column):
        # Lock to ensure that only one sorting operation is performed at a time
        with threading.Lock():
            self.sort_order = "asc" if not hasattr(self, "sort_order") else self.sort_order
            items = self.listView1.get_children("")
            
            # Get the index of the column to sort
            column_index = self.get_column_index(column)
            
            # Sort the items based on the values in the selected column
            items = sorted(items, key=lambda item: self.listView1.item(item, "values")[column_index], reverse=self.sort_order == "desc")
            
            for item in items:
                self.listView1.move(item, "", "end")
            
            self.sort_order = "desc" if self.sort_order == "asc" else "asc"
    
    def get_column_index(self, column_name):
        column_ids = self.listView1["columns"]
        return column_ids.index(column_name)