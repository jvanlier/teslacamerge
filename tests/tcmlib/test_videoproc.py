from pathlib import Path
from tempfile import TemporaryDirectory

from tcmlib.loader import generate_latest_video_groups
import tcmlib.videoproc as victim


def test_merge(fixture_path_abs: Path):
    test_dir = "2020-06-02_09-10-25"

    vg = list(generate_latest_video_groups(fixture_path_abs / test_dir, 3))

    with TemporaryDirectory() as dest_dir_str:
        dest_dir = Path(dest_dir_str)
        victim.merge(vg, dest_dir, 1)

        out_file = (dest_dir / (test_dir + ".mp4"))
        assert out_file.is_file()
        assert out_file.stat().st_size > 0
