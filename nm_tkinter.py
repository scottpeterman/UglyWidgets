# Theme from https://github.com/rdbende/Forest-ttk-theme
import tkinter as tk 
from tkinter import ttk, messagebox
from netmiko import ConnectHandler

def connect_device(device_params):
    try:
        connection = ConnectHandler(
            device_type=device_params["device_type"],
            ip=device_params["ip"],
            username=device_params["username"],
            password=device_params["password"]
        )
        output = connection.send_command(device_params['command'])
        return output
    except Exception as e:
        return str(e)

def run_clicked():
    try:
        device_params = {
            "device_type": combo_device_type.get(),
            "ip": entry_ip.get(),
            "username": entry_username.get(),
            "password": entry_password.get(),
            "command": entry_command.get(),
        }

        result = connect_device(device_params)
        txt_output.insert(tk.END, result)
    except Exception as e:
        txt_output.insert(tk.END, str(e))

def show_python_code():
    device_params = {
        "device_type": combo_device_type.get(),
        "ip": entry_ip.get(),
        "username": entry_username.get(),
        "password": entry_password.get(),
        "command": entry_command.get(),
    }

    code_window = tk.Toplevel(root)
    code_window.title("Python Code")

    txt_code = tk.Text(code_window, width=80, height=20)
    txt_code.pack()

    code = f"""
from netmiko import ConnectHandler

device = {{
    "device_type": '{device_params["device_type"]}',
    "ip":   '{device_params["ip"]}',
    "username": '{device_params["username"]}',
    "password": '{device_params["password"]}',
}}

connection = ConnectHandler(**device)

output = connection.send_command('{device_params["command"]}')

print(output)
    """

    txt_code.insert(tk.END, code)

root = tk.Tk()
# Create a style
style = ttk.Style(root)

# Import the tcl file
root.tk.call("source", "forest-dark.tcl")

# Set the theme with the theme_use method
style.theme_use("forest-dark")
root.title('Netmiko GUI')

root.geometry("800x600")

menu = tk.Menu(root)
root.config(menu=menu)

view_menu = tk.Menu(menu)
menu.add_cascade(label="View", menu=view_menu)
view_menu.add_command(label="Python", command=show_python_code)

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(expand=True, fill='both')

tk.Label(frame, text="IP").grid(row=0, sticky='ew')
tk.Label(frame, text="Username").grid(row=1, sticky='ew')
tk.Label(frame, text="Password").grid(row=2, sticky='ew')
tk.Label(frame, text="Device Type").grid(row=3, sticky='ew')
tk.Label(frame, text="Command").grid(row=4, sticky='ew')

entry_ip = tk.Entry(frame)
entry_username = tk.Entry(frame)
entry_password = tk.Entry(frame, show='*')
entry_command = tk.Entry(frame)

entry_ip.grid(row=0, column=1, sticky='w')
entry_username.grid(row=1, column=1, sticky='w')
entry_password.grid(row=2, column=1, sticky='w')
entry_command.grid(row=4, column=1, sticky='ew')

device_types = ['cisco_ios', 'cisco_xr', 'juniper', 'arista_eos']
combo_device_type = ttk.Combobox(frame, values=device_types)
combo_device_type.grid(row=3, column=1, sticky='w')
combo_device_type.set('cisco_ios')

run_button = tk.Button(frame, text="Run", command=run_clicked)
run_button.grid(row=5, column=1, sticky='w')

entry_command.insert(0, "show run")

txt_output = tk.Text(frame, width=40, height=25, fg='#34eb34', bg='#111111')
txt_output.grid(row=6, column=0, columnspan=2, sticky='ew')

frame.grid_columnconfigure(1, weight=1)
scrollbar = tk.Scrollbar(frame, command=txt_output.yview)
scrollbar.grid(row=6, column=2, sticky='ns')

txt_output['yscrollcommand'] = scrollbar.set
root.mainloop()
