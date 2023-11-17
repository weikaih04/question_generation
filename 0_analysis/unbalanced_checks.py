from multiprocessing import Process
import sys
import json
import pickle


with open('../data/train_video_names.txt', 'rb') as f:
    train_stsgs = json.load(f)

with open('../data/test_video_names.txt', 'rb') as f:
    test_stsgs = json.load(f)

with open('../data/stsgs/train_stsgs.pkl', 'rb') as f:
    train_stsgs_complete= pickle.load(f)

with open('../data/stsgs/test_stsgs.pkl', 'rb') as f:
    test_stsgs_complete = pickle.load(f)

with open('../data/eng.pkl', 'rb') as f:
    ENG = pickle.load(f)

with open('../data/templ2global.txt', 'rb') as f:
    templ2global = json.load(f)


def getVideos(group, start=0, stop=99999):
    if group == 'test':
        return test_stsgs[start:stop]
    elif group == 'train':
        return train_stsgs[start:stop]
    else:
        print("Incorrect group %s" % group)


def getQA(d_path, bal, group, v):
    with open('../exports/%s/%s/%s/%s.txt' % (d_path, bal, group, v), 'rb') as f:
        QA = json.load(f)

    return QA


def getTemp(q):
    return q['attributes']['type']


def getQuestions(d_path, bal, group, start=0, stop=99999):
    videos = getVideos(group, start, stop)
    qs = []

    for v in videos:
        QA = list(getQA(d_path, bal, group, v).values())
        for q in QA:
            q['video_id'] = q['id'][:5]
            q['global'] = templ2global[getTemp(q)]
        qs += QA

    return qs


def add(dic, cat, item):
    if cat not in dic:
        dic[cat] = {}

    if item not in dic[cat]:
        dic[cat][item] = 0

    dic[cat][item] += 1


def getByTemplate(all_qs):
    by_t = {}

    for q in all_qs:
        t = getTemp(q)
        if t not in by_t:
            by_t[t] = []

        by_t[t].append(q)

    return by_t


def getByProgram(all_qs):
    by_p = {}

    for q in all_qs:
        v_id = q['video_id']
        p = q['program']

        if v_id not in by_p:
            by_p[v_id] = {}

        if p not in by_p[v_id]:
            by_p[v_id][p] = []

        by_p[v_id][p].append(q)

    return by_p


def noRepeatingPrograms(by_p):
    for v_id in by_p:
        ps = by_p[v_id]

        for p in ps:
            if len(ps[p]) > 1:
                print("Repeating %s in video %s" % (p, v_id))
                raise(Exception("Repeating %s in video %s" % (p, v_id)))


def equalParentheses(by_p):
    # checks if the number of "(" and ")" parentheses are the same
    for v_id in by_p:
        ps = by_p[v_id]
        for p in ps:
            start_cnt = p.count('(')
            end_cnt = p.count(')')
            if start_cnt != end_cnt:
                raise(Exception("Inequal parentheses in %s, %s" % (p, v_id)))


def checkPrograms(all_qs, s, e):
    # separate by program
    by_p = getByProgram(all_qs)

    tryTest(noRepeatingPrograms, by_p, 'No Repeating Programs', s, e)
    tryTest(equalParentheses, by_p, 'Equal number of parentheses', s, e)


def validSGIndices(all_qs):
    for q in all_qs:
        sg = q['sg_grounding']
        q_len = len(q['question'])
        for x in sg:
            s, e = x.split('-')

            for i in [int(s), int(e)]:
                if i < 0:
                    raise(Exception("Negative scene graph indices"))

                if i >= q_len:
                    raise(Exception("Too large scene graph indices"))


def validSGVertices(args):
    all_qs, group = args

    if group == 'train':
        all_stsgs = train_stsgs_complete
    elif group == 'test':
        all_stsgs = test_stsgs_complete
    else:
        print('invalid group: ', group)
        return

    stsgs = {}
    for v_id in all_stsgs:
        stsgs[v_id] = []
        old_sg = all_stsgs[v_id]
        new_sg = stsgs[v_id]

        new_sg += old_sg['ordered_frames']
        new_sg += list(old_sg['stsg']['actions'].keys())
        new_sg += list(old_sg['stsg']['objects'].keys())
        new_sg += list(old_sg['stsg']['contact'].keys())
        new_sg += list(old_sg['stsg']['spatial'].keys())
        new_sg += list(old_sg['stsg']['verb'].keys())

    for q in all_qs:
        grounding = q['sg_grounding']
        sg = stsgs[q['id'][:5]]
        for x in grounding:
            refs = grounding[x]
            for r in refs:
                if r not in sg:
                    raise(Exception("References nonexistent vertex"))


def internalKeyMatches(args):
    d_path, group, bal, s, e = args
    for v_id in getVideos(group, start=s, stop=e):
        QA = getQA(d_path, bal, group, v_id)

        for q_id in QA:
            i = QA[q_id]['id']
            if i != q_id:
                raise(Exception("Key does not match internal key"))


def localMatchesDirect(args):
    d_path, group, bal, s, e = args
    for v_id in getVideos(group, start=s, stop=e):
        QA = getQA(d_path, bal, group, v_id)

        for q_id in QA:
            q = QA[q_id]

            # objwhat general they're different but its ok
            if getTemp(q) in ['objWhatGeneral', 'actWhatBefore', 'actWhatAfterAll', 'actFirst', 'actLast']:
                continue

            loc = q['local']
            direct = q['metrics']['direct_args']

            if loc != direct:
                print("local does not match direct: %s" % q_id)
                raise(Exception("Local does not match direct"))


def tryTest(func, args, message, s, e):
    # check no repeating programs
    try:
        func(args)
        print("PASSED: (%s-%s) %s" % (s, e, message))
    except Exception:
        print("FAILED: (%s-%s) %s" % (s, e, message))


def unbalancedChecks(d_path, group, s, e):
    bal = 'all'
    all_qs = getQuestions(d_path, bal, group, start=s, stop=e)
    checkPrograms(all_qs, s, e)
    tryTest(validSGIndices, all_qs, 'Valid scene graph indices', s, e)
    tryTest(validSGVertices, [all_qs, group], 'Valid scene graph indices', s, e)
    tryTest(internalKeyMatches, [d_path, group, bal, s, e],
            "Key Matches Internal Key", s, e)
    tryTest(localMatchesDirect, [d_path, group, bal, s, e],
            "Local Matches Direct", s, e)


if __name__ == '__main__':
    group = sys.argv[1:][0]
    d_path = 'dataset'
    print("Unbalanced checks for group:", group)

    jobs = []
    if group == 'test':
        ranges = [(0, 303), (303, 555), (555, 807), (807, 1059),
                  (1059, 1311), (1311, 1563), (1563, 1814)]
        ranges = [(5, 10), (10, 15), (15, 20), (20, 25), (25, 30)]
    elif group == 'train':
        ranges = [(0, 1110), (1110, 2220), (2220, 3330), (3330, 4440),
                  (4440, 5550), (5550, 6660), (6660, 7787)]

    else:
        print("Invalid group", group)

    for r in ranges:
        p = Process(target=unbalancedChecks, args=(d_path, group, r[0], r[1]))
        jobs.append(p)
        p.start()
