import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

from vectorizer import Sent2VecLSTM

class SimilarityNet(nn.Module):
    """Central Network Architecture, processing routes seperately"""
    def __init__(self, SENT_LSTM, word_features, sent_features):
        super(MainNetworkIndiv, self).__init__()
        self.lstmA = Sent2VecLSTM(in_features = word_features, out_features = sent_features)
        self.lstmB = Sent2VecLSTM(in_features = word_features, out_features = sent_features)
        self.fc1 = nn.Linear(in_features = sent_features, out_features = 50)
        self.fc2 = nn.Linear(in_features = 50, out_features = 30)
        self.out = nn.Linear(in_features = 30, out_features = 2)

        self.temp_state = None

    #Verarbeiten der Karte und der ersten Route
    def forward_first(self, sent_1):
        self.temp_state = self.lstmA(sent_1)

    #Verarbeiten der zweiten Route, im Anschluss auf forward_first
    def forward_second(self,rt2):
        sent_1 = self.temp_state
        sent_2 = self.lstmB (sent_2)

        #process 2 sents
        t = sent_1 * sent_2
        #print("Cat", t.shape)

        t = self.fc1(t)
        t = F.relu(t)
        #print("Fc1", t)

        t = self.fc2(t)
        t = F.relu(t)
        #print("Fc2", t)

        t = self.out(t)
        t = F.softmax(t, dim=1)
        #print("softmax", t)
        return t


    def forward(self, t):
        sent_1, sent_2 = t

        self.forward_first(sent_1)
        t = self.forward_second(sent_2)

        return t
