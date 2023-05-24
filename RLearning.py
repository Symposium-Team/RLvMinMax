import random
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np


class QNetwork(nn.Module):
    def __init__(self, input_size, output_size):
        super(QNetwork, self).__init__()
        self.fc1 = nn.Linear(input_size, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, output_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x


class QLearning:
    def __init__(self, symbol, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.symbol = symbol
        self.learning_rate = alpha
        self.discount_factor = gamma
        self.exploration_factor = epsilon
        self.q_network = QNetwork(42, 7)
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=self.learning_rate)

    def choose_move(self, board):
        state = self.preprocess_state(board.board)
        state_tensor = torch.from_numpy(state).float().unsqueeze(0)
        q_values = self.q_network(state_tensor)
        action = torch.argmax(q_values, dim=1).item()
        move = (self.symbol, action)
        return move

    def update_q_table(self, state, action, next_state, reward):
        state = self.preprocess_state(state)
        next_state = self.preprocess_state(next_state)

        state_tensor = torch.from_numpy(state).float().unsqueeze(0)
        next_state_tensor = torch.from_numpy(next_state).float().unsqueeze(0)

        q_values = self.q_network(state_tensor)
        next_q_values = self.q_network(next_state_tensor)
        max_next_q_value = torch.max(next_q_values).item()

        q_values[0][action] = (1 - self.learning_rate) * q_values[0][action] + \
                              self.learning_rate * (reward + self.discount_factor * max_next_q_value)

        loss = nn.MSELoss()(q_values, self.q_network(next_state_tensor))
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def preprocess_state(self, board):
        state = np.zeros((6, 7), dtype=np.float32)
        for i in range(6):
            for j in range(7):
                if board[i][j] == self.symbol:
                    state[i][j] = 1.0
                elif board[i][j] != ' ':
                    state[i][j] = -1.0
        return state.flatten()

    def train(self, board, num_episodes=5000):
        state_size = len(self.preprocess_state(board.board))
        action_size = len(board.board[0])

        self.q_network = QNetwork(state_size, action_size)
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=self.learning_rate)

        for episode in range(num_episodes):
            board.refresh_board(board)
            done = False

            while not done:
                current_state = board.board.copy()

                move = self.choose_move(board)
                board.do_move(board, move)

                reward = 0
                if board.is_winner(board, self.symbol):
                    reward = 100
                    done = True
                elif board.is_draw(board):
                    reward = 0
                    done = True

                self.update_q_table(current_state, move[1], board.board, reward)
