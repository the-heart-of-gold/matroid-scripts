'''
Script: make_collections.py
Author: Dave Dyke
Created: 27/10/2021

Script to process youtube_bb image files extracted from videos
using https://github.com/mbuckler/youtube-bb.

The output is a set of .zip files containing test images for each label given on the CLI.

'''

import matroid
from matroid.client import Matroid
import sys
import os
import pandas as pd
import zipfile


#api = Matroid(client_id='XXXXX', client_secret='XXXXXXXXXXX')
#api = Matroid(base_url='http://www.matroid.com/api/v1/',
#        client_id='',
#        client_secret=''
#        )
base_url = 'https://www.matroid.com/api/v1/'
bearer_token = 'YOUR-TOKEN-HERE'
headers = {'Authorization': f'{bearer_token}'}

#labels = ['boat','car','knife','person',]

suffixes = ['_train.txt','_test.txt',]
#data_dir = '/data/dev/youtube-bb/output_data/youtubebbdevkit2017/youtubebb2017/ImageSets/Main/'


def sample_data(file_path:str, columns, n=5000, delimiter=' ',):
    '''
    Load file of image IDs into a pandas DataFrame and take 'n' samples.
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


def zip_collections(src_path, zip_filepath, df):
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
        print(df)
        for root, dirs, files in os.walk(src_path):
            for index, row in df.iterrows():
                if row[1] == 1:  # only write out annotations for present (1) objects, not absent (-1).
                    if os.path.isfile(f'{src_path}/{row[0]}.jpg'):
                        ziph.write(os.path.join(root, f'{src_path}{row[0]}.jpg'), f'{row[2]}/{row[0]}.jpg')


def main():
    assert(len(sys.argv) == 5), \
        'Usage: python make_collections.py [SOURCE_DIR] [DEST_DIR] ["COMMA,SEPARATED,LABELS"] [COLLECTION_SIZE]'
    src_dir = sys.argv[1]+'/'
    dest_dir = sys.argv[2]+'/'
    labels = sys.argv[3].split(',')
    collection_size = int(sys.argv[4])

    assert(os.path.exists(src_dir)), \
            f'Source file {src_file} not found!'

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    '''
    Part 1: Collect images for each label and zip into a collection.
    '''
    frames = {}
    # Loop through the labels and take 'collection_size' of each.
    for label in labels:
        sample_df = sample_data(f'{src_dir}ImageSets/Main/{label}_test.txt',
                columns=['id','is_present'],
                n=collection_size,
                delimiter=' ',
                )
        sample_df['label'] = label
        frames[label] = sample_df

    # Make a .zip of all the images in format for Matroid detector training (CoCo)
    for label in frames:
        zip_collections(f'{src_dir}JPEGImages/', f'{dest_dir}{label}_test_collection.zip', frames[label])


if __name__ == "__main__":
    main()

