import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F



class Sent2VecLSTM(nn.Module):
    """Route Network base-architecture using CNN"""
    def __init__(self, in_features, out_features=0):
        super(RouteNetworkRNN, self).__init__()

        hidden_dim = out_features

        self.lstm = nn.LSTM(in_features, out_features)

    def forward(self,t):
        sent_batch = list()
        for sent in t:
            route = sent.squeeze()
            _, (sent,_) = self.lstm(sent.view(-1,1,in_features))
            sent_batch.append(sent)

        t = torch.stack(sent_batch)
        t = F.relu(t)

        return t
