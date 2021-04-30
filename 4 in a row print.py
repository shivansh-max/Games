# Imports
import numpy as np
print()

# Global
column_count = 6
row_count = 7


# Functions
def create_grid():
    function_board = np.zeros((column_count, row_count))
    return function_board


def print_board(board):
    print('__1__2__3__4__5__6__7__')
    print(np.flip(board, 0))


board = create_grid()


# print(board)

def check_win(board, peice):
    # Check for horozontal wins
    for c in range(column_count):
        for r in range(row_count):
            if board[c][r] == peice and board[c][r + 1] == peice and board[c][r + 2] == peice and board[c][
                r + 3] == peice:
                print('\n')
                print_board(board)
                print('\n')
                print(peice, ' has won the game ! ')
                exit()

    # Check for vertical wins
    for c in range(column_count):
        for r in range(row_count):
            if board[c][r] == peice and board[c + 1][r] == peice and board[c + 2][r] == peice and board[c + 3][r] == peice:
                print('\n')
                print_board(board)
                print('/n')
                print('Player ', peice, ' has won the game ! ')
                exit()
    # Check for horozontal wins [ / ]
    for c in range(column_count):
        for r in range(row_count):
            if board[c][r] == peice and board[c + 1][r + 1] == peice and board[c + 2][r + 2] == peice and board[c + 3][r + 3] == peice:
                print('\n')
                print_board(board)
                print('\n')
                print('Player ', peice, ' has won the game ! ')
                exit()
    # Check for horozontal wins [ \ ]
    for c in range(column_count):
        for r in range(row_count):
            if board[c][r] == peice and board[c - 1][r - 1] == peice and board[c - 2][r - 2] == peice and board[c - 3][r - 3] == peice:
                print('\n')
                print_board(board)
                print('\n')
                print('Player ', peice, ' has won the game ! ')
                exit()


def drop_peice(row, board, col, peice):
    board[row][col] = peice


def get_next_open_row(board, col):
    for r in range(row_count):
        if board[r][col] == 0:
            row = r
            return row


def check_if_valid(board, col):
    if board[5][col] == 0:
        return True


print_board(board)


def main():
    turn = 'X'
    while True:
        # Xs turn
        if turn == 'X':
            print("It's Player 1's turn")
            col = int(input("What is the column that you want : "))
            col -= 1
            row = get_next_open_row(board, col)
            if check_if_valid(board, col):
                drop_peice(row, board, col, 1)
            turn = 'O'
            check_win(board, 1)


        # Xs turn
        else:
            print("It's Player 2's turn")
            col = int(input("What is the column that you want : "))
            col -= 1
            row = get_next_open_row(board, col)
            if check_if_valid(board, col):
                drop_peice(row, board, col, 2)
            turn = 'X'
            check_win(board, 2)
        print_board(board)


if __name__ == '__main__':
    main()
