from tkinter import Tk
from design import Design

root = Tk()
design = Design(root)

# sample data
data = open("sample-data.txt")
for line in data:
    design.app_list_listbox.insert("end", line.splitlines())

root.mainloop()
