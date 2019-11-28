import tkinter as tk

# todo, build validation logic for this class


class lbox:
    def __init__(self, lbox, data):
        # Initiate the internal representation of the list box and the data
        # entry field
        self.lbox = lbox
        self.data = data

    def com_remove(self):
        # Get the current selection and assign it to a variable. Cast this variable
        # to an int so we can use it to remove an item from the list
        sidx = self.lbox.curselection()
        idx = int(sidx[0])

        self.lbox.delete(idx)

    def com_insert(self, value):
        # Function for inserting a command into the list
        if (not (value.get() == '')):
            self.lbox.insert(0, value.get())

    def update_data(self, *args):
        # Function to set self.data to the current selection of the listbox.
        # since self.data is a stringvar then using self.data.set() updates this
        # stringvar
        sidx = self.lbox.curselection()
        idx = int(sidx[0])

        self.data.set(self.lbox.get(idx))

    def create_list(self):
        # Create and return a list of all the elements in the listbox
        i = 0
        new_list = []

        while i < self.lbox.size():
            new_list.append(self.lbox.get(i))
            i += 1

        return new_list
