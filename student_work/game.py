#Write your game here
import curses

game_data = {
    # Store board dimensions, player/enemy positions, score, energy, collectibles, and icons

    "width": 50,
    "height": 10,
    "player": {"x": 0, "y": 2, "score": 0, "health": 100},
    "dragon_pos": {"x": 40, "y": 3},
    "princess": [
        {"x": 30, "y": 3, "collected": False},
    ],
    "obstacles": [
        {"x": 11, "y": 1}, 
        {"x": 12, "y": 2}, 
        {"x": 15, "y": 3},
        {"x": 39, "y": 1},
        {"x": 38, "y": 2},
        {"x": 38, "y": 3},
        {"x": 40, "y": 4},
        {"x": 40, "y": 5}
    ],

    # Sticker Icons
    "knight": "\U0001F3C7",
    "dragon": "\U0001F409",
    "wall": "\U0001F9F1",
    "princess_icon": "\U0001F478",
    "empty": " ",
}

def draw_board(stdscr):
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, -1)
    # Print the board and all game elements using curses

    stdscr.clear()
    for y in range(game_data["height"]):
        row = ""
        for x in range(game_data["width"]):
            # Player
            if x == game_data["player"]["x"] and y == game_data["player"]["y"]:
                row += game_data["knight"]
             # Dragon
            elif x == game_data["dragon_pos"]['x'] and y == game_data["dragon_pos"]['y']:
                row += game_data["dragon"]
              # Obstacles
            elif any(o['x'] == x and o['y'] == y for o in game_data["obstacles"]):
                row += game_data["wall"]
             # Princess
            elif any(c['x'] == x and c['y'] == y and not c["collected"] for c in game_data["princess"]):
                row += game_data["princess_icon"]
            else:
                row += game_data["empty"]
        stdscr.addstr(y, 0, row, curses.color_pair(1))
    stdscr.addstr(game_data['height'] + 1, 0,
                  f"Moves Taken: {game_data['player']['score']}",
                  curses.color_pair(1))
    stdscr.addstr(game_data['height'] + 2, 0,
                  "Move with W/A/S/D, Q to quit",
                  curses.color_pair(1))
    stdscr.refresh()
def move_player(key):
    x  = game_data["player"]["x"]
    y = game_data["player"]["y"]

    new_x, new_y = x, y
    key = key.lower()

    if key == "w":
        new_y -= 1
    elif key == "s":
        new_y += 1
    elif key == "a":
        new_x -= 1
    elif key == "d":
        new_x += 1
    else:
        return  # Invalid key
    if any(o['x'] == new_x and o['y'] == new_y for o in game_data["obstacles"]):
        return

    game_data["player"]["x"] = new_x
    game_data["player"]["y"] = new_y
    game_data["player"]["score"] += 1
def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    draw_board(stdscr)

    while True:
        key = stdscr.getkey()
        if key.lower() == "q":
            break
        move_player(key)
        draw_board(stdscr)
curses.wrapper(main)