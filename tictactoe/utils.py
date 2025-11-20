# utils.py

def check_winner(board):
    win_lines = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
        (0, 4, 8), (2, 4, 6)              # diagonals
    ]

    for a, b, c in win_lines:
        if board[a] == board[b] == board[c] and board[a] != " ":
            return board[a]  # X or O

    return None
