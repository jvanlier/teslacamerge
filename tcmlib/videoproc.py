import logging
from pathlib import Path
import asyncio
from typing import List

import numpy as np
import cv2

from .loader import VideoGroup

LOG = logging.getLogger(__name__)

IN_HEIGHT = 960
IN_WIDTH = 1280
OUT_HEIGHT = IN_HEIGHT * 2
OUT_WIDTH = IN_WIDTH * 2
FRONT_X_OFFSET = round(IN_WIDTH / 2)
FPS = 80  # 40 is normal-ish, 80 is 2x speed


def _open_captures(vg: VideoGroup):
    caps = {}

    for cam_name, video_path in vg.items():
        cap = cv2.VideoCapture(str(video_path))
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        if width == 0 and height == 0:
            # zero byte videos have these properties - happens to repeaters sometimes.
            cap = None
            LOG.warning(f"Seems like {video_path} is corrupt - got dimensions 0x0. Ignoring it.")
        elif not width == IN_WIDTH or not height == IN_HEIGHT:
            raise ValueError(f"Incorrect dimensions, got {width}x{height}")

        caps[cam_name] = cap
    return caps


async def _reader(queue, vg_list: List[VideoGroup]):
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
                        frame_arr[0:IN_HEIGHT, FRONT_X_OFFSET:FRONT_X_OFFSET+IN_WIDTH, :] = frame
                    elif cam_idx == 2:
                        frame_arr[IN_HEIGHT:IN_HEIGHT * 2, IN_WIDTH:IN_WIDTH * 2, :] = frame
                    else:
                        raise ValueError(f"cam_idx {cam_idx}")

            await queue.put(frame_arr)

    await queue.put(None)


async def _writer(queue, dest_video_path: Path):
    vid = cv2.VideoWriter(
        str(dest_video_path),
        cv2.VideoWriter_fourcc(*"mp4v"),
        FPS,
        (OUT_WIDTH, OUT_HEIGHT)
    )

    try:
        while True:
            frame = await queue.get()
            if not isinstance(frame, np.ndarray):
                LOG.debug(f"Writer for {dest_video_path.name} seems to be done!")
                break
            vid.write(frame)
            queue.task_done()
    finally:
        vid.release()


def merge_group(vg: List[VideoGroup], dest_dir: Path):
    dest_video_path = dest_dir / (vg[-1].timestamp_str + ".mp4")

    loop = asyncio.get_event_loop()
    queue = asyncio.Queue(loop=loop, maxsize=128)

    reader = _reader(queue, vg)
    writer = _writer(queue, dest_video_path)

    loop.run_until_complete(asyncio.gather(reader, writer))
