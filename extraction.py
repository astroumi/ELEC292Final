import h5py
import pandas as pd
import numpy as np

from hdf import h5_path, appdata_dir

#Calculates 10 features of a 5-second segment
#Takes in a numpy array of [Time, X, Y, Z, Magnitude]
#Returns a list of features
def extract_features(data):
    #Extract features from the magnitude
    mag = pd.Series(data[:, 4])

    centered_mag = mag - mag.mean()
    zcr = ((centered_mag[:-1].values * centered_mag[1:].values) < 0).sum()

    features = {
        'mean': mag.mean(),
        'max': mag.max(),
        'min': mag.min(),
        'range': mag.max() - mag.min(),
        'variance': mag.var(),
        'std_dev': mag.std(),
        'skewness': mag.skew(),  # Built-in Pandas Skew
        'kurtosis': mag.kurt(),  # Built-in Pandas Kurtosis
        'rms': np.sqrt((mag ** 2).mean()),
        'zcr': zcr
    }
    return list(features.values())

# Extracts features from magnitude, x, y and z
def extract_mxyz(data):
    #Extract features from the magnitude
    mag = pd.Series(data[:, 4])
    x = pd.Series(data[:, 1])
    y = pd.Series(data[:, 2])
    z = pd.Series(data[:, 3])

    centered_mag = mag - mag.mean()
    centered_x = x - x.mean()
    centered_y = y - y.mean()
    centered_z = z - z.mean()
    zcr_x = ((centered_x[:-1].values * centered_x[1:].values) < 0).sum()
    zcr_y = ((centered_y[:-1].values * centered_y[1:].values) < 0).sum()
    zcr_z = ((centered_z[:-1].values * centered_z[1:].values) < 0).sum()
    zcr_m = ((centered_mag[:-1].values * centered_mag[1:].values) < 0).sum()

    features = {
        #mag features
        'mean': mag.mean(),
        'max': mag.max(),
        'min': mag.min(),
        'range': mag.max() - mag.min(),
        'variance': mag.var(),
        'std_dev': mag.std(),
        'skewness': mag.skew(),  # Built-in Pandas Skew
        'kurtosis': mag.kurt(),  # Built-in Pandas Kurtosis
        'rms': np.sqrt((mag ** 2).mean()),
        'zcr_mag': zcr_m,

        #x features
        'mean_x': x.mean(),
        'max_x': x.max(),
        'min_x': x.min(),
        'range_x': x.max() - x.min(),
        'variance_x': x.var(),
        'std_dev_x': x.std(),
        'skewness_x': x.skew(),  # Built-in Pandas Skew
        'kurtosis_x': x.kurt(),  # Built-in Pandas Kurtosis
        'rms_x': np.sqrt((x ** 2).mean()),
        'zcr_x': zcr_x,

        # y features
        'mean_y': y.mean(),
        'max_y': y.max(),
        'min_y': y.min(),
        'range_y': y.max() - y.min(),
        'variance_y': y.var(),
        'std_dev_y': y.std(),
        'skewness_y': y.skew(),  # Built-in Pandas Skew
        'kurtosis_y': y.kurt(),  # Built-in Pandas Kurtosis
        'rms_y': np.sqrt((y ** 2).mean()),
        'zcr_y': zcr_y,

        # z features
        'mean_z': z.mean(),
        'max_z': z.max(),
        'min_z': z.min(),
        'range_z': z.max() - z.min(),
        'variance_z': z.var(),
        'std_dev_z': z.std(),
        'skewness_z': z.skew(),  # Built-in Pandas Skew
        'kurtosis_z': z.kurt(),  # Built-in Pandas Kurtosis
        'rms_z': np.sqrt((z ** 2).mean()),
        'zcr_z': zcr_z

    }
    return list(features.values())

# Loops through the split datasets and extracts features
def run_extraction(mode="mag"):
    global features_path
    #Initialize variables for feature list and label list for testing and training
    test_features = []
    test_labels = []

    train_features = []
    train_labels = []

    # print(f"INFO: Starting feature extraction (Mode: {mode})...")

    with h5py.File(h5_path, 'r') as hdf:
        #Start at the top of the Split_Group
        split_group = hdf['Split_Data']

        #Loop through training and testing
        for split_type in split_group.keys():
            type_group = split_group[split_type]

            #Loop through walking and jumping
            for activity in type_group.keys():
                activity_group = type_group[activity]

                #Loop through every 5 second file
                for filename in activity_group.keys():
                    # Pull the actual data array
                    data = activity_group[filename][:]

                    # Extract features depending on mode
                    if mode == 'mag':
                        feature_row = extract_features(data)
                    elif mode == 'xyz_mag':
                        feature_row = extract_mxyz(data)

                    #Set label as 0 if walking and 1 if jumping
                    label = 0 if activity == 'walking' else 1

                    #Check what split type it is
                    if split_type == 'training':
                        train_features.append(feature_row)
                        train_labels.append(label)
                    if split_type == 'testing':
                        test_features.append(feature_row)
                        test_labels.append(label)



    #Convert the features and labels list into numpy arrays
    features_train = np.array(train_features)
    labels_train = np.array(train_labels)
    features_test = np.array(test_features)
    labels_test = np.array(test_labels)

    features_path = appdata_dir / f'extracted_features.npz'

    # Save the extracted features to disk
    np.savez(features_path,
             X_train=features_train, y_train=labels_train,
             X_test=features_test, y_test=labels_test)

    print(f"INFO: Feature extraction complete, saved to disk. (Mode: {mode})")
    return 0