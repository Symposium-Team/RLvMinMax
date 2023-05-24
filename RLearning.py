import random
import numpy as np


class QLearning:
    def __init__(self, symbol, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.symbol = symbol
        self.learning_rate = alpha  # learning rate
        self.discount_factor = gamma  # discount factor
        self.exploration_factor = epsilon  # exploration factor
        self.q_table = {}

    def state_to_string(self, board):
        rows, cols = len(board), len(board[0])
        binary_vector = np.zeros((rows, cols))

        for i in range(rows):
            for j in range(cols):
                if board[i][j] == self.symbol:
                    binary_vector[i][j] = 1
                elif board[i][j] != ' ':
                    binary_vector[i][j] = -1

        return binary_vector.flatten().tostring()

    def choose_move(self, board):
        state = self.state_to_string(board.board).strip()

        if random.random() < self.exploration_factor or state not in self.q_table:
            valid_moves = [col for col in range(7) if board.is_valid_move(board, (self.symbol, col))]
            move = random.choice(valid_moves)
            return self.symbol, move

        q_values = self.q_table[state]
        valid_moves = [col for col in range(7) if board.is_valid_move(board, (self.symbol, col))]
        best_moves = np.argwhere(q_values[valid_moves] == np.amax(q_values[valid_moves])).flatten()
        move_index = random.choice(best_moves)
        move = valid_moves[move_index]
        return self.symbol, move

    def update_q_table(self, state, action, next_state, reward):
        if state not in self.q_table:
            self.q_table[state] = np.zeros(7)

        if next_state not in self.q_table:
            self.q_table[next_state] = np.zeros(7)

        current_q_value = self.q_table[state][action]
        max_next_q_value = np.max(self.q_table[next_state])
        new_q_value = (1 - self.learning_rate) * current_q_value + self.learning_rate * (
                    reward + self.discount_factor * max_next_q_value)
        self.q_table[state][action] = new_q_value
