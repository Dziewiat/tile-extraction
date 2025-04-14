## Downloading
Downloads Whole Slide Images (WSI) files from https://portal.gdc.cancer.gov by patient ID.

## Tiling
Extracts tiles from WSI (uses https://github.com/KatherLab/preprocessing-ng project).

#### Usage
python download_and_tile_WSI.py PATIENT_FILE_PATH -o OUTPATH <flags>

PATIENT_FILE_PATH is a file containing patient IDs.
    
Input Variable name | Description
--- | --- 
-o or --outdir | Path to the output folder where tiles are saved
--tile_size | The size of the output tiles in pixels, default int 224
--um_per_tile| Size each tile spans in µm, default float 256.0
--brightness-cutoff | Brightness past which tiles are rejected as background, default int 224
-f or --force | Overwrite existing tile
--no-canny | Disable rejection of edge tiles. Useful for TMAs / sparse slides.


## Normalization
Normalize extracted tiles using https://github.com/KatherLab/preProcessing normalization script.

#### Usage
python normalize_tiles.py RAW_PATH -n NORMALIZED_PATH

RAW_PATH is the directory where the patient tile folders are stored.

Input Variable name | Description
--- | --- 
-n or --normalized-DIR | Path to the output folder where normalized tiles are saved, default 'normalized_tiles'
--unzip | Unzip the raw tiles dataset if it is in a .zip format


## Sorting
Sort normalized tile folders into categories (MSI/MSS) based on provided mapping file ('liu.csv').

#### Usage
python sort_tiles.py SOURCE_PATH -d DATASET_PATH

SOURCE_PATH is the directory where the normalized patient tile folders are stored.

Input Variable name | Description
--- | --- 
-d or --dataset-dir | Path to the output folder where the sorted dataset is saved, default 'dataset'


## Example Usage Pipeline

#### Download and tile

    python download_and_tile_WSI.py patient_ids.txt -o tiles

#### Normalize

    python normalize_tiles.py tiles -n normalized_tiles

#### Sort

    python sort_tiles.py normalized_tiles -d dataset
