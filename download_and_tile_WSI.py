import argparse
from pathlib import Path

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract tiles from WSIs.')
    parser.add_argument('patient_file_path', type=Path)
    parser.add_argument('-o', '--outdir', type=Path)
    parser.add_argument(
        '--tile-size', type=int, default=224,
        help='Size of output tiles.')
    parser.add_argument(
        '--um-per-tile', type=float, default=256.,
        help='Microns covered by each tile.')
    parser.add_argument(
        '--brightness-cutoff', type=int, default=224,
        help='Brightness past which tiles are rejected as background.')
    parser.add_argument(
        '-f', '--force', action='store_true',
        help='Overwrite existing tile.')
    parser.add_argument(
        '--no-canny', dest='use_canny', action='store_false',
        help='Disable rejection of edge tiles. Useful for TMAs / sparse slides.')
    args = parser.parse_args()
    

import requests
import json
import os
import subprocess
import shutil
import sys
import logging


def get_svs_file_ids(patient_ids):
    url = "https://api.gdc.cancer.gov/files"
    headers = {"Content-Type": "application/json"}
    
    payload = {
        "filters": {
            "op": "and",
            "content": [
                {"op": "in", "content": {"field": "cases.submitter_id", "value": patient_ids}},
                {"op": "in", "content": {"field": "data_format", "value": ["SVS"]}},
                {"op": "in", "content": {"field": "experimental_strategy", "value": ["Diagnostic Slide"]}}
            ]
        },
        "fields": "file_id,file_name,cases.submitter_id",
        "format": "JSON",
        "size": "2000"
    }
    
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()
    
    return ([file["file_id"] for file in data.get("data", {}).get("hits", [])],  # return file UUID
            [file["file_name"] for file in data.get("data", {}).get("hits", [])])  # return file name

def download_svs_files(file_ids, file_names, save_dir="WSI"):
    os.makedirs(save_dir, exist_ok=True)
    
    for file_id, file_name in zip(file_ids, file_names):
        file_url = f"https://api.gdc.cancer.gov/data/{file_id}"
        response = requests.get(file_url, stream=True)
        response.raise_for_status()
        
        file_path = os.path.join(save_dir, file_name)  # TODO change filename
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        print(f"Downloaded: {file_path}")

def main(
        patient_file_path: Path, outdir: Path,
        tile_size: int = 224, um_per_tile: float = 256.,
        brightness_cutoff: int = 224, force: bool = False, use_canny: bool = True
        ) -> None:
    '''
    Download WSI slides from https://portal.gdc.cancer.gov/.
    Then extract tiles from .svs files.

    Args:
    cohort_path:  A folder containing whole slide images.
    outpath:  The output folder.
    tile_size:  The size of the output tiles in pixels.
    um_per_tile:  Size each tile spans in µm.
    force:  Overwrite existing tiles.
    '''
    logging.basicConfig(filename='logfile', level=logging.DEBUG)
    logging.getLogger().addHandler(logging.StreamHandler())

    # Load patient IDs from file
    patient_ids = []
    with open(patient_file_path, 'r') as f:
        for line in f:
            id = line.strip()
            patient_ids.append(id)

    # TILING PARAMETERS
    COHORT_PATH = 'WSI'
    os.makedirs(outdir, exist_ok=True)

    for patient_id in patient_ids:
        try:
            # Download slide image
            file_ids, file_names = get_svs_file_ids([patient_id])  # Get filenames one at a time
            print(f'Found files: {file_names}')
            print(f"Found {len(file_ids)} SVS files.")
            download_svs_files(file_ids, file_names, save_dir=COHORT_PATH)  # Download all records for the patient

            logging.info(f'{patient_id} slides succesfully downloaded.')

            # Tile the image
            tiling_args = [sys.executable, 'preprocessing-ng/tile.py', COHORT_PATH, '-o', outdir, '--tile-size', str(tile_size),
                           '--um-per-tile', str(um_per_tile), '--brightness-cutoff', str(brightness_cutoff)]
            print(tiling_args)
            if force:
                tiling_args.append('-f')
            if not use_canny:
                tiling_args.append('--no-canny')

            subprocess.run(tiling_args)

            # Delete the image dir
            shutil.rmtree(COHORT_PATH)

            logging.info(f'{patient_id} slides succesfully tiled.')
        
        except Exception as e:
            logging.exception(f'{patient_id}: {e}')



if __name__ == "__main__":
    main(**vars(args))
