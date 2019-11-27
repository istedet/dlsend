import socket
import tkinter as tk
import utils
import select
from tkinter import messagebox as msgbox


class TCPClient():
    def __init__(self, reply):
        # this is the constructor that takes in host and port. retryAttempts is given
        # a default value but can also be fed in.
        self.host = ''
        self.port = ''
        self.reply = reply
        self.socket = None

    def connect(self):
        #
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def disconnect(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        self.socket = None

    def send(self, command):
        try:
            self.data = str.encode(utils.convert_to_char(command.get()))

            self.socket.sendall(self.data)
        except Exception as e:
            msgbox.showerror("Error", f'An error has occured: {e}')
        finally:
            self.read()

    def read(self):
        ready = select.select([self.socket], [], [], 5)

        if ready[0]:
            self.data = self.socket.recv(1024)
            # reply.set(repr(data)[2:-1])
            conv_data = utils.convert_from_char(self.data)
            self.reply.set(conv_data[1:-1])
        else:
            self.reply.set("No data received (Timeout 5s)")

    def sethostdetails(self, host, port):
        self.host = host
        self.port = port
