import os

import pandas as pd
import constants
import typing
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed

from skin_class import SkinClass

class Splitter:
    def __init__(self):
        pass

    def split_80_20(self):
        self._cleanup(constants.get_training_split_path())
        self._cleanup(constants.get_testing_split_path())

        df = pd.read_csv(constants.get_ground_truth_file_path())
        y_training = df.sample(frac=0.8, random_state=25)
        y_testing = df.drop(y_training.index)

        training_images = y_training['image'].tolist()
        testing_images = y_testing['image'].tolist()

        threads= []
        with ThreadPoolExecutor(max_workers=20) as executor:
            threads.append(
                executor.submit(
                    self._copy,
                    training_images,
                    constants.get_training_split_path(),
                ))
            threads.append(
                executor.submit(
                    self._copy,
                    testing_images,
                    constants.get_testing_split_path(),
                ))

        for task in as_completed(threads):
            task.result()

    def split_train_val_test(
        self, train: float = 0.72, validation: float = 0.08, test: float = 0.2
    ):
        if train + validation + test != 1:
            raise ValueError(f"Fractions don't add up to 1: {train=}, {validation=}, {test=}")

        self._cleanup(constants.get_training_split_path())
        self._cleanup(constants.get_testing_split_path())
        self._cleanup(constants.get_validation_split_path())

        random_seed = 25

        df = pd.read_csv(constants.get_ground_truth_file_path())
        y_train_and_val = df.sample(frac=train+validation, random_state=random_seed)
        y_validation = y_train_and_val.sample(
            frac=(validation/(train + validation)),
            random_state=random_seed,
        )
        y_training = y_train_and_val.drop(y_validation.index)
        y_testing = df.drop(y_train_and_val.index)

        training_images = y_training['image'].tolist()
        validation_images = y_validation['image'].tolist()
        testing_images = y_testing['image'].tolist()

        # Save csv into each split directory for records of what the directory has
        y_training.to_csv(constants.get_training_split_manifest_path(), index=False)
        y_validation.to_csv(constants.get_validation_split_manifest_path(), index=False)
        y_testing.to_csv(constants.get_testing_split_manifest_path(), index=False)

        threads= []
        with ThreadPoolExecutor(max_workers=20) as executor:
            threads.append(
                executor.submit(
                    self._copy,
                    training_images,
                    constants.get_training_split_path(),
                ))
            threads.append(
                executor.submit(
                    self._copy,
                    testing_images,
                    constants.get_testing_split_path(),
                ))
            threads.append(
                executor.submit(
                    self._copy,
                    validation_images,
                    constants.get_validation_split_path(),
                ))

        for task in as_completed(threads):
            task.result()

    def split_into_class_subdirectories(
        self,
        src_dir_path: str = constants.get_validation_split_path(),
        dest_dir_path: str = constants.get_validation_split_class_path(),
        manifest_path: str = constants.get_validation_split_manifest_path(),
    ):
        """From a directory that has no separation in skin classes, create
        a directory copy that has skin class separation (e.g. one directory
        for MEL, one for NV etc) for ease of loading into Tensorflow."""
        self._cleanup(dest_dir_path)
        constants._create_if_needed(dest_dir_path)

        df = pd.read_csv(manifest_path)
        classlist: typing.List[str] = df.columns.tolist()
        for c_to_remove in [c for c in classlist if c not in SkinClass.__members__]:
            classlist.remove(c_to_remove)

        for skin_class in classlist:  # MEL, NV, BCC etc
            if skin_class == SkinClass.UNK.name:
                print(f"Skipping {SkinClass.UNK.name}")
                continue  # Don't process this one

            class_subdir = "/".join([dest_dir_path, skin_class])

            if not os.path.exists(class_subdir):
                os.mkdir(class_subdir)

            all_images = df[df[skin_class]==1]["image"].tolist()

            all_images.sort()

            for image_id in all_images:
                image_file = typing.cast(str, image_id) + ".jpg"
                shutil.copy(
                    "/".join([src_dir_path, image_file]),
                    "/".join([class_subdir, image_file]),
                )

    def _copy(self, images, dest_poath):
         for image_id in images:
            image_file = typing.cast(str, image_id) + ".jpg"
            shutil.copy(
                "/".join([constants.get_cropped_path(), image_file]),
                "/".join([dest_poath, image_file]),
            )

    def _cleanup(self, path):
        try:
            print(f"Cleaning up {path}")
            shutil.rmtree(path)
        except OSError as e:
            print (f"Error: {e.strerror}")