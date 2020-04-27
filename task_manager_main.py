from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from ttkthemes import themed_tk as ttkt
import random
from datetime import datetime
from datetime import timedelta
from datetime import date
from dateutil.parser import parse

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import tkcalendar
from tkcalendar import Calendar, DateEntry

import db


password_root = Tk()
password_root.withdraw()
password = simpledialog.askstring("Password", "Enter password:", show="*")
password_root.destroy()

if password is None:
    sys.exit()

db.initialize_db(password)
db.create_table()
db.create_table2()


root = ttkt.ThemedTk()
root.set_theme('radiance')
root.title("Task Manager")
columns = ("task_name", "priority_of_task", "category", "is_done","deadline")
tree = ttk.Treeview(root, height=36, selectmode="browse", columns=columns, show="headings")
scrollbar = ttk.Scrollbar(root, orient=VERTICAL, command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
tree.grid(row=0, column=0, rowspan=2)
scrollbar.grid(row=0, column=1, rowspan=2, sticky=(W, N, E, S))

def already_notified(taskn):
    for item in db.get_notified_tasks():
        if taskn[0]==item[0]:
            return True
    return False

def notify():
    for item in db.get_tasks():
        if not already_notified(item):
            dd=datetime.strptime(item[5], "%d-%m-%Y")
            dd2= dd -timedelta(days=1)
            dd3=dd2.strftime('%d-%m-%Y')
            today=datetime.today().strftime('%d-%m-%Y')
            if (dd3==today) and (item[4]=="false"):
                email_notify(item)
                db.add_notify_date(item)
                print("Email notification sent sucessfully")


def email_notify(item):
    email = 'task.diary534@gmail.com'#add your gmail id from which u want to sent (only gmail account)
    password = 'task@diary'#add your email password
    send_to_email = 'abc123@somaiya.edu'#add your email id where u want to sent (any mail account)
    subject = 'Task Notifier'# The subject line
    message ='Category of task: '+item[3]+'\n\nYour Task:'+ item[1]
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = send_to_email
    msg['Subject'] = subject

    # Attach the message to the MIMEMultipart object
    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string() # You now need to convert the MIMEMultipart object to a string to send
    server.sendmail(email, send_to_email, text)
    server.quit()




def treeview_sort_column(treeview, column, reverse):
    children_list = [(treeview.set(child, column), child) for child in treeview.get_children("")]
    children_list.sort(reverse=reverse)

    for index, (value, child) in enumerate(children_list):
        treeview.move(child, "", index)

    treeview.heading(column, command=lambda: treeview_sort_column(treeview, column, not reverse))


for column in columns:
    tree.heading(column, text=column, command=lambda col=column: treeview_sort_column(tree, col, False))

width, height = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("{0}x{1}+0+0".format(width, height))

width_task_name = int(width * 0.25)
tree.column("task_name", width=width_task_name, anchor="center")
tree.heading("task_name", text="Tasks")

width_priority_of_task = int(width * 0.08)
tree.column("priority_of_task", width=width_priority_of_task, anchor="center")
tree.heading("priority_of_task", text="Priority")

width_category = int(width * 0.15)
tree.column("category", width=width_category, anchor="center")
tree.heading("category", text="Category")

width_is_done = int(width * 0.11)
tree.column("is_done", width=width_is_done, anchor="center")
tree.heading("is_done", text="Is Finished")

width_deadline = int(width * 0.11)
tree.column("deadline", width=width_is_done, anchor="center")
tree.heading("deadline", text="Due date")

mainframe = ttk.Frame(root, padding="25 25 100 50")
mainframe.grid(row=0, column=2, sticky=(N, S, W, E))
mainframe.rowconfigure(0, weight=1)
mainframe.columnconfigure(0, weight=1)

task_name = StringVar()
ttk.Label(mainframe, text="Task name:").grid(column=1, row=1, sticky=(W, E))
task_name_widget = ttk.Entry(mainframe, width=20, textvariable=task_name)
task_name_widget.grid(column=2, row=1, sticky=(W, E))

priority_of_task = StringVar()
ttk.Label(mainframe, text="Priority of task \n(E.g 1 to 10):").grid(column=1, row=2, sticky=(W, E))
priority_of_task_widget = ttk.Entry(mainframe, width=20, textvariable=priority_of_task)
priority_of_task_widget.grid(column=2, row=2, sticky=(W, E))

category = StringVar()
ttk.Label(mainframe, text="Category:").grid(column=1, row=3, sticky=(W, E))
category_widget = ttk.Entry(mainframe, width=20, textvariable=category)
category_widget.grid(column=2, row=3, sticky=(W, E))

deadline = StringVar()
ttk.Label(mainframe, text="Deadline: \n(Format:dd-mm-yyyy)").grid(column=1, row=4, sticky=(W, E))
deadline_widget = ttk.Entry(mainframe, width=20, textvariable=deadline)
deadline_widget.grid(column=2, row=4, sticky=(W, E))

is_done = BooleanVar()
ttk.Label(mainframe, text="Is Done:").grid(column=1, row=5, sticky=(W, E))
is_done_widget = ttk.Checkbutton(mainframe, variable=is_done,
                                     onvalue=True, offvalue=False)
is_done_widget.grid(column=2, row=5, sticky=(W, E))


notify()

def create_task_item():
    task_name_value = task_name.get()
    priority_of_task_value = priority_of_task.get()
    category_value = category.get()
    is_done_value = is_done.get()
    deadline_value=deadline.get()

    if inputs_validation():
        item_values = (task_name_value,
                       priority_of_task_value,
                       category_value,
                       is_done_value,
                       deadline_value)

        item_id = db.add_task(item_values)

        tree.insert("", "end", item_id, text=item_id, values=(item_values[0],
                                                              item_values[1],
                                                              item_values[2],
                                                              item_values[3],
                                                              item_values[4]))

        task_name.set("")
        priority_of_task.set("")
        category.set("")
        deadline.set("")
        is_done.set(False)

        create_button["state"] = "normal"
        change_button["state"] = "disabled"
        notify()


def inputs_validation():
    task_name_value = task_name.get()
    priority_of_task_value = priority_of_task.get()
    category_value = category.get()
    deadline_value=deadline.get()
    dd=datetime.strptime(deadline_value,"%d-%m-%Y")
    today=datetime.today().strftime('%d-%m-%Y')
    today1=datetime.strptime(today,"%d-%m-%Y")




    if not(len(task_name_value) > 0 and len(task_name_value) <=25):
        messagebox.showerror("Task name", "Task name limit exceeded")
        return False
    if not(int(priority_of_task_value) > 0 and int(priority_of_task_value) <= 10):
        messagebox.showerror("Priority", "Priority is not valid")
        return False
    if not(len(category_value) > 0 and len(category_value) <= 15):
        messagebox.showerror("Category", "Category limit exceeded")
        return False
    if (dd<today1):
        messagebox.showwarning("Due date", "Deadline is gone!")
        return False
    return True


create_button = ttk.Button(mainframe, text="Create Task", command=create_task_item)
create_button.grid(column=1, row=6, sticky=(W, E))

z=0
def change_theme():
    global z
    themes=root.get_themes()
    length=int(len(themes))
    while(True):
        z=z%length
        root.set_theme(themes[z])
        cal.tag_config('reminder', background='red', foreground='yellow')
        z+=1
        break

changeTheme_button = ttk.Button(mainframe, text="Change Theme", command=change_theme)
changeTheme_button.grid(column=1, row=7, sticky=(W, E))




top = tk.Toplevel(root)
cal = Calendar(top, selectmode='none')  
date = cal.datetime.today()
cal.calevent_create(date, 'Today', 'message')
cal.pack(fill="both", expand=True)
def calendar_events():  
    top = tk.Toplevel(root)
    cal = Calendar(top, selectmode='none')  
    for item in db.get_tasks():
        dd=datetime.strptime(item[5], "%d-%m-%Y")
        cal.calevent_create(dd,item[1], 'reminder')
        cal.tag_config('reminder', background='red', foreground='yellow')
        cal.pack(fill="both", expand=True)
    date = cal.datetime.today()
    cal.calevent_create(date, 'Today', 'message')

# class ToolTip(object):

#     def __init__(self, widget):
#         self.widget = widget
#         self.tipwindow = None
#         self.id = None
#         self.x = self.y = 0

#     def showtip(self, text):
#         "Display text in tooltip window"
#         self.text = text
#         if self.tipwindow or not self.text:
#             return
#         x, y, cx, cy = self.widget.bbox("insert")
#         x = x + self.widget.winfo_rootx() + 57
#         y = y + cy + self.widget.winfo_rooty() +27
#         self.tipwindow = tw = Toplevel(self.widget)
#         tw.wm_overrideredirect(1)
#         tw.wm_geometry("+%d+%d" % (x, y))
#         label = Label(tw, text=self.text, justify=LEFT,
#                       background="#ffffe0", relief=SOLID, borderwidth=1,
#                       font=("tahoma", "8", "normal"))
#         label.pack(ipadx=1)

#     def hidetip(self):
#         tw = self.tipwindow
#         self.tipwindow = None
#         if tw:
#             tw.destroy()

# def CreateToolTip(widget, text):
#     toolTip = ToolTip(widget)
#     def enter(event):
#         toolTip.showtip(text)
#     def leave(event):
#         toolTip.hidetip()
#     widget.bind('<Enter>', enter)
#     widget.bind('<Leave>', leave)

# button = Button(top, text = 'Hover over me')
# button.pack()
# CreateToolTip(button, text = 'Hello you!\n'
#                 'Have a nice day\n')    
cal_events_btn=ttk.Button(mainframe, text='calendar with events', command=calendar_events)
cal_events_btn.grid(column=1, row=8, sticky=(W, E))


search_task = StringVar()
search_task_widget = ttk.Entry(mainframe, width=20, textvariable=search_task)
search_task_widget.grid(column=2, row=9, sticky=(W, E))

def show():
    global data
    search_task_value= search_task.get()
    data=db.read_from_db(search_task_value)
    data.sort(key=lambda e: e[1], reverse=True)
    if(len(data)==0):
       textMsg="Search Result(Task not found)"
    else:
        textMsg="Search Result"
    search_result = tk.Toplevel(root)
    tk.Label(search_result, text=textMsg, font=("Arial",27)).grid(row=0, columnspan=3)
    # create Treeview with 3 columns
    cols = ('Sr no.','Category', 'Task', 'Due date')
    tree_search = ttk.Treeview(search_result, columns=cols, show='headings')
    for i in range(4):
        tree_search.column(i, anchor="center")    
    # set column headings
    for col in cols:
        tree_search.heading(col, text=col)    
    tree_search.grid(row=1, column=0, columnspan=2)
    for i, (category,task_name,deadline) in enumerate(data, start=1):
        tree_search.insert("", "end", values=(i,category,task_name,deadline))
    tk.Button(search_result, text="Close", width=15, command=search_result.destroy).grid(row=4, column=1)


Search_btn=ttk.Button(mainframe, text='Search', command=show)
Search_btn.grid(column=1, row=9, sticky=(W, E))




def change_item():
    task_name_value = task_name.get()
    priority_of_task_value = priority_of_task.get()
    category_value = category.get()
    is_done_value = is_done.get()
    deadline_value=deadline.get()

    if inputs_validation():
        item_id = tree.item(tree.selection()[0], "text")
        item_values = (task_name_value,
                       priority_of_task_value,
                       category_value,
                       is_done_value,
                       deadline_value)

        db.edit_task(item_id, item_values)
        tree.item(tree.selection()[0], values=item_values)

        task_name.set("")
        priority_of_task.set("")
        category.set("")
        deadline.set("")
        is_done.set(False)

        create_button["state"] = "normal"
        change_button["state"] = "disabled"
        notify()

change_button = ttk.Button(mainframe, text="Change Task", command=change_item)
change_button.grid(column=2, row=6, sticky=(W, E))
change_button["state"] = "disabled"

for child in mainframe.winfo_children():
    child.grid_configure(padx=25, pady=25)

for item in db.get_tasks():
    tree.insert("", "end", item[0], text=item[0],values=(item[1], item[2], item[3], item[4],item[5]))

menu = Menu(root, tearoff=0)


def remove_task_item():
    item_id = tree.item(tree.selection()[0], "text")
    db.delete_task(item_id)
    tree.delete(item_id)

    task_name.set("")
    priority_of_task.set("")
    category.set("")
    deadline.set("")
    is_done.set(False)

    create_button["state"] = "normal"
    change_button["state"] = "disabled"


menu.add_command(label="Remove Task", command=remove_task_item)


def change_task_item_helper():
    item_values = tree.item(tree.selection()[0], "values")

    task_name.set(item_values[0])
    priority_of_task.set(item_values[1])
    category.set(item_values[2])
    is_done.set(item_values[3])
    deadline.set(item_values[4])

    create_button["state"] = "disabled"
    change_button["state"] = "normal"


menu.add_command(label="Change Task", command=change_task_item_helper)


def right_click_handler(event):
    show_contextual_menu(event)


def show_contextual_menu(event):
    if tree.focus():
        menu.post(event.x + 65, event.y)


tree.bind("<3>", right_click_handler)


def left_click_handler(event):
    menu.unpost()


tree.bind("<1>", left_click_handler)


def shutdown_hook():
    if messagebox.askyesno(message="Are you sure you want to quit?",
                           icon="question", title="Quit"):
        db.shutdown_db()
        root.destroy()

root.protocol("WM_DELETE_WINDOW", shutdown_hook)

root.mainloop()