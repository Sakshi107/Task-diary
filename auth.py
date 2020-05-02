from tkinter import *
import os
from tkinter import messagebox
import users_database
from ttkthemes import themed_tk as ttkt

users_database.initialize_users_database()

def SignUp():
    global SignUp_screen
    SignUp_screen = Toplevel(root)
    SignUp_screen.title("SignUp")
    SignUp_screen.geometry("300x250")

    global username
    global password
    global username_entry
    global password_entry
    username = StringVar()
    password = StringVar()

    Label(SignUp_screen, text="Please enter details below", bg="green").pack()
    Label(SignUp_screen, text="").pack()
    username_label = Label(SignUp_screen, text="Username * ")
    username_label.pack()
    username_entry = Entry(SignUp_screen, textvariable=username)
    username_entry.pack()
    password_label = Label(SignUp_screen, text="Password * ")
    password_label.pack()
    password_entry = Entry(SignUp_screen, textvariable=password)
    password_entry.pack()
    Label(SignUp_screen, text="").pack()
    Button(SignUp_screen, text="SignUp", width=10, height=1, bg="green", command = SignUp_user).pack()

def SignIn():
    global SignIn_screen
    SignIn_screen = Toplevel(root)
    SignIn_screen.title("SignIn")
    SignIn_screen.geometry("300x250")
    Label(SignIn_screen, text="Please enter details below to SignIn").pack()
    Label(SignIn_screen, text="").pack()

    global username_verify
    global password_verify

    username_verify = StringVar()
    password_verify = StringVar()

    global username_SignIn_entry
    global password_SignIn_entry

    Label(SignIn_screen, text="Username * ").pack()
    username_SignIn_entry = Entry(SignIn_screen, textvariable=username_verify)
    username_SignIn_entry.pack()
    Label(SignIn_screen, text="").pack()
    Label(SignIn_screen, text="Password * ").pack()
    password_SignIn_entry = Entry(SignIn_screen, textvariable=password_verify)
    password_SignIn_entry.pack()
    Label(SignIn_screen, text="").pack()
    Button(SignIn_screen, text="SignIn", width=10, height=1, command = SignIn_verify).pack()

def SignUp_user():
    username_value = username.get()
    for i in users_database.get_users():# i represents element of info which is list itself
        if username_value==i[0]:#to access the username of the "i" list and compare with the username entered by user
            occur=1 # if username already exists in database
    if occur==1:
        messagebox.showerror('Username',"User already xeists")
    else:
        password_value = password.get()#input password if username doesn't already exists
        length=len(password_value)# taking the length of password
        if  length>=5 and length<=10:#To check all the conditions on the password are satisfied
            t=(username_value,password_value)#create a tuple "t" containing name and password
            users_database.add_user(t)# add to database
            Label(SignUp_screen, text="Registration Success", fg="green", font=("calibri", 11)).pack()
        else:
           
            if(length<8 or length>15):
                messagebox.showerror('Password',"Your password should have 8-15 characters")
    username_entry.delete(0, END)
    password_entry.delete(0, END)

def SignIn_verify():
    username_value1 = username_verify.get()
    password_value1=password_verify.get()
    log=0#to check the sign-in success
    for g in users_database.get_users():
        if g[0]==username_value1:#comparing the name
            if g[1]==password_value1:#if name is present comparing the name
                messagebox.showinfo('Login','Logged in successfully!')
                log=1#sign-in successful
                tr=-1#since successful to come out of the for loop
            else:
                messagebox.showerror('Login','Password incorrect!Try again')
    if log==0:
        messagebox.showerror('Login','Failed to SignIn')
    
def main_frame_screen():
    global root
    root = ttkt.ThemedTk()
    root.set_theme('radiance')
    root.geometry("300x250")
    root.title("Account SignIn")
    Label(text="Select Your Choice", bg="green", width="300", height="2", font=("Calibri", 13)).pack()
    Label(text="").pack()
    Button(text="SignIn", height="2", width="30", command = SignIn).pack()
    Label(text="").pack()
    Button(text="SignUp", height="2", width="30", command=SignUp).pack()

    root.mainloop()


main_frame_screen()