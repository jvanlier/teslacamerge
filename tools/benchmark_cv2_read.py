"""Quick 'n dirty benchmark to determine which method of traversing videos is faster.
Intended as a one-off check (hence the hardcoded path), included in repo for lookup purposes.

The second method is an order of magnitude faster.
"""
import cv2
from datetime import datetime


def main():
    fn = "/Volumes/TESLASTICK/TeslaCam/SavedClips/2020-06-02_09-10-25/2020-06-02_09-10-05-front.mp4"

    start = datetime.now()
    cap = cv2.VideoCapture(str(fn))
    cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 1)  # Go to last frame to determine nr. of frames
    n_frames = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
    for frame_pos in range(0, n_frames):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_pos)
        cap.read()
    cap.release()
    end = datetime.now()
    diff_s = (end - start).total_seconds()
    print(f"Took {diff_s} seconds")

    start = datetime.now()
    print("Loop")
    cap = cv2.VideoCapture(str(fn))
    while cap.isOpened():
        ret, _ = cap.read()
        if not ret:
            break
    cap.release()
    end = datetime.now()
    diff_s = (end - start).total_seconds()
    print(f"Took {diff_s} seconds")


if __name__ == "__main__":
    main()
