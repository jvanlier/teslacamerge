teslacamerge
============
Python tool for merging TeslaCam SavedClips. It collects, for each event, the most recent videos (default the
last 2 minutes) and merges them all into a single side-by-side video. The video speed is 2x by default 
(configurable).

## Why was this made?

Usually, the most interesting bits are in the last few minutes of the 10 minute event. And it's best to watch
all cameras synchronized side-by-side instead of in isolation. Still, watching on 1x speed takes quite some 
time, which explains the speedup to 2x.

## How to use this?
The package isn't released on PyPI. 
However, setting it up is straight forward if you have a bit of *nix command line + Python experience:
    
    git clone https://github.com/jvanlier/teslacamerge
    cd teslacammerge
    python3 -m venv path/to/virtualenv
    source path/to/virtualenv/bin/activate
    pip install .  # or .[test] if you intend to run unit tests
    
Once it's installed (and the virtualenv is activated):

    tcm -s /path/to/TeslaCam/SavedClips -d ~/output_path
    
Command line flag `-x` controls the speed ratio, `-m` controls how many minutes back to start from for each
clip, and `-w` controls the number of workers. The default for `-w` is 6, which uses 600-700 % CPU on my 
8-Core MacBook. Change accordingly for your system. See `tcm --help` for details.

![example-video](example-output-video.jpg?raw=true)

