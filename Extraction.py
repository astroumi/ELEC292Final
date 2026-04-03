import h5py
import os
import pandas as pd

from hdf import *
from preprocessing import *
from sklearn.preprocessing import StandardScaler

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

#Initialize variables for feature list and label list for testing and training
test_features = []
test_labels = []

train_features = []
train_labels = []

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

                # Extract features
                feature_row = extract_features(data)

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

print("FEATURES TRAIN")
print(features_train)
print("LABLES TRAIN")
print(labels_train)
#Normalization
#Initialize the scaler
# scaler = StandardScaler()
#
# #Fit the scaler only the training data
# scaler.fit(features_train)
#
# #Normalize both sets using the training values
# #This is z-scoring the features
# features_train_scaled = scaler.transform(features_train)
# features_test_scaled = scaler.transform(features_test)
#
#     #Save the fitted scaler to disk
#     joblib.dump(scaler, 'scaler.pkl')
#
#     #Print to check that it worked
#     print("Normalization Completed")
#     print(f"Mean of first training feature after scaling: {features_train_scaled[:,0].mean():.2f}") # Should be ~0
#     print(f"Std of first training feature after scaling: {features_train_scaled[:,0].std():.2f}")  # Should be ~1
