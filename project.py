import subprocess
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
device_list = []


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
    full_command = f"cd {directory} && {command}"
    try:
        result = subprocess.check_output(
            full_command, stderr=subprocess.STDOUT, shell=True, universal_newlines=True
        )
        return result
    except subprocess.CalledProcessError as e:
        return f"Error message:\n{e.output}"

def save_to_file(path, log):
    log = str(log).splitlines()
    with open(path, "a") as file:
        file.writelines(f"{log}\n")

# get search key
def Scankey(event):
    global package_names
    data = []
    val = event.widget.get()

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
        design.app_list_listbox.insert("end", item)


def list_devices():
    global device_list
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

    design.device_chose_cmb["values"] = device_list


design.refresh_devices_btn.config(command=list_devices)


def list_apps():
    global serial_number
    global package_names

    design.app_list_listbox.delete(0, tk.END)  # listbox clear
    design.search_box.delete(0, tk.END)  # Clear existing text

    if design.device_chose_cmb.get() in ["No device connected!", "Select Your Device"]:
        messagebox.showwarning("No device selected", "You must choose a device.")
    else:
        serial_number = design.device_chose_cmb.get()
        command = f"adb -s {serial_number} shell pm list packages"
        response = run_command(get_adb_folder(), command).splitlines()
        save_to_file("apps.txt", response)
        if "Error" in response[0]:
            # save_to_log_file(f"")
            # Connection failed
            if f"'{serial_number}' not found" in response[1]:
                messagebox.showerror(
                    f"Device '{serial_number}' not found",
                    "1) Connect your phone.\n"
                    + "2) Enable USB debugging in your phone's settings.",
                )
            # Other errors
            else:
                messagebox.showerror(f"{response[0]}", f"{response[1]}")
        else:
            # Application names have been pulled successfully.
            package_names = []
            for item in response:
                package_names.append(item.replace("package:", ""))
                design.app_list_listbox.insert("end", item.replace("package:", ""))
                
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
    global device_list
    global package_names
    global serial_number
    global log_file
    if not package_names:
        messagebox.showwarning(
            "No application selected",
            "Select your device or refresh app list.",
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
            # Application uninstall successful.
            if "success" in response.lower():
                result = f"device: {serial_number} || state: {response.splitlines()[0].lower()} -> {package_name} || date: {datetime.datetime.now()}"
                save_to_file(log_file, result)
                package_names.remove(package_name)
                list_apps()
            # Connection failed
            elif f"'{serial_number}' not found" in response:
                save_to_file(log_file, f"device: {serial_number} || result: {response} || package name: {package_name} || date: {datetime.datetime.now()}")
                messagebox.showerror(
                    f"Device '{serial_number}' not found",
                    "1) Connect your phone.\n"
                    + "2) Enable USB debugging in your phone's settings.",
                )
            # Other error messages
            else:
                print(response)
                save_to_file(log_file, f"device: {serial_number} || result: {response} || package name: {package_name} || date: {datetime.datetime.now()}")
                messagebox.showerror("Error", f"{response}")
                


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
