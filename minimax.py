
class MiniMax:
    def __init__(self, depth, symbol):
        self.max_depth = depth
        self.symbol = symbol

    def choose_move(self, board):
        best_move = None
        best_score = float('-inf')

        for col in range(7):
            move = (self.symbol, col)
            if board.is_valid_move(board, move):
                board.do_move(board, move)
                eval_score = self.minmax(board, self.max_depth - 1, float('-inf'), float('inf'), False)
                board.undo_move(board, move)

                if eval_score > best_score:
                    best_score = eval_score
                    best_move = move

        return best_move

    def minmax(self, board, depth, alpha, beta, maximizingplayer):
        if depth == 0:
            symbol = self.symbol if maximizingplayer else 'red' if self.symbol == 'black' else 'red'
            score = self.evaluate_board(board, symbol)
            return score

        if not board.moves_available(board):
            if board.is_winner(board, self.symbol):
                return 100
            elif board.is_winner(board, 'red' if maximizingplayer else 'black'):
                return -100
            else:
                return 0

        opp_symbol = 'red' if self.symbol == 'black' else 'black'                                                  ''
        if maximizingplayer:
            max_score = float('-inf')
            for col in range(7):
                move = (self.symbol, col)
                if board.is_valid_move(move):
                    board.do_move(move)
                    eval_score = self.minmax(board, depth - 1, alpha, beta, False)
                    board.undo_move(move)

                    max_score = max(max_score, eval_score)
                    alpha = max(alpha, eval_score)
                    if beta <= alpha:
                        break
            return max_score
        else:
            min_score = float('inf')
            for col in range(7):
                move = (opp_symbol, col)
                if board.is_valid_move(board, move):
                    board.do_move(move)
                    eval_score = self.minmax(board, depth - 1, alpha, beta, True)
                    board.undo_move(move)

                    min_score = min(min_score, eval_score)
                    alpha = min(alpha, min_score)
                    if beta <= alpha:
                        break
            return min_score

    def evaluate_board(self, board, symbol):
        score = 0

        for row in range(6):
            for col in range(4):
                window = board[row][col:col + 4]
                score += self.evaluate_window(window, symbol)

        for col in range(7):
            for row in range(3):
                window = [board[row + i][col] for i in range(4)]
                score += self.evaluate_window(window, symbol)

        for row in range(3):
            for col in range(4):
                window = [board[row + i][col + i] for i in range(4)]
                score += self.evaluate_window(window, symbol)

        for row in range(3, 6):
            for col in range(4):
                window = [board[row - i][col + i] for i in range(4)]
                score += self.evaluate_window(window, symbol)

        return score

    def evaluate_window(self, window, symbol):
        opp_symbol = 'red' if symbol == 'black' else 'red'
        score = 0

        if window.count(symbol) == 4:
            score += 100
        elif window.count(symbol) == 3 and window.count(' ') == 1:
            score += 5
        elif window.count(symbol) == 2 and window.count(' ') == 2:
            score += 2

        if window.count(opp_symbol) == 3 and window.count(' ') == 1:
            score -= 4

        return score