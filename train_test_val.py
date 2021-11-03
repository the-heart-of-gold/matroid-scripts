###################################################
# Script: test_train_val.py                       #
# Date: 26/10/2021                                #
# Author: Dave Dyke                               #
#                                                 #
# Processes VOC train, val, test files to extract #
# the labels given as input.                      #
###################################################
import os
import re

# Examples
# dataset = 'knife'
# labels = ['person', 'bicycle', 'bus', 'motorcycle', 'knife',
#           'airplane', 'skateboard', 'train', 'truck', 'car',]
# src_dir = '../voc-decodes/youtubebbdevkit2017/youtubebb2017/ImageSets/Main/'
# dest_dir = '../data/train-test-val-knife/'


def main():
    assert(len(argv) == 5) \
            'Usage: python test_train_val.py [DATASET] [COMMA,SEPARATED,LABELS] [SRC_DIR] [DEST_DIR].'
    dataset_name = argv[1]
    labels = argv[2].split(',')
    src_dir = argv[3] +'/'
    dest_dir = argv[4] +'/'
    assert(os.path.exists(src_dir)) \
            f'Source directory {src_dir} not found.'

    for suffix in ['_test.txt', '_train.txt', '_trainval.txt', ]:
        with open(f'{dest_dir}{dataset_name}{suffix}', 'w') as of:
            for label in labels:
                filename = f'{data_dir}{label}{suffix}'
                with open(filename, 'r') as f:
                    data = f.readlines()
                    for line in data:
                        parts = line.rstrip().split(' ')
                        if parts[1] == '1':
                            of.write(f'{parts[0]}\n')


if __name__ == '__main__':
    main()
