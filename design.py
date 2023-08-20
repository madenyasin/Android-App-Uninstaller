from tkinter import *
from tkinter import ttk

class Design:
    def __init__(self, root):
        self.root = root
        self.root.title("App Remover")
        self.root.geometry("900x450")
        self.root.resizable(width=False, height=False)

        self.canvas = Canvas(self.root, height=450, width=900)
        self.canvas.pack()

        self.frame_app_list = Frame(self.root, bg="#D5D8DC")
        self.frame_app_list.place(relx=0.04, rely=0.065, relwidth=0.45, relheight=0.85)

        self.frame_device_config = Frame(self.root, bg="#D5D8DC")
        self.frame_device_config.place(relx=0.6, rely=0.150, relwidth=0.3, relheight=0.3)

        self.frame_app_func = Frame(self.root, bg="#D5D8DC")
        self.frame_app_func.place(relx=0.6, rely=0.535, relwidth=0.3, relheight=0.3)

        self.n = StringVar(value="Select Your Device")
        self.device_chose_cmb = ttk.Combobox(self.frame_device_config, width=27, textvariable=self.n, font="Arial 12")
        self.device_chose_cmb["values"] = ("x", "y", "z")
        self.device_chose_cmb.pack(anchor="ne", padx=35, pady=20)
        self.device_chose_cmb.current()

        self.refresh_devices_btn = Button(self.frame_device_config, text="Refresh devices", bd="5", font="Arial 12")
        self.refresh_devices_btn.pack(side="top", pady=7)

        self.uninstall_app_btn = Button(self.frame_app_func, text="Uninstall selected app", bd="5", font="Arial 12")
        self.uninstall_app_btn.pack(side="top", pady=16)

        self.refresh_app_list_btn = Button(self.frame_app_func, text="Refresh app list", bd="5", font="Arial 12")
        self.refresh_app_list_btn.pack(side="top", pady=7)

        self.app_list_listbox = Listbox(self.frame_app_list, font="Arial 12")
        self.app_list_listbox.pack(side=LEFT, fill="both", expand=True)

        self.scrollbar = Scrollbar(self.frame_app_list)
        self.scrollbar.pack(side=RIGHT, fill=BOTH)
        self.app_list_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.app_list_listbox.yview)
