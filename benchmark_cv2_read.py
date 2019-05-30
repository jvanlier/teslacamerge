import cv2
from datetime import datetime


def main():
    fn = "/Volumes/TESLASTICK/TeslaCam/SavedClips/2019-05-30_09-23-14/2019-05-30_09-23-12-front.mp4"

    start = datetime.now()
    print("Explicitly incrementing position")
    cap = cv2.VideoCapture(str(fn))
    cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 1)  # Go to last frame
    n_frames = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
    for frame_pos in range(0, n_frames):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_pos)
        frame_read, frame = cap.read()
    cap.release()
    end = datetime.now()
    diff_s = (end-start).total_seconds()
    print(f"Took {diff_s} seconds")

    start = datetime.now()
    print("Loop")
    cap = cv2.VideoCapture(str(fn))
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
    cap.release()
    end = datetime.now()
    diff_s = (end-start).total_seconds()
    print(f"Took {diff_s} seconds")


if __name__ == "__main__":
    main()