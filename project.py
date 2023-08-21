from tkinter import Tk
from design import Design
import platform
import os
import tkinter as tk

root = tk.Tk()
design = Design(root)

package_names = []
serial_number = ""



def main():
    global root

    set_colors()
    
    list_devices()  
    if design.device_chose_cmb.get() in ["No device connected!", "Select Your Device"]:
        print("SELECT DEVİCE!!!!!")  
        design.uninstall_app_btn['state'] = 'disabled'
    else:
        design.uninstall_app_btn['state'] = 'enabled'
    root.mainloop()
    
# detect user's OS
def get_OS():
    return platform.system().lower()

def get_adb_folder():
    return os.path.join(os.getcwd(), ("adb\\" + get_OS() + "\\platform-tools"))

def run_command(directory, command):
    command = f"cd {directory} & {command}" 
    p = os.popen(command)
    return p.read()

# get search key
def Scankey(event):
    global package_names
    data = []
    val = event.widget.get()
    # print(val)

    if val == "":
        for item in package_names:
            data.append(item)
    else:
        for item in package_names:
            if val.lower() in str(item).lower():
                data.append(item)

    Update(data)


design.search_box.bind("<KeyRelease>", Scankey)


# update the listbox
def Update(data):
    # global app_list
    design.app_list_listbox.delete(0, "end")

    # put new data
    for item in data:
        # print(item)
        design.app_list_listbox.insert("end", item)


def list_devices():
    if run_command(get_adb_folder(), "adb devices").splitlines()[1] == "":
        design.device_chose_cmb.set("No device connected!")
    else:
        response = run_command(get_adb_folder(), "adb devices")
        devices = response.replace("\tdevice", "").splitlines()
        for device in devices:
            if "\tunauthorized" in device:
                device = device.replace('\tunauthorized', '')
                print(f"{device} Nolu cihazın USB hata ayıklama yetkisi yok! Lütfen yetki verin.")
        
        devices = response.splitlines()[1:-1]
        device_numbers = []
        for item in devices:
            if "\tunauthorized" in item:
                device_numbers.append(item.replace("\tunauthorized", ""))
            elif "\tdevice" in item:
                device_numbers.append(item.replace("\tdevice", ""))
        # print(devices)
        # print(device_numbers)
        design.device_chose_cmb['values'] = tuple(device_numbers)
    
design.refresh_devices_btn.config(command=list_devices)


def list_apps():
    apps = []
    global serial_number
    global package_names

    design.app_list_listbox.delete(0, tk.END) #listbox clear

    design.search_box.delete(0, tk.END)  # Clear existing text
    # design.search_box.insert(0, "")  # Insert new text

    if design.device_chose_cmb.get() in ["No device connected!", "Select Your Device"]:
        print("SELECT DEVİCE!!!!!")
    else:
        serial_number = design.device_chose_cmb.get()
        # print(serial_number)
        command = f"adb -s {serial_number} shell pm list packages"
        apps = run_command(get_adb_folder(), command).splitlines()

        package_names = []
        for app in apps:
            package_names.append(app.replace("package:", ""))
            design.app_list_listbox.insert("end", app.replace("package:", ""))

    
design.refresh_app_list_btn.config(command=list_apps)


def modified_cmb(event):
    global serial_number
    if design.device_chose_cmb.get() not in ["No device connected!", "Select Your Device"]:
        serial_number = design.device_chose_cmb.get()
        design.uninstall_app_btn['state'] = 'active'

    list_apps()

design.device_chose_cmb.bind('<<ComboboxSelected>>', modified_cmb)

def uninstall_app():
    global package_names
    package_name = design.app_list_listbox.get(design.app_list_listbox.curselection())   

    command = f"adb -s {serial_number} shell pm uninstall --user 0 {package_name}"
    response = run_command(get_adb_folder(), command)

    if "success" in response.lower():
        print(response)
        package_names.remove(package_name)
        list_apps()
    else:
        print(response)
    
design.uninstall_app_btn.config(command=uninstall_app)


def set_colors():
    color_canvas = "#232323"
    color_btn = "#1ABC9C"
    color_frames = "#333333"
    color_listbox = "#292929"
    color_searchbox = "#444444"

    design.canvas.configure(bg=color_canvas)
    design.frame_app_list.config(bg=color_canvas)

    design.frame_device_config.config(bg=color_frames)
    design.frame_app_func.config(bg=color_frames)

    design.search_box.config(bg=color_searchbox)
    design.app_list_listbox.config(bg=color_listbox)

    design.refresh_devices_btn.config(bg=color_btn)
    design.uninstall_app_btn.config(bg=color_btn)
    design.refresh_app_list_btn.config(bg=color_btn)

    text_color= "#000000"
    font_name = ("Comic Sans MS", 12, "normal")



    design.device_chose_cmb.config(foreground=text_color, font=font_name)

    design.uninstall_app_btn.config(foreground=text_color, font=font_name)
    design.refresh_devices_btn.config(foreground=text_color, font=font_name)
    design.refresh_app_list_btn.config(foreground=text_color, font=font_name)

    design.search_box.config(foreground="#FFFFFF", font=font_name)
    design.app_list_listbox.config(foreground="#FFFFFF", font=("Segoe UI", 13, "normal"))

if __name__ == "__main__":
    main()