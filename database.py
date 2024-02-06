import sqlite3
import graphics


def init_todolist_db(db_file):
    # create tasks table if it doesn't exist.
    conn = sqlite3.connect(db_file)
    with conn:
        create_table_sql = """CREATE TABLE IF NOT EXISTS tasks (
                              id INTEGER PRIMARY KEY,
                              task TEXT NOT NULL,
                              status TEXT NOT NULL
                              );"""
        conn.execute(create_table_sql)
    return conn


def add_task(stdscr, y, conn):
    while True:
        y = graphics.type_effect(stdscr, y, 0, 'Enter a task or type "done" to finish: ')
        task = stdscr.getstr().decode()

        if task.lower() == 'done':
            break
 
        sql = "INSERT INTO tasks(task, status) VALUES(?,?)"
        with conn:
            conn.execute(sql, (task, 'pending'))
        y = graphics.type_effect(stdscr, y, 0, 'Task added.')
