
import json
import pickle
import sys
import pandas as pd

from multiprocessing import Process




def getCSV(d_path, x):
    train = pd.read_csv('../../exports/%s/final_csvs/%s-%s.csv' % (d_path, 'train', x))
    val = pd.read_csv('../../exports/%s/final_csvs/%s-%s.csv' % (d_path, 'valid', x))
    train = pd.concat([train, val])
    test = pd.read_csv('../../exports/%s/final_csvs/%s-%s.csv' % (d_path, 'test', x))
    total = pd.read_csv('../../exports/%s/final_csvs/%s-%s.csv' % (d_path, 'total', x))
    
    return train, test, total


def getTXT(x, train, test, total):
    if x == 'balanced':
        return train, test, total
    elif x == 'compo':

        train_compo = {}
        for i in train:
            q = train[i]
            if q['novel_comp'] == 0:
                train_compo[i] = q
                
        test_compo = {}
        for i in test:
            q = test[i]
            if q['novel_comp'] == 1:
                test_compo[i] = q
        total_compo = {}
        total_compo.update(train_compo)
        total_compo.update(test_compo)
        return train_compo, test_compo, total_compo
    elif x == 'steps':
        train_steps = {}
        for i in train:
            q = train[i]
            if q['more_steps'] == 0:
                train_steps[i] = q
        
        test_steps = {}
        for i in test:
            q = test[i]
            if q['more_steps'] == 1:
                test_steps[i] = q

        total_steps = {}
        total_steps.update(train_steps)
        total_steps.update(test_steps)

        return train_steps, test_steps, total_steps
    else:
        print('invalid type %s' % x)


def byV(ids):
    by_v = {}
    for i in ids:
        v = i[:5]
        if v not in by_v:
            by_v[v] = []
        by_v[v].append(i)
    return by_v


def keysMatch(csv, txt, start, stop):
    csv_keys = list(csv['key'].values)
    txt_keys = list(txt.keys())

    csv_byv = byV(csv_keys)
    txt_byv = byV(txt_keys)

    if start > len(csv_keys):
        print("              skipping range because unnecessary: %s-%s" % (start, stop))
        return
    
    csv_keys_to_check = csv_keys[start:stop]
    txt_keys_to_check = txt_keys[start:stop]


    
    if len(csv_keys) != len(txt_keys):
        print("ERROR not same size")
        return False
    if len(csv_keys_to_check) != len(txt_keys_to_check):
        print("ERROR subset not same size")
        return False
    # make sure all in csv are in txt
    for k in csv_keys_to_check:
        v = k[:5]
        if k not in txt_byv[v]:
            print('%s not in txt keys' % k)
            return False
    
    # make sure all in txt are in csv
    for k in txt_keys_to_check:
        v = k[:5]
        if k not in csv_byv[v]:
            print('%s not in csv keys' % k)
            return False
    return True


def checkRange(metric, start, stop, names, csvs, txts):
    for name, csv, txt in zip(names, csvs, txts):
        print("%s: %s-%s %s keys match" % (keysMatch(csv, txt, start, stop), start, stop, name))



if __name__ == '__main__':
    print("done imports")
    metric = sys.argv[1:][0]
    d_path = 'dataset'
    print("starting mp with metric", metric, "dpath", d_path)
    jobs = []

    
    #ranges = [(0, 303), (303, 555), (555, 807), (807, 1059), (1059, 1311), (1311, 1563), (1563, 1814)]
    if metric == 'balanced':
        ranges = [(0, 454020), (454020, 908040), (908040, 1362060), (1362060, 1816080), (1816080, 2270102)]
    elif metric == 'compo':
        ranges = [(0, 303027), (303027, 606054), (606054, 909081), (909081, 1212108), (1212108, 1515140)]
    elif metric == 'steps':
       ranges = [(0, 298406), (298406, 596812), (596812, 895218), (895218, 1193624), (1193624, 1492034)]
    else:
        print("invalid metric %s" % metric)

    # Load train and test
    with open('../../exports/%s/json_format_balanced_combined/test-0-1814.txt' % (d_path), 'rb') as f:
        test = json.load(f)
        
    with open('../../exports/%s/json_format_balanced_combined/train-0-7787.txt' % (d_path), 'rb') as f:
        train = json.load(f)
        
    total = {}
    total.update(train)
    total.update(test)

    names = ['train', 'test', 'total']
    csvs = getCSV(d_path, metric)
    txts = getTXT(metric, train, test, total)

    comb = {}
    for r in ranges:
        p = Process(target=checkRange, args=(metric, r[0], r[1], names, csvs, txts))
        jobs.append(p)
        p.start()

