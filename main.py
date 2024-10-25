from pathlib import Path
import enlighten
import pycolmap


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
    sfm_dir = output_dir / "0_sfm"
    undistort_dir = output_dir / "1_undistort"

    # first step, feature extract & match
    # this only writes to the database, there is no file output yet
    # if db_path.exists():
    #    db_path.unlink()
    pycolmap.set_random_seed(0)
    pycolmap.extract_features(
            db_path,
            image_dir,
            camera_model="SIMPLE_PINHOLE",
    )
    pycolmap.match_exhaustive(db_path)

    # reconstruct image by image
    # writes output to sfm_dir, the output is
    recs = incremental_mapping_with_pbar(db_path, image_dir, sfm_dir)
    print(recs)

    # undistort images writes to output/1_undistort
    pycolmap.undistort_images(undistort_dir, sfm_dir / "0", image_dir)

    # match stereo writes to output/1_undistort/stereo
    # it writes:
    pycolmap.patch_match_stereo(undistort_dir)
    # pycolmap.stereo_fusion(undistort_dir / "dense.ply", undistort_dir / "stereo")


if __name__ == "__main__":
    run()
