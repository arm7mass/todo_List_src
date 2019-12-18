from tkinter import Tk, Button, Label, Scrollbar, Listbox, StringVar, Entry, W, E, N, S,END
from tkinter import ttk
from tkinter import messagebox

root = Tk()  # Create Application window

root.title('My Todo List App') # Add a Title on Application Window 
root.configure(background='light blue') # add background color to application window
root.geometry('550x550') # set a size for application window
root.resizable(width=False,height=False) #prevent further rsizing 

root.mainloop() # run the application until exit 
