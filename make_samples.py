'''
Script: make_training_sample.py
Author: Dave Dyke
Created: 21/10/2021

Hacked Python3 script to process youtube_bb image files extracted from videos
using https://github.com/mbuckler/youtube-bb.

The output is:
    1. List of VOC annotation files in .txt file
    2. .zip file of uncompressed images corresponding to the annotations list
    3. .zip file for each label containing images that are NOT that label

The VOC annotation file can be used to generate CoCo.json formatted json using https://github.com/yukkyo/voc2coco
'''

import sys
import os
import pandas as pd
import zipfile


#labels = ['boat','car','knife','person',]
suffixes = ['_train.txt','_test.txt',]
#data_dir = '/data/dev/youtube-bb/output_data/youtubebbdevkit2017/youtubebb2017/ImageSets/Main/'

'''
To do
1. Process all files from list of prefixes, ['boat','knife','car','person',], ...
2. ... using a list of suffixes, ['_train.txt','_test.txt',]
3. Fn to load the file and return a pandas DataFrame
4. Fn to sample the DataFrame, params: df, n=num in sample
5. Use the training data sample to generate CoCo .zip file for training a new detector
6. Use the test data sample to generate a test .zip file to test the new detector
7. Try the API for doing tasks 5 & 6 above
'''


def sample_data(file_path:str, columns, n=5000, delimiter=' ',):
    '''
    Load an annotations file into a pandas DataFrame and take 'n' samples.
    :param file_path: the full path to the data file.
    :param columns: a list of names for the columns in the data file.
    :param n: number of items to include in the sample, default 5000.
    :param delimuter: the character used to delimit columns in the data file, default ' '.
    :type file_path: str
    :type columns: list[str]
    :type n: int
    :type delimiter: str
    :return: the sampled DataFrame
    :rtype: pandas.DataFrame
    '''
    if os.path.isfile(file_path):
        df = pd.read_csv(file_path, names=columns, sep=delimiter)
        # 'is_present' column is 1 if object is present, -1 if absent.
        # Next line takes 'n' random samples of each.
        df = df.groupby('is_present').sample(n=n, random_state=1)
    else:
        df = None
    return df


def extract_annotations_list(dest_dir, labels, df):
    '''
    Extracts the sample Annotations and writes them to a .txt file.
    :param dest_dir: dir to write the annotations lists
    :param labels: a list of labels for annotation.
    :param df: pandas DataFrame containing image IDs for the specified labels. 
    :return: None.
    '''
    with open(f'{dest_dir}{labels}annotations.txt','w') as annot:
        for index, row in df.iterrows():
            # ToDo remove hardwired path to Annotations dir.
            if row[1] == 1:  # only write out annotations for present (1) objects, not absent (-1).
                annotations_src_dir = '/data/dev/youtube-bb/output_data/youtubebbdevkit2017/youtubebb2017/Annotations/'
                if os.path.isfile(f'{annotations_src_dir}{row[0]}.xml'):
                    annot.write(f'{annotations_src_dir}{row[0]}.xml\n')


def zip_positives(src_path, zip_filepath, df):
    '''
    :param src_path: path to the dir with files to be zipped
    :param zip_filepath: path to target zipfile.
    :param df: pandas DataFrame containing image file IDs.
    :type src_path: str
    :type zip_filename: str
    :type df: pandas DataFrame
    :return: 
    :rtype: 
    '''
    with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_STORED) as ziph:
        for root, dirs, files in os.walk(src_path):
            for index, row in df.iterrows():
                if row[1] == 1:  # only write out annotations for present (1) objects, not absent (-1).
                    if os.path.isfile(f'{src_path}/{row[0]}.jpg'):
                        ziph.write(os.path.join(root, f'{src_path}{row[0]}.jpg'), f'{row[2]}/{row[0]}.jpg')


def zip_negatives(src_path, zip_filepath, labels, df):
    '''
    :param src_path: path to the dir with files to be zipped
    :param zip_filepath: path to target zipfile.
    :param labels: list of labels used to generate negative samples.
    :param df: pandas DataFrame containing image file IDs.
    :type src_path: str
    :type zip_filename: str
    :type labels: list[str]
    :type df: pandas DataFrame
    :return: 
    :rtype: 
    '''
    for label in labels:
        with zipfile.ZipFile(f'{zip_filepath}not_{label}.zip', 'w', zipfile.ZIP_STORED) as ziph:
            for root, dirs, files in os.walk(src_path):
                for index, row in df.iterrows():
                    if row[2] == label and row[1] == -1:  # only write out annotations for absent (-1) objects.
                        if os.path.isfile(f'{src_path}/{row[0]}.jpg'):
                            ziph.write(os.path.join(root, f'{src_path}{row[0]}.jpg'), f'{row[2]}/{row[0]}.jpg')


def main():
    assert(len(sys.argv) == 6), \
        'Usage: python sample_data.py [TRAIN_OR_TEST] [SOURCE_DIR] [DEST_DIR] ["COMMA,SEPARATED,LABELS"] [SAMPLE_SIZE]'
    train_or_test = sys.argv[1]
    assert(train_or_test.lower() == 'train' | train_or_test == 'test'), \
            'Must specify either 'train' or 'test' as sample type.'
    src_dir = sys.argv[2]+'/'
    dest_dir = sys.argv[3]+'/'
    labels = sys.argv[4].split(',')
    sample_size = int(sys.argv[5])

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    ##
    ## Part 1: Generate positive sample for each label ##
    ##
    frames = []
    # Loop through the labels and take 'sample_size' of each.
    for label in labels:
        sample_df = sample_data(f'{src_dir}/ImageSets/Main/{label}_{train_or_test}.txt',
                columns=['id','is_present'],
                n=sample_size,
                delimiter=' ',
                )
        sample_df['label'] = label
        frames.append(sample_df)

    # Concatenate the frames into one.
    sample_df = pd.concat(frames)

    # Make a string from list of labels, for filenames.
    annot_labels = ''
    for label in labels:
        annot_labels = annot_labels + label + '_'
    # Extract all the annotations for the selected samples.
    extract_annotations_list(dest_dir, annot_labels, sample_df)
    # Make a .zip of all the images in format for Matroid detector training (CoCo)
    zip_positives(f'{src_dir}JPEGImages/', f'{dest_dir}{annot_labels}{train_or_test}.zip', sample_df)

    ##
    ## Part 2: Generate negative sample for each label.
    ##
    zip_negatives(f'{src_dir}JPEGImages/', f'{dest_dir}', labels, sample_df)

    '''
        train_df = load_dataframe(f'{data_dir}{label}_train.txt',
                columns=['id','is_present'],
                delimiter=' '
                )
        train_df.sort_
    print(df.columns)
    print(df.nunique())
    print(df['is_present'].value_counts())
    df = df.sort_values(by=['is_present'])
    print(df)
    df = df.sort_values(by=['id'])
    print(df)
    sample_df = df.sample(frac=0.1)
    print(sample_df['is_present'].value_counts())
    sample_df = df.groupby("is_present").sample(n=10000, random_state=1)
    sample_df = df.groupby("is_present").sample(frac=0.1, random_state=1)
    print(sample_df['is_present'].value_counts())
    '''

if __name__ == "__main__":
    main()

