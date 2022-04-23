from torch import nn


class Perceptron(nn.Module):
    def __init__(self, in_dim, out_dim, hidden_layer=(32, 32)):
        super(Perceptron, self).__init__()

        self.l1 = nn.Sequential(nn.Linear(in_dim,          hidden_layer[0]), nn.Softsign())
        self.l2 = nn.Sequential(nn.Linear(hidden_layer[0], hidden_layer[1]), nn.Softsign())
        self.l3 = nn.Sequential(nn.Linear(hidden_layer[1],         out_dim), nn.Softsign())

    def forward(self, x):
        x   = self.l1(x)
        x   = self.l2(x)
        out = self.l3(x)

        return out
