import ffmpeg
import subprocess
import os.path
from colorthief import ColorThief
from colormap import rgb2hex

class Overlay():

    def __init__(self, base, overlay):
        self.base = base
        self.overlay = overlay

    def video_width(video):
        probe = ffmpeg.probe(video)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        return int(video_stream['width'])

    def video_height(video):
        probe = ffmpeg.probe(video)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        return int(video_stream['height'])

    def video_get_color(video):
        out_filename = str(video).split('.')[-2] + ".jpg"
        if os.path.exists(out_filename):
            print("Img from overlay already exist")
        else:
            print("Create img from overlay")
            Overlay.extract_img(video)
        color_thief = ColorThief(str(out_filename))
        dominant_color = color_thief.get_color(quality=1)
        return rgb2hex(dominant_color[0], dominant_color[1], dominant_color[2]) 

    def extract_img(video):
        width =  Overlay.video_width(video)
        out_filename = str(video).split('.')[-2] + ".jpg"
        (
            ffmpeg
            .input(video, ss=0)
            .filter('scale', width, -1)
            .output(out_filename, vframes=1)
            .run()
        )

    def color_key_overlay(base,overlay):
        color = Overlay.video_get_color(overlay)
        out_filename = str(base).split('.')[-2] + "_out.mp4"
        cmd = 'ffmpeg -i ' + str(base) + \
        ' -i ' + str(overlay) +  ' -filter_complex "[1:v]colorkey=' + str(color) + \
        ':0.3:0.2[ckout];[0:v][ckout]overlay[out]" -map "[out]" ' + str(out_filename)
        with open(subprocess.Popen(cmd, shell=True)) as sp:
            sp.communicate()