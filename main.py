import minimax
import game
import RLearning
import matplotlib.pyplot as plt


def main(board, P1, P2, S1, S2):
    p1_score = 0
    p2_score = 0

    for _ in range(50000):
        board.refresh_board(board)

        while True:
            move1 = P1.choose_move(board)
            state1 = ''.join([item for sublist in board.board for item in sublist])
            board.do_move(board, move1)

            if board.is_winner(board, S1):
                p1_score += 1
                reward = 100
                state2 = ''.join([item for sublist in board.board for item in sublist])
                P1.update_q_table(state1, move1[1], state2, reward)
                break

            move2 = P2.choose_move(board)
            board.do_move(board, move2)

            if board.is_winner(board, S2):
                p2_score += 1
                reward = -100
                state2 = ''.join([item for sublist in board.board for item in sublist])
                P1.update_q_table(state1, move1[1], state2, reward)
                break

            if board.is_draw(board):
                reward = 0
                state2 = ''.join([item for sublist in board.board for item in sublist])
                P1.update_q_table(state1, move1[1], state2, reward)
                break

    print("Total no:of wins for P1 :", p1_score)
    print("Total no: of wins for P2 :", p2_score)
    return p1_score, p2_score


if __name__ == '__main__':
    board = game.ConnectFour()
    playermini = minimax.MiniMax(3, board.RED)
    playerRL = RLearning.QLearning(board.BLACK, alpha=0.9, epsilon=0.8)

    episode = 1
    RLscores = []
    miniscores = []
    while True:
        print("Episode:", episode)
        RLscore, miniscore = main(board, playerRL, playermini, playerRL.symbol, playermini.symbol)
        RLscores.append(RLscore)
        miniscores.append(miniscore)

        if RLscore > miniscore or episode == 500:
            break

        # Changing the learning rate and the exploration rate dynamically
        alpha = max(0.1, 0.8 / episode)
        epsilon = max(0.1, 0.9 / episode)
        playerRL.learning_rate = alpha
        playerRL.exploration_factor = epsilon

        episode += 1

    episodes = [i for i in range(1, episode + 1)]
    plt.plot(episodes, RLscores, label='Q-Learning')
    plt.plot(episodes, miniscores, label='Minimax')
    plt.legend()
    plt.show()
