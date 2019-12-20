from tkinter import *
from tkinter import ttk
import sqlite3


class StudentDB:
# class field
    db_conn = 0
    theCursor = 0
    curr_student = 0

    def setup_db(self):
        #  open or create DB
        self.db_conn = sqlite3.connect('student.db')

        #  create Cursor
        self.theCursor = self.db_conn.cursor()

        try:
            #  Create the Table if it doesn't exist
            self.db_conn.execute("CREATE TABLE if not exists Students(ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, FName TEXT NOT NULL , LName TEXT NOT NULL);")

            self.db_conn.commit()

        except sqlite3.OperationalError:
            print("ERROR : Table is not created ")

    def stud_submit(self):

        # insert student into the DB
        self.db_conn.execute("INSERT INTO Students(FName, LName) " + "VALUES ('" + self.fn_entry_value.get() + "', '" + self.ln_entry_value.get() + "')")

        # Clear Entry Box
        self.fn_entry.delete(0, "end")
        self.ln_entry.delete(0, "end")

        # Update list Box
        self.update_listbox()

    def update_listbox(self):
        # Delete items in the list box
        self.list_box.delete(0, "end")

        # Get Students from the db
        try:
            result = self.theCursor.execute("SELECT ID, FName, LName FROM Students")

            for row in result:
                stud_id = row[0]
                stud_fname = row[1]
                stud_lname = row[2]
            # put student in the list box
                self.list_box.insert(stud_id, stud_fname + " " + stud_lname)

        except sqlite3.OperationalError:
            print("The Table is not exist ")

        except:
            print("1 : could not retrieve data from database")

    def load_student(self, event=None):
        # Get index selected which is the student id
        lb_widget = event.widget
        index = str(lb_widget.curselection()[0] + 1)

        # Store the current student index
        self.curr_student = index

        # Retrieve student list from db
        try:
            result = self.theCursor.execute("SELECT ID, FName, LName FROM Students WHERE ID=" + index)

            for row in result:
                stud_id = row[0]
                stud_fname = row[1]
                stud_lname = row[2]

            # set the names in the entries
                self.fn_entry_value.set(stud_fname)
                self.ln_entry_value.set(stud_lname)

        except sqlite3.OperationalError:
            print("The Table is not exist  ")

        except:
            print("2 : could not retrieve data from database")

    def update_student(self):
        # update based on current student
        try:
            self.db_conn.execute("UPDATE Students SET FName='" + self.fn_entry_value.get() + "', LName='" + self.ln_entry_value.get() + "' WHERE ID=" + self.curr_student)
            self.db_conn.commit()

        except sqlite3.OperationalError:
            print("DataBase could not be updated")

        # clear entries
        self.fn_entry.delete(0, "end")
        self.ln_entry.delete(0, "end")

        # update list box with new student list
        self.update_listbox()

    def __init__(self, root):
        root.title("Student DataBase")
        root.geometry("300x350")

#             ----------1st Row---------------
        fn_label = Label(root, text='First Name')
        fn_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)

        self.fn_entry_value = StringVar(root, value='')
        self.fn_entry = ttk.Entry(root, textvariable=self.fn_entry_value)
        self.fn_entry.grid(row=0, column=1, padx=10, pady=10, sticky=W)

#             ----------2nd Row---------------
        ln_label = Label(root, text='Last Name')
        ln_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)

        self.ln_entry_value = StringVar(root, value='')
        self.ln_entry = ttk.Entry(root, textvariable=self.ln_entry_value)
        self.ln_entry.grid(row=1, column=1, padx=10, pady=10, sticky=W)

#             ----------3rd Row---------------
        self.submit_button = ttk.Button(root, text='Submit', command=lambda : self.stud_submit())
        self.submit_button.grid(row=2, column=0, padx=10, pady=10, sticky=W)
        self.update_button = ttk.Button(root, text='Update', command=lambda: self.update_student())
        self.update_button.grid(row=2, column=1, padx=10, pady=10)

#             ----------4th Row---------------


        scrollbar = Scrollbar(root)

        self.list_box = Listbox(root)

        self.list_box.bind('<<ListboxSelect>>', self.load_student)

        self.list_box.insert(1, 'Student Here')

        self.list_box.grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky=W+E)

        self.setup_db()

        self.update_listbox()


root = Tk()

studDB = StudentDB(root)

root.mainloop()
