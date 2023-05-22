import minimax
import game
import random
import RLearning


def main(board, P1, P2, S1, S2):
    p1_score = 0
    p2_score = 0

    for _ in range(10000):
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
    playerRL = RLearning.QLearning(board.BLACK, alpha=0.5)

    for _ in range(1000):
        print("iter:", _)
        main(board, playerRL, playermini, playerRL.symbol, playermini.symbol)
