teslacamerge
============
Python tool for merging TeslaCam SavedClips.

I've realised that these videos are best watched side-by-side, and usually the interesting bits are in the very last videos. This tool will, for each SavedClip, take the last minute, all 3 videos, and stitch them together. Output gets written out elsewhere.

In a later version, I'll probably add an option to include not only the last minute, but also a few minutes earlier, if available (configurable).

In the future, I might add my own Deep Learning magic: detect vehicles and persons. Auto-timelapse if there are no objects detected. Otherwise, play at normal speed.
