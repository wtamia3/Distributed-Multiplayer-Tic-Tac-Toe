def format_board(board):
    lines = []
    for i in range(3):
        row = board[i*3:(i+1)*3]
        lines.append(" | ".join(cell if cell != " " else " " for cell in row))
        if i < 2:
            lines.append("---------")
    return "\n".join(lines)


def check_winner(board):
    win_lines = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]
    for a,b,c in win_lines:
        if board[a] == board[b] == board[c] != " ":
            return board[a]
    return None
