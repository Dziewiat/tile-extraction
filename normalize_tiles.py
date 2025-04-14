import argparse
from pathlib import Path

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Normalize extracted WSI tiles.')
    parser.add_argument('raw_DIR', type=Path)
    parser.add_argument('-n', '--normalized-DIR',
                        default='normalized_tiles',
                        type=Path)
    parser.add_argument(
        '--unzip', dest='dataset_is_zip', action='store_true',
        help='Unzip the dataset.')
    args = parser.parse_args()


import os
import shutil
import subprocess

def unzip_dataset(zip_DIR: str, raw_DIR: str = 'raw'):
    '''Unzip dataset and move it to the 'raw' directory.
    
        zip_DIR - directory where the ZIP dataset is stored
        raw_DIR - destination directory to unzip files to
    '''
    # Unzip raw dataset
    for file in os.listdir(zip_DIR):
        if file.endswith('.zip'):
            zip_file_path = os.path.join(zip_DIR, file)
        else:
            continue

        shutil.unpack_archive(zip_file_path, raw_DIR)

    # Unzip slide tiles
    for file in os.listdir(zip_DIR):
        if file.endswith('.zip'):
            zip_file_path = os.path.join(zip_DIR, file)
        else:
            continue

        shutil.unpack_archive(zip_file_path, raw_DIR)
        os.remove(zip_file_path)


def normalize_slide_tiles(raw_DIR: str, normalized_DIR: str):
    '''Normalize extracted tiles.
    
        raw_DIR - directory where ALL raw patient tiles are stored
        normalized_DIR - directory to store all normalized patient tiles
    '''
    cmd = ['python', 'preProcessing/Normalize.py',
           '-ip', raw_DIR,
           '-op', normalized_DIR,
           '-si', 'preProcessing/normalization_template.jpg']
    subprocess.run(cmd)


def main(raw_DIR: str, normalized_DIR: str = 'normalized_tiles', dataset_is_zip: bool = False):
    '''Normalize extract tiles and optionally unzip the dataset before normalization.
    
        raw_DIR - directory where ALL raw patient tiles are stored
        output_DIR - directory to store all normalized patient tiles
        dataset_is_zip - set True if dataset is in a .zip format
    '''
    if dataset_is_zip:
        unzip_dataset(raw_DIR)
        raw_DIR = 'raw'

    os.makedirs(normalized_DIR, exist_ok=True)
    normalize_slide_tiles(raw_DIR, normalized_DIR)


if __name__ == "__main__":
    main(**vars(args))
