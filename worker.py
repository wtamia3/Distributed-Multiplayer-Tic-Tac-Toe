# worker.py

from utils import check_winner

def worker_loop(task_queue, result_queue):
    while True:
        player, move, board = task_queue.get()

        new_board = board.copy()

        if new_board[move] != " ":
            result_queue.put((False, board, None))
            continue

        new_board[move] = player
        winner = check_winner(new_board)

        result_queue.put((True, new_board, winner))
