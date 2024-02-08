import curses
import sqlite3
import graphics
import database
import os
from pathlib import Path


def _print_menu(stdscr, selected_idx, menu_items):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    for idx, item in enumerate(menu_items):
        x = w // 2 - len(item) // 2
        y = h // 2 - len(menu_items) // 2 + idx
        if idx == selected_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, item)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, item)
    stdscr.refresh()


def main(stdscr):
    y = 6
    directory_path = Path('databases/')
    graphics.screen_setup(stdscr)
    curses.cbreak()
    stdscr.keypad(True)
    try:
        if not os.path.exists('databases/'):
            y = graphics.type_effect(stdscr, y, 'Please run the setup.py and follow the prompts to generate a database.', True) 
        graphics._print_ascii_title(stdscr)


        y = graphics.type_effect(stdscr, y, 0, 'Welcome to DailyPlanner! v1.0 \nPress Ctrl-C to cancel.\n')

        database_username, y = _check_user_exists(stdscr, y, directory_path)
        y = graphics.type_effect(stdscr, y, 0, 'You have succesfully logged in...')
        y = 0
        stdscr.clear()
        curses.curs_set(0)
        menu_items = ['To-do list', 'Schedule', 'Extra', 'Exit']
        current_item = 0

        # Main loop to display the menu and respond to user input
        while True:
            _print_menu(stdscr, current_item, menu_items)

            key = stdscr.getch()
            if key == curses.KEY_UP and current_item > 0:
                current_item -= 1
            elif key == curses.KEY_DOWN and current_item < len(menu_items) - 1:
                current_item += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                stdscr.clear()
                if current_item == 0:
                    __todolist_menu(stdscr, y, directory_path, database_username)
                    continue
                elif current_item == 1:
                    # Schedule selected
                    # Placeholder for now
                    graphics.type_effect(stdscr, y, 0, 'Schedule feature coming soon.')
                elif current_item == 2:
                    # Extra selected
                    # Placeholder for now
                    graphics.type_effect(stdscr, y, 0, 'Extra feature coming soon.')

                elif current_item == len(menu_items) - 1:  # Exit option
                    break

            elif key == curses.KEY_BACKSPACE or key == 27:# ESC key or Backspace to go back
                break

    except KeyboardInterrupt:
        pass
    finally:
        graphics.exit_script(stdscr, y)


def toggle_task_status(conn, task_id, new_status):
    """Toggle the status of a task in the database."""
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET task_status = ? WHERE id = ?", (new_status, task_id))
    conn.commit()


def __todolist_menu(stdscr, y, directory_path, database_username ):
    conn = sqlite3.connect(f'{directory_path/database_username}/{database_username}todolist.db')
    cur = conn.cursor()
    cur.execute("SELECT id, task_status, task_name, task_date, task_priority FROM tasks")
    tasks = cur.fetchall()
    current_line = 0  # Keep track of the current line for keyboard navigation
    stdscr.clear()
    while True:
        stdscr.clear()
        y = 2  # Start printing from the second line
        stdscr.addstr(0, 0, "Use arrow keys to navigate, 'Enter' to toggle completion,\n'a' to add a task, 'd' to delete a task, 'q' to quit.")
        for i, task in enumerate(tasks):
            id, status, name, date, priority = task
            checkbox = "[x]" if status == 1 else "[ ]"
            task_str = f"{checkbox} {name} - Due: {date} - Priority: {priority}"
            if i == current_line:
                stdscr.addstr(y, 0, task_str, curses.A_REVERSE)  # Highlight the selected task
            else:
                stdscr.addstr(y, 0, task_str, curses.color_pair(1))
            y += 1
        key = stdscr.getch()
        if key == curses.KEY_UP and current_line > 0:
            current_line -= 1
        elif key == curses.KEY_DOWN and current_line < len(tasks) - 1:
            current_line += 1
        elif key == ord('\n'):  # Enter key is pressed
            # Toggle the status of the selected task
            task_id = tasks[current_line][0]
            new_status = 0 if tasks[current_line][1] == 1 else 1
            toggle_task_status(conn, task_id, new_status)
            cur.execute("SELECT id, task_status, task_name, task_date, task_priority FROM tasks")
            tasks = cur.fetchall()
        elif key == ord('a'):
            database.add_task(stdscr, y+1, conn)
            cur.execute("SELECT id, task_status, task_name, task_date, task_priority FROM tasks")
            tasks = cur.fetchall()
        elif key == ord('d'):
            stdscr.addstr(y-1, 0, task_str, curses.color_pair(2))
            confirm_delete = stdscr.getch()
            if confirm_delete == ord('d'):
                database.remove_task_id(stdscr, y, conn, tasks[current_line][0])
                cur.execute("SELECT id, task_status, task_name, task_date, task_priority FROM tasks")
                tasks = cur.fetchall()

        elif key == ord('q'):
            break
        stdscr.refresh()


def _check_user_exists(stdscr, y, directory_path):
    while True:
        y = graphics.type_effect(stdscr, y, 0, 'Please enter your name: ')
        database_username = stdscr.getstr().decode()
        full_path = directory_path / database_username
        if full_path.exists():
            return database_username, y
        else:
            y = graphics.type_effect(stdscr, y, 0, 'Could not find database associated with name.')


if __name__ == "__main__":
    curses.wrapper(main)
