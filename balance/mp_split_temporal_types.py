import json
import pickle
import sys

from multiprocessing import Process

with open('../data/template_ids.txt') as json_file:
    templ_ids_dict = json.load(json_file)

templ_ids = []

for i in templ_ids_dict:
    templ_ids.append(i)

with open('../data/train_video_names.txt', 'rb') as f:
    train_stsgs = json.load(f)


with open('../data/test_video_names.txt', 'rb') as f:
    test_stsgs = json.load(f)

QA = {}


def getQ(q_id):
    v_id = q_id.split("-")[0]
    return QA[v_id][q_id]


def qaTotal():
    total = 0
    for v_id in QA:
        total = total + len(QA[v_id])
    print("QA Total: ", total)


def printLens(dic, name):
    print()
    print(name)
    total = 0
    for i in dic:
        print(i, len(dic[i]))
        total = total + len(dic[i])
    print("TOTAL: ", total)


def pickleDump(var, destination):
    f = open(destination, "wb")
    pickle.dump(var, f)
    f.close()


def pickleLoad(path):
    file = open(path, 'rb')
    info = pickle.load(file)
    file.close()
    return info


def dumpMetrics(var, title, d_path, group, balanced):
    if type(balanced) == bool:
        print("in dump metrics, balanced should be text")
        return
    path = '../exports/%s/metrics/%s/%s/%s.pkl' % (d_path, balanced, group, title)

    pickleDump(var, path)


def loadMetrics(title, d_path, group, balanced):
    if type(balanced) == bool:
        print("balanced should be text")
        return
    path = '../exports/%s/metrics/%s/%s/%s.pkl' % (d_path, balanced, group, title)

    return pickleLoad(path)


def getVideoIDS(group):
    if group == 'train':
        return list(train_stsgs)
    elif group == 'test':
        return list(test_stsgs)


def loadJSON(path):
    with open(path) as json_file:
        QA = json.load(json_file)
    return QA


def getVideoQA(d_path, group, balanced, v_id):
    if type(balanced) == bool:
        print("balanced should not be bool")
    QA = loadJSON('../exports/%s/%s/%s/%s.txt' % (d_path, balanced, group, v_id))


    return QA


# Indirect Ref Consistency
def getIndirectRefConsistencyTime(d_path, group, balanced, start, stop):
    if type(balanced) == bool:
        print("balanced should be text")
        return

    same_direct = {}
    comp = {}

    video_ids = getVideoIDS(group)
    # inspect_direct = None
    for cnt, v_id in enumerate(video_ids):
        if cnt < start:
            cnt = cnt + 1
            continue
        if cnt >= stop:
            break

        if cnt % 50 == 0:
            print('done', cnt)

        comp[v_id] = {}

        QA = getVideoQA(d_path, group, balanced, v_id)
        same_direct[v_id] = {}
        for i in templ_ids:
            same_direct[v_id][i] = {}

        for q_id in QA:
            q = QA[q_id]
            t_id = q['attributes']['type']
            indirects = q['metrics']['indirects']

            direct = q['metrics']['direct_args']

            sd_templ = same_direct[v_id][t_id]

            if direct not in sd_templ:
                sd_templ[direct] = {}
                sd_templ[direct]['all'] = []
                sd_templ[direct]['no_time'] = []
                sd_templ[direct]['time'] = []

            sd_templ[direct]['all'].append(q_id)

            if indirects[3]:
                sd_templ[direct]['time'].append(q_id)
                # inspect_direct = direct
            else:
                sd_templ[direct]['no_time'].append(q_id)

        for templ in same_direct[v_id]:
            sd_templ = same_direct[v_id][templ]
            for direct in sd_templ:
                thing = sd_templ[direct]
                no_time = thing['no_time']

                if len(no_time) > 0:
                    no_time_ans = QA[no_time[0]]['answer']
                else:
                    no_time_ans = "None without time"

                time = thing['time']
                for q_id in time:
                    q_ans = QA[q_id]['answer']
                    if no_time_ans == "None without time":
                        comp[v_id][q_id] = 'no_direct'
                    elif no_time_ans == q_ans:
                        comp[v_id][q_id] = 'same_ans'
                    else:
                        comp[v_id][q_id] = 'diff_ans'

                for q_id in thing['no_time']:
                    q_ans = QA[q_id]['answer']
                    comp[v_id][q_id] = 'no_temporal'


    print("Saving temporal change ans in ../exports/%s/metrics/%s/%s/temporalChangeAns-%s-%s.txt" % (d_path, balanced, group, start, stop))
    with open('../exports/%s/metrics/%s/%s/temporalChangeAns-%s-%s.txt' % (d_path, balanced, group, start, stop), 'w+') as f:
        json.dump(comp, f)
    f.close()

    print("Saving direct change ans in ../exports/%s/metrics/%s/%s/same-direct-%s-%s.txt" % (d_path, balanced, group, start, stop))
    with open('../exports/%s/metrics/%s/%s/same-direct-%s-%s.txt' % (d_path, balanced, group, start, stop), 'w+') as f:
        json.dump(same_direct, f)
    f.close()

    return same_direct, comp


if __name__ == '__main__':
    print("done imports")
    group = sys.argv[1:][0]
    balanced = sys.argv[1:][1]
    step = sys.argv[1:][2]
    d_path = 'dataset'
    print("starting mp with group", group, "dpath", d_path)
    jobs = []
    if group == 'test':
        ranges = [(0, 303), (303, 555), (555, 807), (807, 1059),
                  (1059, 1311), (1311, 1563), (1563, 1814)]
    elif group == 'train':
        ranges = [(0, 2220), (2220, 4440), (4440, 6660), (6660, 7787)]
    else:
        print("Invalid group", group)

    #ranges = [(0, 5), (5, 10), (10, 15), (15, 20)]
    comb = {}
    for r in ranges:
        if step == 'get_time':
            p = Process(target=getIndirectRefConsistencyTime, args=(d_path, group, balanced, r[0], r[1],))
            jobs.append(p)
            p.start()
        elif step == 'combine':
            with open('../exports/%s/metrics/%s/%s/temporalChangeAns-%s-%s.txt' % (d_path, balanced, group, r[0], r[1]), 'rb') as f:
                info = json.load(f)
            comb.update(info)

    if step == 'combine':
        with open('../exports/%s/metrics/%s/%s/temporalChangeAns.txt' % (d_path, balanced, group), 'w+') as f:
            json.dump(comb, f)