import chess


class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.available_moves = {i for i in range(9)}

    def print_board(self):
        print('---------')
        for row in [self.board[i:i + 3] for i in range(0, 9, 3)]:
            print('|', end='')
            for cell in row:
                if cell == 'X':
                    print(' ✖️' + ' |', end='')
                elif cell == 'O':
                    print(' ⭕' + ' |', end='')
                else:
                    print('  ' + ' |', end='')
            print('\n---------')

    def do_move(self, move, player):
        if self.is_valid_move(move, player):
            self.board[move] = player
            self.available_moves.remove(move)
            return True
        return False

    def undo_move(self, move):
        if self.board[move] != ' ':
            self.board[move] = ' '
            self.available_moves.add(move)

    def is_valid_move(self, move, player):
        return player == 'X' or player == 'O' and self.board[move] == ' '

    def is_winner(self, player):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Horizontal
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Vertical
            [0, 4, 8], [2, 4, 6]  # Diagonal
        ]
        for combo in winning_combinations:
            if all(self.board[pos] == player for pos in combo):
                return True
        return False

    def is_draw(self):
        if all(self.board[move] != ' ' for move in range(9)):
            if not self.is_winner('X') and not self.is_winner('O'):
                return True
        return False

    def get_valid_moves(self):
        return [i for i in range(9) if self.board[i] == ' ']


class ConnectFour:
    def __init__(self):
        self.board = [[' ' for _ in range(7)] for _ in range(6)]
        self.move_history = []

    def print_board(self):
        print('---------------')
        for row in self.board:
            print('|', end='')
            for cell in row:
                if cell == 'red':
                    print(' 🔴' + ' |', end='')
                elif cell == 'yellow':
                    print(' 🟡' + ' |', end='')
                else:
                    print('  ' + cell + ' |', end='')
            print('\n---------------')

    def do_move(self, coloumn, player):
        if self.is_valid_move(coloumn, player):
            for row in range(5, -1, -1):
                if self.board[row][coloumn] == ' ':
                    self.board[row][coloumn] = player
                    self.move_history.append((row, coloumn, player))
                    return True

        return False

    def undo_move(self):
        if len(self.move_history) > 0:
            row, column, player = self.move_history.pop()
            self.board[row][column] = ' '

    def is_winner(self, player):
        for row in range(6):
            for col in range(7):
                if self.board[row][col] == player:
                    # Check horizontal
                    if col <= 3 and all(self.board[row][col + i] == player for i in range(4)):
                        return True
                    # Check vertical
                    if row <= 2 and all(self.board[row + i][col] == player for i in range(4)):
                        return True
                    # Check diagonal (top-left to bottom-right)
                    if row <= 2 and col <= 3 and all(self.board[row + i][col + i] == player for i in range(4)):
                        return True
                    # Check diagonal (bottom-left to top-right)
                    if row >= 3 >= col and all(self.board[row - i][col + i] == player for i in range(4)):
                        return True
        return False

    def is_draw(self):
        if all(self.board[row][col] != ' ' for row in range(6) for col in range(7)):
            if not self.is_winner('red') and not self.is_winner('yellow'):
                return True

        return False

    def is_valid_move(self, coloumn, player):
        return player == 'red' or player == 'yellow' and self.board[0][coloumn] == ' '

    def get_valid_moves(self):
        return [i for i in range(7) if self.board[0][i] == ' ']


class Chess:
    def __init__(self):
        self.board = chess.Board()
        self.move_history = []  # To track the move history

    def print_board(self):
        print(self.board)

    def do_move(self, move):
        if move in self.board.legal_moves:
            self.move_history.append(move)
            self.board.push(move)
            return True
        else:
            return False

    def undo_move(self):
        if len(self.move_history) > 0:
            move = self.move_history.pop()
            self.board.pop()
            return move
        else:
            return None

    def is_winner(self, color):
        return self.board.is_checkmate() and self.board.turn != color

    def is_game_over(self):
        return self.board.is_game_over()

    def get_valid_moves(self):
        return list(self.board.legal_moves)
