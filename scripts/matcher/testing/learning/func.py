import torch

@torch.no_grad()
def get_all_preds(model, loader):
    """Returns all predicted labels and all correct labels"""
    all_preds = torch.tensor([])
    all_labels = torch.tensor([], dtype = torch.long)
    for batch in loader:
        data, labels = batch
        preds = model(data)
        all_preds = torch.cat((all_preds, preds), dim = 0)
        all_labels = torch.cat((all_labels, labels), dim = 0)

    return all_preds.argmax(1), all_labels

def get_num_correct(pred, labels):
    """Returns amount of correctly classified labels"""
    return pred.eq(labels).sum().item()
