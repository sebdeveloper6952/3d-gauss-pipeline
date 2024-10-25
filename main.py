import shutil
import urllib.request
import zipfile
from pathlib import Path
import enlighten
import pycolmap
from pycolmap import logging

def incremental_mapping_with_pbar(db_path, image_path, sfm_dir):
    num_images = pycolmap.Database(db_path).num_images
    with enlighten.Manager() as manager:
        with manager.counter(
            total=num_images, desc="Images registered:"
        ) as pbar:
            pbar.update(0, force=True)
            reconstructions = pycolmap.incremental_mapping(
                db_path,
                image_path,
                sfm_dir,
                initial_image_pair_callback=lambda: pbar.update(2),
                next_image_callback=lambda: pbar.update(1),
            )
    return reconstructions

def run():
    output_dir = Path("./output")
    image_dir = Path("./input")
    
    db_path = output_dir / "database.db"
    stereo_dir = output_dir / "stereo"
    sfm_dir = output_dir / "sfm"
    
    # first step, feature extract & match
    # this only writes to the database, there is no file output yet
    if db_path.exists():
        db_path.unlink()
    pycolmap.set_random_seed(0)
    pycolmap.extract_features(db_path, image_dir)
    pycolmap.match_exhaustive(db_path)

    # reconstruct image by image
    # writes output to sfm_dir, the output is
    recs = incremental_mapping_with_pbar(db_path, image_path, sfm_dir) 

    # dense reconstruction
    #pycolmap.undistort_images(stereo_path, output_path, image_dir)
    #pycolmap.patch_match_stereo(stereo_path)
    #pycolmap.stereo_fusion(stereo_path / "dense.ply", stereo_path)

if __name__ == "__main__":
    run()
