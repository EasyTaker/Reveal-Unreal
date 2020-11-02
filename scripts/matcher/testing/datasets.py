import torch, torchvision
from torch.utils.data import Dataset

from preprocessing import normalize_route, normalize_route_values, preprocess_route_sample

import numpy as np

import h5py

path_dataset = "dataset/"

class IndoorRoutesDataset(Dataset):
    """A dataset of alternative routes on several complex rooms.
    Initialize a specific dataset by creating a child of this class"""

    def __init__(self, path, test_train, known_unknown, kind):
        self.ALT = 0
        self.HOMO = 1
        self.mapping = {"homotopic":1, "alternative":0, 0:"alternative",1:"homotopic"}
        self.test_train = test_train
        self.known_unknown = known_unknown
        self.kind = kind
        self.dataset = h5py.File(path + "dataset.hdf5", "r")
        self.index = list()

        #Build an index making it possible to iterate over this kind of dataset
        print("Building index")
        for map_name in list(self.dataset["maps"].keys()):
            for key in ["alternative", "homotopic"]:
                if key in self.dataset[self.test_train][self.known_unknown][map_name]:
                    for pair_id, pair in enumerate(self.dataset[self.test_train][self.known_unknown][map_name][key]):
                        self.index.append((map_name,pair_id,self.mapping[key]))
        print("Index Built!")

    def concat_embedding(self, rt1, rt2):
        """Concat route pair to a polygon and then apply maxlen embedding"""
        maxlen = len(rt1)*2
        rt1, rt2 = normalize_route(rt1), normalize_route(rt2)
        route_cat = preprocess_route_sample(rt1, rt2, maxlen, cat = True)
        return route_cat

    def __len__(self):
        return len(self.index)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()
        routes = self.dataset["routes"]

        map_name, pair_id, label = self.index[idx]

        bitmap = torch.Tensor(self.dataset["maps"][map_name]).unsqueeze(0)
        rid1, rid2= self.dataset[self.test_train][self.known_unknown][map_name][self.mapping[label]][pair_id]
        if self.kind == "concat":
            route_cat = torch.Tensor(self.concat_embedding(routes[map_name][rid1] , routes[map_name][rid2])).unsqueeze(0)
            return (bitmap, route_cat), label
        elif self.kind == "individual":
            route1, route2 = torch.Tensor(routes[map_name][rid1]).unsqueeze(0), torch.Tensor(routes[map_name][rid2]).unsqueeze(0)
            return (bitmap, route1, route2), label
        else:
            raise(Exception("Unknown Kind"))

##Specific child classes, serving as datasets A & B,
##while each of these use somewhat different data for training and testing

class IndoorRoutesTrainSetA(IndoorRoutesDataset):
    """Maps of the Train Set A also appear in the Test Set A"""

    def __init__(self, kind, path=path_dataset):
        super().__init__(path,"train", "known", kind=kind)

class IndoorRoutesTrainSetB(IndoorRoutesDataset):
    """Maps of the Train Set B don't appear in the Test Set B"""

    def __init__(self, kind, path=path_dataset):
        super().__init__(path,"train", "unknown", kind=kind)

class IndoorRoutesTestSetA(IndoorRoutesDataset):
    """Maps of the Train Set A also appear in the Test Set A"""

    def __init__(self, kind, path=path_dataset):
        super().__init__(path,"test", "known", kind=kind)

class IndoorRoutesTestSetB(IndoorRoutesDataset):
    """Maps of the Train Set B don't appear in the Test Set B"""

    def __init__(self, kind, path=path_dataset):
        super().__init__(path,"test", "unknown", kind=kind)
