'''
Script: sample_data.py
Author: Dave Dyke
Created: 21/10/2021

Hacked Python3 script to process youtube_bb image files extracted from videos
using https://github.com/mbuckler/youtube-bb.

The output is:
    1. Labelled training data for creating a new detector
    2. Labelled test data to evaluate the new detector
'''

import sys
import os
import pandas as pd
import zipfile


labels = ['boat','car','knife','person',]
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
    Fn to load a text file into a pandas DataFrame and take 'n' samples.
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


def extract_annotations_list(dest_dir, label, df):
    '''
    :param df: pandas DataFrame containing image IDs.
    :return: None.
    '''
    with open(f'{dest_dir}{label}_annotations.txt','w') as annot:
        for index, row in df.iterrows():
            # ToDo hardwired path to Annotations
            if os.path.isfile(f'/data/dev/youtube-bb/output_data/youtubebbdevkit2017/youtubebb2017/Annotations/{row[0]}.xml'):
                annot.write(f'{row[0]}.xml\n')


def zipdir(src_path, zip_filepath, df):
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
    with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as ziph:
        print(src_path)
        print(df)
        for root, dirs, files in os.walk(src_path):
            print(root)
            for index, row in df.iterrows():
                print(f'{src_path}/{row[0]}.jpg')
                if os.path.isfile(f'{src_path}/{row[0]}.jpg'):
                    #file = open(f'{src_path}{row[0]}.jpg', 'r')
                    ziph.write(os.path.join(root, f'{src_path}{row[0]}.jpg'),
                            os.path.relpath(os.path.join(root, f'{row[0]}.jpg'),
                                os.path.join(src_path, '..')
                                )
                            )


def main():
    assert(len(sys.argv) == 5), \
        'Usage: python sample_data.py [SOURCE_DIR] [DEST_DIR] ["COMMA,SEPARATED,LABELS"] [SAMPLE_SIZE]'
    src_dir = sys.argv[1]+'/'
    dest_dir = sys.argv[2]+'/'
    labels = sys.argv[3].split(',')
    sample_size = int(sys.argv[4])
    print(sample_size)
    # Loop through the labels and process associated train and test samples
    for label in labels:
        sample_train_df = sample_data(f'{src_dir}/ImageSets/Main/{label}_train.txt',
                columns=['id','is_present'],
                n=sample_size,
                delimiter=' ',
                )
        extract_annotations_list(dest_dir, label, sample_train_df)
        # Todo make a .zip of all the images in format for Matroid detector training (CoCo)
        #zipdir(f'{src_dir}JPEGImages/', f'{dest_dir}{label}_train.zip', sample_train_df)

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

