import os
import pandas as pd
import matplotlib.image as mpimg
import numpy as np
from PIL import Image

DATA_DIR = "isic_data"
BASE_URL = "https://isic-challenge-data.s3.amazonaws.com/2019/"

# Training
TRAINING_ZIP = "ISIC_2019_Training_Input.zip"
TRAINING_DIR = "ISIC_2019_Training_Input"
TRAINING_AUGMENTED = "ISIC_2019_Training_Augmented"
TRAINING_GROUND_TRUTH_CSV = "ISIC_2019_Training_GroundTruth.csv"
TRAINING_CROPPED_DIR = "ISIC_2019_Training_Cropped"
TRAINING_SPLIT = "Training_Split"
TRAINING_SPLIT_MANIFEST = TRAINING_SPLIT + "/training_split.csv"

# Validation
VALIDATION_SPLIT = "Validation_Split"
VALIDATION_SPLIT_CLASS = "Validation_Split_class"
VALIDATION_SPLIT_MANIFEST = VALIDATION_SPLIT + "/validation_split.csv"

# Test
TEST_ZIP = "ISIC_2019_Test_Input.zip"
TEST_SPLIT = "Test_Split"
TEST_SPLIT_CLASS = "Test_Split_class"
TEST_SPLIT_MANIFEST = TEST_SPLIT + "/test_split.csv"

## Metadata 
# Training 
TRAINING_METADATA_CSV = "ISIC_2019_Training_Metadata.csv"
# Test
TEST_METADATA_CSV = "ISIC_2019_Test_Metadata.csv"


def get_training_path():
    """This is ISIC's 'Training' dataset, which has labels. Will be split
    into our own training, validation, and test sets later."""
    path = "/".join([DATA_DIR, TRAINING_DIR])
    return path

def get_testing_split_path():
    """Note: this is split from ISIC's 'training' set, not 'test' set, and
    hence, has labels. Images in here should already be cropped.

    Individual class directories: False
    """
    path = "/".join([DATA_DIR, TEST_SPLIT])
    _create_if_needed(path)
    return path

def get_testing_split_class_path():
    """Images in here should already be cropped.

    Individual class directories: True
    """
    path = "/".join([DATA_DIR, TEST_SPLIT_CLASS])
    _create_if_needed(path)
    return path

def get_training_split_path():
    """Images in here should already be cropped.

    Individual class directories: False
    """
    path = "/".join([DATA_DIR, TRAINING_SPLIT])
    _create_if_needed(path)
    return path

def get_validation_split_path():
    """Images in here should already be cropped.

    Individual class directories: False
    """
    path = "/".join([DATA_DIR, VALIDATION_SPLIT])
    _create_if_needed(path)
    return path

def get_validation_split_class_path():
    """Images in here should already be cropped.

    Individual class directories: True
    """
    path = "/".join([DATA_DIR, VALIDATION_SPLIT_CLASS])
    _create_if_needed(path)
    return path

def get_testing_split_manifest_path():
    path = "/".join([DATA_DIR, TEST_SPLIT])
    _create_if_needed(path)
    return "/".join([DATA_DIR, TEST_SPLIT_MANIFEST])

def get_training_split_manifest_path():
    path = "/".join([DATA_DIR, TRAINING_SPLIT])
    _create_if_needed(path)
    return "/".join([DATA_DIR, TRAINING_SPLIT_MANIFEST])

def get_validation_split_manifest_path():
    path = "/".join([DATA_DIR, VALIDATION_SPLIT])
    _create_if_needed(path)
    return "/".join([DATA_DIR, VALIDATION_SPLIT_MANIFEST])

def get_training_augmented_path():
    """Images in here should already be cropped AND augmented.

    Individual class directories: True
    """
    path = "/".join([DATA_DIR, TRAINING_AUGMENTED])
    _create_if_needed(path)
    return path

def get_training_augmented_path_with_count_suffix(count:int):
    """Images in here should already be cropped AND augmented.

    count will be used a suffix in the path
    """
    path = "/".join([DATA_DIR, TRAINING_AUGMENTED])
    path = path + f'_{count}'
    _create_if_needed(path)
    return path

def get_ground_truth_file_path():
    """This is ISIC ground truth file, which covers all 3 of our splits."""
    path = "/".join([DATA_DIR, TRAINING_GROUND_TRUTH_CSV])
    _create_if_needed(path)
    return path

def get_training_metadata_file_path():
    """This is training metadata file."""
    path = "/".join([DATA_DIR, TRAINING_METADATA_CSV])
    return path

def get_test_metadata_file_path():
    """This is test metadata file."""
    path = "/".join([DATA_DIR, TEST_METADATA_CSV])
    return path


def get_cropped_path():
    """Individual class directories: False"""
    path = "/".join([DATA_DIR, TRAINING_CROPPED_DIR])
    _create_if_needed(path)
    return path

def load_training_metadata():
    return pd.read_csv(get_training_metadata_file_path())


def load_all_ground_truth_data():
    return pd.read_csv(get_ground_truth_file_path())

def load_training_ground_truth_data():
    y_train = pd.read_csv(get_ground_truth_file_path())
    training_files = os.listdir(get_training_split_path())
    training_files = [image_file.rsplit('.', 1)[0] for image_file in training_files]
    y_train = y_train[y_train['image'].isin(training_files)]
    y_train = y_train.drop(columns=['UNK'])

    return y_train.to_numpy()


def load_training_split_data_with_labels(limit:int=-1, resize:(int, int)=(244,244)):
    """
    Load Splitted Training Data
    
    Limit is the number of images to return. Default is -1, load all
    resize used to resize the returned images 
    
    returns X_train and Y_train in np.Array format"""
    
    return _load_split_data_with_labels(path=get_training_split_path(), limit=limit, resize=resize)

def load_validation_split_data_with_labels(limit:int=-1, resize:(int, int)=(244,244)):
    """
    Load Splitted Validation Data
    
    Limit is the number of images to return. Default is -1, load all
    resize used to resize the returned images 
        
    returns X_val and Y_val in np.Array format"""
    
    return _load_split_data_with_labels(path=get_validation_split_path(), limit=limit, resize=resize)

def load_testing_split_data_with_labels(limit:int=-1, resize:(int, int)=(244,244)):
    """
    Load Splitted Test Data
     
    Limit is the number of images to return. Default is -1, load all
    resize used to resize the returned images 
        
    returns X_test and Y_test in np.Array format"""
    
    return _load_split_data_with_labels(path=get_testing_split_path(), limit=limit, resize=resize)


def _load_split_data_with_labels(path, limit:int, resize:(int, int)):
    y = pd.read_csv(get_ground_truth_file_path())
    files = os.listdir(path)
    image_names = [image_file.rsplit('.', 1)[0] for image_file in files]
    y = y[y['image'].isin(image_names)]
    y = y.drop(columns=['UNK'])

    x_out = list()
    y_out = list()

    for image_file in files:
        if not image_file.endswith('.jpg'):
            continue 
            
        if limit > 0 and len(x_out) >= limit:
            break
        image_path = "/".join([path, image_file])
        img = Image.open(image_path)
        img = img.resize(resize)
        x_out.append(np.asarray(img))

        temp = y[y.image == image_file.rsplit('.', 1)[0]]
        temp = temp.drop(columns=['image'])
        temp = temp.to_numpy()
        y_out.append(temp)

    return np.array(x_out), np.array(y_out)

def _create_if_needed(path):
    if not os.path.exists(path):
        os.mkdir(path)
