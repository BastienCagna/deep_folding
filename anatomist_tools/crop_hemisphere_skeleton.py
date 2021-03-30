from soma import aims
from bbox_definition import compute_transform_tal_to_native, compute_box_voxel
import os
from os.path import join
import numpy as np

#root_dir='/home/ad265693/tmp/hcp/ANALYSIS/3T_morphologist'
#side = 'L'

def get_subject_list(root_dir):
    subject_list=[]
    for subject in os.listdir(root_dir):
        subject_list.append(subject)
    return subject_list

def crop_tal(side, root_dir):
    subject_list = get_subject_list(root_dir)
    n_sub=0
    N_sub=len(subject_list)
    tal_to_native, voxel_size = compute_transform_tal_to_native()
    bbmin=[154.72618214040995, 88.5711843650788, 118.70861482061446]
    bbmax=[304.3427610481158, 382.61495191883296, 313.1459983550012]
    for subject in subject_list:
        dir_sub= side + subject + '.arg'
        arg_dir = join(root_dir,subject,'t1mri','default_acquisition','default_analysis','folds','3.1', side + subject + '.arg')
        graph = aims.read(arg_dir)
        bb_min, bb_max  = graph['boundingbox_min'], graph['boundingbox_max']
        bbmin_mni = np.asarray(tal_to_native.transform(bb_min))
        bbmax_mni = np.asarray(tal_to_native.transform(bb_max))
        bbmin=[min(bbmin_mni[0], bbmin[0]),min(bbmin_mni[1], bbmin[1]),min(bbmin_mni[2], bbmin[2])]
        bbmax=[max(bbmax_mni[0], bbmax[0]),max(bbmax_mni[1], bbmax[1]),max(bbmax_mni[2], bbmax[2])]
        n_sub += 1
        print('bbmin : ', bbmin,'bbmax : ', bbmax)
        print(n_sub, "/", N_sub)
    return bbmin, bbmax
