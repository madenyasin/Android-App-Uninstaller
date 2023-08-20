from tkinter import Tk
from design import Design
import os
import platform

root = Tk()
design = Design(root)

def main():
    global app_list
    print(get_adb_folder())
    
    app_list = []
    
    file = open("sample-data.txt")
    for line in file:
        app_list.append(line.splitlines())
        design.app_list_listbox.insert("end", line.splitlines())
    
    root.mainloop()
    

# detect user's OS
def get_OS():
    return platform.system().lower()

def get_adb_folder():
    return os.path.join(os.getcwd(), ("adb\\platform-tools\\" + get_OS()))

def run_command(command):
    p = os.popen(command)
    return p.read()

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
    global app_list
    design.app_list_listbox.delete(0, "end")

    # put new data
    for item in data:
        design.app_list_listbox.insert("end", item)


if __name__ == "__main__":
    main()