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


def merge(vg: VideoGroup, dest: Path):
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
    # max_n_frames = min(100, max_n_frames)
    LOG.debug(f"Number of frames in each video: {n_frames}, max: {max_n_frames}")

    out_vid = cv2.VideoWriter(str(dest / (vg.timestamp_str + ".mp4")),
                              cv2.VideoWriter_fourcc(*"mp4v"),
                              np.mean(fpses),
                              (OUT_WIDTH, OUT_HEIGHT)
    )

    for frame_pos in tqdm(range(0, max_n_frames)):
        frame_loc = 0
        frame_arr = np.zeros((OUT_HEIGHT, OUT_WIDTH, 3), dtype=np.uint8)

        # TODO: see if the reading of files can be done multi-core, since it's quite a bottleneck
        # or at least threads to do other work during blocking io
        for cap, cap_fname in zip(caps, cap_fnames):
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_pos)
            frame_read, frame = cap.read()

            if not frame_read:
                LOG.warning(f"Could not read frame at pos {frame_pos} in file {cap_fname}")
            else:
                frame_arr[:, frame_loc * IN_WIDTH:(frame_loc + 1) * IN_WIDTH, :] = frame

            frame_loc += 1

        # cv2.imwrite(str(dest / f"test-{frame_pos}.jpg"), frame_arr)
        out_vid.write(frame_arr)

    out_vid.release()


