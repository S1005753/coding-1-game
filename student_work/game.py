#Write your game here
import curses
import time
import random

game_data = {
    # Store board dimensions, player/enemy positions, score, energy, collectibles, and icons

    "width": 49,
    "height": 10,
    "player": {"x": 0, "y": 2, "score": 0, "health": 100},
    "dragon_pos": {"x": 43, "y": 3},    
    "2dragon_pos": {"x": 7, "y": 2},    
    "3dragon_pos": {"x": 20, "y": 7},
    "4dragon_pos": {"x": 30, "y": 1},


    "princess": [
        {"x": 47, "y": 3, "collected": False},
    ],
    "obstacles": [
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
    ],

    # Sticker Icons
    "knight": "\U0001F3C7",
    "dragon": "\U0001F409",
    "wall": "\U0001F9F1",
    "princess_icon": "\U0001F478",
    "empty": "\U00002B1B",
}

def draw_board(stdscr):
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    # color pair 3 for knight background yellow (foreground black)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_BLUE)
    # color pair 4 for princess - yellow background, white foreground
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_MAGENTA)
    # color pair 5 for dragon - red foreground on black
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_RED)
    #curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK) #Test for later
    
    # Print the board and all game elements using curses

    stdscr.clear()
    for y in range(game_data["height"]):
        for x in range(game_data["width"]):
            # Player
            if x == game_data["player"]["x"] and y == game_data["player"]["y"]:
                stdscr.addstr(y, x, game_data["knight"], curses.color_pair(3))
             # Dragon
             # Dragon
            elif x == game_data["dragon_pos"]['x'] and y == game_data["dragon_pos"]['y']:
                stdscr.addstr(y, x, game_data["dragon"], curses.color_pair(5))  
            # Dragon2
            elif x == game_data["2dragon_pos"]['x'] and y == game_data["2dragon_pos"]['y']:
                stdscr.addstr(y, x, game_data["dragon"], curses.color_pair(5))           
             # Dragon3
            elif x == game_data["3dragon_pos"]['x'] and y == game_data["3dragon_pos"]['y']:
                stdscr.addstr(y, x, game_data["dragon"], curses.color_pair(5))
                #Dragon4
            elif x == game_data["4dragon_pos"]['x'] and y == game_data["4dragon_pos"]['y']:
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
                  curses.color_pair(1))
    stdscr.addstr(game_data['height'] + 2, 0,
                  "Move with W/A/S/D, Q to quit",
                  curses.color_pair(1))
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

def move_dragon():
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    random.shuffle(directions)
    ex, ey = game_data['dragon_pos']['x'], game_data['dragon_pos']['y']

    for dx, dy in directions:
        new_x = ex + dx
        new_y = ey + dy
        if 0 <= new_x < game_data['width'] and 0 <= new_y < game_data['height']:
            if not any(o['x'] == new_x and o['y'] == new_y for o in game_data['obstacles']):
                game_data['dragon_pos']['x'] = new_x
                game_data['dragon_pos']['y'] = new_y
                break
def move_dragon2():
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    random.shuffle(directions)
    ex, ey = game_data['2dragon_pos']['x'], game_data['2dragon_pos']['y']

    for dx, dy in directions:
        new_x = ex + dx
        new_y = ey + dy
        if 0 <= new_x < game_data['width'] and 0 <= new_y < game_data['height']:
            if not any(o['x'] == new_x and o['y'] == new_y for o in game_data['obstacles']):
                game_data['2dragon_pos']['x'] = new_x
                game_data['2dragon_pos']['y'] = new_y
                break
def move_dragon3():
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    random.shuffle(directions)
    ex, ey = game_data['3dragon_pos']['x'], game_data['3dragon_pos']['y']

    for dx, dy in directions:
        new_x = ex + dx
        new_y = ey + dy
        if 0 <= new_x < game_data['width'] and 0 <= new_y < game_data['height']:
            if not any(o['x'] == new_x and o['y'] == new_y for o in game_data['obstacles']):
                game_data['3dragon_pos']['x'] = new_x
                game_data['3dragon_pos']['y'] = new_y
                break
def move_dragon4():
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    random.shuffle(directions)
    ex, ey = game_data['4dragon_pos']['x'], game_data['4dragon_pos']['y']

    for dx, dy in directions:
        new_x = ex + dx
        new_y = ey + dy
        if 0 <= new_x < game_data['width'] and 0 <= new_y < game_data['height']:
            if not any(o['x'] == new_x and o['y'] == new_y for o in game_data['obstacles']):
                game_data['4dragon_pos']['x'] = new_x
                game_data['4dragon_pos']['y'] = new_y
                break


def main(stdscr):
    curses.curs_set(0)  
    draw_board(stdscr)

    while True:
        key = stdscr.getkey()
        if key.lower() == "q":
            break
        move_player(key)
        move_dragon ()
        move_dragon2()
        move_dragon3()
        move_dragon4()
        draw_board(stdscr)

curses.wrapper(main)