import pycolmap
from pathlib import Path

output_dir = Path("output/")
image_dir = Path("./input")
db_path = output_dir / "database.db"

mvs_path = output_path / "mvs"
database_path = output_path / "database.db"

pycolmap.extract_features(database_path, image_dir)
pycolmap.match_exhaustive(database_path)
maps = pycolmap.incremental_mapping(database_path, image_dir, output_path)
maps[0].write(output_path)

# dense reconstruction
pycolmap.undistort_images(mvs_path, output_path, image_dir)
pycolmap.patch_match_stereo(mvs_path)  # requires compilation with CUDA
pycolmap.stereo_fusion(mvs_path / "dense.ply", mvs_path)
