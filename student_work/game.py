# Write your game here
    import curses

game_data = {
    # Store board dimensions, player/enemy positions, score, energy, collectibles, and icons

    'width': 10,
    'height': 10,
    'knight': {"x": 0, "y": 0, "score": 0, "health": 100},
    'dragon_pos': {"x": 10, "y": 10},
    'princess': [
        {"x": 10, "y": 1, "collected": False},
    ],
    'obstacles': [
        {"x": 4, "y": 5},
        {"x": 5, "y": 6},
        {"x": 6, "y": 7}
    ],

    # Sticker Icons
    'Knight': " ",
    'Dragon': " ",
    'Wall': " ",
    'Princess': " ",
    'empty': "  "
}


def draw_board(screen):
    # Print the board and all game elements using curses


# Good Luck!