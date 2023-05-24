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


def main(board, P1, P2, train=False):
    p1_score = 0
    p2_score = 0

    for _ in range(500):
        board.refresh_board(board)

        while True:
            move1 = P1.choose_move(board)
            state1 = ''.join([item for sublist in board.board for item in sublist])
            board.do_move(board, move1)

            if board.is_winner(board, P1.symbol):
                p1_score += 1
                reward = 100
                state2 = ''.join([item for sublist in board.board for item in sublist])
                if isinstance(P1, RLearning.QLearning) and train:
                    P1.update_q_table(state1, move1[1], state2, reward)
                break

            move2 = P2.choose_move(board)
            board.do_move(board, move2)

            if board.is_winner(board, P2.symbol):
                p2_score += 1
                reward = -100
                state2 = ''.join([item for sublist in board.board for item in sublist])
                if isinstance(P1, RLearning.QLearning) and train:
                    P1.update_q_table(state1, move1[1], state2, reward)
                break

            if board.is_draw(board):
                reward = 0
                state2 = ''.join([item for sublist in board.board for item in sublist])
                if isinstance(P1, RLearning.QLearning) and train:
                    P1.update_q_table(state1, move1[1], state2, reward)
                break

    return p1_score, p2_score


if __name__ == '__main__':
    board = game.ConnectFour()
    playermini = minimax.MiniMax(3, board.RED)
    playerRL = RLearning.QLearning(board.RED, alpha=0.9, epsilon=0.8)
    playerrandom = randomPlayer(board.BLACK)

    RLscores1 = []
    RLscores2 = []
    miniscores = []

    # minimax plays
    print("Minimax is playing...")
    for episode in range(100):
        miniscore, randomscore = main(board, playermini, playerrandom)
        miniscores.append(miniscore)

    # RL plays
    print("Training the RL player...")
    for episode in range(1, 501):
        RLscore, miniscore = main(board, playerRL, playermini, train=True)
        RLscores1.append(RLscore)

        # Changing the learning rate and the exploration rate dynamically
        alpha = max(0.1, 0.8 / episode)
        epsilon = max(0.1, 0.9 / episode)
        playerRL.learning_rate = alpha
        playerRL.exploration_factor = epsilon

    print("Trained RL is playing...")
    for episode in range(1, 101):
        RLscore, randomscore = main(board, playerRL, playerrandom)
        RLscores2.append(RLscore)

    episodes = [i for i in range(1, 101)]
    plt.plot(episodes, RLscores1, label='Mid-training Q-Learning')
    plt.plot(episodes, RLscores2, label='Trained Q-Learning')
    plt.plot(episodes, miniscores, label='Minimax')
    plt.legend()
    plt.show()
