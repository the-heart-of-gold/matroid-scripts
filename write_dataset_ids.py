import os


def write_dataset_ids():
    # assign directory
    dir = '../data/youtube_bb/Annotations'

    with open('../data/youtube_bb/dataset_ids/youtube_bb.txt', 'a') as out:
        # iterate over files in that directory
        for filepath in os.scandir(dir):
            if filepath.is_file():
                out.write(os.path.splitext(os.path.basename(filepath))[0] + '\n')
                # print(os.path.splitext(os.path.basename(filepath))[0])


if __name__ == '__main__':
    write_dataset_ids()
