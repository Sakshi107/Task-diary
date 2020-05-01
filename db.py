import sys
import psycopg2
from tkinter import messagebox
conn = None

def initialize_db(password):
    """Initialize db connection with provided user password."""
    print('Starting...')
    global conn

    try:
        conn = psycopg2.connect(database="task_manager",#default databse in postgreSQL
                                user="postgres",#username of postgreSQL
                                password="password",#password of that user in postgreSQL
                                host="127.0.0.1",
                                port="5432")
    except psycopg2.OperationalError as exception:
        messagebox.showerror("password","PASSWORD IS INCORRECT. TRY AGAIN...")
        sys.exit()


    # except psycopg2.OperationalError as exception:
    #     print("PASSWORD IS INCORRECT. TRY AGAIN...")
    #     sys.exit()

def create_table():
    global conn
    try:
        #Creating a cursor object using the cursor() method
        cursor = conn.cursor()
        #Creating table tasks if it not exists...
        sql ='''CREATE TABLE IF NOT EXISTS TASKS(
        id int GENERATED ALWAYS AS IDENTITY primary key,
        task_name text,
        priority_of_task text,
        category text,
        is_done text,
        deadline text
        )'''
        cursor.execute(sql)
        conn.commit()
        print("Table Tasks loaded successfully........")

        #Closing the connection       
    except:
        print("Table Tasks is not loaded...")
        conn.close()

def create_table2():
    global conn
    try:
        #Creating table tasks if it not exists...
        cursor = conn.cursor()
        sql='''CREATE TABLE IF NOT EXISTS notification_tracker
        (
            id int,
            notify_date text
        ) '''
        cursor.execute(sql)
        conn.commit()
        print("Table notification_tracker loaded successfully........")
        #Closing the connection       
    except:
        print("Table notification_tracker is not loaded...")
        conn.close()

def create_table3():
    global conn
    try:
        #Creating table notify_email if it not exists...
        cursor = conn.cursor()
        sql='''CREATE TABLE IF NOT EXISTS notification_email
        (
            id int GENERATED ALWAYS AS IDENTITY primary key,
            from_email text,
            password VARCHAR(30),
            to_email text,
            time text
        ) '''
        cursor.execute(sql)
        conn.commit()
        print("Table notification_email loaded successfully........")
        #Closing the connection       
    except:
        print("Table notification_email is not loaded...")
        conn.close()



def shutdown_db():
    """Close connection to db."""
    print('Exit.')
    global conn
    conn.close()

def add_task(values):
    """Add specified task to the database.."""
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (task_name, priority_of_task, category, is_done,deadline) VALUES (%s, %s, %s, %s,%s) RETURNING id;",
                   (values[0], values[1], values[2], values[3],values[4]))

    text = cursor.fetchone()[0]
    conn.commit()
    print("Task added successfully")
    return text

def add_email(values):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notification_email (from_email,password,to_email,time) VALUES (%s,%s,%s,%s);",
                   (values[0],values[1],values[2],values[3]))
    conn.commit()
    print("email added successfully")

def get_email():
    cursor = conn.cursor()
    cursor.execute("SELECT from_email,password,to_email,time from notification_email ORDER BY time DESC LIMIT 1;")
    rows_count = cursor.fetchall()
    return rows_count

def add_notify_date(values):
    """Add specified task which is notified to user to the database."""
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notification_tracker(id,notify_date) VALUES (%s, %s)",
                   (values[0], values[5]))

    # text = cursor.fetchone()[0]
    conn.commit()
    print("Notifier date added to notification_tracker table")
    # return text

def get_notified_tasks():
    """Get all tasks which are already notified from the database."""
    cursor = conn.cursor()
    cursor.execute("SELECT id,notify_date from notification_tracker;")
    rows_count = cursor.fetchall()
    return rows_count   

def tasks_to_notify():
    """Get all tasks which are in notification_tracker table from the database."""
    cursor = conn.cursor()
    cursor.execute("SELECT category,task_name,priority_of_task,notify_date from tasks as t,notification_tracker as nt where t.id=nt.id and is_done='false' ")
    rows_count = cursor.fetchall()
    return rows_count 


def get_tasks():
    """Get all tasks from the database."""
    cursor = conn.cursor()
    cursor.execute("SELECT id, task_name, priority_of_task, category, is_done,deadline from tasks;")
    rows_count = cursor.fetchall()
    return rows_count


def edit_task(id, values):
    """Edit specified task in the database."""
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET task_name = %s, priority_of_task = %s, category = %s, is_done = %s ,deadline=%s WHERE id = %s;",
                   (values[0], values[1], values[2], values[3],values[4], id))

    conn.commit()
    print("Number of records updated:", cursor.rowcount)


def delete_task(id):
    """Delete specified task from the tasks table of database."""
    cursor = conn.cursor()
    cursor.execute("DELETE from tasks where id = %s;", (id, ))
    conn.commit()
    print("Number of records deleted:", cursor.rowcount)

def remove_item_notification_tracker(item_id):
    """Delete specified task from the notification_tracker table of database."""
    cursor = conn.cursor()
    cursor.execute("DELETE from notification_tracker where id = %s;", (item_id, ))
    conn.commit()
    print("Number of records deleted:", cursor.rowcount)


def search_task(var):
    cursor = conn.cursor()
    cursor.execute("SELECT category,task_name, deadline from tasks where task_name=%s OR category=%s OR deadline=%s;", (var,var,var ))
    rows = cursor.fetchall()
    return rows
