#Write your game here
import curses

game_data = {
    # Store board dimensions, player/enemy positions, score, energy, collectibles, and icons

    "width": 50,
    "height": 10,
    "player": {"x": 0, "y": 2, "score": 0, "health": 100},
    "dragon_pos": {"x": 40, "y": 4},
    "princess": [
        {"x": 29, "y": 3, "collected": False},
    ],
    "obstacles": [
        {"x": 11, "y": 1}, 
        {"x": 12, "y": 2}, 
        {"x": 13, "y": 3},
        {"x": 39, "y": 1},
        {"x": 39, "y": 2},
        {"x": 39, "y": 3},
        {"x": 39, "y": 4},
        {"x": 39, "y": 5},
        {"x": 39, "y": 6},
        {"x": 39, "y": 7},
        {"x": 39, "y": 8}
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
    # color pair 2 used for obstacles (wall) - red on black
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    # color pair 3 for knight background yellow (foreground black)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    # color pair 4 for princess - yellow background, white foreground
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_MAGENTA)
    # color pair 5 for dragon - red foreground on black
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_RED)
    
    # Print the board and all game elements using curses

    stdscr.clear()
    for y in range(game_data["height"]):
        for x in range(game_data["width"]):
            # Player
            if x == game_data["player"]["x"] and y == game_data["player"]["y"]:
                # use color pair 3 to highlight knight's space with yellow background
                stdscr.addstr(y, x, game_data["knight"], curses.color_pair(3))
             # Dragon
            elif x == game_data["dragon_pos"]['x'] and y == game_data["dragon_pos"]['y']:
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
def main(stdscr):
    curses.curs_set(0)  
    draw_board(stdscr)

    while True:
        key = stdscr.getkey()
        if key.lower() == "q":
            break
        move_player(key)
        draw_board(stdscr)
curses.wrapper(main)