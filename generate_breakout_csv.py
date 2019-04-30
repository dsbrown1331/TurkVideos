#python code to create csv file for MTurk
checkpoint_min = 50
checkpoint_max = 600
checkpoint_step = 50
env_name = "breakout"
video_list = []

video_repo = "https://raw.githubusercontent.com/dsbrown1331/TurkVideos/master/"

for c in range(checkpoint_min, checkpoint_max + checkpoint_step, checkpoint_step):
    if c < 10:
        checkpoint = "0000" + str(c)
    elif c < 100:
        checkpoint = "000" + str(c)
    elif c < 1000:
        checkpoint = "00" + str(c)
    elif c < 1000:
        checkpoint = "0" + str(c)
        
    video_list.append("{}{}_{}_crop.mp4".format(video_repo, env_name, checkpoint))
   
#write to csv file for uploading to MTurk
writer = open("input" + env_name + "_pref_mturk.csv", "w")
#write variable labels in first row
writer.write("{},{}\n".format("video_url_A","video_url_B"))

for i in range(len(video_list)):
    for j in range(len(video_list)):
        if i == j:
            continue
        writer.write("{},{}\n".format(video_list[i], video_list[j]))
