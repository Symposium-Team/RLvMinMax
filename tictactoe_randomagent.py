import random

# Tic Tac Toe game implementation
class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'

    def display_board(self):
        print('---------')
        for i in range(0, 9, 3):
            print('|', self.board[i], '|', self.board[i + 1], '|', self.board[i + 2], '|')
            print('---------')

    def make_move(self, position):
        self.board[position] = self.current_player
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def is_winner(self, player):
        winning_combinations = (
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        )
        for combo in winning_combinations:
            if all(self.board[i] == player for i in combo):
                return True
        return False

    def is_draw(self):
        return ' ' not in self.board

    def is_game_over(self):
        return self.is_winner('X') or self.is_winner('O') or self.is_draw()


# Minimax player implementation
class MinimaxPlayer:
    def __init__(self, player):
        self.player = player

    def get_best_move(self, game):
        if game.is_game_over():
            return None

        if self.player == 'X':
            best_score = float('-inf')
            best_move = None
            for i in range(9):
                if game.board[i] == ' ':
                    game.board[i] = self.player
                    score = self.minimax(game, 'O')
                    game.board[i] = ' '
                    if score > best_score:
                        best_score = score
                        best_move = i
        else:
            best_score = float('inf')
            best_move = None
            for i in range(9):
                if game.board[i] == ' ':
                    game.board[i] = self.player
                    score = self.minimax(game, 'X')
                    game.board[i] = ' '
                    if score < best_score:
                        best_score = score
                        best_move = i

        return best_move

    def minimax(self, game, player):
        if game.is_winner('X'):
            return 1
        elif game.is_winner('O'):
            return -1
        elif game.is_draw():
            return 0

        if player == 'X':
            best_score = float('-inf')
            for i in range(9):
                if game.board[i] == ' ':
                    game.board[i] = player
                    score = self.minimax(game, 'O')
                    game.board[i] = ' '
                    best_score = max(score, best_score)
        else:
            best_score = float('inf')
            for i in range(9):
                if game.board[i] == ' ':
                    game.board[i] = player
                    score = self.minimax(game, 'X')
                    game.board[i] = ' '
                    best_score = min(score, best_score)

        return best_score


# Q-learning player implementation
class QLearningPlayer:
    def __init__(self, player, learning_rate=0.3, discount_factor=0.9, exploration_rate=1.0):
        self.player = player
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.q_table = {}

    def get_best_move(self, game):
        if game.is_game_over():
            return None

        if random.uniform(0, 1) < self.exploration_rate:
            possible_moves = [i for i, value in enumerate(game.board) if value == ' ']
            return random.choice(possible_moves)

        max_q_value = float('-inf')
        best_move = None

        for i in range(9):
            if game.board[i] == ' ':
                game.board[i] = self.player
                state = tuple(game.board)
                q_value = self.q_table.get((state, i), 0)
                if q_value > max_q_value:
                    max_q_value = q_value
                    best_move = i
                game.board[i] = ' '

        return best_move

    def update_q_table(self, state, action, next_state, reward):
        current_q_value = self.q_table.get((state, action), 0)
        max_next_q_value = max([self.q_table.get((next_state, i), 0) for i in range(9)])
        new_q_value = current_q_value + self.learning_rate * (
                reward + self.discount_factor * max_next_q_value - current_q_value)
        self.q_table[(state, action)] = new_q_value

    def decrease_exploration_rate(self, episode):
        # Gradually decrease the exploration rate over time
        self.exploration_rate = max(0.1, min(1.0, 1.0 - (episode / 100)))



# Function to play the game
def play_game(player1, player2):
    game = TicTacToe()

    while not game.is_game_over():
        current_player = player1 if game.current_player == 'X' else player2

        if isinstance(current_player, MinimaxPlayer):
            move = current_player.get_best_move(game)
        else:
            move = current_player.get_best_move(game)
            state = tuple(game.board)

        game.make_move(move)

        if isinstance(current_player, QLearningPlayer):
            next_state = tuple(game.board)
            reward = 1 if game.is_winner(current_player.player) else 0
            current_player.update_q_table(state, move, next_state, reward)

    return game
class RandomAgent:
    def get_best_move(self, game):
        possible_moves = [i for i, value in enumerate(game.board) if value == ' ']
        return random.choice(possible_moves)


# Function to play the game against a random agent
def play_game_vs_random(player, random_agent):
    game = TicTacToe()

    while not game.is_game_over():
        current_player = player if game.current_player == 'X' else random_agent

        move = current_player.get_best_move(game)
        game.make_move(move)

    return game


# Main program
if __name__ == '__main__':
    player = MinimaxPlayer('X')
    random_agent = RandomAgent()

    games_won_by_player = 0
    games_drawn = 0

    ra_win=[]
    mm_win=[]

    for _ in range(100):
        game = play_game_vs_random(player, random_agent)

        if game.is_winner('X'):
            games_won_by_player += 1
            ra_win.append(0)
            mm_win.append(1)
        elif game.is_draw():
            games_drawn += 1
            mm_win.append(-1)
            ra_win.append(-1)
        else:
            ra_win.append(1)
            mm_win.append(0)

    print(f"Minimax vs Random Agent:")
    print(f"Games won by Minimax: {games_won_by_player}")
    print(f"Games drawn: {games_drawn}")
    print(ra_win,mm_win)


    player = QLearningPlayer('O', learning_rate=0.3, discount_factor=0.9, exploration_rate=1.0)

    games_won_by_player = 0
    games_drawn = 0

    ra_win=[]
    ql_win=[]

    for episode in range(100):
        player.decrease_exploration_rate(episode)

        game = play_game_vs_random(player, random_agent)

        if game.is_winner('O'):
            games_won_by_player += 1
            ql_win.append(1)
            ra_win.append(0)
        elif game.is_draw():
            games_drawn += 1
            ql_win.append(-1)
            ra_win.append(-1)
        else:
            ql_win.append(0)
            ra_win.append(1)

    print(f"\nQLearning vs Random Agent:")
    print(f"Games won by QLearning: {games_won_by_player}")
    print(f"Games drawn: {games_drawn}")
    print(ra_win,ql_win)
