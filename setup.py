import sqlite3
import curses
import os
from graphics import type_effect
from sqlite3 import Error


def setup(stdscr):
    # No need for initscr() here, stdscr is alreaddy the initialized WindowsError

    # Sets up terminal colors
    curses.start_color()
    curses.init_pair(1, 10, curses.COLOR_BLACK)
    stdscr.clear()  # Clear the screen

    start_message = """-------------------\nHello anon. You have run the setup script for DailyPlanner.\nPlease press ENTER if you wish to continue.\nOtherwise, if you want to close this script please press ESC.\n"""
    # y represents the line number
    y = 0

    y = type_effect(stdscr, y, 0, start_message)


    while True:
        key = stdscr.getch()
        if key == 27:  # ESC key
            y = type_effect(stdscr, y, 0, 'Now exiting...')
            curses.napms(2000)  # Wait a bit before exiting
            curses.endwin()  # Restore the terminal to its original operating mode
            return
        elif key in [10, 13]:  # ENTER key is pressed; 10 is '\n' and 13 is '\r'
            y = type_effect(stdscr, y, 0, 'You will now be asked a few questions...')
            stdscr.refresh()
            curses.napms(2000)
            break
 
    while True: 
        y = type_effect(stdscr, y, 0, 'What should we call you? ')
        name = stdscr.getstr().decode()
        y = type_effect(stdscr, y, 0, f'Is {name} correct?\nPress ENTER to confirm, ESC to change it.')
        key = stdscr.getch()

        if key == 27:
           continue 
        elif key in [10, 13]:
            try:
                new_database_direc_path = os.path.join(path, name)
                os.makedirs(new_database_direc_path, exist_ok=True)
                y = type_effect(stdscr, y, 0, f'{name} has been confirmed and recorded in the database.')
                curses.wrapper(create_connection(name))

            except OSError as error:
                y = type_effect(stdscr, y, 0, f"Creation of the directory '{new_database_direc_path}' failed due to: {error}")
                y = type_effect(stdscr, y, 0, f"Upon the next prompt please enter a different name")
                continue

            return

    curses.napms(2000)

# Remember to use curses.wrapper to call your function
def create_connection(db_file):

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    path = './databases'
    curses.wrapper(setup)

