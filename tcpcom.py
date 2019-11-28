import socket
import tkinter as tk
import utils
import select
import ipaddress
from tkinter import messagebox as msgbox


class TCPClient():
    def __init__(self, reply):
        # this is the constructor that takes in host and port.
        self.host = ''
        self.port = ''
        self.connected = False
        self.reply = reply
        self.socket = None

    def connect(self):
        if ((not self.connected) and type(self.host) == str and type(self.port) == int):
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((self.host, self.port))
            except Exception as e:
                msgbox.showerror("Error", f'An error has occured: {e}')
                return False
            else:
                self.connected = True
                return True

    def disconnect(self):
        if (self.connected):
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()
            self.socket = None
            self.connected = False

    def send(self, command):
        try:
            self.data = str.encode(utils.convert_to_char(command.get()))
            self.socket.sendall(self.data)
        except Exception as e:
            msgbox.showerror("Error", f'An error has occured: {e}')
        finally:
            self.read()

    def read(self):
        try:
            ready = select.select([self.socket], [], [], 5)

            if ready[0]:
                self.data = self.socket.recv(1024)
                # reply.set(repr(data)[2:-1])
                conv_data = utils.convert_from_char(self.data)
                self.reply.set(conv_data[1:-1])
            else:
                self.reply.set("No data received (Timeout 5s)")
        except Exception as e:
            msgbox.showerror("Error", f'An error has occured: {e}')

    def sethostdetails(self, host, port):
        try:
            if (not (type(host.get() == str) and port.get().isdigit())):
                raise Exception("host is not a string or port is not a number")

            ipaddress.ip_address(host.get())
        except Exception as e:
            msgbox.showerror("Error", f'An error has occured: {e}')
        else:
            self.host = host.get()
            self.port = int(port.get())
