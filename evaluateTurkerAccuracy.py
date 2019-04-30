#parse checkpoint_to_score file
def parse_checkpoint_to_scores(filename):
    reader = open(filename)
    count = 0
    checkpoint_to_score = {}
    for line in reader:
        count += 1
        if count == 1:
            continue #skip header line
        #split on : as delimiter
        parsed = line.split(":")
        print(parsed)
        checkpoint_to_score[parsed[0].strip()] = float(parsed[1])
    print(count)
    print(checkpoint_to_score)
    return checkpoint_to_score      

def parse_turk_responses(filename, env_name):
    reader = open(filename)
    count = 0
    ranking = {} #store as pair of checkpoints and A or B or Not Sure for preferences
    for line in reader:
        count += 1
        if count == 1:
            continue #skip header line
        #split on : as delimiter
        parsed = line.split(",")
        video_a = parsed[-5]
        video_b = parsed[-4]
        label = parsed[-3]
        #extract checkpoints and MTurk label
        idx_a_env = video_a.find(env_name+"_")
        idx_a_mp4 = video_a.find(".mp4")
        checkpoint_a = video_a[idx_a_env+len(env_name + "_") : idx_a_mp4]
        idx_b_env = video_b.find(env_name+"_")
        idx_b_mp4 = video_b.find(".mp4")
        checkpoint_b = video_b[idx_b_env+len(env_name + "_") : idx_b_mp4]
        print(checkpoint_a, checkpoint_b, parsed[-3])
        #add to ranking dict
        ranking[(checkpoint_a, checkpoint_b)] = label
    print(ranking)
    print(count - 1, "lines of turker responses parsed")
    
    return ranking
    


#evaluate Turker accuracy
def evaluate_accuracy(checkpoint_to_scores, ranking_dict):
    #use the ground truth returns from checkpont_to_scores to evalute the acuracy of MTurk
    correct = 0
    incorrect = 0
    for r in ranking_dict:
        print("-"*10)
        #find scores
        checkpoint_a = r[0]
        checkpoint_b = r[1]
        mturk_label = ranking_dict[r]
        print("checkpoints", checkpoint_a, checkpoint_b)
        print("MTurk label", mturk_label)
        score_a = checkpoint_to_scores[r[0]]
        score_b = checkpoint_to_scores[r[1]]
        print("scores", score_a, score_b)
        if score_a > score_b:
            if mturk_label == "A":
                print("correct")
                correct += 1
            elif mturk_label == "B":
                print("incorrect")
                incorrect += 1
        elif score_b > score_a:
            if mturk_label == "B":
                print("correct")
                correct += 1
            elif mturk_label == "A":
                print("incorrect")
                incorrect += 1
        elif score_a == score_b and mturk_label == "Not sure":
            print("correct")
            correct += 1
            
    return correct / len(ranking_dict), incorrect / len(ranking_dict)

if __name__=="__main__":
    env_name = "breakout"
    checkpoint_filename = "checkpoint_to_score.txt"
    turk_batch_filename = "Batch_3624797_batch_results.csv"
    checkpoints_to_scores = parse_checkpoint_to_scores(checkpoint_filename)
    ranking_dict = parse_turk_responses(turk_batch_filename, env_name)
    pos_accuracy, neg_accuracy = evaluate_accuracy(checkpoints_to_scores, ranking_dict)
    print("% correct = ", pos_accuracy)
    print("% incorrect = ", neg_accuracy)
    print("% not sure = ", 1 - pos_accuracy - neg_accuracy)
    
    


#from numpy import genfromtxt
#my_data = genfromtxt('inputbreakout_pref_mturk.csv', delimiter=',')
#print(my_data)
