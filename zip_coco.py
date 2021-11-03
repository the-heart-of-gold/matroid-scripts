import os
import json
import shutil
import pathlib
import zipfile

root_dir = '../data/'
parent_name = 'knife'
datasets = [f'{parent_name}_test', f'{parent_name}_train', f'{parent_name}_trainval', ]
#datasets = ['youtube_bb_test', 'youtube_bb_train', 'youtube_bb_trainval', ]


def copy_images():
    images_dir = '../../youtube-bb/voc-decodes/youtubebbdevkit2017/youtubebb2017/JPEGImages/'
    for dataset in datasets:
        dst = f'{root_dir}{parent_name}/output/'
        with open(f'{dst}coco_{dataset}.json', 'r') as f:
            coco_json = json.load(f)
            images = coco_json['images']
            for image in images:
                shutil.copy2(f'{images_dir}{image["file_name"]}', f'{dst}{dataset}/data/')


def zip_dir(zip_dir, filename):
    """Zip the provided directory without navigating to that directory using `pathlib` module"""

    # Convert to Path object
    zip_dir = pathlib.Path(zip_dir)

    with zipfile.ZipFile(filename, "w", zipfile.ZIP_STORED) as zip_file:
        for entry in zip_dir.rglob("*"):
            zip_file.write(entry, entry.relative_to(zip_dir))


if __name__ == '__main__':
    #copy_images()
#    for dataset in datasets:
#        zip_dir(f'{root_dir}{parent_name}/output/{dataset}/', f'{root_dir}{parent_name}/{dataset}.zip')
        zip_dir(f'../../youtube-bb/data/all/class-decodes-absents/yt_bb_classification_train/12/', f'{root_dir}{parent_name}/not_knife.zip')
