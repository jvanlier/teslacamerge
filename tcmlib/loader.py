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
    def __init__(self, timestamp_str, path_left, path_front, path_right):
        self.timestamp_str = timestamp_str
        self.path_left = path_left
        self.path_front = path_front
        self.path_right = path_right
        self._verify()

    def _verify(self):
        for p in [self.path_left, self.path_front, self.path_right]:
            if not p.is_file():
                raise FileNotFoundError(p)

    @classmethod
    def from_dir(cls, timestamp_str, path):
        vid_paths = sorted(path.glob(timestamp_str + "*.mp4"))
        if len(vid_paths) != 3:
            raise FileNotFoundError(f"Expected 3 mp4s in {path}, got {len(vid_paths)}")

        # List is sorted, so can grab appropriate index directly
        return cls(timestamp_str, path_left=vid_paths[1], path_front=vid_paths[0],
                   path_right=vid_paths[2])

    def __repr__(self):
        return f"VideoGroup({self.timestamp_str}, {self.path_left.name}, " \
            f"{self.path_front.name}, {self.path_right.name}"

    def __iter__(self):
        """Iterate over cams, guaranteeing good order for side-by-side viewing, left-to-right.
        :return: iterator
        """
        for p in [self.path_left, self.path_front, self.path_right]:
            yield p


def select_latest_videos(path: Path) -> VideoGroup:
    files = [f.name for f in path.glob("*")]
    if len(files) < 3:
        raise FileNotFoundError(f"Not enough videos in {path}")
    dates = {f[:19] for f in files}
    max_date = max(dates)
    return VideoGroup.from_dir(max_date, path)
