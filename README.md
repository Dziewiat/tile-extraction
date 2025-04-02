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
