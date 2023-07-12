
class Minimax:
    def __init__(self, game, player='X'):
        self.best_move = None
        self.game = game
        if player == 'O':
            self.player = 'O'
            self.opponent = 'X'
        else:
            self.player = 'X'
            self.opponent = 'O'

    def get_best_move(self):
        best_score = float('-inf')
        best_move = None

        for move in self.game.get_valid_moves():
            self.game.do_move(move, self.player)
            score = self.minimax(self.game, False, float('-inf'), float('inf'))
            self.game.undo_move(move)

            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def minimax(self, game, maximizing_player, alpha, beta):
        if game.is_winner(self.player):
            return 1
        if game.is_winner(self.opponent):
            return -1
        if game.is_draw():
            return 0

        if maximizing_player:
            max_score = float('-inf')
            for move in game.get_valid_moves():
                game.do_move(move, self.player)
                score = self.minimax(game, False, alpha, beta)
                game.undo_move(move)
                max_score = max(max_score, score)
                alpha = max(alpha, max_score)
                if beta <= alpha:
                    break
            return max_score
        else:
            min_score = float('inf')
            for move in game.get_valid_moves():
                game.do_move(move, self.opponent)
                score = self.minimax(game, True, alpha, beta)
                game.undo_move(move)
                min_score = min(min_score, score)
                beta = min(beta, min_score)
                if beta <= alpha:
                    break
            return min_score
