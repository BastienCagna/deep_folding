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


def fetch_data(root_dir, type_input, save_dir=None, side=None, file_n=0, until=-1):
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
        print(len(os.listdir(root_dir)))
        for filename in os.listdir(root_dir)[:until]:
            file_n += 1
            file = os.path.join(root_dir, filename)
            if os.path.isfile(file) and '.nii' in file and '.minf' not in file and 'normalized' in file:
                aimsvol = aims.read(file)
                sample = np.asarray(aimsvol).T
                filename = re.search('(\d{6})', filename).group(0)
                print('filename = ' + filename)
                print('file = ' + file)

                data_dict[filename] = [sample]
                file_data= open("save_data.txt", 'w')
                file_data.write(str(data_dict))
                file_data.close()
                n += 1
                print('file',n, 'total : ',file_n)
                    #print(filename)

        dataframe = pd.DataFrame.from_dict(data_dict)


        if save_dir:
            file_pickle_basename = str(file_n) + '_' + side + type_input + '.pkl'
            file_pickle = os.path.join(save_dir, file_pickle_basename)
            dataframe.to_pickle(file_pickle)

    else:
        df=pd.read_pickle(join('/neurospin/dico/adneves/output/L_gw', str(506) + '_' + side + type_input + '.pkl'))
        n= len(list(df.columns))
        data_dict= df.to_dict()
        for filename in os.listdir(root_dir)[file_n:until]:
            file_n+=1
            file = os.path.join(root_dir, filename)
            if os.path.isfile(file) and '.nii' in file and '.minf' not in file and 'normalized' in file:
                aimsvol = aims.read(file)
                sample = np.asarray(aimsvol).T
                filename = re.search('(\d{6})', filename).group(0)
                print('filename = ' + filename)
                print('file = ' + file)

                data_dict[filename] = [sample]
                file_data= open("save_data.txt", 'w')
                file_data.write(str(data_dict))
                file_data.close()
                n += 1
                print('file',n, 'total : ',file_n)
                    #print(filename)

        dataframe = pd.DataFrame.from_dict(data_dict)


        if save_dir:
            file_pickle_basename = str(until) + '_' + side + type_input + '.pkl'
            file_pickle = os.path.join(save_dir, file_pickle_basename)
            dataframe.to_pickle(file_pickle)
