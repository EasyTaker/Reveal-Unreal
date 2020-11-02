import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

from torch.utils.data import DataLoader, Dataset
import wandb

from time import clock
import shelve

import sys, os
sys.path.append("learning/networks")

from torch.utils.data import DataLoader, Dataset
from learning.datasets import *
from learning.networks.MainNetwork import *
from learning.func import *


@torch.no_grad()
def test_network(network, test_set):
    """Test model on given dataset"""
    network.eval()
    test_loader = DataLoader(test_set, batch_size=100)
    all_preds, all_labels = get_all_preds(network, test_loader)
    correct = get_num_correct(all_preds, all_labels)
    accuracy = correct/len(all_labels)
    #loss = F.cross_entropy(all_preds, all_labels)
    return accuracy

def train_network(network, train_set, validation_set, lr=0.0001, bsize=100, eps=10, net_name="undefined", train_set_name="undefined"):
    """Train Model on given Dataset"""
    lr = lr
    batch_size = bsize
    shuffle = True
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    network = network.to(device)
    train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True)
    optimizer = optim.Adam(network.parameters(), lr=lr)
    print("Training network", net_name, "on", train_set_name)

    network.train()
    accuracy_last = 0
    total_time = 0
    for epoch in range(eps):
        start_time = clock()
        total_loss = 0
        total_correct = 0
        print("Starting Epoch", epoch)
        for batch in train_loader:
            data, labels = batch
            preds = network(data)
            loss = F.cross_entropy(preds,labels)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_loss += loss.item() * batch_size
            total_correct += get_num_correct(preds.argmax(1), labels)
        total_time += start_time - clock()
        accuracy = total_correct/len(train_set)
        ##Uncomment for wandb logs:
        #val_acc= test_network(network, validation_set)
        #wandb.log({"epoch":epoch,"loss": ytotal_loss, "total_correct": total_correct,"accuracy": accuracy, "validation accuracy": val_acc})
        ##Uncomment for console logs:
        #print("Epoch", epoch,"Total Loss", total_loss,"Total Correct", total_correct)
        if (accuracy - accuracy_last < 0.015):
            break
        accuracy_last = accuracy
        with shelve.open("_data/shelves/networks/"+train_set_name+"/"+net_name) as df:
            df[f"{train_set_name}_lr{lr}_bs{bsize}_eps{eps}"] = network
    #wandb.save(net_name+".h5")

default_models = {"individual":{"CSTS_Siamese":MainNetworkCSTSSiamese,"RNNSiamese":MainNetworkRNNSiamese, "CNN_2Channel": MainNetworkCNN2Channel,"CNN_2Channel": MainNetworkCNN2Channel}, "concat":{"CNN_Double":MainNetworkDouble}}

def train_all_models(models_to_train, train_known, train_unknown):
    train_sets = dict()
    test_sets = dict()
    if train_known:
        train_sets["known"] = IndoorRoutesTrainSetA
        test_sets["known"] = IndoorRoutesTestSetA
    if train_unknown:
        train_sets["unknown"] = IndoorRoutesTrainSetB
        test_sets["unknown"] = IndoorRoutesTestSetB

    if not models_to_train:
        models_to_train = default_models

    for kind in models_to_train:
        for train_name in train_sets:
            train_set = train_sets[train_name](kind)
            validation_set = test_sets[train_name](kind)
            route_len=0
            if kind == "individual":
                (_,rt1,_),_ = train_set[0]
                route_len = rt1.shape[1]
            if kind == "concat":
                (_,rts),_ = train_set[0]
                route_len = rts.shape[1]
            print(route_len)
            for net_name in models_to_train[kind]:
                network = models_to_train[kind][net_name](route_len=route_len)
                ##Uncomment for wandb logs:
                #wandb.init(project=(your_project_name)+train_name)
                #wandb.watch(network)
                train_network(network, train_set, validation_set, lr=0.00015, bsize=100, eps=20, net_name=net_name, train_set_name=train_name)
