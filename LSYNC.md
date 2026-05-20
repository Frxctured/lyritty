I used this python script to get my lyrics:
```python
from lsync import LyricsSync

import os
import sys

os.makedirs("output/lrc", exist_ok=True)
os.makedirs("output/vocals", exist_ok=True)
os.makedirs("output/words", exist_ok=True)

if len(sys.argv) >= 2:
    path = sys.argv[1]

    if os.path.exists(f"{path}.mp3") and os.path.exists(f"{path}.txt"):
        lsync = LyricsSync()

        words, lrc = lsync.sync(
            f"{path}.mp3", 
            f"{path}.txt"
        )
        print("Output is in output/lrc")
    else:
        print("Couldn't find either song or txt file")
else:
    print("You must provide a path")
```

Instructions:

1. Clone the lsync repo
2. Paste the script from above into the project root directory.
   I saved it as `get_lyrics.py`
3. If you set up lsync correctly (explained in their repo), you should be able to use:
```bash
python get_lyrics.py path/to/your/song # NO EXTENSION
```
You must have both song.mp3 and song.txt files in the same directory.
```
some_folder/
├── SAINT.mp3
└── SAINT.txt
```
For this example the command would look like this:
```bash
python get_lyrics.py some_folder/SAINT
```

After getting the lyrics in `output/lrc`, you can copy the file into this repo to convert it into the correct format using:
```bash
python elrc_to_lrc.py path/to/song_name.lrc
```

this script just overwrites the original file so you can directly use it with the appropriate song
