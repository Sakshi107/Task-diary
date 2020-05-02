from tkinter import *
from tkinter import simpledialog
import db

#Sign in to task-diary
if __name__=='__main__':
    password_root = Tk()
    password_root.withdraw()
    password = simpledialog.askstring("Password", "Enter your PostgreSQL password:",show="*")
    password_root.destroy()

    if password is None:
        sys.exit()
    db.initialize_db(password)


db.create_table5()
import auth

if(auth.signin==1):
    global username
    username=auth.f_username
    import task_diary_main


   