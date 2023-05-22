import minimax
import game
import random
import RL


# to check if either algorithm is working properly
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

    for _ in range(10000):
        board.refresh_board(board)
        while True:
            move1 = P1.choose_move(board)
            board.do_move(board, move1)

            if board.is_winner(board, board.RED):
                p1_score += 1
                print("P1 wins")
                break

            move2 = P2.choose_move(board)
            board.do_move(board, move2)

            if board.is_winner(board, board.BLACK):
                p2_score += 1
                print("P2 wins")
                break

            if board.is_draw(board):
                print("draw")
                break

    print("Total no:of wins for P1 :", p1_score)
    print("Total no: of wins for P2 :", p2_score)


if __name__ == '__main__':
    board = game.ConnectFour()
    player1 = minimax.MiniMax(15, board.RED)
    player2 = randomPlayer(board.BLACK)

    main(board, player1, player2)
