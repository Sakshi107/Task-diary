import sys
import psycopg2
conn = None

def initialize_db(password):
    print('Starting...')
    global conn

    try:
        conn = psycopg2.connect(database="task_manager",
                                user="postgres",#username of postgreSQL
                                password="password",#password of that user in postgreSQL
                                host="127.0.0.1",
                                port="5432")

    except psycopg2.OperationalError as exception:
        print("PASSWORD IS INCORRECT. TRY AGAIN...")
        sys.exit()


def shutdown_db():
    print('Exit.')
    global conn
    conn.close()

def add_task(values):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (task_name, priority_of_task, category, is_done,deadline) VALUES (%s, %s, %s, %s,%s) RETURNING id;",
                   (values[0], values[1], values[2], values[3],values[4]))

    text = cursor.fetchone()[0]
    conn.commit()
    print("Records created successfully")
    return text


def get_tasks():
    cursor = conn.cursor()
    cursor.execute("SELECT id, task_name, priority_of_task, category, is_done,deadline from tasks;")
    rows_count = cursor.fetchall()
    return rows_count


def edit_task(id, values):
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET task_name = %s, priority_of_task = %s, category = %s, is_done = %s ,deadline=%s WHERE id = %s;",
                   (values[0], values[1], values[2], values[3],values[4], id))

    conn.commit()
    print("Number of records updated:", cursor.rowcount)


def delete_task(id):
    cursor = conn.cursor()
    cursor.execute("DELETE from tasks where id = %s;", (id, ))
    conn.commit()
    print("Number of records deleted:", cursor.rowcount)

def read_from_db(var):
    cursor = conn.cursor()
    cursor.execute("SELECT task_name, priority_of_task, category, is_done,deadline from tasks where task_name=%s;", (var, ))
    rows = cursor.fetchall()
    return rows