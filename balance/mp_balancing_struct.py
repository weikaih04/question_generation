import pickle
import json
import random
import math
import sys
import balance_support as bs


infile = open('../data/stsgs/test_stsgs.pkl', 'rb')
test_stsgs = pickle.load(infile)
infile.close()

infile = open('../data/stsgs/train_stsgs.pkl', 'rb')
train_stsgs = pickle.load(infile)
infile.close()


def getQA(d_path, v_id, group, old_path):
    with open('../exports/%s/%s/%s/%s.txt' % (d_path, old_path, group, v_id)) as json_file:
        QA = json.load(json_file)
    return QA


def getSTSGS(group):
    if group == 'train':
        return train_stsgs
    elif group == 'test':
        return test_stsgs
    else:
        print("INVALID GROUP", group)
        return


def getInfo(d_path, group, old_path):
    v_ids = list(getSTSGS(group))
    temp_type = bs.getTemporalType(group, d_path, 'all')
    info = {
        'total': 0,
        'struct': {}
    }

    for i in ['logic', 'verify', 'compare', 'choose', 'query']:
        info['struct'][i] = {
            'total': 0,
            'templ': {}
        }
    print()
    print(group)
    cnt = 0
    for v_id in v_ids:
        if cnt % 100 == 0:
            print(cnt)
        cnt = cnt + 1

        QA = getQA(d_path, v_id, group, old_path)
        for q_id in QA:
            q = QA[q_id]

            struct = q['attributes']['structural']
            templ = q['attributes']['type']

            # make loc bs. get category
            if struct == 'query':
                loc = q['local']
            else:
                loc = bs.getBinaryCat(q)

            time = q['metrics']['direct_time'][0]

            ans = q['answer']

            info['total'] += 1
            s = info['struct'][struct]
            s['total'] += 1
            if templ not in s['templ']:
                s['templ'][templ] = {
                    'total': 0,
                    'time': {},
                }

            t = s['templ'][templ]
            t['total'] += 1

            if time not in t['time']:
                t['time'][time] = {
                    'total': 0,
                    'local': {},
                }
            t = t['time'][time]
            t['total'] += 1

            if loc not in t['local']:
                t['local'][loc] = {
                    'total': 0,
                    'answer': {}
                }

            l = t['local'][loc]
            l['total'] += 1
            if ans not in l['answer']:
                l['answer'][ans] = bs.getTempTypeDic()

            tt = temp_type[v_id][q_id]

            l['answer'][ans][tt].append(q_id)

    return info


def numToDelStruct(info, percs):
    num_query = info['struct']['query']['total']
    num_total = num_query / percs[0][1]

    tot = 0
    for _, cnt in percs:
        tot += cnt

    if tot != 1:
        print("Invalid percs")
        return info

    
    for struct, perc in percs:
        num = info['struct'][struct]['total']

        target = math.ceil(perc * num_total)

        if num < target:
            print("no few to delete", struct, 'target is ', target, 'num is ', num)
            info['struct'][struct]['num_del'] = 0
        else:
            info['struct'][struct]['num_del'] = num - target

    # CHANGED!!!! delete this chunck of code under
    #info['struct']['verify']['num_del'] = 0
    #info['struct']['query']['num_del'] = 0
    #info['struct']['logic']['num_del'] = 0
    #info['struct']['choose']['num_del'] =  info['struct']['choose']['total'] - 17000
    #info['struct']['compare']['num_del'] = info['struct']['compare']['total'] - 43000



    return info


def numToDelTempl(info):
    for struct in info['struct']:
        num_del = info['struct'][struct]['num_del']
        templs = info['struct'][struct]['templ']

        for templ in templs:
            templs[templ]['num_del'] = 0

        while num_del > 0:
            per_cat = {}
            for templ in templs:
                tot = templs[templ]['total'] - templs[templ]['num_del']
                if tot not in per_cat:
                    per_cat[tot] = []

                per_cat[tot].append(templ)

            per_cat_sorted = sorted(per_cat, reverse=True)

            max_templs = per_cat[per_cat_sorted[0]]
            num_per_max = math.ceil(num_del / len(max_templs))

            if len(per_cat_sorted) > 1:
                diff = per_cat_sorted[0] - per_cat_sorted[1]
            else:
                diff = per_cat_sorted[0]

            if num_per_max > diff:
                num_per_max = diff
            for t in max_templs:
                templs[t]['num_del'] += num_per_max
                num_del -= num_per_max

    return info


def numToDelTime(info):
    for struct in info['struct']:
        for t_idx in info['struct'][struct]['templ']:
            num_del = info['struct'][struct]['templ'][t_idx]['num_del']

            # calling it locs for ease of fixing, but it's actually time!!!
            locs = info['struct'][struct]['templ'][t_idx]['time']

            total_locs = 0
            for loc in locs:
                locs[loc]['num_del'] = 0
                total_locs += locs[loc]['total']

            num_times = 0
            while num_del > 0:
                num_times += 1
                per_cat = {}
                for loc in locs:
                    tot = locs[loc]['total'] - locs[loc]['num_del']
                    if tot not in per_cat:
                        per_cat[tot] = []

                    per_cat[tot].append(loc)

                per_cat_sorted = sorted(per_cat, reverse=True)

                max_locs = per_cat[per_cat_sorted[0]]
                num_per_max = math.ceil(num_del / len(max_locs))

                if len(per_cat_sorted) > 1:
                    diff = per_cat_sorted[0] - per_cat_sorted[1]
                else:
                    diff = per_cat_sorted[0]

                if num_per_max > diff:
                    # here, would be too far.
                    # only delete pcs[0] - pcs[1] from all max,
                    # and reduce num_del by the right amount
                    num_per_max = diff
                else:
                    print("it is equal!!", num_times, num_per_max, diff)

                for cnt in range(num_per_max):
                    if num_del <= 0:
                        break
                    if True:
                        for l in max_locs:
                            if num_del <= 0:
                                break
                            locs[l]['num_del'] += 1
                            num_del -= 1

            print('num_times', num_times, 'and numdlete is now', num_del)
    return info


def numToDelLocal(info):
    for struct in info['struct']:
        for t_idx in info['struct'][struct]['templ']:
            for time in info['struct'][struct]['templ'][t_idx]['time']:
                num_del = info['struct'][struct]['templ'][t_idx]['time'][time]['num_del']
                locs = info['struct'][struct]['templ'][t_idx]['time'][time]['local']

                total_locs = 0
                for loc in locs:
                    locs[loc]['num_del'] = 0
                    total_locs += locs[loc]['total']

                num_times = 0
                while num_del > 0:
                    num_times += 1
                    per_cat = {}
                    for loc in locs:
                        tot = locs[loc]['total'] - locs[loc]['num_del']
                        if tot not in per_cat:
                            per_cat[tot] = []

                        per_cat[tot].append(loc)

                    per_cat_sorted = sorted(per_cat, reverse=True)

                    max_locs = per_cat[per_cat_sorted[0]]
                    num_per_max = math.ceil(num_del / len(max_locs))

                    if len(per_cat_sorted) > 1:
                        diff = per_cat_sorted[0] - per_cat_sorted[1]
                    else:
                        diff = per_cat_sorted[0]

                    if num_per_max > diff:
                        # here, would be too far.
                        # only delete pcs[0] - pcs[1] from all max,
                        # and reduce num_del by the right amount
                        num_per_max = diff
                    else:
                        print("it is equal!!", num_times, num_per_max, diff)

                    for cnt in range(num_per_max):
                        if num_del <= 0:
                            break
                        if True:
                            for l in max_locs:
                                if num_del <= 0:
                                    break
                                locs[l]['num_del'] += 1
                                num_del -= 1
                print('num_times', num_times, 'and numdlete is now', num_del)

    return info


def printInfo(info, local):
    print("TOTAL: ", info['total'])
    for struct in info['struct']:
        print()
        s = info['struct'][struct]
        print(" "*4, struct, s['total'])
        if 'num_del' in info['struct'][struct]:
            print(" "*5, "delete", s['num_del'])
            print(" "*5, "leave", s['total'] - s['num_del'])
        for templ in info['struct'][struct]['templ']:
            t = info['struct'][struct]['templ'][templ]
            print(" "*8, templ, t['total'])
            if 'num_del' in t:
                print(" "*9, "delete", t['num_del'])
                print(" "*9, "leave", t['total'] - t['num_del'])
            if local:
                for local in t['local']:
                    l = t['local'][local]
                    print(" "*16, local, l['total'])
                    if 'num_del' in l:
                        print(" "*17, "delete", l['num_del'])
                        print(" "*17, "leave", l['total'] - l['num_del'])


def deleteXFromDistr(dist, x):
    to_del = {}
    for a in dist:
        to_del[a] = 0

    while x > 0:
        per_cat = {}
        for a in dist:
            remain = len(dist[a]) - to_del[a]
            if remain not in per_cat:
                per_cat[remain] = []

            per_cat[remain].append(a)

        per_cat_sorted = sorted(per_cat, reverse=True)

        max_ans = per_cat[per_cat_sorted[0]]
        num_per_max = math.ceil(x / len(max_ans))

        if len(per_cat_sorted) > 1:
            diff = per_cat_sorted[0] - per_cat_sorted[1]
        else:
            diff = per_cat_sorted[0]

        if num_per_max > diff:
            # here, would be too far.
            # only delete pcs[0] - pcs[1] from all max,
            # and reduce num_del by the right amount
            num_per_max = diff
        for a in max_ans:
            to_del[a] += num_per_max
            x -= num_per_max

    return to_del


def sums(dic):
    tot = 0
    for i in dic:
        if type(dic[i]) == list:
            tot += len(dic[i])
        else:
            tot += dic[i]

    return tot


def getQidsToDel(info):
    to_del = []

    # for each local distribution
    #    if it's uneven, first balance that out
    #    split into 2
    #    if .5, then delete an extra one from each
    #    and update ad a "left" thing to loc
    #    append q_ids to delete to the main thing
    for struct in info['struct']:
        print(struct)
        if info['struct'][struct]['num_del'] == 0:
            print("don't delete any from ", struct)
            continue
        for templ in info['struct'][struct]['templ']:
            if info['struct'][struct]['templ'][templ]['num_del'] == 0:
                print("don't delete any from ", templ)
                continue
            print("  ", templ)
            for time in info['struct'][struct]['templ'][templ]['time']:
                if info['struct'][struct]['templ'][templ]['time'][time]['num_del'] == 0:
                    print("don't delete any from ", templ)
                    continue
                print("      ", time)

                locals_list = list(info['struct'][struct]['templ'][templ]['time'][time]['local'])
                random.shuffle(locals_list)
                t = info['struct'][struct]['templ'][templ]['time'][time]
                templ_total = t['total']
                templ_delete = t['num_del']
                templ_leave = templ_total - templ_delete

                keeping = 0
                num_deleted_already = 0

                kept_enough = False
                for loc in locals_list:
                    if keeping >= templ_leave:
                        kept_enough = True

                    l = info['struct'][struct]['templ'][templ]['time'][time]['local'][loc]
                    num_del = l['num_del']
                    deleted = 0

                    if num_del == 0:
                        l['remaining'] = l['total']
                        continue

                    if len(l['answer']) < 2:
                        for a in l['answer']:
                            for tt in l['answer'][a]:
                                to_del.append(l['answer'][a][tt])
                        l['remaining'] = 0
                        continue

                    if len(l['answer']) > 2:
                        print("C")
                        print("SHOULDNT BE GETTING MORE THAN 2 ANSWERS", len(l['answer']))
                        print(struct, templ, loc)
                        print(type(l['answer']))
                        delete = deleteXFromDistr(l['answer'], l['num_del'])
                        for i in l['answer']:
                            to_del.append(random.sample(l['answer'][i], k=delete[i]))
                        print("Done this part!")
                        continue
                    dist = []
                    for a in l['answer']:
                        dist.append((a, l['answer'][a]))
                    (a1, lst1), (a2, lst2) = dist
                    cnt1 = sums(lst1)
                    cnt2 = sums(lst2)

                    if cnt1 != cnt2:
                        if cnt1 < cnt2:
                            diff = cnt2 - cnt1
                            if diff >= num_del:
                                num_del2 = num_del
                                num_del1 = 0
                                deleted = num_del
                            else:
                                num_del = math.floor(abs(num_del - diff) / 2)
                                deleted = 2 * num_del + diff
                                num_del1 = num_del
                                num_del2 = num_del + diff
                        if cnt2 < cnt1:
                            diff = cnt1 - cnt2
                            if diff >= num_del:
                                num_del1 = num_del
                                num_del2 = 0
                                deleted = num_del
                            else:
                                num_del = math.floor(abs(num_del - diff) / 2)
                                deleted = 2 * num_del + diff
                                num_del2 = num_del
                                num_del1 = num_del + diff
                    else:
                        num_del1 = math.floor(num_del / 2)
                        num_del2 = math.floor(num_del / 2)
                        deleted += 2 * num_del1

                    # If kept enough, numdel1 == sums(l['answer'][a1])
                    if kept_enough:
                        num_del1 = sums(l['answer'][a1])
                        num_del2 = sums(l['answer'][a2])
                        deleted = num_del1 + num_del2
                        if deleted != l['total']:
                            print("the total is %s and we are deleting %s (a1: %s, a2: %s)" % (l['total'], deleted, num_del1, num_del2))

                    if sums(l['answer'][a1]) < num_del1:
                        print('%s is less than %s' % (sums(l['answer'][a1]), num_del1))

                    to_add1 = bs.getIdsToDelete(l['answer'][a1], num_del1)
                    for i in to_add1:
                        if type(i) == dict:
                            print("There is something in add1 that is a dict")
                            print(to_add1)
                    if type(to_add1) == dict:
                        print("to add 1 is a dict")

                    if 'no_temporal' == to_add1:
                        print("no temporal is to_add 1")
                    to_add2 = bs.getIdsToDelete(l['answer'][a2], num_del2)
                    for i in to_add2:
                        if type(i) == dict:
                            print("There is something in add2 that is a dict")
                            print(to_add2)
                    if type(to_add2) == dict:
                        print("to add 2 is a dict")
                    to_del.append(to_add1)
                    to_del.append(to_add2)
                    for lst in to_del:
                        if '0Z1PC-192974' in lst:
                            print("LIST that includes thing in dic")
                    if 'no_temporal' == to_add2:
                        print("no temporal is to_add2")

                    l['remaining'] = l['total'] - deleted
                    num_deleted_already += deleted
                    keeping += l['remaining']

        print("checking todel after ", struct)
        # so there is always in to_del
        for lst in to_del:
            if type(lst) == dict:
                print("List is a dict")
            for lst2 in lst:
                if type(lst2) != list:
                    print("Second list not a list")
                for q_id in lst2:
                    if type(q_id) != str:
                        print('non-string in list')

                    if len(q_id) < 5:
                        print("wrong q id just letters, ", q_id)

    # at the end, go through all q_ids to delete and sort by video
    del_by_video = {}
    for lst in to_del:
        if type(lst) == dict:
            print("still returned a dic")
            new_lst = []
            for i in lst:
                new_lst.append(lst[i])

            lst = new_lst

        for lst2 in lst:
            for q_id in lst2:
                v_id = q_id[:5]

                if v_id not in del_by_video:
                    if len(v_id) != 5:
                        print('v_id is ', v_id, ' from q_id', q_id)
                    del_by_video[v_id] = []
                del_by_video[v_id].append(q_id)

    print('Ihave kept %s and deleted %s out of expected keeping %s and deleteing %s' % (keeping, num_deleted_already, templ_leave, templ_delete))
    return info, del_by_video


def deleteQuestions(to_del, d_path, old_path, new_path, group, save=False):
    cnt = 0
    num_deleted = 0
    cnt_actually_done = 0
    for v_id in to_del:
        if cnt % 100 == 0:
            print(cnt)
        cnt += 1

        if len(v_id) != 5:
            print('v_id is not 5 and we dont know why. instead it is', v_id)
            if v_id in to_del:
                print("delby-video[v_id] is: ", to_del[v_id])
            else:
                print("v_id is not in to_del")
            continue

        cnt_actually_done += 1
        with open('../exports/%s/%s/%s/%s.txt' % (d_path, old_path, group, v_id)) as json_file:
            QA = json.load(json_file)

        if v_id in to_del:
            qs_to_del = to_del[v_id]

            for q_id in qs_to_del:
                if q_id in QA:
                    num_deleted = num_deleted + 1
                    del QA[q_id]

        if save:
            with open('../exports/%s/%s/%s/%s.txt' % (d_path, new_path, group, v_id), 'w+') as json_file:
                json.dump(QA, json_file)

    return num_deleted


def rebalanceDataset(old_path, d_path, new_path, group, percs, save=False, onlyDel=False):
    print("Rebalancing data by struct within ", d_path, " taking it", group, "from ", old_path, "to", new_path, "and save = ", save)
    print("percs = ", percs)
    if not onlyDel:
        print('get info')
        info = getInfo(d_path, group, old_path)

        print("saving info to ../exports/%s/%s-info0.txt" % (d_path, group))
        with open('../exports/%s/info/%s-info0.txt' % (d_path, group), 'w+') as f:
            json.dump(info, f)

        print("num to del struct")
        info = numToDelStruct(info, percs)
        print("saving info to ../exports/%s/%s-info1.txt" % (d_path, group))
        with open('../exports/%s/info/%s-info1.txt' % (d_path, group), 'w+') as f:
            json.dump(info, f)

        print("num to del template")
        info = numToDelTempl(info)

        print("saving info to ../exports/%s/%s-info2.txt" % (d_path, group))
        with open('../exports/%s/info/%s-info2.txt' % (d_path, group), 'w+') as f:
            json.dump(info, f)

        print("num to del time")
        info = numToDelTime(info)

        print("saving info to ../exports/%s/%s-info2b.txt" % (d_path, group))
        with open('../exports/%s/info/%s-info2b.txt' % (d_path, group), 'w+') as f:
            json.dump(info, f)

        print("num to local delete")
        info = numToDelLocal(info)
        print("saving info to ../exports/%s/%s-info3.txt" % (d_path, group))
        with open('../exports/%s/info/%s-info3.txt' % (d_path, group), 'w+') as f:
            json.dump(info, f)

    else:
        with open('../exports/%s/info/%s-info3.txt' % (d_path, group), 'rb') as f:
            info = json.load(f)

    print('get q-ids to delete')

    info, del_by_video = getQidsToDel(info)

    print("saving info to ../exports/%s/%s-info4.txt" % (d_path, group))
    with open('../exports/%s/info/%s-info4.txt' % (d_path, group), 'w+') as f:
        json.dump(info, f)

    print("saving info to ../exports/%s/%s-del_by_video.txt" % (d_path, group))
    with open('../exports/%s/info/%s-del_by_video.txt' % (d_path, group), 'w+') as f:
        json.dump(del_by_video, f)
    
    print("delete questions and put in", new_path)
    if save:
        num_deleted = deleteQuestions(del_by_video, d_path, old_path, new_path, group, save)

    return info, num_deleted

#percs = [('query', .5), ('logic', .05), ('verify', .1), ('compare', .25), ('choose', .1)]
percs = [('query', .5), ('logic', .05), ('verify', .15), ('compare', .15), ('choose', .15)]


if __name__ == '__main__':
    print("done imports")
    onlyDel = False
    sv = sys.argv[1:][4]
    group = sys.argv[1:][3]
    new_path = sys.argv[1:][2]
    old_path = sys.argv[1:][1]
    d_path = sys.argv[1:][0]
    valid = True
    _, num_deleted = rebalanceDataset(old_path, d_path, new_path,
                                      group, percs, save=sv, onlyDel=onlyDel)
    print("DELETED: ", num_deleted)
