from soma import aims
from bbox_definition import compute_transform_tal_to_native, compute_box_voxel
import os
from os.path import join
import numpy as np

#root_dir='/home/ad265693/tmp/hcp/ANALYSIS/3T_morphologist'
#side = 'L'

def crop_tal(side, root_dir):
    subject_list = [ name for name in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, name)) ]
    print(subject_list)
    n_sub=0
    N_sub=len(subject_list)
    tal_to_native, voxel_size = compute_transform_tal_to_native()
    bbmin=[86, 15, 25]
    bbmax=[162, 195, 160]
    for subject in subject_list:
        dir_sub= side + subject + '.arg'
        arg_dir = join(root_dir,subject,'t1mri','t1','default_analysis','folds','3.3', 'base2018_manual', side + subject + '_'+'base2018_manual' + '.arg')
        #arg_dir = join(root_dir,subject,'t1mri','default_acquisition','default_analysis','folds','3.1', side + subject + '.arg')
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
