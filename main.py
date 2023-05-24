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


def main(board, P1, P2):
    p1_score = 0
    p2_score = 0

    for _ in range(500):
        board.refresh_board(board)

        while True:
            move1 = P1.choose_move(board)
            board.do_move(board, move1)

            if board.is_winner(board, P1.symbol):
                p1_score += 1
                break

            move2 = P2.choose_move(board)
            board.do_move(board, move2)

            if board.is_winner(board, P2.symbol):
                p2_score += 1
                break

            if board.is_draw(board):
                reward = 0
                break

    return p1_score, p2_score


if __name__ == '__main__':
    board = game.ConnectFour()
    playermini = minimax.MiniMax(3, board.RED)
    playerRL = RLearning.QLearning(board.RED)
    playerrandom = randomPlayer(board.BLACK)

    RL1scores = []
    RL2scores = []
    miniscores = []

    # minimax plays
    print("Minimax is playing...")
    for episode in range(1000):
        miniscore, randomscore = main(board, playermini, playerrandom)
        miniscores.append(miniscore)

    print("RL is playing...")
    for episode in range(1000):
        RLscore, randomscore = main(board, playerRL, playerrandom)
        RL1scores.append(RLscore)

    # RL plays
    playerRL.train(board)

    print("Trained RL is playing...")
    for episode in range(1000):
        RLscore, randomscore = main(board, playerRL, playerrandom)
        RL2scores.append(RLscore)

    episodes = [i for i in range(1, 1001)]
    plt.plot(episodes, RL1scores, label='Untrained Q-Learning')
    plt.plot(episodes, RL2scores, label='Trained Q-Learning')
    plt.plot(episodes, miniscores, label='Minimax')
    plt.legend()
    plt.ylabel("No: of wins")
    plt.xlabel("No: of games")
    plt.show()