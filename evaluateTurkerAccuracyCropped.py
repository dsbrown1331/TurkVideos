import argparse
import numpy as np
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
    ranking = [] #store as tupes: pair of checkpoints and A or B or Not Sure for preferences
    for line in reader:
        count += 1
        if count == 1:
            continue #skip header line
        #split on : as delimiter
        parsed = line.split(",")
        #print(parsed)
        video_a = parsed[-6]
        video_b = parsed[-5]
        label = parsed[-3]
        #print(video_a)
        #print(video_b)
        #print(label)
        #input()
        #extract checkpoints and MTurk label
        idx_a_env = video_a.find(env_name+"_")
        idx_a_mp4 = video_a.find("_crop.webm")
        checkpoint_a = video_a[idx_a_env+len(env_name + "_") : idx_a_mp4]
        idx_b_env = video_b.find(env_name+"_")
        idx_b_mp4 = video_b.find("_crop.webm")
        checkpoint_b = video_b[idx_b_env+len(env_name + "_") : idx_b_mp4]
        print(checkpoint_a, checkpoint_b, parsed[-3])
        #add to ranking dict
        ranking.append(((checkpoint_a, checkpoint_b), label))
    print(ranking)
    print(count - 1, "lines of turker responses parsed")
    
    return ranking
    


#evaluate Turker accuracy
def evaluate_accuracy(checkpoint_to_scores, ranking_dict):
    #use the ground truth returns from checkpont_to_scores to evalute the acuracy of MTurk
    correct = 0
    incorrect = 0
    for r, label in ranking_dict:
        print("-"*10)
        #find scores
        checkpoint_a = r[0]
        checkpoint_b = r[1]
        mturk_label = label
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
    
#evaluate Turker accuracy
def evaluate_accuracy_majority(checkpoint_to_scores, ranking_dict):
    #use the ground truth returns from checkpont_to_scores to evalute the acuracy of MTurk
    correct = 0
    incorrect = 0
    #keep a dictionary of checkpoints and labels to parse to get majority votes
    vote_dict = {}
    for r, label in ranking_dict:
        print("-"*10)
        #find scores
        checkpoint_a = r[0]
        checkpoint_b = r[1]
        mturk_label = label
        
        score_a = checkpoint_to_scores[r[0]]
        score_b = checkpoint_to_scores[r[1]]
        if score_a > score_b:
            #flip checkpoints and scores
            temp = checkpoint_a
            checkpoint_a = checkpoint_b
            checkpoint_b = temp
            temp_s = score_a
            score_a = score_b
            score_b = temp_s
            if mturk_label == "A":
                mturk_label = "B"
            elif mturk_label == "B":
                mturk_label = "A"
        if (checkpoint_a, checkpoint_b) not in vote_dict:
            vote_dict[(checkpoint_a, checkpoint_b)] = [0,0,0]        
        
        print("incrementing")
        print("before", vote_dict[(checkpoint_a, checkpoint_b)])
        if mturk_label == "A": #increment index 0
            vote_dict[(checkpoint_a, checkpoint_b)][0]+=1
        elif mturk_label =="B": #increment index 1
            vote_dict[(checkpoint_a,checkpoint_b)][1]+=1
        else:
            vote_dict[(checkpoint_a, checkpoint_b)][2]+=1
    
        print("after", vote_dict[(checkpoint_a, checkpoint_b)])
        
        
        print("checkpoints", checkpoint_a, checkpoint_b)
        print("MTurk label", mturk_label)    
        print("scores", score_a, score_b)
            
    count = 0
    for pair in vote_dict:
        #check if majority vote is right
        maj_vote_idxs = np.argwhere(vote_dict[pair] == np.amax(vote_dict[pair])).flatten().tolist()
        #if tie then don't consider it
        if len(maj_vote_idxs) > 1:
            continue
        #skip if unsure
        if maj_vote_idxs[0] == 2:
            continue
        else:
            count += 1
            print(pair, vote_dict[pair])
            #check if correct, by design answer B is always correct
            if maj_vote_idxs[0] == 1:
                correct += 1
            else:
                incorrect += 1
                
            
    return correct / count, incorrect / count

if __name__=="__main__":
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument('--env_name', default='', help='Select model, i.e. spaceinvaders')
    parser.add_argument('--checkpoint_to_score', default='', help="checkpoint_to_score")
    parser.add_argument('--turk_batch', default = '', help = 'turk csv file from batch')
    args = parser.parse_args()
    env_name = args.env_name
    checkpoint_filename = args.checkpoint_to_score
    turk_batch_filename = args.turk_batch #"Batch_3624797_batch_results.csv"
    checkpoints_to_scores = parse_checkpoint_to_scores(checkpoint_filename)
    ranking_dict = parse_turk_responses(turk_batch_filename, env_name)
    print(ranking_dict)
    pos_accuracy, neg_accuracy = evaluate_accuracy_majority(checkpoints_to_scores, ranking_dict)
    print("% correct = ", pos_accuracy)
    print("% incorrect = ", neg_accuracy)
    print("% not sure = ", 1 - pos_accuracy - neg_accuracy)
    
    


#from numpy import genfromtxt
#my_data = genfromtxt('inputbreakout_pref_mturk.csv', delimiter=',')
#print(my_data)
