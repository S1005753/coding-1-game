#Write your game here
import curses
import time
import random

game_data = {
    # Store board dimensions, player/enemy positions, score, energy, collectibles, and icons

    "width": 49,
    "height": 11,
    "player": {"x": 0, "y": 2, "score": 0, "health": 100},
    'dragons': [
        {"x": 43, "y": 8},    
        {"x": 7, "y": 2},    
        {"x": 20, "y": 8},
        {"x": 30, "y": 1},
    ],
    "princess": [
        {"x": 47, "y": 8, "collected": False},
    ],
    "obstacles": [
        #Horizontal Wall
        {"x": 0, "y": 5},
        {"x": 1, "y": 5},
        {"x": 2, "y": 5},
        {"x": 3, "y": 5},
        {"x": 4, "y": 5}, 
        {"x": 5, "y": 5}, 
        {"x": 6, "y": 5},
        {"x": 7, "y": 5},
        {"x": 8, "y": 5},
        {"x": 9, "y": 5},
        {"x": 13, "y": 5},
        {"x": 14, "y": 5},
        {"x": 15, "y": 5},
        {"x": 16, "y": 5},
        {"x": 17, "y": 5},
        {"x": 18, "y": 5},
        {"x": 19, "y": 5},
        {"x": 20, "y": 5},
        {"x": 21, "y": 5},
        {"x": 22, "y": 5},
        {"x": 26, "y": 5},
        {"x": 27, "y": 5},
        {"x": 28, "y": 5},
        {"x": 29, "y": 5},
        {"x": 30, "y": 5},
        {"x": 31, "y": 5},
        {"x": 32, "y": 5},
        {"x": 33, "y": 5},
        {"x": 34, "y": 5},
        {"x": 35, "y": 5},
        {"x": 39, "y": 5},
        {"x": 40, "y": 5},
        {"x": 41, "y": 5},
        {"x": 42, "y": 5},
        {"x": 43, "y": 5},
        {"x": 44, "y": 5},
        {"x": 45, "y": 5},
        {"x": 46, "y": 5},
        {"x": 47, "y": 5},
        {"x": 48, "y": 5},
        #Vertical Walls
        {"x": 9, "y": 6},
        {"x": 9, "y": 7},
        {"x": 9, "y": 8},
        {"x": 9, "y": 9},
        {"x": 9, "y": 10},

        {"x": 13, "y": 4}, 
        {"x": 13, "y": 3},
        {"x": 13, "y": 2},
        {"x": 13, "y": 1},
        {"x": 13, "y": 0},

        {"x": 22, "y": 4}, 
        {"x": 22, "y": 3},
        {"x": 22, "y": 2},
        {"x": 22, "y": 1},
        {"x": 22, "y": 0},

        {"x": 26, "y": 6}, 
        {"x": 26, "y": 7},
        {"x": 26, "y": 8},
        {"x": 26, "y": 9},
        {"x": 26, "y": 10},

        {"x": 35, "y": 6}, 
        {"x": 35, "y": 7},
        {"x": 35, "y": 8},
        {"x": 35, "y": 9},
        {"x": 35, "y": 10},

        {"x": 39, "y": 4}, 
        {"x": 39, "y": 3},
        {"x": 39, "y": 2},
        {"x": 39, "y": 1},
        {"x": 39, "y": 0},
],

    # Sticker Icons
    "knight": "\U0001F3C7",
    "dragon": "\U0001F409",
    "wall": "\U0001F9F1",
    "princess_icon": "\U0001F478",
    "empty": "\U00002B1B",
}
def display_welcome_screen():
    print(" ")
    print("Welcome to Save The Princess!")
    print(" ")
    print("Use WSAD for movement")
    print("Avoid the dragons")
    print("Get your princess!")

def draw_board(stdscr):
    curses.start_color()
    curses.use_default_colors()
    # color pair 3 for knight background yellow (foreground black)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLUE)
    # color pair 4 for princess - yellow background, white foreground
    curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_MAGENTA)
    # color pair 5 for dragon - red foreground on black
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_RED)
    
    # Print the board and all game elements using curses

    stdscr.clear()
    for y in range(game_data["height"]):
        for x in range(game_data["width"]):
            # Player
            if x == game_data["player"]["x"] and y == game_data["player"]["y"]:
                stdscr.addstr(y, x, game_data["knight"], curses.color_pair(3))
            # Dragons
            elif any(d['x'] == x and d['y'] == y for d in game_data["dragons"]):
                stdscr.addstr(y, x, game_data["dragon"], curses.color_pair(5))
              # Obstacles
            elif any(o['x'] == x and o['y'] == y for o in game_data["obstacles"]):
                stdscr.addstr(y, x, game_data["wall"], curses.color_pair(2))
             # Princess
            elif any(c['x'] == x and c['y'] == y and not c["collected"] for c in game_data["princess"]):
                stdscr.addstr(y, x, game_data["princess_icon"], curses.color_pair(4))
            else:
                stdscr.addstr(y, x, game_data["empty"], curses.color_pair(1))
    stdscr.addstr(game_data['height'] + 1, 0,
                  f"Moves Taken: {game_data['player']['score']}",
                  curses.color_pair(0))
    stdscr.addstr(game_data['height'] + 2, 0,
                  "Move with W/A/S/D, Q to quit",
                  curses.color_pair(0))
    stdscr.refresh()

def move_player(key):
    x = game_data['player']['x']
    y = game_data['player']['y']

    new_x, new_y = x, y
    key = key.lower()

    if key == "w" and y > 0:
        new_y -= 1
    elif key == "s" and y < game_data['height'] - 1:
        new_y += 1
    elif key == "a" and x > 0:
        new_x -= 1
    elif key == "d" and x < game_data['width'] - 1:
        new_x += 1
    else:
        return  

    if any(o['x'] == new_x and o['y'] == new_y for o in game_data['obstacles']):
        return
    
    game_data["player"]["x"] = new_x
    game_data["player"]["y"] = new_y
    game_data["player"]["score"] += 1

def move_dragons():
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    for dragon in game_data['dragons']:
        random.shuffle(directions)
        ex, ey = dragon['x'], dragon['y']
        for dx, dy in directions:
            new_x = ex + dx
            new_y = ey + dy
            if 0 <= new_x < game_data['width'] and 0 <= new_y < game_data['height']:
                if not any(o['x'] == new_x and o['y'] == new_y for o in game_data['obstacles']):
                    dragon['x'] = new_x
                    dragon['y'] = new_y
                    break

def play_game(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    
    stdscr.nodelay(True)

    draw_board(stdscr)

def main(stdscr):
    curses.curs_set(0)  
    draw_board(stdscr)

    while True:
        try:
            key = stdscr.getkey()
        except:
            key = None

        if key:
            if key.lower() == "q":
                break

            move_player(key)
            move_dragons()

            if any(game_data['player']["x"] == d["x"] and game_data['player']["y"] == d["y"] for d in game_data['dragons']):
                break

            draw_board(stdscr)

    stdscr.clear()
    stdscr.addstr(2, 2, "GAME OVER")
    stdscr.addstr(3, 2, "YOU GOT HIT BY A DRAGON!")
    stdscr.addstr(4, 2, f"Final Score (Moves Survived): {game_data['player']['score']}")
    stdscr.refresh()
    time.sleep(6.7)

display_welcome_screen()
time.sleep(0.0) 
curses.wrapper(main)