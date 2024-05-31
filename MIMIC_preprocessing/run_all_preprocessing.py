import os
import json
import sys

# Get the current directory of the script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory (main directory)
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))

# Add the parent directory to the Python path
sys.path.append(parent_dir)


from MIMIC_preprocessing.timeseries import timeseries_main
from MIMIC_preprocessing.flat_and_labels import flat_and_labels_main
from eICU_preprocessing.split_train_test import split_train_test


with open('paths.json', 'r') as f:
    MIMIC_path = json.load(f)["MIMIC_path"]

if __name__=='__main__':
    print('==> Removing the stays.txt file if it exists...')
    try:
        os.remove(MIMIC_path + 'stays.txt')
    except FileNotFoundError:
        pass
    timeseries_main(MIMIC_path, test=False)
    flat_and_labels_main(MIMIC_path)
    split_train_test(MIMIC_path, is_test=False, MIMIC=True)