from moviepy.editor import *

#clip = ImageSequenceClip("breakout_00500.mp4", fps = 30)
#print(clip)


video = VideoFileClip("spaceinvaders/spaceinvaders_00500.mp4")
#cropped = video.crop(y2=135)
cropped = video.crop(y1=30, y2=196)
cropped.write_videofile("crop_test.mp4", fps=30)

# Make the text. Many more options are available.
#txt_clip = ( TextClip("My Holidays 2013",fontsize=70,color='white')
#             .set_position('center')
#             .set_duration(10) )

#result = CompositeVideoClip([video, txt_clip]) # Overlay text on video
#result.write_videofile("myHolidays_edited.mp4",fps=30) # Many options...
