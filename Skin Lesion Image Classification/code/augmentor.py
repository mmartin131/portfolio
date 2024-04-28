import math
import os
import random
import shutil
import typing
from concurrent import futures
from PIL import Image

import pandas as pd
import numpy as np
import matplotlib.image as mpimg
import tensorflow as tf

import constants
from skin_class import SkinClass

class Augmentor:
    def __init__(
        self,
        dir_path: typing.Optional[str] = None,
        manifest_path: typing.Optional[str] = None,
    ):
        """Augment and save augmented images to a new directory.

        dir_path: directory path to save augmented images to. If not supplied, uses
        default path."""
        self.dir_path = dir_path or constants.get_training_augmented_path()
        if not os.path.exists(self.dir_path + "/"):
            os.mkdir(self.dir_path)
        self.manifest_path = manifest_path or constants.get_training_split_manifest_path()
        # Get y_train label data to organize image files into subdirectories
        self.y_train = pd.read_csv(self.manifest_path)

    def simple_augmentation(self, count:int, skip_downsampled:bool=False):
        """Move images into subdirs only for training data. No augmentation;
        purely a subsetting action."""

        # Clean up first before we copy
        self._cleanup()
        constants._create_if_needed(self.dir_path)

        if skip_downsampled:
            print("Will filter downsampled images")

        classlist: typing.List[str] = self.y_train.columns.tolist()
        classlist.remove('image')

        for skin_class in classlist:  # MEL, NV, BCC etc
            if skin_class == SkinClass.UNK.name:
                print(f"Skipping {SkinClass.UNK.name}")
                continue  # Don't process this one

            class_subdir = "/".join([self.dir_path, skin_class])

            if not os.path.exists(class_subdir):
                os.mkdir(class_subdir)

            all_images = self.y_train[self.y_train[skin_class]==1]["image"].tolist()

            if skip_downsampled:
                all_images = list(filter(lambda val: (not val.endswith("_downsampled")), all_images))

            all_images.sort()
            all_images = all_images[:count]

            for image_id in all_images:
                image_file = typing.cast(str, image_id) + ".jpg"
                shutil.copy(
                    "/".join([constants.get_training_split_path(), image_file]),
                    "/".join([class_subdir, image_file]),
                )

            print(f"Done with subsetting class {skin_class}. It has {len(all_images)} images. Expected {count}")


            
    def get_numpy_data(self, resize:(int, int)=(244,244)):        
        class_dic = dict()
        class_dic[SkinClass.MEL.name]  = np.array([1, 0, 0, 0, 0, 0, 0, 0])
        class_dic[SkinClass.NV.name]   = np.array([0, 1, 0, 0, 0, 0, 0, 0])
        class_dic[SkinClass.BCC.name]  = np.array([0, 0, 1, 0, 0, 0, 0, 0])
        class_dic[SkinClass.AK.name]   = np.array([0, 0, 0, 1, 0, 0, 0, 0])
        class_dic[SkinClass.BKL.name]  = np.array([0, 0, 0, 0, 1, 0, 0, 0])
        class_dic[SkinClass.DF.name]   = np.array([0, 0, 0, 0, 0, 1, 0, 0])
        class_dic[SkinClass.VASC.name] = np.array([0, 0, 0, 0, 0, 0, 1, 0])
        class_dic[SkinClass.SCC.name]  = np.array([0, 0, 0, 0, 0, 0, 0, 1])
        
        classes_dir = os.listdir(self.dir_path)  
        x_out = list()
        y_out = list()
        
        for class_dir in classes_dir: 
            class_path = "/".join([self.dir_path, class_dir])
            class_images = os.listdir(class_path)  
            
            for image_file in class_images:
                image_path = "/".join([class_path, image_file])
                img = Image.open(image_path)
                img = img.resize(resize)
                x_out.append(np.asarray(img))

                temp = class_dic[class_dir]
                y_out.append(temp)

        return np.array(x_out), np.array(y_out)            

    def augment(self, count: int):
        """Move images into subdirs only for training data. Depending on number
        of images, the Augmentor either:
        - down sizes/subsets the directory if number of images >= `count`
        - generate new images via augmentation if number of images < `count`
        """

        # Clean up first before we copy
        self._cleanup()
        constants._create_if_needed(self.dir_path)

        classlist: typing.List[str] = self.y_train.columns.tolist()
        for c_to_remove in [c for c in classlist if c not in SkinClass.__members__]:
            classlist.remove(c_to_remove)

        threads= []
        with futures.ThreadPoolExecutor(max_workers=4) as executor:
            for skin_class in classlist:  # MEL, NV, BCC etc
                # self._subset_or_augment(count, skin_class)

                threads.append(
                    executor.submit(
                        self._subset_or_augment,
                        count,
                        skin_class,
                    )
                )

            for task in futures.as_completed(threads):
                task.result()



    def _subset_or_augment(self, count: int, skin_class: str):
        if skin_class == SkinClass.UNK.name:
            print(f"Skipping {SkinClass.UNK.name}")
            return  # Don't process this one

        print(f"Start processing class: {skin_class}")

        class_subdir = "/".join([self.dir_path, skin_class])

        if not os.path.exists(class_subdir):
            os.mkdir(class_subdir)

        all_images = self.y_train[self.y_train[skin_class]==1]["image"].tolist()

        # Find out how many images exist in this class
        if len(all_images) >= count:
            print(f"({skin_class}) --> {len(all_images)=}, {count=}, subsetting without augmentation.")
            # Down size with random sampling
            all_images.sort()
            random.seed(42)
            all_images = random.sample(all_images, count)
            all_images.sort()

            for image_id in all_images:
                image_file = typing.cast(str, image_id) + ".jpg"
                shutil.copy(
                    "/".join([constants.get_training_split_path(), image_file]),
                    "/".join([class_subdir, image_file]),
                )

            print(f"({skin_class}) --> Done with downsampling class {skin_class}.")

        else:
            print(f"({skin_class}) --> {len(all_images)=}, {count=}, augmenting up to required count.")
            # Calculate how many augmented images per original image
            multiplier = int(math.ceil(count / len(all_images)))
            total_copied = 0
            remaining_original_images = len(all_images)
            all_images.sort()
            for image_id in all_images:
                # First, copy over the original image
                image_file = typing.cast(str, image_id) + ".jpg"
                original_image_path = "/".join([constants.get_training_split_path(), image_file])
                shutil.copy(
                    original_image_path,
                    "/".join([class_subdir, image_file]),
                )
                total_copied += 1
                remaining_original_images -= 1

                # Then, augment as many times as needed
                img = [mpimg.imread(original_image_path)]
                for i in range(multiplier - 1):  # minus one because original image counts as 1
                    if total_copied + remaining_original_images >= count:
                        continue  # no need any more augmentation
                    # Create seed
                    random_seed = (total_copied, i)
                    img = tf.image.stateless_random_brightness(img, max_delta=5e-9, seed=random_seed)
                    img = tf.image.stateless_random_contrast(img, lower=0.8, upper=1.2, seed=random_seed)
                    # img = tf.image.stateless_random_crop
                    img = tf.image.stateless_random_flip_left_right(img, seed=random_seed)
                    img = tf.image.stateless_random_flip_up_down(img, seed=random_seed)
                    # img = tf.image.stateless_random_hue
                    # img = tf.image.stateless_random_jpeg_quality
                    img = tf.image.stateless_random_saturation(img, lower=0.8, upper=1.2, seed=random_seed)
                    img = tf.keras.layers.RandomRotation(0.5, seed=random_seed)(img).numpy()

                    # Make sure it's within bounds
                    img = np.maximum(0 * img, img)
                    img = np.minimum(0 * img + 255, img)

                    augmented_image_id = image_id + f"_aug_{i:02d}"
                    augmented_image_path =  "/".join([class_subdir, augmented_image_id + ".jpg"])
                    mpimg.imsave(augmented_image_path, img[0].astype("uint8"))

                    total_copied += 1

            print(f"({skin_class}) --> Done with augmenting class {skin_class}.")

    def _cleanup(self):
        try:
            print(f"Cleaning up {self.dir_path}")
            shutil.rmtree(self.dir_path)
        except OSError as e:
            print (f"Error: {e.strerror}")