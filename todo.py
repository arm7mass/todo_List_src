from tkinter import Tk, Button, Label, Scrollbar, Listbox, StringVar, Entry, W, E, N, S,END
from tkinter import ttk
from tkinter import messagebox
import psycopg2 as psy
from dbconfig import dbcon

selected_task=None

# create connection variable
con = psy.connect(**dbcon)  # (**) telling connection method to unpack connection setting 
print(con)

cursor =con.cursor()  # any time you want to perform operation on the database from python the cursor will do that 

#create TodoApp class 
class TodoApp:
    # method to auatomatically connect python to database 
    def __init__(self): # automatically called every time new object is created self used to access the variable in the class
        self.con = psy.connect(**dbcon)
        self.cursor = con.cursor()
        print(' You have connected to the database ')

    # metod to called to close the connection to database 
    def __del__(self):
        self.con.close()

    # method to allow rows to fetch all records from database table  
    def view(self):
        self.cursor.excute('SELECT * FROM todo')
        rows = self.cursor.fetchall()
        return rows

    # method to insert the record in the database 
    def insert(self, title):
        sql = ('INSERT INTO todo(title)VALUES (%s)') # query to insert
        values = [title]
        self.cursor.excute(sql,values)
        self.con.commit() # to save the record ( save what ever done)
        messagebox.showinfo(title='Todolist DataBase', message='New Task added to database')

    
    # method to update the record we already have in the database 
    def update(self, id, title):
        tsql = ('UPDATE todo SET title = %s WHERE id=%s') # query to update 
        self.cursor.excute(tsql,[title, id])
        self.con.commit() # to save the record ( save what ever done)
        messagebox.showinfo(title='Todolist DataBase', message='Task Updated')


    # method to delete record from the database 
    def delete(self, id):
        delquery = 'DELETE FROM todo WHERE id=%s' # query to Delete 
        self.cursor.excute(delquery,[id])
        self.con.commit() # to save the record ( save what ever done)
        messagebox.showinfo(title='Todolist DataBase', message='Task deleted')

db = TodoApp()


# method to 
def get_selected_row(event): # event refer to any thing the user does in the application  like button click
    global selected_task
    index = list_bx.curselection()[0] # [0] to start from initial value return tuple for selcetion record
    selected_task = list_bx.get(index) # passing the index from which i select
    title_entry.delete(0, 'end') # delete record from select box 
    title_entry.insert('end', selected_task[1]) # insert at the end of the data


def view_records(): # 
    list_bx.delete(0, 'end') # clear the list box  from the start to the end
    for row in db.view():
        list_bx.insert('end', row)


def add_task():# add new task in db in list box
    db.insert(title_text.get()) 
    list_bx.delete(0, 'end')
    list_bx.insert('end', (title_text.get()))
    title_entry.delete(0, 'end')
    con.commit()
    view_records() # display all records
    clear_screen() 


def delete_task(): # delete any task 
    db.delete(selected_task[0])
    con.commit()


def clear_screen(): # clear any enter
    title_entry.delete(0, 'end')


def update_records(): # update the task
    db.update(selected_task[0], title_text.get())
    title_entry.delete(0, 'end')
    con.commit()







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


# add scollbar to enable scrolling
scroll_bar = Scrollbar(root)
scroll_bar.grid(row=1, column=8, rowspan=14, sticky=W)

list_bx.configure(yscrollcommand=scroll_bar.set) # Enables vertical scrolling
scroll_bar.configure(command=list_bx.yview)

# add more Button Widgets

modify_btn = Button(root, text='Modify Task', bg='purple', fg='White', font='helvetica 10 bold', command='')
modify_btn.grid(row=15, column=1)

delete_btn = Button(root, text='Delete Task', bg='red', fg='White', font='helvetica 10 bold', command='')
delete_btn.grid(row=15, column=2, padx=35)


exit_btn = Button(root, text='Exit Application', bg='blue', fg='White', font='helvetica 10 bold', command=root.destroy)
exit_btn.grid(row=15, column=3)







root.mainloop() # run the application until exit 
