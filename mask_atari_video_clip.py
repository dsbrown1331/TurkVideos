from moviepy.editor import *
import argparse

#python code to create csv file for MTurk
def get_videonames(env_name):
    checkpoint_min = 50
    checkpoint_max = 600
    checkpoint_step = 50
    if env_name == "enduro":
        checkpoint_min = 3100
        checkpoint_max = 3600
    elif env_name == "seaquest":
        checkpoint_min = 10
        checkpoint_max = 65
        checkpoint_step = 5

    videos_to_crop = []
    for c in range(checkpoint_min, checkpoint_max + checkpoint_step, checkpoint_step):
        if c < 10:
            checkpoint = "0000" + str(c)
        elif c < 100:
            checkpoint = "000" + str(c)
        elif c < 1000:
            checkpoint = "00" + str(c)
        elif c < 10000:
            checkpoint = "0" + str(c)
        else:
            checkpoint = str(c)
        #add video file to list of videos to crop
        videos_to_crop.append(env_name + "/" + env_name + "_" + checkpoint)
    
    return videos_to_crop
    
def crop_video(video_filename, env_name):
    print("cropping", video_filename)
    video = VideoFileClip(video_filename + ".mp4")
    if env_name == "breakout":
        cropped = video.crop(y1=17)
    elif env_name == "beamrider":
        cropped = video.crop(y1=40, y2=180)
    elif env_name == "enduro":
        cropped = video.crop(y2=160)
    elif env_name == "hero":
        cropped = video.crop(y2=135)
    elif env_name == "pong":
        cropped = video.crop(y1=30)
    elif env_name == "qbert":
        cropped = video.crop(y1=28)
    elif env_name == "seaquest":
        cropped = video.crop(y1=30, y2=160)
    elif env_name == "spaceinvaders":
        cropped = video.crop(y1=30, y2=196)
   
    cropped.write_videofile(video_filename + "_crop.webm")
        


parser = argparse.ArgumentParser(description=None)
parser.add_argument('--env_name', default='', help='Select the environment name to run, i.e. pong')
args = parser.parse_args()
env_name = args.env_name

videos_to_crop = get_videonames(env_name)
for v in videos_to_crop:
    crop_video(v, env_name)


