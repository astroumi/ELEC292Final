from preprocessing import *
from split import *

init_hdf5()
preprocess_data()
split_all('hdf')
isolate_test_splits()

# print_h5_tree(h5_path)
# features_train_scaled, labels_train_scaled, features_test_scaled, labels_test_scaled = extract_and_normalize()


#love kip<3