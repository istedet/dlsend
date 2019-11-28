import socket
import select
import tkinter as tk
import ipaddress
from tkinter import messagebox as msgbox


def del_stored_command(lbox):
    # Get the current selection and assign it to a variable. Cast this variable
    # to an int so we can use it to remove an item from the list
    try:
        sidx = lbox.curselection()
        idx = int(sidx[0])

        lbox.delete(idx)
    except Exception as e:
        pass


def insert_stored_command(lbox, new_var):
    # Build type checking logic
    new_str = new_var.get()
    if (not (new_var.get() == '')):
        lbox.insert(0, new_str)


def convert_to_char(in_str):
    # Create an empty string
    new_str = ''
    i = 0

    # Search through the string and convert the #** values to a byte value and
    # then to the correct ASCII value
    while (i < len(in_str)):
        # Conditional logic to catch the '#' character
        if (in_str[i] == '$'):
            new_str += chr(int(in_str[i+1:i+3], 16))
            i = i+3
            # The continue is used to escape this loop without running the bit
            # of code underneath
            continue

        new_str += in_str[i]
        i += 1

    return new_str


def convert_from_char(b_arr):
    i = 0
    buf_str = ''
    cont_str = ''

    while i < len(b_arr):
        if (b_arr[i] <= 31):
            buf_str += '<'
            cont_str = repr(b_arr[i])
            buf_str += cont_str.rjust(2, '0')
            buf_str += '>'
            i += 1
            continue

        buf_str += chr(b_arr[i])
        i += 1

    new_str = repr(buf_str)

    return new_str


def update_and_connect(sock, chost, cport, ip_entry, port_entry):
    # (host, port) = validate_ip_port(chost, cport)
    sock.sethostdetails(chost, cport)
    connected = sock.connect()
    if (connected):
        ip_entry.configure(state="readonly")
        port_entry.configure(state="readonly")


def update_and_disconnect(sock, ip_entry, port_entry):
    sock.disconnect()
    ip_entry.configure(state="normal")
    port_entry.configure(state="normal")


# def validate_ip_port(host, port):
#     try:
#         ipaddress.ip_address(host.get())
#         if (not port.get().isdigit()):
#             raise Exception("Port is not a number")
#     except Exception as e:
#         msgbox.showerror("Error", f'An error has occured: {e}')
#     else:
#         return (host.get(), int(port.get()))


def update_data(*args):
    sidx = args[1].curselection()
    idx = int(sidx[0])

    args[0].set(args[1].get(idx))
