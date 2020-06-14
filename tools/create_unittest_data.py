"""One-off script to create unit test data.

Approach:
- select a few random events from SRC_PATH.
- Get the last 12 videos (= 3 minutes of video for 4 cameras).
- Use ffmpeg to keep only 5 seconds in order to keep file sizes manageable.

N.b.: this tool uses moviepy which has a convenient ffmpeg interface. Moviepy isn't listed in the setup.py,
since this tool isn't really part of the application and was only intended as a one-off script. Install it
manually if needed.
"""
from pathlib import Path

import numpy as np
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


SRC_PATH = Path("/Volumes/TESLASTICK/TeslaCam/SavedClips/")
DEST_PATH = Path(__file__).parent.parent / "tests" / "data"
N_EVENTS = 1
N_VIDEOS = 12
VID_SECS = 1  # Seconds per video to keep

selected_event_paths = np.random.choice(list(SRC_PATH.glob("*")), size=N_EVENTS, replace=False)

for event_path in selected_event_paths:
    print(f"\nStarting on event {event_path}.name")
    vids = sorted(event_path.glob("*.mp4"))
    if len(vids) < N_VIDEOS:
        print(f"Only {len(vids)} videos in {event_path} - skipping.")
        continue

    vids = vids[-N_VIDEOS:]

    event_path_dest = DEST_PATH / event_path.name
    event_path_dest.mkdir()

    for vid in vids:
        print(f"Processing {vid.name}")
        ffmpeg_extract_subclip(vid, 0, VID_SECS, targetname=event_path_dest / vid.name)
