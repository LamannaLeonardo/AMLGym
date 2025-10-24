import torch
import torch.nn as nn
import torch.nn.functional as F


class GridConv(nn.Module):
    """
    Convolutional neural network for MNIST digit recognition. From:
    https://github.com/pytorch/examples/blob/master/mnist/main.py
    """

    def __init__(self, digit_class_num, input_channel=1):
        super(GridConv, self).__init__()
        self.conv1 = nn.Conv2d(input_channel, 20, 5, 1)
        self.conv2 = nn.Conv2d(20, 50, 5, 1)
        self.fc1 = nn.Linear(4 * 4 * 50, 500)
        self.fc2 = nn.Linear(500, digit_class_num)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.max_pool2d(x, 2, 2)
        x = F.relu(self.conv2(x))
        x = F.max_pool2d(x, 2, 2)
        x = x.view(-1, 4 * 4 * 50)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x


class CVGrid(nn.Module):
    def __init__(
        self, grid_convnet, block_dim, block_size, hidden_dim, digit_class_num, prop_dim
    ):
        super(CVGrid, self).__init__()

        self.block_dim = block_dim
        self.hidden_dim = hidden_dim
        self.digit_class_num = digit_class_num
        self.prop_dim = prop_dim

        self.grid_convnet = grid_convnet

        self.mlp = nn.Sequential(
            nn.Linear(
                self.block_dim[0] * self.block_dim[1] * self.digit_class_num,
                self.hidden_dim * 4,
            ),
            nn.ReLU(),
            nn.Linear(self.hidden_dim * 4, self.hidden_dim * 2),
            nn.ReLU(),
            nn.Linear(self.hidden_dim * 2, self.hidden_dim),
            nn.ReLU(),
            nn.Linear(self.hidden_dim, self.prop_dim),
        )

    def forward(self, x):
        pred = x.flatten(start_dim=0, end_dim=2)
        pred = self.grid_convnet(pred)
        pred = pred.view(
            -1, self.block_dim[0] * self.block_dim[1] * self.digit_class_num
        )
        pred = self.mlp(pred)

        return F.sigmoid(pred)
