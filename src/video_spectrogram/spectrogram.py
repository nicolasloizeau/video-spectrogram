
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from tqdm import tqdm
from PIL import Image, ImageDraw
import pydub
from os import system
import cv2
import os
import moviepy as mpe
import matplotlib
matplotlib.use('Agg')



def read(f, normalized=False):
    """MP3 to numpy array"""
    a = pydub.AudioSegment.from_mp3(f)
    y = np.array(a.get_array_of_samples())
    if a.channels == 2:
        y = y.reshape((-1, 2))
        y = y.mean(axis=1)
    return a.frame_rate, y


def spectrogram(y, rate, args):
    f, t, Sxx = signal.spectrogram(y, rate, nperseg=int(rate*args.prec))
    i = np.argmin(np.abs(f - args.maxfreq))
    f = f[:i]
    Sxx = Sxx[:i, :]
    Sxx /= np.max(Sxx)  # Normalize the spectrogram
    Sxx = np.log(Sxx+np.min(Sxx)+args.logoffset)
    return f, t, Sxx

def saveframe_plt(f, t, Sxx, i, args):
    """Save a single frame of the spectrogram as an image."""
    plt.cla()
    plt.pcolormesh(t, f, Sxx, shading='gouraud', cmap=args.colormap)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    tbar = (t[-1]+t[0])/2
    plt.plot([tbar,tbar], plt.gca().get_ylim(), color=args.bar_color, linewidth=1)
    plt.savefig('frames/{:08d}.png'.format(i))



def fromarray(data_array, args):
    data_array = np.flipud(data_array)
    vmin = data_array.min()
    vmax = data_array.max()
    colormap = plt.get_cmap(args.colormap)
    norm_data = (data_array - vmin) / (vmax - vmin)
    norm_data = np.clip(norm_data, 0, 1)
    rgba_data = colormap(norm_data)
    rgb_data = (rgba_data[:, :, :3] * 255).astype(np.uint8)
    pil_image = Image.fromarray(rgb_data)
    pil_image = pil_image.resize((args.width, args.height))
    shape = [args.width/2, 0, args.width/2, args.height]
    draw = ImageDraw.Draw(pil_image)
    draw.line(shape, fill =args.bar_color, width = 2)
    return pil_image


def saveframe_pil(f, t, Sxx, i, args):
    img = fromarray(Sxx, args)
    img.save('frames/{:08d}.png'.format(i))



def frames_to_video(args):
    image_folder = 'frames'
    video_name = 'video.avi'
    fnames = sorted(os.listdir(image_folder))
    images = [img for img in fnames if img.endswith(".png")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape
    video = cv2.VideoWriter(video_name, 0, args.fps, (width,height))
    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))
    cv2.destroyAllWindows()
    video.release()

def saveframes(f, t, Sxx, args):
    system('rm -r frames')
    system('mkdir frames')
    tmax = t[-1]
    rate2 = len(t)/tmax
    pad = np.zeros(( len(f), int(rate2*args.window_lenght/2)))+np.min(Sxx)
    Sxx = np.concatenate([pad, Sxx, pad], axis=1)

    t = np.linspace(-args.window_lenght/2, tmax+args.window_lenght/2, Sxx.shape[1])

    timestep = 1/args.fps
    time = 0
    maxi1 = int(args.max_video_lenght * args.fps)
    maxi2 = int(tmax * args.fps)
    saveframe = saveframe_pil
    if args.matplotlib:
        saveframe = saveframe_plt
    for i in tqdm(range(min(maxi1, maxi2))):
        window = [int(time*rate2), int((time + args.window_lenght)*rate2)]
        ti = t[window[0]:window[1]]
        Sxxi = Sxx[:, window[0]:window[1]]
        time += timestep
        saveframe(f, ti, Sxxi, i, args)

def add_audio(args):
    audio = mpe.AudioFileClip(args.file)
    video1 = mpe.VideoFileClip('video.avi')
    final = video1.with_audio(audio)
    final.write_videofile("output.mp4")
    os.system('rm video.avi')


def generate_spectrogram_video(args):
    rate, y = read(args.file)
    print('fourier transform...')
    f, t, Sxx = spectrogram(y, rate, args)
    print('saving the frames...')
    saveframes(f, t, Sxx, args)
    print('generating the video...')
    frames_to_video(args)
    add_audio(args)
