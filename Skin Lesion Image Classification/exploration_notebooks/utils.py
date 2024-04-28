"""Basic helper functions."""
import copy
import os
import random
import shutil
import typing

import numpy as np
import pandas as pd
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import tensorflow as tf

import data

dir_name = "../isic_data"
subdir_name = "images"
image_format = "jpg"


def load_train_data(count: int = 100, ignore_sampled: bool = True):
    y_train_all = data.y_train.sort_values(by='image', ascending=True)
    x_train = list()
    y_train = list()

    if ignore_sampled:
        y_train_all = y_train_all[y_train_all["image"].str.contains("wnsampled") == False]

    base_shape = (768, 1024, 3)

    for i, row in y_train_all.iterrows():
        if len(x_train) >= count:
            break

        image = get_image_by_id(row['image'], dataset="train")

        if image.shape != base_shape:
            # Skip all images that doesn't have the same shape
            continue

        x_train.append(image)
        y_train.append(row)

    return np.asarray(x_train), np.asarray(y_train)


def load_images(count: int = 100, dataset: str = "train"):
    subdir = os.path.join(dir_name, _get_subdir_name(dataset))
    all_imagefile_paths = [
        f for f in os.listdir(subdir)
        if os.path.isfile(os.path.join(subdir, f))
           and f.endswith("." + image_format)
    ]
    all_imagefile_paths.sort()
    all_imagefile_paths = all_imagefile_paths[:count]

    return np.asarray([mpimg.imread("/".join([subdir, x])) for x in all_imagefile_paths])


def shuffle(x_train, y_train, seed: int = 0):
    np.random.seed(seed)  # For reproducibility

    indices = np.arange(x_train.shape[0])
    shuffled_indices = np.random.permutation(indices)
    return x_train[shuffled_indices], y_train[shuffled_indices]


def get_random_image_id(
        random_seed: typing.Optional[int] = None, dataset: str = "train"
):
    subdir = os.path.join(dir_name, _get_subdir_name(dataset))
    all_imagefile_paths = [
        f for f in os.listdir(subdir)
        if os.path.isfile(os.path.join(subdir, f))
           and f.endswith("." + image_format)
    ]
    random.seed(random_seed)
    img_idx = random.randrange(len(all_imagefile_paths))
    return all_imagefile_paths[img_idx].strip("." + image_format)


def get_random_image_ids(
        size: int,
        random_seed: typing.Optional[int] = None,
        dataset: str = "train",
):
    subdir = os.path.join(dir_name, _get_subdir_name(dataset))
    all_imagefile_paths = list()
    for class_dir in data.SkinClass.__members__.keys():
        all_imagefile_paths = all_imagefile_paths + [
            f for f in os.listdir(os.path.join(subdir, class_dir))
            if os.path.isfile(os.path.join(subdir, class_dir, f))
            and f.endswith("." + image_format)
        ]
    all_imagefile_paths = sorted(all_imagefile_paths)
    np.random.seed(random_seed)
    img_idxs = np.random.choice(range(0, len(all_imagefile_paths)), size, replace=False)
    return sorted(
        [all_imagefile_paths[img_idx].strip("." + image_format) for img_idx in img_idxs]
    )


subdir_dict = {
    "train": {"path": "ISIC_2019_Training_Input", "y": data.y_train},
    "test": {"path": "ISIC_2019_Training_Input", "y": NotImplemented},
    "undersampled": {"path": "undersampled", "y": data.y_train_undersampled()},
    "playground": {"path": "playground", "y": data.y_train_playground()},
}

def _get_subdir_name(dataset: str = "train"):
    subdir_data = subdir_dict.get(dataset)
    if not subdir_data:
        raise ValueError(f"Invalid dataset choice {dataset}")
    return subdir_data.get("path")


def get_image_by_id(id: str, dataset: str = "train"):
    """Returns image file object."""
    subdir = _get_subdir_name(dataset)

    label = get_label_of_image_id([id], text_label=True).tolist()[0]

    # Read Images
    img = mpimg.imread("/".join([dir_name, subdir, label, id + "." + image_format]))

    return img


def plot_image(img: np.ndarray):
    return plt.imshow(img)


def plot_image_by_id(id: str, dataset: str = "train"):
    img = get_image_by_id(id, dataset)
    return plot_image(img)


def get_label_of_image_id(
    img_idxs: typing.List[str], text_label: bool = False
) -> pd.Series:
    """Only applicable to data in 'Training input' dataset."""
    labels = data.y_train.set_index("image", drop=True)
    subset_labels = labels.loc[img_idxs, :]
    ret = subset_labels.apply(
        lambda x: labels.columns.where(x == 1).dropna()[0],
        axis=1,
    )
    if not text_label:
        return ret.apply(lambda x: data.SkinClass[x].value)
    return ret


def select_subset_for_playground(n=100, random_seed=0, subset_from_dataset="undersampled"):
    """Set aside small set of images for playground."""
    source_dir = _get_subdir_name(subset_from_dataset)
    img_idxs = get_random_image_ids(n, random_seed=random_seed, dataset=subset_from_dataset)

    if not os.path.exists(playground_dir := ("/".join([dir_name, 'playground']))):
        os.mkdir(playground_dir)

    # Subdirectory needed -- subdir name is class name
    for skin_class in data.SkinClass._member_names_:
        if not os.path.exists(
                playground_subdir := ("/".join([dir_name, 'playground', skin_class]))
        ):
            os.mkdir(playground_subdir)

    train_labels = get_label_of_image_id(img_idxs, text_label=True)

    for img_idx in img_idxs:
        try:
            shutil.copyfile(
                "/".join([dir_name, source_dir, train_labels[img_idx], img_idx + '.' + image_format]),
                "/".join([dir_name, 'playground', train_labels[img_idx], img_idx + '.' + image_format]),
            )
        except TypeError as e:
            print(train_labels[img_idx])
            raise e

    # Separate metadata table just for playground
    y_train_playground = copy.copy(data.y_train)
    img_ids_to_get_rid = set(data.y_train["image"]) - set(img_idxs)

    y_train_playground.drop(
        index=[i for i, row in y_train_playground.iterrows() if row["image"] in img_ids_to_get_rid],
        inplace=True,
    )

    y_train_playground.to_csv("isic_data/ISIC_2019_Training_GroundTruth_playground.csv", index=False)


def load_tf_dataset(
    dataset="train",
    image_size=(244, 244),
    batch_size=1,
    random_seed=123,
    validation_split=0.2,
    subset="training",
):
    """Load tensorflow Dataset object with labels.

    Tip: get filepaths using `file_paths` attribute."""
    image_directory = dir_name + "/" + _get_subdir_name(dataset)
    if dataset == "test":
        image_ids = data.metadata_test.image.tolist()
    elif dataset in subdir_dict:
        image_ids = subdir_dict.get(dataset).get("y").image.tolist()
    else:
        raise ValueError("not a valid dataset choice")

    # Get list of training labels
    train_labels = get_label_of_image_id(sorted(image_ids), text_label=True).tolist()

    loaded_ds = tf.keras.utils.image_dataset_from_directory(
        image_directory,
        class_names=list(data.SkinClass.__members__.keys()),  # Not sorted
        validation_split=validation_split,
        subset=subset,
        seed=random_seed,
        image_size=image_size,  # default 256x256
        batch_size=batch_size,
        label_mode='categorical',
        shuffle=True,
    )
    # loaded_ds.class_names = list(data.SkinClass.__members__.keys())
    return loaded_ds

#### PREPROCESSING

def preprocess_layers():
    return [tf.keras.layers.Rescaling(1./255)]

def build_model(
    layers: typing.List[typing.Any],
    learning_rate=0.01,
    loss="categorical_crossentropy",
    metrics=["accuracy"],
):
    """Build a multi-class logistic regression model using Keras.

      Args:
        layers: layers between loaded dataset and output. Include preprocessing
            in here.
        learning_rate: The desired learning rate for SGD or Adam.

      Returns:
        model: A tf.keras model (graph).
    """
    tf.keras.backend.clear_session()
    np.random.seed(0)
    tf.random.set_seed(0)

    model = tf.keras.Sequential()
    for layer in layers:
        model.add(layer)

    optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)

    model.compile(
        loss=loss,
        optimizer=optimizer,
        metrics=metrics,
    )

    return model


def plot_history(history, metric="loss"):
    """Stolen from homework 9."""
    plt.ylabel(metric)
    plt.xlabel('Epoch')
    plt.xticks(range(0, len(history[metric] + 1)))
    plt.plot(history[metric], label="training", marker='o')
    plt.plot(history['val_' + metric], label="validation", marker='o')
    plt.legend()
    plt.show()

def plot_metrics(history):
    """From tf website, much better than our HW 9 version."""
    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    metrics = ['loss', 'accuracy', 'precision', 'recall']
    plt.figure(figsize=(10, 8))
    for n, metric in enumerate(metrics):
        name = metric.replace("_"," ").capitalize()
        plt.subplot(2,2,n+1)
        plt.plot(history.epoch, history.history[metric], color=colors[0], label='Train')
        plt.plot(history.epoch, history.history['val_'+metric],
                color=colors[0], linestyle="--", label='Val')
        plt.xlabel('Epoch')
        plt.ylabel(name)
        if metric == 'loss':
            plt.ylim([0, plt.ylim()[1]])
        elif metric == 'auc':
            plt.ylim([0.8,1])
        else:
            plt.ylim([0,1])

        plt.legend()