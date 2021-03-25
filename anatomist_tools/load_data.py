"""
Scripts that enables to create a dataframe of numpy arrays from .nii.gz or .nii
images.
"""
from __future__ import division
import os

import anatomist.api as anatomist
from soma import aims

import pandas as pd
import numpy as np
import re


def fetch_data(root_dir, type_input, save_dir=None, side=None):
    """
    Creates a dataframe of data with a column for each subject and associated
    np.array. Generation a dataframe of "normal" images and a dataframe of
    "abnormal" images. Saved these two dataframes to pkl format on
    Neurospin/dico/lguillon/data directory.
    -----------
    Parameter:
    root_dir: directory of training images
    """

    data = ['train', 'test']
    for phase in data:
        phase=''
        data_dict = dict()
        for filename in os.listdir(root_dir+phase):
            file = os.path.join(root_dir+phase, filename)
            if os.path.isfile(file) and '.nii' in file and '.minf' not in file and 'normalized' in file:
                aimsvol = aims.read(file)
                sample = np.asarray(aimsvol).T
                filename = re.search('(\d{6})', filename).group(0)
                print('filename = ' + filename)
                print('file = ' + file)

                data_dict[filename] = [sample]
                #print(filename)

            dataframe = pd.DataFrame.from_dict(data_dict)

            if save_dir:
                file_pickle_basename = side + type_input + '.pkl'
                file_pickle = os.path.join(save_dir, file_pickle_basename)
                dataframe.to_pickle(file_pickle)
