class ConnectFour:
    def __init__(self):
        self.board = []
        for _ in range(6):
            self.board.append(([' '] * 7))
        self.RED = 'red'
        self.BLACK = 'black'

    def is_valid_move(self, board, move):
        return board.board[0][move[1]] == ' '

    def do_move(self, board, move):
        col = move[1]
        for row in range(5, -1, -1):
            if board.board[row][col] == ' ':
                board.board[row][col] = move[0]
                break

    def undo_move(self, board, move):
        col = move[1]
        for row in range(6):
            if board.board[row][col] == move[0]:
                board.board[row][col] = ' '
                break

    def is_winner(self, board, player):
        # Check horizontal
        for row in range(6):
            for col in range(4):
                if board.board[row][col] == player and \
                        board.board[row][col + 1] == player and \
                        board.board[row][col + 2] == player and \
                        board.board[row][col + 3] == player:
                    return True

        # Check vertical
        for row in range(3):
            for col in range(7):
                if board.board[row][col] == player and \
                        board.board[row + 1][col] == player and \
                        board.board[row + 2][col] == player and \
                        board.board[row + 3][col] == player:
                    return True

        # Check diagonal (top-left to bottom-right)
        for row in range(3):
            for col in range(4):
                if board.board[row][col] == player and \
                        board.board[row + 1][col + 1] == player and \
                        board.board[row + 2][col + 2] == player and \
                        board.board[row + 3][col + 3] == player:
                    return True

        # Check diagonal (bottom-left to top-right)
        for row in range(3, 6):
            for col in range(4):
                if board.board[row][col] == player and \
                        board.board[row - 1][col + 1] == player and \
                        board.board[row - 2][col + 2] == player and \
                        board.board[row - 3][col + 3] == player:
                    return True

        return False

    def is_draw(self, board):
        for row in range(6):
            for col in range(7):
                if board.board[row][col] == ' ':
                    return False
        return True

    def moves_available(self, board):
        return self.is_draw(board)

    def refresh_board(self, board):
        board.board = []
        for _ in range(6):
            board.board.append(([' '] * 7))
