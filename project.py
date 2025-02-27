from prettytable import PrettyTable
from tkinter import messagebox
from design import Design
import tkinter as tk
import subprocess
import platform
import datetime
import sqlite3
import os

root = tk.Tk()
design = Design(root)

package_names = []
serial_number = ""
device_list = []
database_path = "log_database.db"
table_name = "log"


def main():
    global root

    setup_gui()
    list_devices()

    if get_OS() != "windows":
        # adb file has been granted execute permission
        run_command(get_adb_folder(), "chmod +x adb")

    read_database(database_path, table_name)
    root.mainloop()


# detect user's OS
def get_OS():
    return platform.system().lower()


def get_adb_folder():
    return os.path.join(os.getcwd(), ("adb\\" + get_OS() + "\\platform-tools")).replace(
        "\\", "/"
    )


def run_command(directory, command):
    if get_OS() not in ["windows", "linux", "darwin"]:
        raise RuntimeError("Your operating system does not support it.")
    # Edited command for Linux and MacOS
    if get_OS() != "windows":
        if "chmod" not in command:
            command = command.replace("adb", "./adb")

    full_command = f"cd {directory} && {command}"
    try:
        result = subprocess.check_output(
            full_command, stderr=subprocess.STDOUT, shell=True, universal_newlines=True
        )
        return result
    except subprocess.CalledProcessError as e:
        return f"Error message:\n{e.output}"


def save_to_database(path, table_name, data):
    global package_names
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    cursor.execute(
        f""" CREATE TABLE IF NOT EXISTS {table_name} (
            Serial_Number VARCHAR(75) NOT NULL,
            Package_Name VARCHAR(150) NOT NULL,
            Process_Detail VARCHAR(255),
            Response_Detail TEXT,
            Event_Time DATETIME,
            Currently_Installed_Apps TEXT
        ); """
    )

    query = "INSERT INTO log (Serial_Number, Package_Name, Process_Detail, Response_Detail, Event_Time, Currently_Installed_Apps) VALUES (?, ?, ?, ?, ?, ?)"
    cursor.execute(
        query,
        (
            data[0],
            data[1],
            data[2],
            data[3],
            datetime.datetime.now(),
            ", ".join(package_names),
        ),
    )

    conn.commit()
    conn.close()

    read_database(path, table_name)


def read_database(path, table_name):
    if os.path.exists(path):
        conn = sqlite3.connect(path)
        cursor = conn.cursor()

        # to select all column we will use
        statement = f"""SELECT * FROM {table_name}"""
        cursor.execute(statement)

        output = cursor.fetchall()
        write_log(output, "log.json")

        conn.commit()
        conn.close()


def write_log(output, txt_path):
    table = PrettyTable()
    table.field_names = [
        "Serial_Number",
        "Package_Name",
        "Process_Detail",
        "Response_Detail",
        "Event_Time",
        "Currently_Installed_Apps",
    ]

    for row in output:
        table.add_row(row)

    with open(txt_path, "w") as file:
        file.write(table.get_json_string())


# get search key | data source = source
def Scankey(source, event):
    data = []
    val = event.widget.get()

    if val == "":
        for item in source:
            data.append(item)
    else:
        for item in source:
            if val.lower() in str(item).lower():
                data.append(item)

    Update(design.app_list_listbox, data)


# update the listbox
def Update(listbox, data):
    # clear list
    listbox.delete(0, "end")

    # put new data
    for item in data:
        listbox.insert("end", item)


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


def list_apps():
    global serial_number
    global package_names

    design.app_list_listbox.delete(0, tk.END)  # listbox clear
    design.search_box.delete(0, tk.END)  # Clear existing text

    if design.device_chose_cmb.get() in ["No device connected!", "Select Your Device"]:
        messagebox.showwarning("No device selected", "You must choose a device.")
    else:
        serial_number = design.device_chose_cmb.get()
        command = f"adb -s {serial_number} shell pm list packages --user 0"
        response = run_command(get_adb_folder(), command).splitlines()
        if "Error" in response[0]:
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


def modified_cmb(event):
    global serial_number
    if design.device_chose_cmb.get() not in [
        "No device connected!",
        "Select Your Device",
    ]:
        serial_number = design.device_chose_cmb.get()

    list_apps()


def uninstall_app():
    global package_names
    global serial_number
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
                package_names.remove(package_name)
                list_apps()
            # Connection failed
            elif f"'{serial_number}' not found" in response:
                messagebox.showerror(
                    f"Device '{serial_number}' not found",
                    "1) Connect your phone.\n"
                    + "2) Enable USB debugging in your phone's settings.",
                )
            # Other error messages
            else:
                messagebox.showerror("Error", f"{response}")

            save_to_database(
                database_path,
                table_name,
                [serial_number, package_name, command, response],
            )


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
    font_name = ("Georgia", 12, "normal")

    design.device_chose_cmb.config(foreground=text_color, font=font_name)

    design.uninstall_app_btn.config(foreground=text_color, font=font_name)
    design.refresh_devices_btn.config(foreground=text_color, font=font_name)
    design.refresh_app_list_btn.config(foreground=text_color, font=font_name)

    design.search_box.config(foreground="#FFFFFF", font=font_name)
    design.app_list_listbox.config(foreground="#FFFFFF", font=("Georgia", 14, "normal"))


def setup_gui():
    design.search_box.bind("<KeyRelease>", lambda event: Scankey(package_names, event))
    design.refresh_devices_btn.config(command=list_devices)
    design.refresh_app_list_btn.config(command=list_apps)
    design.device_chose_cmb.bind("<<ComboboxSelected>>", modified_cmb)
    design.uninstall_app_btn.config(command=uninstall_app)

    set_colors()


if __name__ == "__main__":
    main()
