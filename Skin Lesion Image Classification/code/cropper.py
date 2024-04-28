import numpy as np
import matplotlib.image as mpimg
import tensorflow_addons as tfa
import constants
import pandas as pd
import typing

class Cropper:
    def __init__(self):
        pass

    def crop_training(self):
        y_train = pd.read_csv(constants.get_ground_truth_file_path())
        all_images = y_train['image'].tolist()
        all_images.sort()

        print("Cropping. Progress bar (every 100 images): ", end="")
        number_cropped = 0
        for image_id in all_images:
            try:
                self._crop_then_save_image(image_id)
            except Exception as e:
                print(f"Received exception; please fix file then continue: {e}")
                input("Continue?")
                self._crop_then_save_image(image_id)
            number_cropped += 1
            if number_cropped % 10 == 99:
                print("*", end="")

        print(f"Done cropping all images. Cropped Path {constants.get_cropped_path()}")

    def _crop_then_save_image(self, image_id):
        image_file = typing.cast(str, image_id) + ".jpg"
        image_path = "/".join([constants.get_training_path(), image_file])
        img = mpimg.imread(image_path)
        cropped_image = self._crop_image(img)
        cropped_image_path =  "/".join([constants.get_cropped_path(), image_file])
        mpimg.imsave(cropped_image_path, cropped_image)

    def _crop_image(self, imagefile):
        if not self._has_black_circle(imagefile):
            return imagefile

        sliced_imagefile = imagefile[2:-2, 2:-2, :]
        blurred_imagefile = tfa.image.gaussian_filter2d(sliced_imagefile, filter_shape=(2, 2))

        dark_threshold = 20  # anything below this value is "black"
        dark_mask = np.all(blurred_imagefile <= dark_threshold, axis=2)

        light_pixels = np.argwhere(dark_mask==False)
        box = (
            (
                light_pixels[:, 0].min(),  # top-most
                light_pixels[:, 0].max(),  # bottom-most
            ),
            (
                light_pixels[:, 1].min(),  # left-most
                light_pixels[:, 1].max(),  # right-most
            )
        )
        cropped_imagefile = sliced_imagefile[
            box[0][0]:box[0][1]+1,
            box[1][0]:box[1][1]+1,
            :
        ]

        trim_fraction = 0.02  # trim additional 2 percent from each edge
        trim_height, trim_width, _ = [s * 0.05 for s in cropped_imagefile.shape]
        trim_height = int(trim_height)
        trim_width = int(trim_width)

        trimmed_imagefile = cropped_imagefile[
            trim_height:-trim_height,
            trim_width:-trim_width,
            :
        ]

        return trimmed_imagefile

    def _has_black_circle(self, imagefile, diff_threshold=90):
        """Detector for if a black circle exists in image.

        Use average then figure out the difference

        Split into 9 rectangles, then compare inner rectangle vs the rest.

        diff_threshold: if difference in mean is greater than this number, mark as positive."""

        shape = imagefile.shape
        inner_fraction = 0.60
        outer_fraction = 0.20
        inner_start = (1 - inner_fraction) / 2
        inner_end = 1 - inner_start

        inner_section = imagefile[
            int(shape[0] * inner_start): int(shape[0] * inner_end),
            int(shape[1] * inner_start): int(shape[1] * inner_end),
            :
        ]
        outer_section_shape = int(shape[0] * outer_fraction), int(shape[1] * outer_fraction)
        outer_sections = [
            imagefile[:outer_section_shape[0], :outer_section_shape[1], :],
            imagefile[-outer_section_shape[0]:, :outer_section_shape[1], :],
            imagefile[:outer_section_shape[0], -outer_section_shape[1]:, :],
            imagefile[-outer_section_shape[0]:, -outer_section_shape[1]:, :],
        ]

        inner_mean = inner_section.mean()
        outer_mean = np.mean([section.mean() for section in outer_sections])
        diff = inner_mean - outer_mean

        return diff >= diff_threshold


    def load_image_by_id(id:str, path:str):
        """Returns image file object."""
        label = get_label_of_image_id([id], text_label=True).tolist()[0]

        # Read Images
        img = mpimg.imread("/".join([dir_name, subdir, label, id + "." + image_format]))

        return img
