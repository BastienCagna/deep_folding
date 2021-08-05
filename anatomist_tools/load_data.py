"""
Scripts that enables to create a dataframe of numpy arrays from .nii.gz or .nii
images.
"""
from __future__ import division
import os
from os.path import join
import anatomist.api as anatomist
from soma import aims

import pandas as pd
import numpy as np
import re


def fetch_data(root_dir, type_input,ss_size, save_dir=None, side=None, file_n=0):
    """
    Creates a dataframe of data with a column for each subject and associated
    np.array. Generation a dataframe of "normal" images and a dataframe of
    "abnormal" images. Saved these two dataframes to pkl format on
    Neurospin/dico/lguillon/data directory.
    -----------
    Parameter:
    root_dir: directory of training images
    """
    if file_n== 0:
        n = 0
        file_n =0
        data_dict = dict()
        for file in os.listdir(os.path.join(root_dir, str(ss_size)+'/')):
            file_n +=1
            if  'normalized' in file and '.minf' not in file:
                file=join(root_dir, str(ss_size)+'/',file)
                aimsvol = aims.read(file)
                sample = np.asarray(aimsvol).T
                filename = file[46:52]
                print(filename)
                print('filename = ' + filename)
                print('file = ' + file)
                data_dict[filename] = [sample]

                n += 1
            print('file',n, 'total : ',file_n)
                    #print(filename)
        print('taille dict',len(data_dict))
        dataframe = pd.DataFrame.from_dict(data_dict)


        if save_dir:
            file_pickle_basename =  side + type_input+'_'+str(ss_size) +'.pkl'
            file_pickle = os.path.join(save_dir, file_pickle_basename)
            dataframe.to_pickle(file_pickle)


fetch_data(root_dir='/home/ad265693/tmp/dico/adneves/benchmark/', type_input='skeleton',ss_size='raw', save_dir='/home/ad265693/tmp/dico/adneves/benchmark/', side='L', file_n=0)
