from preprocessing import *
from split import *

#############  Gets data ready for extraction, then training, then app run
init_hdf5()
preprocess_data()
split_all('hdf')
isolate_test_splits()
# reorganize_split_group_by_recording()
# print_h5_tree(h5_path)


while True:
    print("════════════════════════════════════")
    print(" ELEC 292 Project - Run Controller ")
    print("════════════════════════════════════")
    print("1. Run Data Processing Pipeline (Init, Preprocess, Split)")
    print("2. Extract Features & Train Model (magnitude only)")
    print("3. Launch Desktop App")
    print("4. Print HDF5 Tree")
    print("5. Exit")

    choice = input("\nSelect a run type (1-5): ")

    if choice == '1':
        run_data_pipeline()
    elif choice == '2':
        run_training()
    elif choice == '3':
        run_app()
    elif choice == '4':
        print("\n--- HDF5 Tree ---")
        print_h5_tree(h5_path)
        print("-----------------\n")
    elif choice == '5':
        print("Exiting... peace and love <3")
        sys.exit()
    else:
        print("Invalid choice. Please select 1-5.")







#love kip<3