import minimax
import game
import RLearning
import matplotlib.pyplot as plt
import random


class randomPlayer:
    def __init__(self, symbol):
        self.symbol = symbol

    def choose_move(self, board):
        move = (self.symbol, random.randint(0, 6))
        while not board.is_valid_move(board, move):
            move = (self.symbol, random.randint(0, 6))

        return move


def main(board, P1, P2, S1, S2):
    p1_score = 0
    p2_score = 0

    for _ in range(5000):
        board.refresh_board(board)

        while True:
            move1 = P1.choose_move(board)
            state1 = ''.join([item for sublist in board.board for item in sublist])
            board.do_move(board, move1)

            if board.is_winner(board, S1):
                p1_score += 1
                reward = 100
                state2 = ''.join([item for sublist in board.board for item in sublist])
                if isinstance(P1, RLearning.QLearning):
                    P1.update_q_table(state1, move1[1], state2, reward)
                break

            move2 = P2.choose_move(board)
            board.do_move(board, move2)

            if board.is_winner(board, S2):
                p2_score += 1
                reward = -100
                state2 = ''.join([item for sublist in board.board for item in sublist])
                if isinstance(P1, RLearning.QLearning):
                    P1.update_q_table(state1, move1[1], state2, reward)
                break

            if board.is_draw(board):
                reward = 0
                state2 = ''.join([item for sublist in board.board for item in sublist])
                if isinstance(P1, RLearning.QLearning):
                    P1.update_q_table(state1, move1[1], state2, reward)
                break

    return p1_score, p2_score


if __name__ == '__main__':
    board = game.ConnectFour()
    playermini = minimax.MiniMax(3, board.RED)
    playerRL1 = RLearning.QLearning(board.RED, alpha=0.9, epsilon=0.8)
    playerRL2 = RLearning.QLearning(board.RED, alpha=0.9, epsilon=0.8)
    playerrandom = randomPlayer(board.BLACK)

    RL1scores = []
    RL2scores = []
    miniscores = []

    # minimax plays
    print("Minimax is playing...")
    for episode in range(1000):
        miniscore, randomscore = main(board, playermini, playerrandom, board.RED, board.BLACK)
        miniscores.append(miniscore)

    # untrained RL plays
    print("Untrained RL is playing...")
    for episode in range(1, 1001):
        RL1score, randomscore = main(board, playerRL1, playerrandom, board.RED, board.BLACK)
        RL1scores.append(RL1score)

        # Changing the learning rate and the exploration rate dynamically
        alpha = max(0.1, 0.8 / episode)
        epsilon = max(0.1, 0.9 / episode)
        playerRL1.learning_rate = alpha
        playerRL1.exploration_factor = epsilon

    # other RL plays
    print("Training the other RL player...")
    for episode in range(1, 5001):
        main(board, playerRL2, playerrandom, board.RED, board.BLACK)

        # Changing the learning rate and the exploration rate dynamically
        alpha = max(0.1, 0.8 / episode)
        epsilon = max(0.1, 0.9 / episode)
        playerRL2.learning_rate = alpha
        playerRL2.exploration_factor = epsilon

    print("Trained RL is playing...")
    for episode in range(1, 1001):
        RL2score, randomscore = main(board, playerRL2, playerrandom, board.RED, board.BLACK)
        RL2scores.append(RL2score)

    episodes = [i for i in range(1, 1001)]
    plt.plot(episodes, RL1scores, label='Untrained Q-Learning')
    plt.plot(episodes, RL2scores, label='Trained Q-Learning')
    plt.plot(episodes, miniscores, label='Minimax')
    plt.legend()
    plt.show()
