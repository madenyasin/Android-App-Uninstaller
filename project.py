from tkinter import Tk, messagebox
from design import Design
import platform
import os
import tkinter as tk
import datetime

root = tk.Tk()
design = Design(root)

package_names = []
serial_number = ""
log_file = "log.txt"


def main():
    global root
    set_colors()

    list_devices()
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
    device_list = run_command(get_adb_folder(), "adb devices").splitlines()[1:-1]

    # USB debugging close || No phone connection
    if not device_list:
        messagebox.showwarning(
            "Device not detected",
            "1) Connect your phone.\n"
            + "2) Enable USB debugging in your phone's settings.",
        )
    
    for item in device_list:
        # USB debugging is not allowed.
        if "unauthorized" in item:
            messagebox.showerror(
                "USB debugging is not allowed",
                "Please allow USB debugging in your device's settings.\n\n"
                + "Device serial number: "
                + item.replace("\tunauthorized", ""),
            )
            device_list.remove(item)
            continue
        # other negative results were excluded from the list.
        elif "device" not in item:
            device_list.remove(item)

    # Extraction of serial number.
    for i in range(len(device_list)):
        device_list[i] = device_list[i].replace("\tdevice", "")
        
    print(device_list)
    design.device_chose_cmb['values'] = device_list
    

design.refresh_devices_btn.config(command=list_devices)


def list_apps():
    apps = []
    global serial_number
    global package_names

    design.app_list_listbox.delete(0, tk.END)  # listbox clear
    design.search_box.delete(0, tk.END)  # Clear existing text

    if design.device_chose_cmb.get() in ["No device connected!", "Select Your Device"]:
        messagebox.showwarning("No device selected", "You must choose a device.")
    else:
        serial_number = design.device_chose_cmb.get()
        command = f"adb -s {serial_number} shell pm list packages"
        apps = run_command(get_adb_folder(), command).splitlines()

        package_names = []
        for app in apps:
            package_names.append(app.replace("package:", ""))
            design.app_list_listbox.insert("end", app.replace("package:", ""))


design.refresh_app_list_btn.config(command=list_apps)


def modified_cmb(event):
    global serial_number
    if design.device_chose_cmb.get() not in [
        "No device connected!",
        "Select Your Device",
    ]:
        serial_number = design.device_chose_cmb.get()

    list_apps()


design.device_chose_cmb.bind("<<ComboboxSelected>>", modified_cmb)


def uninstall_app():
    global package_names
    global serial_number
    global log_file
    if not package_names:
        messagebox.showwarning(
            "No application selected",
            "Please select the application you want to uninstall.",
        )
    else:
        package_name = design.app_list_listbox.get(
            design.app_list_listbox.curselection()
        )
        if package_name:
            command = (
                f"adb -s {serial_number} shell pm uninstall --user 0 {package_name}"
            )
            response = run_command(get_adb_folder(), command)

            if "success" in response.lower():
                result = f"device: {serial_number} | state: {response.splitlines()[0].lower()} -> {package_name} | date of removal: {datetime.datetime.now()}"
                print(result)
                with open(log_file, "a") as file:
                    file.writelines(f"{result}\n")
                package_names.remove(package_name)
                list_apps()
            else:
                print(response)
                with open(log_file, "a") as file:
                    file.writelines(
                        f"device: {serial_number} | state: {response} -> {package_name} | date of removal: {datetime.datetime.now()}\n"
                    )


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

    text_color = "#000000"
    font_name = ("Comic Sans MS", 12, "normal")

    design.device_chose_cmb.config(foreground=text_color, font=font_name)

    design.uninstall_app_btn.config(foreground=text_color, font=font_name)
    design.refresh_devices_btn.config(foreground=text_color, font=font_name)
    design.refresh_app_list_btn.config(foreground=text_color, font=font_name)

    design.search_box.config(foreground="#FFFFFF", font=font_name)
    design.app_list_listbox.config(
        foreground="#FFFFFF", font=("Segoe UI", 13, "normal")
    )


if __name__ == "__main__":
    main()
