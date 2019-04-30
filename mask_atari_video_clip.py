from moviepy.editor import *

#python code to create csv file for MTurk
def get_videonames(env_name):
    checkpoint_min = 50
    checkpoint_max = 600
    checkpoint_step = 50

    videos_to_crop = []
    for c in range(checkpoint_min, checkpoint_max + checkpoint_step, checkpoint_step):
        if c < 10:
            checkpoint = "0000" + str(c)
        elif c < 100:
            checkpoint = "000" + str(c)
        elif c < 1000:
            checkpoint = "00" + str(c)
        elif c < 1000:
            checkpoint = "0" + str(c)
        #add video file to list of videos to crop
        videos_to_crop.append(env_name + "_" + checkpoint)
    
    return videos_to_crop
    
def crop_video(video_filename):
    print("cropping", video_filename)
    video = VideoFileClip(video_filename + ".mp4")
    cropped = video.crop(y1=15)
    cropped.write_videofile(video_filename + "_crop.mp4")
        

env_name = "breakout"
videos_to_crop = get_videonames(env_name)
for v in videos_to_crop:
    crop_video(v)


