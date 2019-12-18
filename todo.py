from tkinter import Tk, Button, Label, Scrollbar, Listbox, StringVar, Entry, W, E, N, S,END
from tkinter import ttk
from tkinter import messagebox

root = Tk()  # Create Application window

root.title('My Todo List App') # Add a Title on Application Window 
root.configure(background='light blue') # add background color to application window
root.geometry('550x550') # set a size for application window
root.resizable(width=False,height=False) #prevent further rsizing 

# create label and entry widgets

title_label = ttk.Label(root, text='Title', background='light blue', font=('TkDefaultFont', 16))
title_label.grid(row=0, column=0, sticky=W)
title_text = StringVar()
title_entry = ttk.Entry(root, width=25, textvariable=title_text)
title_entry.grid(row=0, column=1, sticky=W)

# add a button to insert inputs into database

add_btn = Button(root, text='Add Task', bg='blue', fg='white', font='helvetica 10 bold', command='')
add_btn.grid(row=0,column=2, sticky=W)

# add a list box to display data from database 
list_bx = Listbox(root, height=16, width=40, font='helvetica 13', bg='white')
list_bx.grid(row=3, column=1,columnspan=14, sticky=W + E, pady=40, padx=15 )

root.mainloop() # run the application until exit 
