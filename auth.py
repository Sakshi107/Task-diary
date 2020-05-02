from tkinter import *
import os
from ttkthemes import themed_tk as ttkt
from tkinter import messagebox
import db

def SignUp():
    global SignUp_screen
    SignUp_screen = Toplevel(main_root)
    SignUp_screen.title("SignUp")
    SignUp_screen.geometry("300x250")

    global username
    global password
    global username_entry
    global password_entry
    username = StringVar()
    password = StringVar()

    Label(SignUp_screen, text="Please enter details below", bg="light steel blue").pack()
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
    Button(SignUp_screen, text="SignUp", width=10, height=1, bg="light steel blue", command = SignUp_user).pack()

signin=0
def SignIn():
    global SignIn_screen
    SignIn_screen = Toplevel(main_root)
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
    occur=0
    for i in db.get_users():# i represents element of info which is list itself
        if username_value==i[0]:#to access the username of the "i" list and compare with the username entered by user
            occur=1 # if username already exists in database
    if occur==1:
        messagebox.showerror('Username',"User already exists")
        SignUp_screen.destroy()
    else:
        if(len(username_value)>=4 and len(username_value)<=10):
            password_value = password.get()#input password if username doesn't already exists
            length=len(password_value)# taking the length of password
            if  length>=5 and length<=10:#To check all the conditions on the password are satisfied
                t=(username_value,password_value)#create a tuple "t" containing name and password
                db.add_user(t)# add to database
                messagebox.showinfo('SignUp',"Registration successful!")
                SignUp_screen.destroy()
            else:
                if(length<5 or length>10):
                    messagebox.showerror('Password',"Your password should have 5-10 characters")
        else:
            if(len(username_value)<4 or len(username_value)>10):
                messagebox.showerror('Username',"Username should be 5-10 characters")
    # username_entry.delete(0, END)
    # password_entry.delete(0, END)


def SignIn_verify():
    
    username_value1 = username_verify.get()
    password_value1=password_verify.get()
    log=0#to check the sign-in success
    for g in db.get_users():
        if g[0]==username_value1:#comparing the name
            if g[1]==password_value1:#if name is present comparing the name
                # messagebox.showinfo('Login','Logged in successfully!')
                print('Logged in successfully!')
                log=1#sign-in successful
                global signin
                global f_username
                signin=1
                f_username=username_value1
                SignIn_screen.destroy()
                main_root.destroy()
            else:
                messagebox.showerror('Login','Password incorrect!Try again')   
                log=1
                SignIn_screen.destroy()
    if log==0:
        messagebox.showerror('Login','Failed to SignIn')
        SignIn_screen.destroy()
    
def main_frame_screen():
    global main_root
    main_root = ttkt.ThemedTk()
    main_root.set_theme('radiance')
    main_root.geometry("300x250")
    main_root.title("Account SignIn")
    Label(text="Select Your Choice", bg="light steel blue", width="300", height="2", font=("Comic Sans MS", 13)).pack()
    Label(text="").pack()
    Button(text="SignIn", height="2", width="30", command = SignIn).pack()
    Label(text="").pack()
    Button(text="SignUp", height="2", width="30", command=SignUp).pack()
    main_root.mainloop()

main_frame_screen()