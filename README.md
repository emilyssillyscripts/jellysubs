# jellysubs.py
 python script to move subs into jellyfin-acceptable places for tv shows

## Options
```
-c, --clean    | remove an unwanted part of the final filenames
-l, --lang     | specify desired subtitle file language ("English", "Spanish", etc...)
-v             | verbose output
```

## Expected example file structure before running script

```
Example TV Show S01
├── Subs
│   ├── tests01e01-some-random-torrent
│   │   └── 32_English.srt
│   ├── tests01e02-some-random-torrent
│   │   └── 32_English.srt
│   ├── tests01e03-some-random-torrent
│   │   └── 32_English.srt
│   └── tests01e04-some-random-torrent
│       └── 32_English.srt
├── tests01e01-some-random-torrent.mp4
├── tests01e02-some-random-torrent.mp4
├── tests01e03-some-random-torrent.mp4
└── tests01e04-some-random-torrent.mp4
```
