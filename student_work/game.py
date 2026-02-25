# Write your game here
    import curses

game_data = {
    # Store board dimensions, player/enemy positions, score, energy, collectibles, and icons

    "width": 20,
    "height": 10,
    "player": {"x": 0, "y": 0, "score": 0, "health": 100},
    "dragon_pos": {"x": 20, "y": 5},
    "princess": [
        {"x": 15, "y": 2, "collected": False},
    ],
    "obstacles:" [
        {"x": 4, "y": 5},
        {"x": 5, "y": 6},
        {"x": 6, "y": 7}
    ],

    # Sticker Icons
    "Knight": "\U+1F482",
    "Dragon": "\U+1F432",
    "Wall": "\U+1F6A7",
    "Princess": "\U+1F478",
    "empty": " "
}

def draw_board(screen):
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, -1)
    # Print the board and all game elements using curses

    screen.clear()
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
                row += game_data["Princess"]
            else:
                row += game_data["empty"]
        screen.addstr(y, 0, row, curses.color_pair(1))

    screen.refresh()
    screen.getkey()  # pause so player can see board

curses.wrapper(draw_board)