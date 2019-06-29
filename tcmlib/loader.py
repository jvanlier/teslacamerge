from pathlib import Path


def parse_paths(src: str, dest: str):
    src = Path(src)
    src /= "TeslaCam"
    src /= "SavedClips"
    dest = Path(dest)
    return src, dest


def verify_paths(src: Path, dest: Path):
    for p in [src, dest]:
        if not p.is_dir():
            raise NotADirectoryError(p)


class VideoGroup:
    CAM_NAMES = ["left_repeater", "front", "right_repeater"]

    def __init__(self, timestamp_str: str, cam_paths: dict):
        if not set(cam_paths.keys()) == set(VideoGroup.CAM_NAMES):
            raise ValueError(f"Expected dict with keys {VideoGroup.CAM_NAMES}, got {cam_paths.keys()}")
        self.timestamp_str = timestamp_str
        self._cam_paths = cam_paths
        self._verify()

    def _verify(self):
        for cam, path in self._cam_paths.items():
            if not path.is_file():
                raise FileNotFoundError(f"Expected {cam} at {path}")

    @classmethod
    def from_dir(cls, timestamp_str, path):
        cam_paths = {
            cam: path / (timestamp_str + "-" + cam + ".mp4") for cam in VideoGroup.CAM_NAMES
        }

        return cls(timestamp_str, cam_paths)

    def keys(self):
        yield from self._cam_paths.keys()

    def items(self):
        yield from self._cam_paths.items()

    def values(self):
        yield from self._cam_paths.values()


def select_latest_videos(path: Path, last_n: int = 1):
    files = [f.name for f in path.glob("*.mp4")]
    if len(files) < 3:
        raise FileNotFoundError(f"Not enough videos in {path}")
    # Set for deduplication, then sort:
    dates = sorted({f[:19] for f in files}, reverse=True)
    n_to_get = min(last_n, len(dates))

    for date in reversed(dates[:n_to_get]):
        yield VideoGroup.from_dir(date, path)
