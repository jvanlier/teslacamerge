teslacamerge
============
Python tool for merging TeslaCam SavedClips.

I've realised that these videos are best watched side-by-side, and usually the interesting bits are in the very last videos. This tool will, for each SavedClip, take the last minute, all 3 videos, and stitch them together. Output gets written out elsewhere.

## Initial rudimentary version
After a few hours of hacking, got something working. Very slow, but functional:

```
» tcm -s /Volumes/TESLASTICK -d ~/tmp/tcm-out                                                                                         jvlier@joris-mbp
2019-05-30 17:50:46,805 INFO [tcm/main]: Next up: videos in /Volumes/TESLASTICK/TeslaCam/SavedClips/2019-05-30_09-24-35
2019-05-30 17:50:46,806 DEBUG [selector_events/__init__]: Using selector: KqueueSelector
2019-05-30 17:51:16,478 DEBUG [videoproc/_writer]: Writer for 2019-05-30_09-24-34.mp4 seems to be done!
2019-05-30 17:51:16,492 INFO [tcm/main]: Next up: videos in /Volumes/TESLASTICK/TeslaCam/SavedClips/2019-05-30_09-25-43
2019-05-30 17:51:27,049 DEBUG [videoproc/_writer]: Writer for 2019-05-30_09-25-43.mp4 seems to be done!
2019-05-30 17:51:27,062 INFO [tcm/main]: Next up: videos in /Volumes/TESLASTICK/TeslaCam/SavedClips/2019-05-30_09-27-48
2019-05-30 17:51:32,007 DEBUG [videoproc/_writer]: Writer for 2019-05-30_09-27-48.mp4 seems to be done!
2019-05-30 17:51:32,020 INFO [tcm/main]: Next up: videos in /Volumes/TESLASTICK/TeslaCam/SavedClips/2019-05-30_09-29-34
[h264 @ 0x7ff96c8a3200] out of range intra chroma pred mode
[h264 @ 0x7ff96c8a3200] error while decoding MB 33 40
2019-05-30 17:52:38,534 DEBUG [videoproc/_writer]: Writer for 2019-05-30_09-29-32.mp4 seems to be done!
2019-05-30 17:52:38,547 INFO [tcm/main]: Processing took 111.742426 sec
```

![example-video](example-output-video.jpg?raw=true)

[YouTube](https://www.youtube.com/watch?v=tePUa5mpW2Q&feature=youtu.be)

## Future

In a later version, I'll probably add an option to include not only the last minute, but also a few minutes earlier, if available (configurable).

In a much much later version, I might add my own Deep Learning magic: detect vehicles and persons. Auto-timelapse if there are no objects detected. Otherwise, play at normal speed.

Might also be nice to embed TeslaFi data...
