import logging
from pathlib import Path
import asyncio

import numpy as np
import cv2
from tqdm import tqdm

from .loader import VideoGroup

LOG = logging.getLogger(__name__)

IN_HEIGHT = 960
IN_WIDTH = 1280
OUT_HEIGHT = IN_HEIGHT
OUT_WIDTH = 3 * IN_WIDTH
FPS = 40


def _open_captures(vg: VideoGroup):
    for video_path in vg:
        cap = cv2.VideoCapture(str(video_path))
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        if not width == IN_WIDTH or not height == IN_HEIGHT:
            raise ValueError(f"Incorrect dimensions, got {height}x{width}")

        yield cap


async def _reader(queue, vg: VideoGroup):
    caps = list(_open_captures(vg))

    more_content = True
    while more_content:
        more_content = False  # Unless proven otherwise!
        frame_arr = np.zeros((OUT_HEIGHT, OUT_WIDTH, 3), dtype=np.uint8)

        for i, cap in enumerate(caps):
            frame_read, frame = cap.read()

            if frame_read:
                more_content = True
                frame_arr[:, i * IN_WIDTH:(i + 1) * IN_WIDTH, :] = frame
        # LOG.info("Putting frame")
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
            # LOG.info("Got frame")
            if not isinstance(frame, np.ndarray):
                LOG.info("Writer seems to be done!")
                break
            vid.write(frame)
            queue.task_done()
    finally:
        LOG.info("Writer cleaning up")
        vid.release()


def merge_group(vg: VideoGroup, dest_dir: Path):
    dest_video_path = dest_dir / (vg.timestamp_str + ".mp4")

    loop = asyncio.get_event_loop()
    queue = asyncio.Queue(loop=loop, maxsize=128)

    reader = _reader(queue, vg)
    writer = _writer(queue, dest_video_path)

    loop.run_until_complete(asyncio.gather(reader, writer))
    #loop.close()

    #
    #

    # cap_fnames, caps, max_n_frames, fps = _open_captures(vg)
    # # Optionally limit max nr of frames for testing:
    # max_n_frames = min(10, max_n_frames)
    #
    # out_vid = _open_output_video(dest, vg.timestamp_str, fps)
    #
    # for frame_pos in tqdm(range(0, max_n_frames)):
    #     frame_loc = 0
    #     frame_arr = np.zeros((OUT_HEIGHT, OUT_WIDTH, 3), dtype=np.uint8)
    #
    #     # TODO: see if the reading of files can be done multi-core, since it's quite a bottleneck
    #     # or at least threads to do other work during blocking io
    #     for cap, cap_fname in zip(caps, cap_fnames):
    #         # FIXME: incrementing frame nrs like this is probably very slow:
    #         cap.set(cv2.CAP_PROP_POS_FRAMES, frame_pos)
    #         frame_read, frame = cap.read()
    #
    #         if not frame_read:
    #             LOG.warning(f"Could not read frame at pos {frame_pos} in file {cap_fname}")
    #         else:
    #             frame_arr[:, frame_loc * IN_WIDTH:(frame_loc + 1) * IN_WIDTH, :] = frame
    #
    #         frame_loc += 1
    #
    #     out_vid.write(frame_arr)
    # out_vid.release()


