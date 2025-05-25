


# Generate video spectrograms from audio files



[![](src/frame.png)](https://www.youtube.com/watch?v=HNq3KbRVVZ0)

## Install from github


```bash
pip install git+https://github.com/nicolasloizeau/video-spectrogram.git#egg=video-spectrogram
```

## Usage

Help
```bash
video-spectrogram --help
```

Example: Convert `audio.mp3` to a video spectrogram with a maximum frequency of 2000 Hz and a frame rate of 30 fps, and use matplotlib for rendering:
```bash
video-spectrogram audio.mp3 -mf 2000 -fps 30 -plt
```

important options:
- `-mf`: Maximum frequency to display in the spectrogram (default: 2000 Hz)
- `-fps`: Frame rate of the output video (default: 30 fps)
- `-plt`: Use matplotlib for rendering (default: ffmpeg)
- `-lo` : Offset for logarithmic scaling of the spectrogram. Lower values filter out lower amplitudes, increasing the constrast. Default:1e-6




## Contributing
Feel free to open issues or pull requests.
