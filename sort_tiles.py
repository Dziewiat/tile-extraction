import argparse
from pathlib import Path

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sort extracted WSI tiles into category directories.')
    parser.add_argument('source_dir', type=Path)
    parser.add_argument('-d', '--dataset-dir',
                        default='dataset',
                        type=Path)
    args = parser.parse_args()


import os
import shutil
import pandas as pd


def sort_folders_by_category(source_path: str, dest_path: str, mapping_series: pd.Series):
    '''Sort patient folders into corresponding directories by provided mapping.
    
        Arguments:
        source_dir - directory where the tiles are stored
        dest_path - path where to store the sorted dataset
        mapping_series - pandas Series object mapping patient IDs to category (MSI/MSS)
    '''
    for folder in os.listdir(source_path):
        folder_path = os.path.join(source_path, folder)
        patient_id = '-'.join(folder.split('-')[:3])

        if not os.path.isdir(folder_path):
            continue

        # Get category from mapping (if exists)
        category = mapping_series.get(patient_id)
        if category:
            category_dir = os.path.join(dest_path, category)
            os.makedirs(category_dir, exist_ok=True)

            target_path = os.path.join(category_dir, folder)
            print(f"Moving '{folder}' → '{category}/'")
            shutil.move(folder_path, target_path)
        else:
            print(f"⚠️ No category mapping found for folder '{folder}'")


def main(source_dir: str, dataset_dir: str):
    '''Sort patient folders into corresponding directories by provided mapping (liu.csv).
    
        Arguments:
        source_dir - directory where the tiles are stored
        dataset_dir - path where to store the sorted dataset
    '''
    # Load mapping series
    label_df = pd.read_csv('liu.csv')
    category_map = label_df.set_index('TCGA Participant Barcode')['MSI Status']

    # Treat MSS and MSI-L as MSS and MSI-H as MSI
    label_map = {
        'MSS': 'MSS',
        'MSI-L': 'MSS',
        'MSI-H': 'MSI'
    }
    category_map = category_map.map(label_map)

    # Move folders into respectful directories
    sort_folders_by_category(source_dir, dataset_dir, category_map)


if __name__ == '__main__':
    main(**vars(args))
