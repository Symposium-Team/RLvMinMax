class ConnectFour:
    def __init__(self):
        self.board = []
        for _ in range(6):
            self.board.append(([' '] * 7))
        self.RED = 'red'
        self.BLACK = 'black'
        self.BLACK_MOVES = []
        self.RED_MOVES = []

    def is_valid_move(self, board, move):
        return board[0][move[1]] == ' '

    def do_move(self, board, move):
        col = move[1]
        for row in range(5, -1, -1):
            if board[row][col] == ' ':
                board[row][col] = move[0]
                if move[0] == self.RED:
                    self.RED_MOVES.append((row, col))
                else:
                    self.BLACK_MOVES.append((row, col))
                break

    def undo_move(self, board, move):
        col = move[1]
        for row in range(6):
            if board[row][col] == move[0]:
                board[row][col] = ' '
                break

    def is_winner(self, board, playersymbol):
        if playersymbol == self.RED:
            playermoves = self.RED_MOVES
        else:
            playermoves = self.BLACK_MOVES

        # horizontal check
        for row in range(6):
            for col in range(4):
                if (row, col) in playermoves and (row, col+1) in playermoves and (row, col+2) in playermoves and (row, col+3) in playermoves:
                    return True

        # vertical check
        for row in range(3):
            for col in range(7):
                if (row, col) in playermoves and (row+1, col) in playermoves and (row+2, col) in playermoves and (row+2, col) in playermoves:
                    return True

            # Check diagonal (top-left to bottom-right)
        for row in range(3):
            for col in range(4):
                if (row, col) in playermoves and (row+1, col+1) in playermoves and (row+2, col+2) in playermoves and (row+3, col+3) in playermoves:
                    return True

            # Check diagonal (bottom-left to top-right)
        for row in range(3, 6):
            for col in range(4):
                if (row, col) in playermoves and (row-1, col+1) in playermoves and (row-2, col+2) in playermoves and (row-3, col+3) in playermoves:
                    return True

    def is_draw(self, board):
        for row in range(6):
            for col in range(7):
                if board[row][col] == ' ':
                    return False
        return True

    def moves_available(self, board):
        return self.is_draw
