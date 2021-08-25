import torch

# rewards: positive if win (not dependent on turn number to win), negative if click on already open cell, negative if lose

class NeuralNet(torch.nn.Module):
    def __init__(self, output_size):
        super(NeuralNet, self).__init__()
        self.relu = torch.nn.ReLU()
        self.logsoftmax = torch.nn.LogSoftmax()
        self.conv1 = torch.nn.Conv2d(1, 10, kernel_size=3)
        self.conv2 = torch.nn.Conv2d(10, 20, kernel_size=5)
        self.mp = torch.nn.MaxPool2d(2)
        self.fc = torch.nn.Linear(320, output_size)
    def forward(self, x):
        in_size = x.size(0)
        out = self.relu(self.mp(self.conv1(x)))
        out1 = self.relu(self.mp(self.conv2(out)))
        out2 = out1.view(in_size, -1)
        #print(out2.size())
        y_pred = self.fc(out2)
        return y_pred

