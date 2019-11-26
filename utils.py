import socket
import select
import tkinter as tk
from tkinter import messagebox as msgbox


def program_exit(window):
    # Shut down the window that's sent to the function
    window.destroy()


def connect(ip, port):
    # First create the socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Validate the input. Both input values should be tk.StringVar
    if (not (type(ip) == tk.StringVar and type(port) == tk.StringVar)):
        raise Exception('Error: IP or PORT is not a StringVar')
    else:
        # Connect to the IP and PORT.
        s.connect((ip.get(), int(port.get())))

        # Return the connection object. This only happens if the supplied values
        # are correct
        return s


def send(s, command, reply):
    try:
        s_data = str.encode(convert_to_char(command.get()))

        s.sendall(s_data)
        ready = select.select([s], [], [], 5)

        if ready[0]:
            data = s.recv(1024)
            # reply.set(repr(data)[2:-1])
            conv_data = convert_from_char(data)
            reply.set(conv_data[1:-1])
        else:
            reply.set("No data received (Timeout 5s)")
    except Exception as e:
        msgbox.showerror("Error", f'An error has occured: {e}')


def sock_end(s, t):
    # Shutdown the socket, close it and exit the window
    s.shutdown(socket.SHUT_RDWR)
    s.close()

    t.destroy()


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


def send_stored_command(s, lbox, reply):
    # Used to retrieve the current selection from the listbox and send it on the
    # TCP connection
    try:
        sidx = lbox.curselection()
        idx = int(sidx[0])

        s_str = convert_to_char(lbox.get(idx))
        s_data = str.encode(s_str)

        # s_data = str.encode(lbox.get(idx))
        s.sendall(s_data)
        ready = select.select([s], [], [], 5)

        if ready[0]:
            data = s.recv(1024)
            # reply.set(repr(data)[2:-1])
            conv_data = convert_from_char(data)
            reply.set(conv_data[1:-1])
        else:
            reply.set("No data received (Timeout 5s)")
    except Exception as e:
        msgbox.showerror("Error", f'An error has occured: {e}')


def convert_to_char(in_str):
    # Create an empty string
    new_str = ''
    i = 0

    # Search through the string and convert the #** values to a byte value and
    # then to the correct ASCII value
    while (i < len(in_str)):
        # Conditional logic to catch the '#' character
        if (in_str[i] == '#'):
            new_str += chr(int(in_str[i+1:i+3]))
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
