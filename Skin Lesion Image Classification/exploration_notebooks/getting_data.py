"""To download ISIC 2019 dataset. Uses multithreading."""
import glob
import os
import shutil
import typing
import requests
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd

prefix = "https://isic-challenge-data.s3.amazonaws.com/2019/"
file_names = [
    "ISIC_2019_Training_Input.zip",
    "ISIC_2019_Training_Metadata.csv",
    "ISIC_2019_Training_GroundTruth.csv",
    "ISIC_2019_Test_Input.zip",
    "ISIC_2019_Test_Metadata.csv",
]
zipped_fnames = [f for f in file_names if f.endswith(".zip")]

dir_name = "isic_data"
if not os.path.exists(dir_name + "/"):
    os.mkdir(dir_name)

subdir_name = "images"
image_format = "jpg"

# This following will take a long time. Download file in chunks to not kill memory.

def download_file(url, file_name):
    try:
        response = requests.get(url, stream=True)
        file = open(file_name, "wb")
        for chunk in response.iter_content(chunk_size=1024):
            file.write(chunk)
        return response.status_code
    except requests.exceptions.RequestException as e:
        return e

def download_all_files():
    threads= []
    with ThreadPoolExecutor(max_workers=20) as executor:
        for file_name in file_names:
            threads.append(
                executor.submit(
                    download_file,
                    prefix + file_name,
                    dir_name + "/" + file_name,
                )
            )

        for task in as_completed(threads):
            print(task.result())

def unzip_files():
    for zfname in zipped_fnames:
        with zipfile.ZipFile(dir_name + "/" + zfname, 'r') as handle:
            with ThreadPoolExecutor(100) as exe:
                _ = [exe.submit(handle.extract, m, dir_name + "/") for m in handle.namelist()]



def move_train_images_into_subdir():
    """Move images into subdirs only for training data"""
    # Get y_train label data to organize image files into subdirectories
    y_train = pd.read_csv("/".join([dir_name, "ISIC_2019_Training_GroundTruth.csv"]))

    train_dir = "ISIC_2019_Training_Input"
    classlist: typing.List[str] = y_train.columns.tolist()
    classlist.remove('image')

    for skin_class in classlist:  # MEL, NV, BCC etc
        if skin_class == "UNK":
            continue  # Don't process this one

        images_subdir = "/".join([dir_name, train_dir, skin_class])
        if not os.path.exists(images_subdir):
            os.mkdir(images_subdir)

        for image_id in y_train[y_train[skin_class]==1]["image"].tolist():
            image_file = typing.cast(str, image_id) + ".jpg"
            shutil.copy(
                "/".join([dir_name, train_dir, image_file]),
                "/".join([dir_name, train_dir, skin_class, image_file]),
            )

def delete_zip_files():
    for zfname in zipped_fnames:
        if os.path.exists(dir_name + zfname):
            os.remove(dir_name + zfname)


if __name__ == "__main__":
    print("Downloading")
    download_all_files()
    print("Unzipping")
    unzip_files()
    print("Unzipping successful, deleting zipped files")
    delete_zip_files()
