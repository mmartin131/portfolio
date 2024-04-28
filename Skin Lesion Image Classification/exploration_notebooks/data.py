"""Quick import of pandas DataFrames of our non-image data."""
import enum
import pandas as pd

dir_name = "../isic_data"

class SkinClass(enum.Enum):
    MEL = 0
    NV = 1
    BCC = 2
    AK = 3
    BKL = 4
    DF = 5
    VASC = 6
    SCC = 7
    # UNK = 8

metadata_train = pd.read_csv("/".join([dir_name, "ISIC_2019_Training_Metadata.csv"]))
metadata_test = pd.read_csv("/".join([dir_name, "ISIC_2019_Test_Metadata.csv"]))
y_train = pd.read_csv("/".join([dir_name, "ISIC_2019_Training_GroundTruth.csv"]))

def y_train_undersampled():
    try:
        return pd.read_csv("/".join([dir_name, "ISIC_2019_Training_GroundTruth_undersampled.csv"]))
    except:
        return None

def y_train_playground():
    try:
        return pd.read_csv("/".join([dir_name, "ISIC_2019_Training_GroundTruth_playground.csv"]))
    except:
        return None

y_test = pd.read_csv("/".join([dir_name, "ISIC_2019_Test_Metadata.csv"]))
