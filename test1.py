import chess
import random


class ChessGame:
    def __init__(self):
        self.board = chess.Board()

    def initialize_game(self):
        self.board.reset()

    def get_board(self):
        return self.board.copy()

    def get_current_player(self):
        return self.board.turn

    def make_move(self, move):
        if move in self.board.legal_moves:
            self.board.push(move)
            return True
        return False

    def is_game_over(self):
        return self.board.is_game_over()


class QLearningAgent:
    def __init__(self, state_size, action_size, learning_rate=0.1, discount_factor=0.99, exploration_rate=1.0,
                 exploration_decay=0.995):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
        self.q_table = {}

    def choose_action(self, state):
        if random.uniform(0, 1) < self.exploration_rate:
            return random.randint(0, self.action_size - 1)
        else:
            return self.get_best_action(state)

    def get_best_action(self, state):
        if tuple(state) not in self.q_table:
            return random.randint(0, self.action_size - 1)
        return max(range(self.action_size), key=lambda action: self.q_table[tuple(state)][action])

    def update_q_table(self, state, action, reward, next_state):
        state = tuple(state)
        next_state = tuple(next_state)

        if tuple(state) not in self.q_table:
            self.q_table[state] = [0] * self.action_size
        if tuple(next_state) not in self.q_table:
            self.q_table[next_state] = [0] * self.action_size

        current_value = self.q_table[state][action]
        max_next_value = max(self.q_table[next_state])
        new_value = (1 - self.learning_rate) * current_value + self.learning_rate * (
                    reward + self.discount_factor * max_next_value)
        self.q_table[state][action] = new_value

    def decay_exploration_rate(self):
        self.exploration_rate *= self.exploration_decay

    def get_q_table(self):
        return self.q_table


def convert_board_to_state(board):
    state = [0] * (12 * 64)
    for square, piece in board.piece_map().items():
        piece_index = piece.piece_type - 1
        color_offset = 0 if piece.color == chess.WHITE else 6
        state[square + color_offset * 64] = piece_index
    return state


class MinimaxAgent:
    def __init__(self, max_depth):
        self.max_depth = max_depth

    def choose_move(self, board):
        best_move = None
        best_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval_score = self.minimax(board, self.max_depth - 1, float('-inf'), float('inf'), False)
            board.pop()
            if eval_score > best_eval:
                best_eval = eval_score
                best_move = move
        return best_move

    def evaluate_board(self, board):
        score = 0
        for piece_type in [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]:
            score += len(board.pieces(piece_type, chess.WHITE)) - len(board.pieces(piece_type, chess.BLACK))
        return score

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board)

        if maximizing_player:
            max_eval = float('-inf')
            for move in board.legal_moves:
                board.push(move)
                eval_score = self.minimax(board, depth - 1, alpha, beta, False)
                board.pop()
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in board.legal_moves:
                board.push(move)
                eval_score = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval


class Main:
    def __init__(self, num_episodes, max_depth):
        self.num_episodes = num_episodes
        self.max_depth = max_depth
        self.q_agent = QLearningAgent(state_size=12 * 64, action_size=4096)

    def play_game(self):
        game = ChessGame()
        minimax_agent = MinimaxAgent(max_depth=self.max_depth)

        wins = {'Minimax': 0, 'QLearning': 0}

        for episode in range(self.num_episodes):
            game.initialize_game()
            state = convert_board_to_state(game.get_board())
            done = False

            # Determine if Minimax should play optimally or not
            play_optimally = episode < 20

            while not done:
                current_player = game.get_current_player()
                action = None

                if current_player == chess.WHITE and play_optimally:
                    move = minimax_agent.choose_move(game.get_board())
                    valid_move = game.make_move(move)
                else:
                    action = self.q_agent.choose_action(state)
                    moves = list(game.get_board().legal_moves)
                    if action >= len(moves):
                        continue
                    move = moves[action]
                    valid_move = game.make_move(move)

                if not valid_move:
                    continue

                state_prime = convert_board_to_state(game.get_board())

                if game.is_game_over():
                    result = game.board.result()
                    if result == '1-0':
                        wins['Minimax'] += 1
                        print(f"Episode {episode + 1}: Minimax wins")
                    elif result == '0-1':
                        wins['QLearning'] += 1
                        print(f"Episode {episode + 1}: QLearning wins")
                    else:
                        print(f"Episode {episode + 1}: Draw")

                    done = True

                    if current_player == chess.WHITE and play_optimally:
                        reward = 0
                    else:
                        reward = 0.1 if result == '1-0' else -0.1  # Small positive/negative reward for intermediate states

                    if action is not None:
                        self.q_agent.update_q_table(state, action, reward, state_prime)
                    self.q_agent.decay_exploration_rate()

                state = state_prime

        print("Results:")
        print(f"Minimax wins: {wins['Minimax']}")
        print(f"QLearning wins: {wins['QLearning']}")


num_episodes = 100
max_depth = 6

print("Training the Model :")

main = Main(num_episodes=num_episodes, max_depth=max_depth)
main.play_game()
