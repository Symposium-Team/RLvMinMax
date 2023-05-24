import chess
import random
import matplotlib.pyplot as plt

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


class RandomAgent:
    def __init__(self):
        pass

    def choose_move(self, board):
        moves = list(board.legal_moves)
        return random.choice(moves)


class Main:
    def __init__(self, num_episodes):
        self.num_episodes = num_episodes
        self.q_agent = QLearningAgent(state_size=12 * 64, action_size=4096)

    def play_game(self):
        game = ChessGame()
        random_agent = RandomAgent()

        wins = {'QLearning': 0, 'Random': 0}
        draws = 0

        for episode in range(self.num_episodes):
            game.initialize_game()
            state = convert_board_to_state(game.get_board())
            done = False

            while not done:
                current_player = game.get_current_player()
                action = None

                if current_player == chess.WHITE:
                    move = random_agent.choose_move(game.get_board())
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
                        wins['QLearning'] += 1
                        print(f"Episode {episode + 1}: QLearning wins")
                    elif result == '0-1':
                        wins['Random'] += 1
                        print(f"Episode {episode + 1}: Random wins")
                    else:
                        draws += 1
                        print(f"Episode {episode + 1}: Draw")

                    done = True

                    if action is not None:
                        self.q_agent.update_q_table(state, action, 0, state_prime)
                    self.q_agent.decay_exploration_rate()

                state = state_prime

        print("Results:")
        print(f"QLearning wins: {wins['QLearning']}")
        print(f"Random wins: {wins['Random']}")
        print(f"Draws: {draws}")


def convert_board_to_state(board):
    state = [0] * (12 * 64)
    for square, piece in board.piece_map().items():
        piece_index = piece.piece_type - 1
        color_offset = 0 if piece.color == chess.WHITE else 6
        state[square + color_offset * 64] = piece_index
    return state


if __name__=='__main__':
    num_episodes = 100

    print("Training the Model:")

    main = Main(num_episodes=num_episodes)
    main.play_game()
