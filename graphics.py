import random
import time
import curses


def type_effect(stdscr, y, x, text, base_delay=0.03):
 
    for char in text:
        stdscr.move(y, x)
        stdscr.addch(char, curses.color_pair(1))
        stdscr.refresh()
        # Determine delay: base delay plus adjustments
        if char in '.!?':  # Longer pause for end of sentence punctuation
            delay = base_delay + random.uniform(0.2, 0.5)
        elif char == ',':  # Slightly longer pause for commas
            delay = base_delay + random.uniform(0.1, 0.3)
        elif char == ' ':  # Short pause for space
            delay = base_delay + random.uniform(0.03, 0.05)
        else:  # Slightly randomize delay for letters and other characters
            delay = base_delay + random.uniform(-0.02, 0.02)

        # Occasional longer pause to simulate  thinking or repositioning
        if random.randint(1, 100) > 95:  # Roughly 5% chance of a longer pause
            delay += random.uniform(0.5, 1.0)
        time.sleep(delay)

        x += 1 #moves x cursor
 
        if x>= stdscr.getmaxyx()[1] or char == '\n':
            y += 1
            x = 0

    stdscr.move(y+1, 0)
    return y+1


def exit_script(stdscr, y):
    stdscr.clear()
    type_effect(stdscr, y, 0, 'Now exiting...')
    curses.napms(2000)
    curses.endwin()

def screen_setup(stdscr):
    curses.start_color()
    curses.init_pair(1, 10, curses.COLOR_BLACK)
    stdscr.clear()


