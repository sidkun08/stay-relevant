import torch
import torch.nn as nn

class PolyRegress(nn.Module):
    def __init__(self, degree):
        super(PolyRegress, self).__init__()
        self.linear = nn.Linear(degree, 1)

    def forward(self, x_poly):
        return self.linear(x_poly)

