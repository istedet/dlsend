import tkinter as tk
from tkinter import messagebox as msgbox
from tkinter import ttk
import functools as ftools
import ipaddress
import utils


def spawnwindow(root, connection_ip, connection_port):
    try:
        # Check the ip-adress. Raises an exception if it isn't a valid ip-address
        con_ip = connection_ip.get()
        con_port = connection_port.get()
        ipaddress.ip_address(con_ip)

        # Create your socket
        sock = utils.connect(connection_ip, connection_port)

    except Exception as e:
        msgbox.showerror("Error", f'An error occured: {e}')
    else:
        stored_command_list = ['12 23233 344 44141', '2131231441241', '12412121  2332313']
        stored_command_var = tk.StringVar()
        stored_command_var.set(stored_command_list)

        # Create the new window, setting a name and the focus to the window
        t = tk.Toplevel(root)
        t.title('Active connection')
        t.focus()
        t.columnconfigure(0, weight=1)
        t.rowconfigure(0, weight=1)

        # Create a StringVar to hold the reply from the printer
        data_reply = tk.StringVar()
        data_reply.set('No reply received')
        data_to_send = tk.StringVar()

        # Set up the frames for buttons and labelframe
        tframe = ttk.Frame(t, padding="3 3")
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
        ttk.Label(con_frame, text="Active ip:").grid(
            column=0, row=1, sticky=tk.W)
        ttk.Label(con_frame, text=con_ip).grid(column=1, row=1, padx=5, sticky=tk.W)
        ttk.Label(con_frame, text="Active port:").grid(
            column=0, row=2, sticky=tk.W)
        ttk.Label(con_frame, text=con_port).grid(column=1, row=2, padx=5, sticky=tk.W)

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
        stored_command_lbox.configure(selectmode="browse")
        ttk.Button(left_con_frame, text="Store command", command=ftools.partial(
            utils.insert_stored_command, stored_command_lbox, data_to_send)).grid(column=0, row=1)
        ttk.Button(left_con_frame, text="Delete command",
                   command=ftools.partial(utils.del_stored_command, stored_command_lbox)).grid(column=1, row=1)

        # Bottom buttons, the spacing is weird
        b_send_stored = ttk.Button(r_button_frame, text="Send stored", command=ftools.partial(
            utils.send_stored_command, sock, stored_command_lbox, data_reply))
        b_send_stored.grid(column=0, row=0, sticky=(tk.N, tk.E, tk.S, tk.W))
        b_send = ttk.Button(r_button_frame, text="Send", command=ftools.partial(
            utils.send, sock, data_to_send, data_reply))
        b_send.grid(column=0, row=1, sticky=(tk.N, tk.E, tk.S, tk.W))
        b_close_con = ttk.Button(r_button_frame, text="Close connection", command=ftools.partial(
            utils.sock_end, sock, t))
        b_close_con.grid(column=0, row=2, sticky=(tk.N, tk.E, tk.S, tk.W))

        # Give every child item some padding so that it doesn't look like shit.
        for child in tframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        for child in left_con_frame.winfo_children():
            child.grid_configure(padx=5, pady=5)

        for child in l_con_frame.winfo_children():
            child.grid_configure(padx=5, pady=5)

        for child in r_button_frame.winfo_children():
            child.grid_configure(padx=5, pady=5)

        t.mainloop()
