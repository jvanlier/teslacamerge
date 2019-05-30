teslacamerge
============
Python tool for merging TeslaCam SavedClips.

I've realised that these videos are best watched side-by-side, and usually the interesting bits are in the very last videos. This tool will, for each SavedClip, take the last minute, all 3 videos, and stitch them together. Output gets written out elsewhere.

## Initial rudimentary version
After a few hours of hacking, got something working. Very slow, but functional:

```
» tcm -s /Volumes/TESLASTICK -d ~/tmp/tcm-out 
INFO:__main__:Processing dir /Volumes/TESLASTICK/TeslaCam/SavedClips/2019-05-30_09-23-14
INFO:__main__:Will handle videos for 2019-05-30_09-23-12
DEBUG:tcmlib.videoproc:Number of frames in each video: [1467, 1467, 1467], max: 1467
100%|████████████████████████████████████████████████████████████████████████████████████████████| 1467/1467 [02:51<00:00,  8.67it/s]
INFO:__main__:Processing dir /Volumes/TESLASTICK/TeslaCam/SavedClips/2019-05-30_09-24-35
INFO:__main__:Will handle videos for 2019-05-30_09-24-34
DEBUG:tcmlib.videoproc:Number of frames in each video: [635, 635, 634], max: 635
100%|█████████████████████████████████████████████████████████████████████████████████████████████▊| 634/635 [01:19<00:00,  8.71it/s]WARNING:tcmlib.videoproc:Could not read frame at pos 634 in file 2019-05-30_09-24-34-right_repeater.mp4
100%|██████████████████████████████████████████████████████████████████████████████████████████████| 635/635 [01:19<00:00,  8.78it/s]
INFO:__main__:Processing dir /Volumes/TESLASTICK/TeslaCam/SavedClips/2019-05-30_09-25-43
INFO:__main__:Will handle videos for 2019-05-30_09-25-43
DEBUG:tcmlib.videoproc:Number of frames in each video: [212, 212, 212], max: 212
100%|██████████████████████████████████████████████████████████████████████████████████████████████| 212/212 [00:25<00:00,  8.80it/s]
```

![example-video](example-output-video.jpg?raw=true)

## Future

In a later version, I'll probably add an option to include not only the last minute, but also a few minutes earlier, if available (configurable).

In a much much later version, I might add my own Deep Learning magic: detect vehicles and persons. Auto-timelapse if there are no objects detected. Otherwise, play at normal speed.

Might also be nice to embed TeslaFi data...
