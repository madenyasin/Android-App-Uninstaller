from tkinter import Tk
from design import Design

root = Tk()
design = Design(root)
app_list = []

# sample data
file = open("sample-data.txt")
for line in file:
    design.app_list_listbox.insert("end", line.splitlines())
    app_list.append(line.splitlines())


# get search key
def Scankey(event):
    global app_list
    data = []
    val = event.widget.get()
    # print(val)

    if val == "":
        file = open("sample-data.txt")
        for line in file:
            data.append(line.splitlines())
    else:
        for item in app_list:
            if val.lower() in str(item).lower():
                data.append(item)

    Update(data)

design.search_box.bind("<KeyRelease>", Scankey)

# update the listbox
def Update(data):
    design.app_list_listbox.delete(0, "end")

    # put new data
    for item in data:
        design.app_list_listbox.insert("end", item)


root.mainloop()
