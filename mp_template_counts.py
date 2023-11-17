
import json
import pickle
import sys

from multiprocessing import Process
from os import listdir
from os.path import isfile, join

#infile = open('../data/stsgs/test_stsgs.pkl', 'rb')
#test_stsgs = pickle.load(infile)
#infile.close()

#infile = open('../data/stsgs/train_stsgs.pkl', 'rb')
#train_stsgs = pickle.load(infile)
#infile.close()

train_path = '../exports/dataset/balanced/train/'
train_stsgs = [f for f in listdir(train_path) if isfile(join(train_path, f))]
train_stsgs = [i[:5] for i in train_stsgs]

test_path = '../exports/dataset/balanced/test/'
test_stsgs = [f for f in listdir(test_path) if isfile(join(test_path, f))]
test_stsgs = [i[:5] for i in test_stsgs]



with open('../data/templ2global.txt', 'r') as f:
    templ2global = json.load(f)

templs = list(templ2global.keys())


def loadJSON(path):
    with open(path) as json_file:
        QA = json.load(json_file)
    return QA


def dumpJSON(data, path):
    with open(path, 'w+') as json_file:
        json.dump(data, json_file)


def getVideoQA(d_path, group, balanced, v_id):
    if type(balanced) == bool: 
        print("balanced should not be bool")
    #if balanced == 'templ':
    QA = loadJSON('../exports/%s/%s/%s/%s.txt' % (d_path, balanced, group, v_id))
        
    return QA


def dumpData(data, d_path, group, balanced, start, stop):
    QA = dumpJSON(data, 'templ_counts/%s/%s-%s-%s.txt' % (balanced, group, start, stop))
        
    return QA


num_qs = []

def getVideoIDS(group):
    if group == 'train':
        return list(train_stsgs)
    elif group == 'test':
        return list(test_stsgs)


def templates(d_path, group, balanced, start, stop):
    video_ids = getVideoIDS(group)

    templates = {i: 0 for i in templs}

    print('getting from: ../exports/%s/%s/%s/' % (d_path, balanced, group))

    for cnt, v_id in enumerate(video_ids):
        if cnt < start:
            cnt = cnt + 1
            continue
        if cnt >= stop:
            break

        QA = getVideoQA(d_path, group, balanced, v_id)

        for q_id in QA:
            templates[QA[q_id]['attributes']['type']] += 1


    dumpData(templates, d_path, group, balanced, start, stop)



if __name__ == '__main__':
    print("done imports")
    group = sys.argv[1:][0]
    balanced = sys.argv[1:][1]
    d_path = 'dataset'
    print("starting mp with group", group, "dpath", d_path)
    jobs = []
    if group == 'test':
        ranges = [(0, 303), (303, 555), (555, 807), (807, 1059), (1059, 1311), (1311, 1563), (1563, 1814)]
    elif group == 'train':
        ranges = [(0, 1110), (1110, 2220), (2220, 3330), (3330, 4440), (4440, 5550), (5550, 6660), (6660, 7787)]
    else:
        print("Invalid group", group)

    comb = {}
    for r in ranges:
        p = Process(target=templates, args=(d_path, group, balanced, r[0], r[1],))
        jobs.append(p)
        p.start()

