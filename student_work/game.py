#Write your game here
import curses
import random
import time

game_data = {
    # Store board dimensions, player/enemy positions, score, energy, collectibles, and icons

    "width": 50,
    "height": 10,
    "player": {"x": 0, "y": 2, "score": 0, "health": 100},
    "dragon_pos": {"x": 27, "y": 5},
    "princess": [
        {"x": 46, "y": 5, "collected": False},
    ],
    "obstacles": [], #For storing the walls and other obstacles as a list of {"x": int, "y": int} dictionaries

    # Sticker Icons
    "knight": "\U0001F3C7",
    "dragon": "\U0001F409",
    "wall": "\U0001F9F1",
    "princess_icon": "\U0001F478",
    "empty": "\U00002B1B",
    "candle": "\U0001F56F",
}

# builds a simple border-and-bar maze after the data structure is created
for i in range(game_data["width"]):
    # top and bottom borders
    game_data["obstacles"].append({"x": i, "y": 0})
    game_data["obstacles"].append({"x": i, "y": game_data["height"] - 1})

for i in range(game_data["height"]): 
    # left border except the player's starting spot
    if not (i == game_data["player"]["y"] and 0 == game_data["player"]["x"]):
        game_data["obstacles"].append({"x": 0, "y": i})
    # right border
    game_data["obstacles"].append({"x": game_data["width"] - 1, "y": i}) #This creates the right border wall by adding obstacles at x = width - 1 for all y values

#Adding obstacles in vertical ways with gaps
for x in (15, 30): #This removes the brick where the player is at the start
    for y in range(2, game_data["height"]):
        if (y // 2) % 2 == 0:
            continue
        game_data["obstacles"].append({"x": x, "y": y})

#Horizontal obstacles
row = game_data["height"] // 2
# define ranges where space should exist rather than single points
horizontal_gaps = [(5,7), (25,27), (game_data["princess"][0]["x"]-1, game_data["princess"][0]["x"]+1), (45,47)] #Changing the values determines how long the horizontal bars are
for x in range(1, game_data["width"]):
    open_space = False
    for start, end in horizontal_gaps:
        if start <= x <= end:
            open_space = True
            break
    if open_space:
        continue
    game_data["obstacles"].append({"x": x, "y": row})

# Vertical obstacles
for px in (8, 22, 37):
    for py in (2, 7):
        game_data["obstacles"].append({"x": px, "y": py})
        game_data["obstacles"].append({"x": px+1, "y": py})

#Game data for the princess room
px = game_data["princess"][0]["x"]
py = game_data["princess"][0]["y"]

#Demensions of princess room
room_half_w = 3  # room width = 1 + 2*half_w (7 tiles)
room_half_h = 2  # room height = 1 + 2*half_h (5 tiles)

room_x0 = max(1, px - room_half_w)
room_x1 = min(game_data["width"] - 2, px + room_half_w)
room_y0 = max(1, py - room_half_h)
room_y1 = min(game_data["height"] - 2, py + room_half_h)

# clear any obstacles inside the whole room area
game_data["obstacles"] = [
    o for o in game_data["obstacles"]
    if not (room_x0 <= o["x"] <= room_x1 and room_y0 <= o["y"] <= room_y1)
]

# perimeter openings: center of each side
openings = {
    (room_x0, py),  # left
    (room_x1, py),  # right
    (px, room_y0),  # top
    (px, room_y1),  # bottom
}

# add thin perimeter walls but skip opening tiles
for x in range(room_x0, room_x1 + 1): 
    for y in (room_y0, room_y1):
        if (x, y) in openings:
            continue
        game_data["obstacles"].append({"x": x, "y": y})
for y in range(room_y0, room_y1 + 1):
    for x in (room_x0, room_x1):
        if (x, y) in openings:
            continue
        game_data["obstacles"].append({"x": x, "y": y})

# ensure approach tiles just outside each opening are clear so connected
approach_positions = [
    (room_x0 - 1, py),
    (room_x1 + 1, py),
    (px, room_y0 - 1),
    (px, room_y1 + 1),
]
valid_approaches = [
    (ax, ay) for ax, ay in approach_positions
    if 1 <= ax <= game_data["width"] - 2 and 1 <= ay <= game_data["height"] - 2
]
if valid_approaches:
    game_data["obstacles"] = [
        o for o in game_data["obstacles"]
        if (o["x"], o["y"]) not in valid_approaches
    ]

# place several decorative candles in random dungeon-appropriate empty spots
def place_decorative_candles(count=6):
    width = game_data["width"]
    height = game_data["height"]
    # reset candles (idempotent if called multiple times)
    game_data['candles'] = []

    occupied = {(o['x'], o['y']) for o in game_data['obstacles']}
    occupied.add((game_data['player']['x'], game_data['player']['y']))
    occupied.add((game_data['dragon_pos']['x'], game_data['dragon_pos']['y']))
    for p in game_data['princess']:
        occupied.add((p['x'], p['y']))

    # Candidate tiles are empty tiles that are adjacent (4-neighbor) to at least
    # one obstacle — this feels dungeon-like (candles near walls).
    candidates = []
    for x in range(1, width - 1):
        for y in range(1, height - 1):
            if (x, y) in occupied:
                continue
            neighbors = [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]
            if any(n in {(o['x'], o['y']) for o in game_data['obstacles']} for n in neighbors):
                candidates.append((x, y))

    if not candidates:
        return

    n = min(count, len(candidates))
    chosen = random.sample(candidates, n)
    for x, y in chosen:
        game_data['candles'].append({"x": x, "y": y})

place_decorative_candles(count=6) #Places 6 candles in the game board


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
            # draw each logical tile at screen column sx = x*2 so every tile
            # occupies two fixed columns — this prevents emoji double-width
            # glyphs from shifting subsequent tiles.
            sx = x * 2

            # choose glyph and color for this tile
            if x == game_data["player"]["x"] and y == game_data["player"]["y"]:
                glyph = game_data["knight"]
                color = curses.color_pair(3)
            elif x == game_data["dragon_pos"]['x'] and y == game_data["dragon_pos"]['y']:
                glyph = game_data["dragon"]
                color = curses.color_pair(5)
            elif any(o['x'] == x and o['y'] == y for o in game_data["obstacles"]):
                glyph = game_data["wall"]
                color = curses.color_pair(2)
            elif any(c['x'] == x and c['y'] == y and not c["collected"] for c in game_data["princess"]):
                glyph = game_data["princess_icon"]
                color = curses.color_pair(4)
            elif any(ca['x'] == x and ca['y'] == y for ca in game_data.get('candles', [])):
                glyph = game_data["candle"]
                color = curses.color_pair(3)
            else:
                glyph = game_data["empty"]
                color = curses.color_pair(1)

            # Draw a two-column colored background first, then overlay the
            # glyph. This ensures emoji (which occupy two columns) have the
            # same background color on both columns instead of leaving an awkward uncolored space on the second column.
            try:
                stdscr.addstr(y, sx, '  ', color)
            except Exception:
                # fallback: if drawing two spaces fails (very narrow terminal),
                # draw a single space
                stdscr.addstr(y, sx, ' ', color)
            # now overlay the glyph at the same position
            stdscr.addstr(y, sx, glyph, color)
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
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    #Gets current dragon and player coordinates
    ex, ey = game_data['dragon_pos']['x'], game_data['dragon_pos']['y']
    px, py = game_data['player']['x'], game_data['player']['y']

    #Sorts directions: moves that decrease distance to player come first
    directions.sort(key=lambda d: abs((ex + d[0]) - px) + abs((ey + d[1]) - py))

    if random.random() < 0.20:
        random.shuffle(directions)

    for dx, dy in directions:
        new_x = ex + dx
        new_y = ey + dy
        
        # Boundary check
        if 0 <= new_x < game_data['width'] and 0 <= new_y < game_data['height']:
            # Obstacle check
            if not any(o['x'] == new_x and o['y'] == new_y for o in game_data['obstacles']):
                game_data['dragon_pos']['x'] = new_x
                game_data['dragon_pos']['y'] = new_y
                break



def main(stdscr):
    curses.curs_set(0)  
    draw_board(stdscr)

    while True:
        key = stdscr.getkey()
        if key.lower() == "q":
            break
        move_player(key)
        move_dragon()

        draw_board(stdscr)

curses.wrapper(main)