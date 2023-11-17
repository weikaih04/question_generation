from multiprocessing import Process
import sys
import json
import pickle
import math


#infile = open('../data/test_videos_stsg.pkl', 'rb')
infile = open('../data/stsgs/test_stsgs.pkl', 'rb')
test_stsgs = pickle.load(infile)
infile.close()

def decombineSubsampleTrain(num_splits, file, mult):
    with open('../exports/dataset/json_format_all/train_unbalanced_subset-%s.txt' % file, 'rb') as f:
        sampled_qs = json.load(f)

    num = len(sampled_qs)
    print("%s: Length of %s" % (file, num))

    split = math.floor(num / num_splits)
    
    for i in range(num_splits):
        low = split * i
        high = split * (i + 1)
        
        sampled_qs_subset = {}
        
        sampled_ids = list(sampled_qs)[low:high]
        print('length of sampled ids: %s when split %s to %s' % (len(sampled_ids), low, high))
        for id in sampled_ids:
            sampled_qs_subset[id] = sampled_qs[id]
        print("%s: Got indices %s to %s which is of length %s" % (file, low, high, len(sampled_qs_subset)))
        new_file_name = (i + 1) + (num_splits * mult)
        print("go to file ../exports/dataset/json_format_all/train_unbalanced_subset-%s.txt" % new_file_name)

        with open('../exports/dataset/json_format_all/train_unbalanced_subset-%s.txt' % new_file_name, 'w+') as f:
            json.dump(sampled_qs_subset, f)



def combineSubsampleTest(start, stop, size, idx):
    with open('../exports/dataset/json_format_all/test/unbalanced_subset_test_q_ids.txt', 'rb') as f:
        test_indexes = json.load(f)

    by_vid_te = {}
    for q_id in test_indexes:
        v = q_id[:5]
        if v not in by_vid_te:
            by_vid_te[v] = []
        by_vid_te[v].append(q_id)

    v_by_g_te = {}
    sampled_qs_te = {}
        
    for i in range(start, stop, size):
        print(i, len(sampled_qs_te))
        larger = i + size
        if i + larger == 1800:
            larger = 1814
        v_by_g_te[(i, larger)] = list(test_stsgs)[i:larger]
        
        with open('../exports/dataset/json_format_all_combined/test/test-%s-%s.txt' % (i, larger), 'rb') as f:
            x = json.load(f)
        
        for v_id in v_by_g_te[(i, larger)]: 
            for q_id in by_vid_te[v_id]:
                sampled_qs_te[q_id] = x[q_id]

    new_idx = idx + 1
    print("dumping: ../exports/dataset/json_format_all/test_unbalanced_subset-%s.txt" % new_idx)
    with open('../exports/dataset/json_format_all/test_unbalanced_subset-%s.txt' % new_idx, 'w+') as f:
        json.dump(sampled_qs_te, f)
        


if __name__ == '__main__':
    print("done imports")
    group = sys.argv[1:][0]
    version = sys.argv[1:][1]
    jobs = []
    if group == 'test':
        ranges = [(0, 300, 100, 0),(300, 700, 100, 1),(700, 1000, 50, 2),(1000, 1300, 50, 3),(1300, 1600, 50, 4),(1600, 1900, 50, 5)]
        ranges = [(500, 600, 100, 6),(1600, 1900, 50, 5), (600, 700, 50, 7)]
        
    elif group == 'train' or group == 'practice':
        ranges = [(4, 'a', 0),(4, 'b', 1)]
    
    else:
        print("Invalid group", group)

    for r in ranges:
        if version == 'combine':
            p = Process(target=combineSubsampleTest, args=(r[0], r[1], r[2], r[3],))
        if version == 'de-combine':
            p = Process(target=decombineSubsampleTrain, args=(r[0], r[1],r[2]))
        jobs.append(p)
        p.start()
