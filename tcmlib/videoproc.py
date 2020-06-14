import logging
from pathlib import Path
from typing import List, Dict
from threading import Thread
from queue import Queue

import numpy as np
import cv2

from .loader import VideoGroup

LOG = logging.getLogger(__name__)

IN_HEIGHT = 960
IN_WIDTH = 1280
OUT_HEIGHT = IN_HEIGHT * 2
OUT_WIDTH = IN_WIDTH * 2
FPS = 36


def _open_captures(vg: VideoGroup) -> Dict[str, cv2.VideoCapture]:
    caps = {}

    for cam_name, video_path in vg.items():
        cap = None

        if not video_path.is_file():
            # Not a fatal error, since at least one of the other videos is present. Printing for awareness:
            LOG.warning(f"FileNotFound: Expected video for {cam_name} at {video_path}")
        else:
            cap = cv2.VideoCapture(str(video_path))
            width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            if width == 0 and height == 0:
                # zero byte videos have these properties - happens to repeaters sometimes.
                LOG.warning(f"Seems like {video_path} is corrupt - got dimensions 0x0. Ignoring it.")
            elif not width == IN_WIDTH or not height == IN_HEIGHT:
                raise ValueError(f"Incorrect dimensions for {video_path}, got {width}x{height}")

        caps[cam_name] = cap
    return caps


def _reader(queue: Queue, vg_list: List[VideoGroup]):
    for vg in vg_list:
        caps = _open_captures(vg)

        more_content = True
        while more_content:
            more_content = False  # Unless proven otherwise!
            frame_arr = np.zeros((OUT_HEIGHT, OUT_WIDTH, 3), dtype=np.uint8)

            for cam_idx, (cam_name, cap) in enumerate(caps.items()):
                if not cap:
                    continue  # Sometimes one of the videos is corrupt.

                frame_read, frame = cap.read()

                if frame_read:
                    more_content = True

                    # TODO: make this a bit nicer:
                    if cam_idx == 0:
                        frame_arr[IN_HEIGHT:IN_HEIGHT * 2, 0:IN_WIDTH, :] = frame
                    elif cam_idx == 1:
                        frame_arr[0:IN_HEIGHT, 0:IN_WIDTH, :] = frame
                    elif cam_idx == 2:
                        frame_arr[IN_HEIGHT:IN_HEIGHT * 2, IN_WIDTH:IN_WIDTH * 2, :] = frame
                    elif cam_idx == 3:
                        frame_arr[0:IN_HEIGHT, IN_WIDTH:IN_WIDTH * 2, :] = frame
                    else:
                        raise ValueError(f"cam_idx {cam_idx}")

            queue.put(frame_arr)

        for cap in caps.values():
            cap.release()

    queue.put(None)


def _writer(queue: Queue, dest_video_path: Path, speed_ratio: float):
    vid = cv2.VideoWriter(
        str(dest_video_path),
        cv2.VideoWriter_fourcc(*"mp4v"),
        FPS * speed_ratio,
        (OUT_WIDTH, OUT_HEIGHT)
    )

    while True:
        frame = queue.get()
        if not isinstance(frame, np.ndarray):
            vid.release()
            break
        vid.write(frame)


def merge(vg: List[VideoGroup], dest_dir: Path, speed_ratio: float):
    out_mp4_name = vg[0].path.name + ".mp4"
    LOG.info(f"Starting on {out_mp4_name}...")
    out_mp4_path = dest_dir / out_mp4_name

    queue = Queue(maxsize=20)
    thr_reader = Thread(target=_reader, args=(queue, vg))
    thr_reader.start()

    thr_writer = Thread(target=_writer, args=(queue, out_mp4_path, speed_ratio))
    thr_writer.start()

    thr_writer.join()
    LOG.info(f"Done with {out_mp4_name}")
