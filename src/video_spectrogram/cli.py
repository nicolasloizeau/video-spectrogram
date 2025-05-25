
from .spectrogram import generate_spectrogram_video
import argparse



def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="mp3 source file")
    parser.add_argument(
        "-wl",
        "--window_lenght",
        help="Lenght of the display window in seconds",
        default=10,
        type=float,
    )
    parser.add_argument(
        "-fps",
        "--fps",
        help="Frames per second of the output video",
        default=24,
        type=int,
    )
    parser.add_argument(
        "-mf",
        "--maxfreq",
        help="Maximum frequency to display in the spectrogram (in Hz)",
        default=2000,
        type=float,
    )
    parser.add_argument(
        "-p",
        "--prec",
        help="",
        default=0.05,
        type=float,
    )
    parser.add_argument(
        "-w",
        "--width",
        help="Width of the output video in pixels",
        default=800,
        type=int,
    )
    parser.add_argument(
        "-ht",
        "--height",
        help="Height of the output video in pixels",
        default=600,
        type=int,
    )
    parser.add_argument(
        "-c",
        "--colormap",
        help="matplotlib colormap",
        default="plasma",
    )
    parser.add_argument(
        "-vl",
        "--max_video_lenght",
        help="max length of the output video in seconds",
        default=10000,
        type=int,
    )
    parser.add_argument(
        "-bc",
        "--bar_color",
        help="Color of the bar in the spectrogram",
        default="white",
    )
    parser.add_argument(
        "-plt",
        "--matplotlib",
        help="Use matplotlib",
        action='store_true',
    )
    args = parser.parse_args()
    print(args)
    generate_spectrogram_video(args)
