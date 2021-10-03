import json
import pandas as pd


def main():
    with open('labels.json','r') as f:
        labels = json.load(f)
    data = {}

    # Categories
    categories = {}
    for category in labels['categories']:
        categories[category['id']] = category['name']

    # Grab annotations meatadata
    annotations = labels['annotations']
    for annotation in annotations:
        data[annotation['image_id']] = {}
        data[annotation['image_id']]['bbox_x'] = annotation['bbox'][0]
        data[annotation['image_id']]['bbox_y'] = annotation['bbox'][1]
        data[annotation['image_id']]['bbox_width'] = annotation['bbox'][2]
        data[annotation['image_id']]['bbox_height'] = annotation['bbox'][3]
        data[annotation['image_id']]['category_id'] = annotation['category_id']
        data[annotation['image_id']]['category'] = categories[annotation['category_id']]
        
    images = labels['images']
    for image in images:
        data[image['id']]['file_name'] = image['file_name']
        data[image['id']]['image_width'] = image['width']
        data[image['id']]['image_height'] = image['height']

    df = pd.DataFrame()
    df = pd.DataFrame.from_dict(data, orient='index')
    df['min_x'] = df['bbox_x'] / df['image_width']
    df['max_x'] = (df['bbox_x'] + df['bbox_width']) / df['image_width']
    df['min_y'] = df['bbox_y'] / df['image_height']
    df['max_y'] = (df['bbox_y'] + df['bbox_height']) / df['image_height']
    df['type'] = 'positive'
    df = df[['min_x','min_y','max_x','max_y','category','type','file_name']]
    df.to_csv('bbox.csv', header=False, index=False, encoding='utf-8',)


if __name__ == "__main__":
    main()

