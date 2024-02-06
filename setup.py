import sqlite3
import curses
import os
import graphics
import database



def setup(stdscr):
    graphics.screen_setup(stdscr)

    start_message ="""-------------------
Hello anon. You have run the setup script for DailyPlanner.
Press ESC if you wish to close this script.
Otherwise, press any other key to continue.
"""
    y = graphics.type_effect(stdscr, 0, 0, start_message)

    key = stdscr.getch()
    if key == 27:  # ESC
        graphics.exit_script(stdscr, y)
        return

    name, y = ask_for_name(stdscr, y)
    if not name:
        graphics.exit_script(stdscr, y)
        return

    curses.napms(2000)
    setup_todo_list(stdscr, y, name)


def ask_for_name(stdscr, y):
    while True:
        y = graphics.type_effect(stdscr, y, 0, 'What should we call you? ')
        name = stdscr.getstr().decode()
        y = graphics.type_effect(stdscr, y, 0, f'Is {name} correct? (y/n): ')

        confirm = stdscr.getch()
        if confirm in [ord('y'), ord('Y')]:
            return name, y


def setup_todo_list(stdscr, y, name):
    while True:
        y = graphics.type_effect(stdscr, y, 0, '\nWould you like to setup a To-Do-list? (y/n): ')
        confirm = stdscr.getch()
        if confirm in [ord('y'), ord('Y')]:
            return create_todo_list(stdscr, y,  name)
        return


def create_todo_list(stdscr, y, name):
    db_path = os.path.join('./databases', name)
    os.makedirs(db_path, exist_ok=True)
    db_file = os.path.join(db_path, f'{name}todolist.db')
    conn = database.init_todolist_db(db_file)

    database.add_task(stdscr, y, conn) 
    conn.close()
    graphics.exit_script(stdscr, 0)


if __name__ == "__main__":
    curses.wrapper(setup)
