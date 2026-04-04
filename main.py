from preprocessing import *
from split import *

#############  Gets data ready for extraction, then training, then app run
init_hdf5()
preprocess_data()
split_all('hdf')
isolate_test_splits()
# reorganize_split_group_by_recording()
# print_h5_tree(h5_path)










#love kip<3