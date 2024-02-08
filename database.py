import sqlite3
import graphics


def init_todolist_db(db_file):
    # create tasks table if it doesn't exist.
    conn = sqlite3.connect(db_file)
    with conn:
        create_table_sql = """CREATE TABLE IF NOT EXISTS tasks (
                              id INTEGER PRIMARY KEY,
                              task_status INTEGER  NOT NULL,
                              task_name TEXT NOT NULL,
                              tasK_date TEXT NOT NULL,
                              task_priority TEXT NOT NULL
                              );"""
        conn.execute(create_table_sql)
    return conn


def add_task(stdscr, y, conn):
    while True:
        y = graphics.type_effect(stdscr, y, 0, 'Enter a task name or type "done" to finish: ')
        task_name = stdscr.getstr().decode()

        if task_name.lower() == 'done':
            break

        y = graphics.type_effect(stdscr, y, 0, 'Enter a due date (YYYY-MM-DD HH:MM): ')
        task_date = stdscr.getstr().decode()

        y = graphics.type_effect(stdscr, y, 0, 'Enter priority (High, Medium, Low): ')
        task_priority = stdscr.getstr().decode()
        task_status = 0
        sql = "INSERT INTO tasks(task_status, task_name, task_date, task_priority) VALUES(?,?,?,?)"
        with conn:
            conn.execute(sql, (task_status, task_name, task_date, task_priority))
        y = graphics.type_effect(stdscr, y, 0, 'Task added.\n')


def remove_task_id(stdscr, y, conn, task_id):
    sql = "DELETE FROM tasks WHERE id=?"
    cur = conn.cursor()
    cur.execute(sql, (task_id,))
    conn.commit()

