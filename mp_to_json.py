import json
import pickle
import grammar
import sys

from multiprocessing import Process

def pickleLoad(path):
    file = open(path, 'rb')
    info = pickle.load(file)
    file.close()
    return info

infile = open('../data/stsgs/test_stsgs.pkl', 'rb')
test_stsgs = pickle.load(infile)
infile.close()

infile = open('../data/stsgs/train_stsgs.pkl', 'rb')
train_stsgs = pickle.load(infile)
infile.close()

# TODO when have trained need to update here
train_steps_templ = pickleLoad('../exports/dataset/metrics/balanced/train/steps_by_templ.pkl')
test_steps_templ = pickleLoad('../exports/dataset/metrics/balanced/test/steps_by_templ.pkl')



IDX = grammar.IDX
ENG = grammar.ENG
PP = grammar.PP
ART = grammar.ART
vType = grammar.vType
art = grammar.art
pres = grammar.pres
past = grammar.past
pp = grammar.pp


''' id: {
    question: "This is the question?", 
    'answer': 'answer', 
    'videoID': XXXXX, 
    global: templ2glob,
    local: converted str,
    semantic: converted str,
    structural: str,
    novel_comp: 1,
    nc_seq: 1,
    nc_sup: 0, 
    nc_dur: 0,
    nc_objrel: 0,
    indirect: 1, 
    i_obj: 1,
    i_rel: 0, 
    i_act: 0,
    i_temp: 0, 
    more_compo: 0,
    ans_type: translate Type,
    steps: 9,
    direct_counterpart': 'q_ID'
 }
'''

# IF the template is relfirst, delete

# add in correct globals

# make local direct args --- nooo make it the thing iused for balancing

## here I'm putting all the novel compo together

# everything that i did for the csv

# move the attributes stuff here

# if semantic is objrel --> relation


def getQA(bal, group, v_id):
    with open('../exports/dataset/%s/%s/%s.txt' % (bal, group, v_id), 'rb') as f:
        test_qs = json.load(f)
    return test_qs


def dumpQA(QA, bal, group, v_id):
    with open('../exports/dataset/%s/%s/%s.txt' % (bal, group, v_id), 'w+') as f:
        json.dump(QA, f)
    return


def getSTSGS(group):
    if group == 'train':
        return train_stsgs, train_steps_templ
    elif group == 'test':
        return test_stsgs, test_steps_templ
    else:
        print('invalid group', group)
        return


with open('../data/templ2global.txt', 'rb') as f:
    templ2global = json.load(f)


def translateType(q):
    x = q['attributes']['structural']
    if x == 'query':
        return 'open'
    elif x in ['choose', 'compare', 'logic', 'verify']:
        return 'binary'
    else:
        print('a question does not have a good structural to translate into binary: ', q)


# TODO this is like a last minute comment please play attention
# gotta make sure this is consistent with balancing!!!
# esp if changed things in balancing idk
def getBinaryCat(q):
    t = q['attributes']['type']

    # first find local
    if t == 'actCountChooseMore':
        local = "more"
    elif t == 'actCountChooseFewer':
        local = 'fewer'
    elif t == 'actLengthLongerChoose':
        local = 'longer'
    elif t == 'actLengthShorterChoose':
        local = 'shorter'
    else:
        local = q['local']

    # then find answers
    a = q['answer']
    if a == "Yes" or a == "No":
        ans = 'yes-no'
    elif a == 'before' or a == 'after':
        ans = 'before-after'
    elif t in ['actCountChooseMore', 'actCountChooseFewer',
               'actLengthLongerChoose', 'actLengthShorterChoose']:
        ans = q['local']
    else:
        ans = q['metrics']['direct_args']

    time0, time1 = q['metrics']['direct_time']
    category = "%s-%s-%s-%s" % (ans, local, time0, time1)

    category_sp = category.split("-")

    category = ''

    for i in category_sp:
        category += i + '-'

    return category[:-1]


def getDirect(q_id): 
    if q_id in to_direct:
        return to_direct[q_id]
    else:
        return


def getLocal(q):
    if translateType(q) == 'binary':
        return getBinaryCat(q)
    else:
        return q['local']


def translateSemantic(q):
    if q['attributes']['semantic'] == 'objrel':
        return 'relation'
    else:
        return q['attributes']['semantic']


def mark(x):
    if x:
        return 1
    return 0


def getMoreCompo(q, q_id, steps_templ):
    v_id = q['attributes']['video_id']
    m = steps_templ['more']
    if v_id not in m:
        return 0
    return mark(q_id in m[v_id])


def updateQuestions(group, bal, save, start, stop, to_direct):
    stsgs, steps_templ = getSTSGS(group)
    print('doing group ', start, stop, 'withsave', save)
    for i, v_id in enumerate(stsgs):
        if i < start:
            continue
        if i >= stop:
            break

        if i % 100 == 0:
            print(i, v_id)
        QA = getQA(bal, group, v_id)

        newQA = {}
        for q_id in QA:
            q = QA[q_id]
            tp = q['attributes']['type']
            if tp == 'relFirst':
                continue
    
            metrics = q['metrics']
            nc = metrics['novel_comp']

            new_q = {
                'question': q['question'],
                'answer': q['answer'].lower(), 
                'video_id': q['attributes']['video_id'],
                'global': templ2global[tp],
                'local': getLocal(q),
                'ans_type': translateType(q), 
                'steps': q['steps'],
                'semantic': translateSemantic(q),
                'structural': q['attributes']['structural'],
                'novel_comp': mark(nc.count(True) > 0),
                'more_steps': getMoreCompo(q, q_id, steps_templ),
                'program': q['program'],
                'sg_grounding': q['sg_grounding']
            }

            if group == 'test':
                indir = metrics['indirects']
                test_info = {
                    'nc_seq': mark(nc[0]),
                    'nc_sup': mark(nc[1]), 
                    'nc_dur': mark(nc[2]),
                    'nc_objrel': mark(nc[4]),
                    'indirect': mark(indir.count(True) > 0),
                    'i_obj': mark(indir[0]),
                    'i_rel': mark(indir[1]), 
                    'i_act': mark(indir[2]),
                    'i_temp': mark(indir[3]), 
                    'direct_equiv': getDirect(q_id),
                }
                new_q.update(test_info)

            newQA[q_id] = new_q
        if save == 'save':
            path = 'json_format_' + bal
            dumpQA(newQA, path, group, v_id)
    return


def dumpQAcombo(QA, bal, group, start, stop):
    with open('../exports/dataset/%s/%s-%s-%s.txt' % (bal, group, start, stop), 'w+') as f:
        json.dump(QA, f)
    return


def combineFiles(group, bal, save, start, stop, to_direct): 
    newQA = {}
    stsgs, _ = getSTSGS(group)
    print('doing group ', start, stop, 'withsave', save)

    for i, v_id in enumerate(stsgs):
        if i < start:
            continue
        if i >= stop:
            break

        if i % 25 == 0:
            print(i, v_id)

        path = 'json_format_' + bal
        QA = getQA(path, group, v_id)

        newQA.update(QA)

    
    if save == 'save':
        print("saving questions of length: ", len(newQA))
        path = 'json_format_' + bal + '_combined'
        dumpQAcombo(newQA, path, group, start, stop)
        print("done saving: ", path, start, stop)



if __name__ == '__main__':
    print("done imports")
    group = sys.argv[1:][0]
    balanced = sys.argv[1:][1]
    save = sys.argv[1:][2]
    stage = sys.argv[1:][3]
    idx = int(sys.argv[1:][4])

    d_path = 'dataset'


    print("starting mp with group", group, "dpath", d_path, ' balanced ', balanced, ' save ', save, ' stage ', stage)
    jobs = []
    if group == 'test':
        print('in TODIRECT')
        with open('../exports/%s/to_direct.txt' % d_path, 'rb') as f:
            to_direct = json.load(f)
        
        #ranges = [(0, 303), (303, 555), (555, 807), (807, 1059), (1059, 1311), (1311, 1563), (1563, 1814)]
        #ranges = [(0, 303), (303, 807), (807, 1311), (1311, 1814)]
        if stage == 'questions':
            ranges = [(0, 303), (303, 555), (555, 807), (807, 1059), (1059, 1311), (1311, 1563), (1563, 1814)]
            # ranges = [(0, 5)]
        
            #ranges = [(0, 607), (607, 1207), (1207, 1814)]
        elif stage == 'combine' and balanced == 'all':
            #ranges = [(0, 303), (303, 555), (555, 807), (807, 1059)] 
            #ranges = [(1059, 1311), (1311, 1563), (1563, 1814)]

            if idx == 0: 
                ranges = [(0, 50), (50, 100), (100, 150)]
            if idx == 1: 
                ranges = [(150, 200), (200, 250), (250, 300)]
            if idx == 2: 
                ranges = [(300, 350), (350, 400), (400, 450)]
            if idx == 3: 
                ranges = [(450, 500), (500, 550), (550, 600)]
            if idx == 4: 
                ranges = [(600, 650), (650, 700), (700, 750)]
            if idx == 5: 
                ranges = [(750, 800), (800, 850),(1750, 1814)]
            if idx == 6: 
                ranges = [(850, 900), (900, 950), (950, 1000)]
            if idx == 7: 
                ranges = [(1000, 1050), (1050, 1100), (1100, 1150)]
            if idx == 8: 
                ranges = [(1150, 1200), (1200, 1250), (1250, 1300)]
            if idx == 9: 
                ranges = [(1300, 1350), (1350, 1400), (1400, 1450)]
            if idx == 10: 
                ranges = [(1450, 1500), (1500, 1550), (1550, 1600)]
            if idx == 11: 
                ranges = [(1600, 1650), (1650, 1700), (1700, 1750)]
        elif stage == 'combine' and 'balanced' in balanced:
            print('ranges is doing the thing')
            ranges = [(0, 907), (907, 1814)]
            ranges = [(0, 1814)]
            #ranges = [(0, 5)]
    elif group == 'train':
        to_direct = None
        if stage == 'questions':
            ranges = [(0, 1110), (1110, 2220), (2220, 3330), (3330, 4440), (4440, 5550), (5550, 6660), (6660, 7787)]
            #ranges = [(500, 1110), (1500, 2220), (2700, 3330), (3700, 4440), (4900, 5550), (6100, 6660), (7300, 7787)]
            #ranges = [(0, 2220), (2220, 4440), (4440, 6660), (6660, 7787)]
            #ranges = [(400, 475), (475, 550), (550, 625), (625, 700), (700, 750), (750, 800)]
        elif stage == 'combine' and 'balanced' in balanced:
            ranges = [(0, 7787)]
        elif stage == 'combine' and balanced == 'all':
            num = idx * 300
            ranges = []
            for i in range(6):
                ranges.append((num, num + 50))
                num += 50
            #ranges = [(), (), (), ()]
            #if num == 7500:
            #    ranges = [(7500, 7550), (7550, 7600), (7600, 7650), (7650, 7700), (7700, 7750), (7750, 7800)]
            if False:
                if idx == 0: 
                    ranges = [(0, 50), (50, 100), (100, 150), (150, 200)]
                if idx == 0: 
                    ranges = [(200, 250), (250, 300), (300, 350), (350, 400)]
                if idx == 1: 
                    ranges = [(400, 450), (450, 500), (500, 550), (550, 600)]
                if idx == 1: 
                    ranges = [(600, 650), (650, 700), (700, 750), (750, 800)]
                if idx == 2: 
                    ranges = [(800, 900), (900, 1000), (1000, 1100), (1100, 1200)]
                if idx == 2: 
                    ranges = [(800, 900), (900, 1000), (1000, 1100), (1100, 1200)]
                if idx == 3: 
                    ranges = [(1200, 1300), (1300, 1400), (1400, 1500), (1500, 1600)]
                if idx == 4: 
                    ranges = [(1600, 1700), (1700, 1800), (1800, 1900), (1900, 2000)]
                if idx == 5: 
                    ranges = [(2000, 2100), (2100, 2200), (2200, 2300), (2300, 2400)]
                if idx == 6: 
                    ranges = [(2400, 2500), (2500, 2600), (2600, 2700), (2700, 2800)]
                if idx == 7: 
                    ranges = [(2800, 2900), (2900, 3000), (3000, 3100), (3100, 3200)]
                if idx == 8: 
                    ranges = [(3200, 3300), (3300, 3400), (3400, 3500), (3500, 3600)]
                if idx == 9: 
                    ranges = [(3600, 3700), (3700, 3800), (3800, 3900), (3900, 4000)]
                if idx == 10: 
                    ranges = [(4000, 4100), (4100, 4200), (4200, 4300), (4300, 4400)]
                if idx == 11: 
                    ranges = [(4400, 4500), (4500, 4600), (4600, 4700), (4700, 4800)]
                if idx == 12: 
                    ranges = [(4800, 4900), (4900, 5000), (5000, 5100), (5100, 5200)]
                if idx == 13: 
                    ranges = [(5200, 5300), (5300, 5400), (5400, 5500), (5500, 5600)]
                if idx == 14: 
                    ranges = [(5600, 5700), (5700, 5800), (5800, 5900), (5900, 6000)]
                if idx == 15: 
                    ranges = [(6000, 6100), (6100, 6200), (6200, 6300), (6300, 6400)]
                if idx == 16: 
                    ranges = [(6400, 6500), (6500, 6600), (6600, 6700), (6700, 6800)]
                if idx == 17: 
                    ranges = [(6800, 6900), (6900, 7000), (7000, 7100), (7100, 7200)]
                if idx == 18: 
                    ranges = [(7200, 7300), (7300, 7400), (7400, 7500), (7500, 7600)]
                if idx == 19: 
                    ranges = [(7600, 7700), (7700, 7800)]
    else:
        print("Invalid group", group)

    for r in ranges:
        if stage == 'questions':
            p = Process(target=updateQuestions, args=(group, balanced, save, r[0], r[1],to_direct))
        elif stage == 'combine':
            p = Process(target=combineFiles, args=(group, balanced, save, r[0], r[1],to_direct))

        jobs.append(p)
        p.start()