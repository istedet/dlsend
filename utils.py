import socket
import select
import tkinter as tk
import ipaddress
from tkinter import messagebox as msgbox
import filecom


def convert_to_char(in_str):
    # Create an empty string
    new_str = ''
    i = 0

    # Search through the string and convert the $** values to a byte value and
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
    # Logic to scan through the byte array and turn any non-printeable characters
    # into printeable characters
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
    # Update the host details in the class
    sock.sethostdetails(chost, cport)
    # Checn to see if you were actually connected, by doing it this way we
    # can make sure that the ip/port entries are only readonly if we successfully
    # connected to a server
    connected = sock.connect()
    if (connected):
        ip_entry.configure(state="readonly")
        port_entry.configure(state="readonly")


def update_and_disconnect(sock, ip_entry, port_entry):
    # trigger a disconnect from the socket object
    sock.disconnect()
    # Done to make the entries for ip and port writeable again
    ip_entry.configure(state="normal")
    port_entry.configure(state="normal")


def save_com_file(lbox):
    # Create the dictonary to save to the file
    dict = {'commands': lbox.create_list()}

    filecom.save_file(dict)
