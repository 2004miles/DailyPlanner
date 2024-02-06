import curses
import sqlite3
import graphics
import os
from pathlib import Path


def main(stdscr):
    y = 0
    directory_path = Path('databases/')
    graphics.screen_setup(stdscr)
    if not os.path.exists('databases/'):
        y = graphics.type_effect(y, 0, 'Please run the setup.py and follow the prompts to generate a database.')
        y = graphics.exit_script(y, 0)
    y = graphics.type_effect(stdscr, y, 0, 'Welcome to DailyPlanner!')
    y = graphics.type_effect(stdscr, y, 0, 'Please enter your name: ')
    database_name = stdscr.getstr().decode()
    full_path = directory_path / database_name
    if full_path.exists():
        connect_todo_list = sqlite3.connect(f'{full_path}todolist.db')
        y = graphics.type_effect(stdscr, y, 0, 'Connected!')
    else:
        y = graphics.type_effect(stdscr, y, 0, 'Wasnt found')




if __name__ == "__main__":
    curses.wrapper(main)
