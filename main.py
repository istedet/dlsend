import tkinter as tk
from tkinter import ttk
import functools as ftools
import utils
import conwindow

# Create main window
root = tk.Tk()
root.title("Datalogic transmission tool")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Create a root frame
tframe = ttk.Frame(root, padding="3 3")
bframe = ttk.Frame(root, padding="3 3")
tframe.grid(column=0, row=0, sticky=(tk.N, tk.E, tk.S, tk.W))
bframe.grid(column=0, row=1, sticky=(tk.N, tk.E, tk.S, tk.W))
tframe.columnconfigure(0, weight=1)
tframe.rowconfigure(0, weight=1)

# Create the values to hold the IP and Port
connection_ip = tk.StringVar()
connection_port = tk.StringVar()

# Set default values for the connection
connection_ip.set('127.0.0.1')
connection_port.set('4001')

# Create the labelframe and anchor it to the top
top_label_frame = ttk.LabelFrame(tframe, text="Connection details")
top_label_frame.grid(column=1, row=0, sticky=(tk.N, tk.E, tk.S, tk.W))
top_label_frame.columnconfigure(0, weight=1)
top_label_frame.rowconfigure(0, weight=1)

# Set up the rightmost labelframe
ttk.Label(top_label_frame, text="IP address:").grid(column=0, row=0, sticky=tk.W)
ttk.Label(top_label_frame, text="Port:").grid(column=1, row=0, sticky=tk.W)

ip_entry = ttk.Entry(top_label_frame, width=15, textvariable=connection_ip)
port_entry = ttk.Entry(top_label_frame, width=6, textvariable=connection_port)
ip_entry.grid(column=0, row=1, pady=5, padx=5, sticky=tk.W)
port_entry.grid(column=1, row=1, pady=5, padx=5, sticky=tk.W)

# Create buttons in bottom frame
ttk.Button(bframe, text="Connect", command=ftools.partial(
    conwindow.spawnwindow, root, connection_ip, connection_port)).grid(column=0, row=0)
ttk.Button(bframe, text="Exit", command=ftools.partial(
    utils.program_exit, root)).grid(column=1, row=0)

for child in bframe.winfo_children():
    child.grid_configure(padx=5)

for child in tframe.winfo_children():
    child.grid_configure(padx=5)

root.mainloop()
