import logging
from pathlib import Path
from typing import Generator, Tuple

LOG = logging.getLogger(__name__)
MIN_VIDEOS_PER_EVENT = 4
DATE_PREFIX_LENGTH = 19


def parse_paths(src_str: str, dst_str: str) -> Tuple[Path, Path]:
    """Parse string-based paths and ensures src_path is sane. Also creates dst_dir if needed.

    Args:
        src_str: source directory
        dst_str: destination directory

    Returns:
        Tuple [src, dst]

    Raises:
        ValueError if source isn't called "SavedClips" or "SentryClips".
        NotADirectoryError if source isn't a directory.
    """
    src, dst = Path(src_str), Path(dst_str)

    if src.name not in ("SavedClips", "SentryClips"):
        raise ValueError("Source dir should be either 'SavedClips' or 'SentryClips'.")

    if not src.is_dir():
        raise NotADirectoryError(src)

    if not dst.is_dir():
        dst.mkdir()
        LOG.info(f"Created directory {dst}")

    return src, dst


class VideoGroup:
    CAM_NAMES = ["left_repeater", "front", "right_repeater", "back"]

    def __init__(self, timestamp_str: str, path: Path):
        """Container for the Paths for the 4 videos (one for each camera) for a single minute.

        Generates Path for the videos based on the timestamp_str and the path. Videos are not guaranteed
        to actually exist.

        Args:
            timestamp_str: timestamp from filename
            path: Path that the videos (are supposed to) live in.
        """
        self.timestamp_str = timestamp_str
        self.path = path

        self._cam_paths = {
            cam: path / (timestamp_str + "-" + cam + ".mp4") for cam in VideoGroup.CAM_NAMES
        }

    def keys(self):
        return self._cam_paths.keys()

    def items(self):
        return self._cam_paths.items()

    def __getitem__(self, key):
        return self._cam_paths[key]


def generate_latest_video_groups(path: Path, last_n: int) -> Generator[VideoGroup, None, None]:
    """Select latest videos for the last minute or more.

    Args:
        path: Path to event (contains videos).
        last_n: Number of minutes to look back. Should be at least 1, which selects only the videos recorded
            in the very last minute.

    Yields:
        VideoGroup for each minute, containing videos for the 4 cameras.
    """
    files = [f.name for f in path.glob("*.mp4")]
    if len(files) < MIN_VIDEOS_PER_EVENT:
        raise FileNotFoundError(f"Not enough videos in {path}, expected {MIN_VIDEOS_PER_EVENT} but got "
                                f"{len(files)}.")

    # Set comprehension for de-duplication of dates, then sort:
    dates = sorted({f[:DATE_PREFIX_LENGTH] for f in files}, reverse=True)
    n_to_get = min(last_n, len(dates))

    for date in reversed(dates[:n_to_get]):
        yield VideoGroup(date, path)
