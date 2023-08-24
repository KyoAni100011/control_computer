from processDesigner import ProcessViewer
import time
import threading
from Kill import Kil
from Start import StartFunc

class ListProcess(ProcessViewer):
    def __init__(self, nw, nr, ns):
        super().__init__()

        self.nw = nw
        self.nr = nr
        self.ns = ns

    def button1_Click(self):
        temp = "KILL"
        Kil(self.nw, self.nr, self.ns)
        self.nw.write(temp + "\n")
        self.nw.flush()
        # Implement Kill command
       

    def button2_Click(self):
        temp = "XEM"
        self.nw.write(temp + "\n")
        self.nw.flush()
        # Implement Xem command
        threading.Thread(target=self.update_list_view).start()

    def update_list_view(self):
        def update(index):
            s1 = self.nr.readline().strip()
            s2 = self.nr.readline().strip()
            s3 = self.nr.readline().strip()
            print(s1, s2, s3)
            self.listView1.insert("", "end", values=(s1, s2, s3))
            
            if index < soprocess_1 - 1:
                self.after(10, update, index + 1)  # Schedule next update after 10 milliseconds
        
        temp = self.nr.readline().strip()
        print(temp)
        if temp.isdigit():
            soprocess_1 = int(temp)
            update(0)
        else:
            print("Invalid number format:", temp)
        
    def button3_Click(self):
        temp = "START"
        StartFunc(self.nw, self.nr, self.ns)
        self.nw.write(temp + "\n")
        self.nw.flush()
        # Implement Start command

    def button4_Click(self):
        # Xóa tất cả các mục trong listView1
        self.listView1.delete(*self.listView1.get_children())

    def process_closing(self):
        s = "QUIT"
        self.nw.write(s + "\n")
        self.nw.flush()
        self.destroy()