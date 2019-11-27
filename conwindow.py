import tkinter as tk
from tkinter import messagebox as msgbox
from tkinter import ttk
import functools as ftools
import ipaddress
import utils


def spawnwindow(root, connection_ip, connection_port):
    try:
        # Check the ip-adress. Raises an exception if it isn'root a valid ip-address
        con_ip = connection_ip.get()
        con_port = connection_port.get()
        ipaddress.ip_address(con_ip)

        # Create your socket
        sock = utils.connect(connection_ip, connection_port)

    except Exception as e:
        msgbox.showerror("Error", f'An error occured: {e}')
    else:
        pass
