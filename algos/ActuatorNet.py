import torch
import numpy as np

from nn.mlp import Perceptron


class ActuatorNet:
    def __init__(self, in_dim=6, out_dim=1, lr=1e-3):

        self.model = Perceptron(in_dim, out_dim)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr)
        self.loss_fn = torch.nn.MSELoss()

    def train(self, X, Y, epochs=100):
        self.model.train()

        for epoch in range(epochs):
            self.optimizer.zero_grad()

            # forward pass
            Y_hat = self.model(X)

            # compute loss
            loss = self.loss_fn(Y_hat.squeeze(), Y)
            print('Epoch {}: train loss: {}'.format(epoch, loss.item()))

            # backprop
            loss.backward()
            self.optimizer.step()

    def evaluate(self, X, Y):
        self.model.eval()
        Y_hat = self.model(X)
        loss = self.loss_fn(Y_hat.squeeze(), Y)
        print('Test loss after Training', loss.item())

