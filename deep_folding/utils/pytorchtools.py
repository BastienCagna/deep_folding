"""
From https://github.com/Bjarten/early-stopping-pytorch/blob/master/pytorchtools.py
"""

import numpy as np
import torch

class EarlyStopping:
    """Early stops the training if validation loss doesn't improve after a given patience."""
    def __init__(self, patience=7, verbose=False, delta=0):
        """
        Args:
            patience (int): How long to wait after last time validation loss improved.
                            Default: 7
            verbose (bool): If True, prints a message for each validation loss improvement.
                            Default: False
            delta (float): Minimum change in the monitored quantity to qualify as an improvement.
                            Default: 0
        """
        self.patience = patience
        self.verbose = verbose
        self.counter = 0
        self.best_score = None
        self.early_stop = False
        self.val_loss_min = np.Inf
        self.delta = delta

    def __call__(self, val_loss, model, root_dir):

        score = -val_loss

        if self.best_score is None:
            self.best_score = score
            self.save_checkpoint(val_loss, model, root_dir)
        elif score < self.best_score + self.delta:
            self.counter += 1
            print('EarlyStopping counter: {self.counter} out of {self.patience}')
            if self.counter >= self.patience:
                self.early_stop = True
        else:
            print('la saving')
            self.best_score = score
            self.save_checkpoint(val_loss, model, root_dir)
            self.counter = 0

    def save_checkpoint(self, val_loss, model, root_dir):
        '''Saves model when validation loss decrease.'''
        if self.verbose:
            print('Validation loss decreased ({self.val_loss_min:.6f} --> {val_loss:.6f}).  Saving model ...')
        torch.save(model.state_dict(), root_dir+'checkpoint.pt')
        self.val_loss_min = val_loss
