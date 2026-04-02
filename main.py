import h5py
import pandas as pd
import numpy as np
import os
import joblib
import matplotlib.pyplot as plt

from hdf import h5_path
from Extraction import extract_features, extract_and_normalize
from preprocessing import preprocessing
from visualization import *


features_train_scaled, labels_train_scaled, features_test_scaled, labels_test_scaled = extract_and_normalize()


#love kip<3