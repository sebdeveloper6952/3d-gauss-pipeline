import ffmpeg


def video_to_frames(input_path, output_dir, fps):
    (
        ffmpeg
        .input(input_path, ss=0, r=1)
        .filter('fps', fps='1/24')
        .output(f'{output_dir}/frame-%d.jpg', start_number=0)
        .overwrite_output()
        .run()
    )
