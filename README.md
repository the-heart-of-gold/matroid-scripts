# matroid-scripts
Some python scripts for pre-processing data for training Matroid detectors, and interacting with the Matroid API.

##Requirements
Python3 plus dependencies in requirements.txt

I recommend you use a virtual python environment, e.g. virtualenv or similar.

##Scripts
- sample_data.py: script to take 'detector' outputs from youtube_bb github repository and output CoCo.json formatted files for training new detectors.
- coco2bbox.py: script to take coco.json files and produce legacy Matroid bbox data format for training new detectors [obsolete]
- test_knife.py: 
- train_test_val.py:
- upload_to_s3.py: upload files/dirs to S3 buckets
- write_dataset_ids.py: write out a sample of image IDs to be used to train or test a new detector [obsolete now that sample_data.py does similar job, but better]
