import tkinter as tk
from tkinter import ttk
import functools as ftools
import utils
import socket
import tcpcom


# Create main window
root = tk.Tk()
root.title("Datalogic transmission tool")
stored_command_list = ['12 23233 344 44141', '2131231441241', '12412121  2332313']
stored_command_var = tk.StringVar()
stored_command_var.set(stored_command_list)

# Create the new window, setting a name and the focus to the window
root.title('Active connection')
root.focus()
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Create a StringVar to hold the reply from the printer
data_reply = tk.StringVar()
data_reply.set('No reply received')
data_to_send = tk.StringVar()
con_ip = tk.StringVar()
con_port = tk.StringVar()

# Initiate the class so that we have something to connect with
sock = tcpcom.TCPClient(data_reply)

# Set up the frames for buttons and labelframe
tframe = ttk.Frame(root, padding="3 3")
bframe = ttk.Frame(tframe, padding="3 3")

# row and columnconfigure are required to get the labelframe to expand
# to fill the available space
tframe.columnconfigure(0, weight=1)
tframe.rowconfigure(0, weight=1)
tframe.grid(column=0, row=0, sticky=(tk.N, tk.E, tk.S, tk.W))

# Add the printer reply labelframe. Sticky it to all sides to get it to
# expand together with the top frame
con_frame = ttk.LabelFrame(tframe, text="Printer connection data")
con_frame.grid(column=0, row=0, sticky=(tk.N, tk.E, tk.S, tk.W))
l_con_frame = ttk.LabelFrame(tframe, text="Transmit/receive")
l_con_frame.grid(column=0, row=1, sticky=(tk.W, tk.E, tk.S, tk.W))
left_con_frame = ttk.LabelFrame(tframe, text="Stored commands")
left_con_frame.grid(column=0, row=3, rowspan=2, sticky=(tk.N, tk.E, tk.S, tk.W))
r_button_frame = ttk.LabelFrame(tframe, text="Actions")
r_button_frame.grid(column=1, row=0, rowspan=10, sticky=(tk.N, tk.E, tk.S, tk.W))

# Create the text labels and populate the IP and Port
ttk.Label(con_frame, text="Active ip:").grid(column=0, row=0, sticky=tk.W)
ttk.Label(con_frame, text="Active port:").grid(column=0, row=1, sticky=tk.W)
ip_entry = ttk.Entry(con_frame, textvariable=con_ip, width=20)
port_entry = ttk.Entry(con_frame, textvariable=con_port, width=7)
ip_entry.grid(column=1, row=0, columnspan=2, sticky=tk.W)
port_entry.grid(column=1, row=1, sticky=tk.W)

d_ent_reply = ttk.Entry(l_con_frame, textvariable=data_reply, width=75)
d_ent_reply.grid(column=0, row=0, sticky=tk.W)
d_ent_reply.configure(state="readonly")
d_ent_data = ttk.Entry(l_con_frame, textvariable=data_to_send, width=75)
d_ent_data.grid(column=0, row=1, sticky=tk.W)

# Leftmost labelframe labels and listbox. The list variable has to be a
# StringVar.
stored_command_lbox = tk.Listbox(
    left_con_frame, listvariable=stored_command_var, height=7, width=75)
stored_command_lbox.grid(column=0, row=0, columnspan=2)
# Exportselection has to be false otherwhise you get a "tuple index out of range"
# error because the <<ListboxSelect>> event triggers with nothing selected
stored_command_lbox.configure(selectmode="browse", exportselection=False)
ttk.Button(left_con_frame, text="Store command", command=ftools.partial(
    utils.insert_stored_command, stored_command_lbox, data_to_send)).grid(column=0, row=1)
ttk.Button(left_con_frame, text="Delete command", command=ftools.partial(
    utils.del_stored_command, stored_command_lbox)).grid(column=1, row=1)

# Buttons in the frame on the right that lets you connect/disconnect/send commands
# and exit the program
b_connect = ttk.Button(r_button_frame, text="Connect", command=ftools.partial(
    utils.update_and_connect, sock, con_ip, con_port, ip_entry, port_entry))
b_close_con = ttk.Button(r_button_frame, text="Close connection", command=ftools.partial(
    utils.update_and_disconnect, sock, ip_entry, port_entry))
b_send = ttk.Button(r_button_frame, text="Send", command=ftools.partial(
    sock.send, data_to_send))
b_exit = ttk.Button(r_button_frame, text="Exit", command=root.destroy)
b_connect.grid(column=0, row=0, sticky=(tk.N, tk.E, tk.S, tk.W))
b_close_con.grid(column=0, row=1, sticky=(tk.N, tk.E, tk.S, tk.W))
b_send.grid(column=0, row=3, sticky=(tk.N, tk.E, tk.S, tk.W))
b_exit.grid(column=0, row=10, sticky=(tk.N, tk.E, tk.S, tk.W))

# Binding to update data_to_send when you select something in the list
stored_command_lbox.bind('<<ListboxSelect>>', ftools.partial(
    utils.update_data, data_to_send, stored_command_lbox))

# Give every child item some padding so that it doesn'root look like shit.
for child in tframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

for child in left_con_frame.winfo_children():
    child.grid_configure(padx=5, pady=5)

for child in l_con_frame.winfo_children():
    child.grid_configure(padx=5, pady=5)

for child in r_button_frame.winfo_children():
    child.grid_configure(padx=5, pady=5)

for child in con_frame.winfo_children():
    child.grid_configure(padx=5, pady=2)

root.mainloop()
