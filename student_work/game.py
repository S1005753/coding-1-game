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
        {"x": 43, "y": 8}, #Bob   
        {"x": 7, "y": 2},    #Rob
        {"x": 20, "y": 8}, #Cob
        {"x": 30, "y": 0}, #Tob
    ],
    "princess": [
        {"x": 47, "y": 8, "collected": False},
    ],
    "game_won": False,
    "obstacles": [
],

    # Sticker Icons
    "knight": "\U0001F3C7",
    "dragon": "\U0001F409",
    "wall": "\U0001F9F1",
    "princess_icon": "\U0001F478",
    "empty": "\U00002B1B",
}
#Place a brick in every section from 0 to 49 except for the numbers listed at the end
horizontal_walls = [{"x": x, "y": 5} for x in range(49) if x not in [8, 9, 10, 23, 24, 25, 36, 37, 38]]

obstacle_segments = [
    (7, range(6, 11)), (3, range(3, 5)), (7, range(0,2)),   (11, range(0, 5)), #Rob room
    (22, range(0, 5)),  (11, range(3,8)), (17, range(8,12)), (13, range(9, 10)),(14, range(9, 10)),(20, range(9, 10)),(21, range(9, 10)), (22, range(6, 8)), (26, range(6, 11)), #Cob room
    (26, range(0, 1)),(26, range(2,3)), (30, range(1, 4)), (34, range( 2,3)),(35, range(1, 3)), #Tob room
    (35, range(6, 11)), (39, range(0, 5)), (39, range(8, 9)), (40, range(8, 9)), (41, range(8, 9)), (41, range(7,9)), (42, range(8, 9)), (41, range(9, 10)), (45, range(10,11)),( 45, range(8,9)),( 45, range(6,7)), #Bob room
]

vertical_walls = [{"x": x, "y": y} for x, y_range in obstacle_segments for y in y_range]

game_data["obstacles"] = horizontal_walls + vertical_walls

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

            # Check if player collects princess
            for p in game_data["princess"]:
                if game_data['player']["x"] == p["x"] and game_data['player']["y"] == p["y"] and not p["collected"]:
                    p["collected"] = True
                    game_data["game_won"] = True
                    break

            if game_data["game_won"] or any(abs(game_data['player']["x"] - d["x"]) <= 1 and abs(game_data['player']["y"] - d["y"]) <= 1 for d in game_data['dragons']):
                break

            draw_board(stdscr)

    stdscr.clear()
    if game_data["game_won"]:
        stdscr.addstr(2, 2, "YOU WIN!")
        stdscr.addstr(3, 2, "You saved Princess Plum!")
    else:
        stdscr.addstr(2, 2, "GAME OVER")
        stdscr.addstr(3, 2, "YOU GOT HIT BY A DRAGON!")
    stdscr.addstr(4, 2, f"Final Score (Moves Taken): {game_data['player']['score']}")
    stdscr.refresh()
    time.sleep(6.7)

display_welcome_screen()
time.sleep(0.0) 
curses.wrapper(main)