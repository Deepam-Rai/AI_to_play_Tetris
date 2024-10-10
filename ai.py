import os.path
from pathlib import Path

import numpy as np
import torch
from numpy import random
from typing import List

import torch.nn as nn
from torch import optim


class QModel(nn.Module):
    def __init__(self, input_dim: int, hidden_dims: List[int], output_dim: int, epsilon=0.01):
        super().__init__()
        self.input_dim: int = input_dim
        self.output_dim: int = output_dim
        self.hidden_dims: List[int] = hidden_dims
        self.epsilon = epsilon

        self.network = nn.Sequential(
            nn.Linear(self.input_dim, self.hidden_dims[0]),
            nn.LeakyReLU(),
            nn.Linear(self.hidden_dims[0], self.output_dim)
        )
        print(self.network)

    def forward(self, x):
        h = self.network(x)
        return h

    def get_move(self, state, epsilon=None):
        """

        :param state: Game state
        :param epsilon: Exploration vs exploitation [0,1]
        :return:
        """
        epsilon = epsilon or self.epsilon
        moves_count = self.output_dim
        move = [0]*moves_count
        if random.rand() < epsilon:
            move[random.randint(0, moves_count)] = 1
        else:
            state_tensor = torch.tensor(state, dtype=torch.float)
            prediction = self(state_tensor)
            next_move = torch.argmax(prediction).item()
            move[next_move] = 1
        return move

    def save(self, filename='qmodel.pth'):
        folder_path = Path("./models")
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        save_path = folder_path / filename
        torch.save(self.state_dict(), save_path)


class QTrainer:
    def __init__(self, model: QModel, gamma: float = 0.9, lr: float = 0.001):
        """
        :param model:
        :param gamma: discount factor for future moves, uising Q-Learning, Bellman Equation
        :param lr: for Adam Optimizer
        """
        self.model: QModel = model
        self.gamma: float = gamma
        self.lr: float = lr

        self.optimizer = optim.Adam(self.model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, states, actions, rewards, next_states, game_overs):
        """
        :param states: Old states
        :param actions: Action taken in old states
        :param rewards: Reward gained from action taken in old states
        :param next_states: New state from the old state after the action was taken
        :param game_overs: whether new-state is terminating or not
        :return:
        """
        # PREPARE THE DATA
        states = torch.tensor(np.array(states), dtype=torch.float)
        actions = torch.tensor(np.array(actions), dtype=torch.long)
        rewards = torch.tensor(np.array(rewards), dtype=torch.float)
        next_states = torch.tensor(np.array(next_states), dtype=torch.float)
        # convert to batches
        if len(states.shape) == 1:
            states = torch.unsqueeze(states, 0)
            actions = torch.unsqueeze(actions, 0)
            rewards = torch.unsqueeze(rewards, 0)
            next_states = torch.unsqueeze(next_states, 0)
            game_overs = (game_overs,)

        # GET PREDICTIONS
        predQ = self.model(states)  # predicted Q-values of possible current state

        # GET TARGET VALUES
        targetQ = predQ.clone()
        for i in range(len(game_overs)):
            Q_new = rewards[i]
            if not game_overs[i]:  # if the action was non-terminating
                Q_new = rewards[i] + self.gamma * torch.max(self.model(next_states[i]))
            targetQ[i][torch.argmax(actions[i]).item()] = Q_new

        # CLEAR GRADIENTS
        self.optimizer.zero_grad()
        # CALCULATE LOSS
        loss = self.criterion(predQ, targetQ)
        # CALCULATE GRADIENTS
        loss.backward()
        # UPDATE PARAMETERS
        self.optimizer.step()
