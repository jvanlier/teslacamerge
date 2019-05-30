import logging
from pathlib import Path

import numpy as np
import cv2
from tqdm import tqdm

from .loader import VideoGroup

LOG = logging.getLogger(__name__)

IN_HEIGHT = 960
IN_WIDTH = 1280
OUT_HEIGHT = IN_HEIGHT
OUT_WIDTH = 3 * IN_WIDTH


def _open_captures(vg: VideoGroup):
    cap_fnames = []
    caps = []
    n_frames = []
    fpses = []

    for video_path in vg:
        cap = cv2.VideoCapture(str(video_path))
        cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 1)  # Go to last frame
        msec = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

        n_frames.append(msec)
        caps.append(cap)
        cap_fnames.append(video_path.name)

        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        if not width == IN_WIDTH or not height == IN_HEIGHT:
            raise ValueError(f"Incorrect dimensions, got {height}x{width}")
        fps = cap.get(cv2.CAP_PROP_FPS)
        fpses.append(fps)

    max_n_frames = max(n_frames)

    LOG.debug(f"Number of frames in each video: {n_frames}, max: {max_n_frames}")
    return cap_fnames, caps, max_n_frames, float(np.mean(fpses))


def _open_output_video(dest: Path, timestamp: str, fps: float):
    return cv2.VideoWriter(
        str(dest / (timestamp + ".mp4")),
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (OUT_WIDTH, OUT_HEIGHT)
    )


def merge_group(vg: VideoGroup, dest: Path):
    cap_fnames, caps, max_n_frames, fps = _open_captures(vg)
    # Optionally limit max nr of frames for testing:
    max_n_frames = min(10, max_n_frames)

    out_vid = _open_output_video(dest, vg.timestamp_str, fps)

    for frame_pos in tqdm(range(0, max_n_frames)):
        frame_loc = 0
        frame_arr = np.zeros((OUT_HEIGHT, OUT_WIDTH, 3), dtype=np.uint8)

        # TODO: see if the reading of files can be done multi-core, since it's quite a bottleneck
        # or at least threads to do other work during blocking io
        for cap, cap_fname in zip(caps, cap_fnames):
            # FIXME: incrementing frame nrs like this is probably very slow:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_pos)
            frame_read, frame = cap.read()

            if not frame_read:
                LOG.warning(f"Could not read frame at pos {frame_pos} in file {cap_fname}")
            else:
                frame_arr[:, frame_loc * IN_WIDTH:(frame_loc + 1) * IN_WIDTH, :] = frame

            frame_loc += 1

        out_vid.write(frame_arr)

    out_vid.release()
