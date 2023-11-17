from multiprocessing import Process
import balance_support as bs
import json
import pickle
import random
import math
import sys


with open('../data/train_video_names.txt', 'rb') as f:
    train_stsgs = json.load(f)


with open('../data/test_video_names.txt', 'rb') as f:
    test_stsgs = json.load(f)


#infile = open('../data/video_names.txt', 'rb')
#names = json.load(infile)
#infile.close()


def pickleDump(var, destination):
    f = open(destination, "wb")
    pickle.dump(var, f)
    f.close()


def pickleLoad(path):
    file = open(path, 'rb')
    info = pickle.load(file)
    file.close()
    return info


BINARY_GLOBAL_IDS = ['exists', 'first', 'last', 'time',
                     'length', 'what', 'count']
OPEN_GLOBAL_IDS = ['first', 'last', 'what', 'count', 'length', 'count-int']


def getValueCountNA(dic):
    cnt = {}
    for i in dic:
        cnt[i] = len(dic[i])
    return cnt


def sortDictOfCounts(dic):
    return sorted(dic, key=dic.__getitem__)[::-1]


def createOrigionalDist(dic):
    counts = bs.getValueCount(dic)
    sort = sortDictOfCounts(counts)
    P = []
    head = 0
    tail = 0
    for i in sort:
        P.append((i, counts[i]))
        tail = tail + counts[i]
    return P, head, tail


def getBinaryCatNA(ans):
    if ans == "Yes" or ans == "No":
        dic = {
            'Yes': [],
            'No': [],
        }
        return "Yes/No", dic

    if ans == "before" or ans == "after":
        dic = {
            'before': [],
            'after': [],
        }
        return "before/after", dic


def getDictByQTypeNA(group, start, stop, d_path):

    print("Done imports")
    opn = {}
    bny = {}

    for glob in OPEN_GLOBAL_IDS:
        opn[glob] = {}
    for glob in BINARY_GLOBAL_IDS:
        bny[glob] = {}

    # Separate binary further by answer type
    all_binary_cat = ["Yes/No", "before/after"]
    for glob in bny:
        for cat in all_binary_cat:
            bny[glob][cat] = {}

    if group == "train":
        stsgs = train_stsgs
    elif group == "test":
        stsgs = test_stsgs
    #elif group == 'names':
    #    stsgs = names
    else:
        print("INVALID GROUP", group)
        return

    cnt = 0
    for v_id in stsgs:
        if cnt < start:
            continue
        if cnt >= stop:
            break

        with open('../exports/%s/all/%s/%s.txt' % (d_path, group, v_id)) as json_file:
            QA = json.load(json_file)
        for q_id in QA:
            q = QA[q_id]
            glob = q['global']
            loc = q['local']
            ans_type = q['attributes']['ans_type']

            ans = str(q['answer'])

            if ans_type == 'binary':
                cat, dic = bs.getBinaryCat(ans)
                category = bny[glob][cat]
                if loc not in category:
                    category[loc] = dic
                category[loc][ans].append(q_id)
            if ans_type == 'open':
                if glob == 'count' and type(q['answer']) == int:
                    glob = 'count-int'
                if ans not in opn[glob]:
                    opn[glob][ans] = []
                opn[glob][ans].append(q_id)
        cnt = cnt + 1

        if cnt % 100 == 0:
            print("finished", cnt)

    pickleDump(bny, "../exports/%s/by_q_type/binary/%s-%s-%s.pkl" % (d_path, group, start, stop))
    pickleDump(opn, "../exports/%s/by_q_type/open_global/%s-%s-%s.pkl" % (d_path, group, start, stop))


def balance5(P, head, tail, b, mn, mx, binary):
    if len(P) < 2:
        print("LENGTH OF P IS LESS THAN TWO THIS IS AN ISSUE")

    # create similar keep v delete dic
    # but instead associated with the number to keep
    keep = {}
    delete = {}

    if P[1][1] == 0:
        delete[P[0][0]] = P[0][1]
        P[0] = (P[0][0], 0)
        return P, delete, head + tail

    # or is kepe basically P? but a dictionary nvm

    for (ans, cnt) in P:
        keep[ans] = cnt
        delete[ans] = 0

    largest = P[0][1]
    loop = 0
    for i in range(len(P) - 1):
        loop = loop + 1
        # move up the distribution
        (ans, cnt) = P[i]
        head = head + cnt
        tail = tail - cnt

        if cnt < 10:
            break

        # frequency compared to next
        (_, next_cnt) = P[i+1]

        # find head / tail adjusted by how much they are
        prop = (head / (i + 1)) / (tail / (len(P) - (i + 1)))
        num_failed = 0
        while prop > b:
            if not binary and num_failed > (largest * i):
                break

            # get rand ans and rand count
            ans_idx = random.randint(0, i)
            del_idx = random.randint(0, largest)
            ans, cnt = P[ans_idx]

            # see if in length of keep or delete.
            # if it is, see if already a 0. If so continue
            if keep[ans] <= del_idx:
                num_failed = num_failed + 1
                continue

            # if would change distribution, dont do it...
            n_freq = P[ans_idx + 1][1] / cnt

            if n_freq >= mx:
                num_failed = num_failed + 1
                continue

            # reset num_failed
            num_failed = 0

            # change from a 1 to a zero
            keep[ans] = keep[ans] - 1
            delete[ans] = delete[ans] + 1

            # change P[ans_idx] to be subtracting 1
            P[ans_idx] = (ans, cnt - 1)

            if ans_idx == 0:
                largest = P[0][1]

            # update head, prop
            head = head - 1
            prop = (head / (i + 1)) / (tail / (len(P) - (i + 1)))

    return P, delete, head + tail


def balanceLocalBny(local_binary, b, mn):
    """ balances a distribution for questions of a given attribute

    Args:
        loc_bin: a dictionary mapping local values to quesiton ids

    Returns:
        og_dist: origional answer distribution
        up_dist: updated answer distribution
        keep:
        delete:
    """

    og_dist, head, tail = createOrigionalDist(local_binary)

    if len(og_dist) != 2:
        if len(og_dist) == 0:
            print("Weird - og dist has 0 things in it")
            return
        a1, cnt1 = og_dist[0]
        delete = {
            a1: cnt1,
        }
        og_dist = [og_dist[0], ("placement", 0)]
        up_dist = [(a1, 0), ("placement", 0)]

        return og_dist, up_dist, delete, -1

    (a1, cnt1), (a2, cnt2) = og_dist
    if cnt1 > cnt2:
        delete = {
            a1: cnt1 - cnt2,
            a2: 0
        }
        up_dist = [(a1, cnt2), (a2, cnt2)]
    elif cnt2 > cnt1:
        delete = {
            a2: cnt2 - cnt1,
            a1: 0
        }
        up_dist = [(a1, cnt1), (a2, cnt1)]

    else:
        delete = {
            a1: 0,
            a2: 0
        }
        up_dist = [(a1, cnt1), (a2, cnt2)]

    return og_dist, up_dist, delete, -1


def balanceBinary(group, delete_from_QA, glob_idx, d_path):
    up = {}
    og = {}
    q_ids_to_delete = []

    if group == 'train':
        bny = pickleLoad("../exports/%s/by_q_type/binary/train-0-%s.pkl" % (d_path, len(train_stsgs)))
    elif group == 'test':
        bny = pickleLoad("../exports/%s/by_q_type/binary/test-0-%s.pkl" % (d_path, len(test_stsgs)))
    else:
        print("A invalid group", group)
        return

    for glob in BINARY_GLOBAL_IDS:
        up[glob] = {}
        og[glob] = {}

    all_binary_cat = ['all']
    for glob in up:
        for cat in all_binary_cat:
            up[glob][cat] = {}
            og[glob][cat] = {}

    glob = BINARY_GLOBAL_IDS[glob_idx]
    num_to_del = 0
    for cat in bny[glob]:
        for loc in bny[glob][cat]:
            # if there's only one in the lcoal, delete all of it
            og_dist, up_dist, delete, total = balanceLocalBny(bny[glob][cat][loc], 1, 0)
            if up_dist == "illegal":
                og[glob][cat][loc] = []
                up[glob][cat][loc] = []
                continue
            og[glob][cat][loc] = og_dist
            up[glob][cat][loc] = up_dist
            for ans in delete:
                cnt = delete[ans]
                x = bs.getIdsToDelete(bny[glob][cat][loc][ans], cnt)
                q_ids_to_delete.append(x)

                tot_cnt = 0
                for lst in x:
                    tot_cnt += len(lst)
                if tot_cnt != cnt:
                    print("The number to delet is different: should be %s, but actually is %s" % (cnt, tot_cnt))
                num_to_del = num_to_del + cnt
    print(glob_idx, " deleted ", num_to_del)

    print("finished idx: ", glob_idx)
    pickleDump(og, "../exports/%s/distributions/%s-binary-og-%s.pkl" % (d_path, group, BINARY_GLOBAL_IDS[glob_idx]))
    pickleDump(up, "../exports/%s/distributions/%s-binary-up-%s.pkl" % (d_path, group, BINARY_GLOBAL_IDS[glob_idx]))
    pickleDump(q_ids_to_delete, "../exports/%s/q_ids_to_delete/%s-binary-%s.pkl" % (d_path, group, BINARY_GLOBAL_IDS[glob_idx]))


def binarySortDelByVID(d_path, group):
    total = 0
    by_v_id = {}
    for glob in BINARY_GLOBAL_IDS:
        q_idx_to_del = pickleLoad("../exports/%s/q_ids_to_delete/%s-binary-%s.pkl" % (d_path, group, glob))
        g_count = len(q_idx_to_del)
        total = total + len(q_idx_to_del)
        for lst in q_idx_to_del:
            for i in lst:
                g_count = g_count + len(i)
                total = total + len(i)
                for j in i:
                    v_id = j[:5]

                    if v_id not in by_v_id:
                        by_v_id[v_id] = []
                    by_v_id[v_id].append(j)
        print(glob, g_count)
    pickleDump(by_v_id, "../exports/%s/q_ids_to_delete/%s-binary-byvid.pkl" % (d_path, group))


def delBottomPercent(P, total, percent):
    if percent > 1:
        print("invalid percent ", percent)
        return
    num_to_delete = int(total * percent)

    num_deleted = 0
    idx_to_del = 0
    while num_deleted < num_to_delete:
        idx_to_del = idx_to_del - 1
        _, cnt = P[idx_to_del]

        num_deleted = num_deleted + cnt
 
    return P[:idx_to_del], (total - num_deleted), P[idx_to_del:]


def headNotExtreme(dist, total):
    num_answers_in_head = math.ceil(len(dist) * head_percent_of_x_axis)

    in_head = 0
    for i in range(num_answers_in_head):
        in_head = in_head + dist[i][1]

    percent_in_head = in_head / total
    return percent_in_head <= max_head_percent_of_dist


def haveDeletedTooMuch(og_total, current_total):
    percent_retained = current_total / og_total

    return percent_retained < percent_og_to_retain


def balanceSingleOpenDist(open_dist, b, mn):
    og_dist, head, og_tail = createOrigionalDist(open_dist)
    P = og_dist.copy()

    if len(open_dist) == 0:
        return [], [], {}, [], []
    if len(open_dist) == 1:
        answers = list(open_dist.keys())
        ans = answers[0]

        cnt = 0
        for i in open_dist[ans]:
            cnt += len(open_dist[ans][i])

        empty_dist = [(ans, 0)]
        deleted = {ans: cnt}
        return og_dist, empty_dist, deleted, og_dist, empty_dist

    if og_dist[0][0].isnumeric():
        print()
        print("Balancing Count differently", og_dist)
        truncated = og_dist[:3]
        end_of_dist = og_dist[3:]
        tail = 0
        for a1, cnt1 in truncated:
            tail += cnt1

    else:
        truncated, tail, end_of_dist = delBottomPercent(P, og_tail, trunc_perc)

        if len(truncated) <= 2:
            truncated = og_dist
            end_of_dist = []
            tail = og_tail
    P = truncated.copy()
    if len(P) < 2:
        print("p is < 2 even after it shouldnt have been", P)

    b = b_val
    working_dist = truncated.copy()
    working_delete = {}

    if len(P) == 2:
        (a1, cnt1), (a2, cnt2) = working_dist
        if cnt1 > cnt2:
            # do something
            deleted = {
                a1: cnt1 - cnt2,
                a2: 0
            }
            up_dist = [(a1, cnt2), (a2, cnt2)]
        elif cnt2 > cnt1:
            deleted = {
                a2: cnt2 - cnt1,
                a1: 0
            }
            up_dist = [(a1, cnt1), (a2, cnt1)]
        else:
            deleted = {
                a1: 0,
                a2: 0
            }
            up_dist = [(a1, cnt1), (a2, cnt2)]
        return truncated + end_of_dist, up_dist + end_of_dist, deleted, truncated, working_dist

    while b >= 1 and len(P) > 2:
        up_dist, delete, total = balance5(working_dist, head, tail, b, mn, 1, False)

        # if successfullly smoothed
        if headNotExtreme(up_dist, total):
            return truncated + end_of_dist, up_dist + end_of_dist, delete, truncated, up_dist

        # if taking this step deletes too much, return last one
        if haveDeletedTooMuch(og_tail, total):
            return truncated + end_of_dist, working_dist + end_of_dist, working_delete, truncated, working_dist

        # if not smoothed and haven't deleted too much
        working_dist = up_dist
        working_delete = delete
        b = b * .75

    return truncated + end_of_dist, working_dist + end_of_dist, working_delete, truncated, working_dist


def balanceGlobalOpen(group, d_path):
    up = {}
    og = {}
    trunc_up = {}
    trunc_og = {}
    q_ids_to_delete = []

    if group == 'train':
        open_global = pickleLoad("../exports/%s/by_q_type/open_global/train-0-%s.pkl" % (d_path, len(train_stsgs)))
    elif group == 'test':
        open_global = pickleLoad("../exports/%s/by_q_type/open_global/test-0-%s.pkl" % (d_path, len(test_stsgs)))
    else:
        print("B invalid group", group)
        return
    for glob in OPEN_GLOBAL_IDS:
        up[glob] = {}
        og[glob] = {}
        trunc_up[glob] = {}
        trunc_og[glob] = {}

    for glob in open_global:
        print()
        print(glob)

        if glob == 'count-int':
            og_dist, _, _ = createOrigionalDist(open_global[glob])
            trunc_up[glob] = []
            trunc_og[glob] = []
            og[glob] = og_dist
            up_dist = []
            delete = {}

            sum_post_2 = 0
            for a, cnt in og_dist[2:]:
                sum_post_2 += cnt

            for a, cnt in og_dist:
                if a == "0" or a == "1":
                    delete[a] = cnt - sum_post_2
                    up_dist.append((a, sum_post_2))
                else:
                    delete[a] = 0
                    up_dist.append((a, cnt))

            up[glob] = up_dist

        else:
            og_dist, up_dist, delete, og_trunc, up_trunc = balanceSingleOpenDist(open_global[glob], 1, 0)
            trunc_og[glob] = og_trunc
            trunc_up[glob] = up_trunc
            og[glob] = og_dist
            up[glob] = up_dist

        for ans in delete:
            cnt = delete[ans]
            q_ids_to_delete.append(bs.getIdsToDelete(open_global[glob][ans], cnt))

    print("deleted ", len(q_ids_to_delete))

    print("finished open global")
    pickleDump(og, "../exports/%s/distributions/%s-open-global-og.pkl" % (d_path, group))
    pickleDump(up, "../exports/%s/distributions/%s-open-global-up.pkl" % (d_path, group))
    pickleDump(q_ids_to_delete, "../exports/%s/q_ids_to_delete/%s-open-global.pkl" % (d_path, group))


def openGlobSortDelByVID(d_path, group):
    print("Group is ", group)
    by_v_id = {}
    q_idx_to_del = pickleLoad("../exports/%s/q_ids_to_delete/%s-open-global.pkl" % (d_path, group))
    num = 0
    for lst in q_idx_to_del:
        for i in lst:
            for j in i:
                v_id = j[:5]

                if v_id not in by_v_id:
                    by_v_id[v_id] = []
                by_v_id[v_id].append(j)
                num += 1
    print("deleted num", num)
    pickleDump(by_v_id, "../exports/%s/q_ids_to_delete/%s-open-global-byvid.pkl" % (d_path, group))


def alreadyDeleted(q_id, group, ans_type):
    # check if deleted in open global
    v_id = q_id[:5]
    if ans_type == 'open':
        ans_type = 'open-global'
    by_vid = pickleLoad("../exports/%s/q_ids_to_delete/%s-%s-byvid.pkl" % (d_path, group, ans_type))
    deleted = by_vid[v_id]

    if q_id in deleted:
        return False
    return True


def balanceLocalOpen(group, d_path):
    up = {}
    og = {}
    trunc_up = {}
    trunc_og = {}
    q_ids_to_delete = []

    if group == 'train':
        open_local = pickleLoad("../exports/%s/by_q_type/open_local/train-0-%s.pkl" % (d_path, len(train_stsgs)))
    elif group == 'test':
        open_local = pickleLoad("../exports/%s/by_q_type/open_local/test-0-%s.pkl" % (d_path, len(test_stsgs)))
    #elif group == 'names':
    #    open_local = pickleLoad("../exports/%s/by_q_type/open_local/names-0-%s.pkl" % (d_path, len(test_stsgs)))
        
    else:
        print("C invalid group", group)
        return

    for glob in OPEN_GLOBAL_IDS:
        up[glob] = {}
        og[glob] = {}
        trunc_up[glob] = {}
        trunc_og[glob] = {}

    for glob in open_local:
        for loc in open_local[glob]:
            og_dist, up_dist, delete, og_trunc, up_trunc = balanceSingleOpenDist(open_local[glob][loc], 1, 0)
            trunc_og[glob][loc] = og_trunc
            trunc_up[glob][loc] = up_trunc
            og[glob][loc] = og_dist
            up[glob][loc] = up_dist

            for ans in delete:
                cnt = delete[ans]
                q_ids_to_delete.append(bs.getIdsToDelete(open_local[glob][loc][ans], cnt))

    print("deleted ", len(q_ids_to_delete))
    print("finished open local")
    pickleDump(og, "../exports/%s/distributions/%s-open-local-og.pkl" % (d_path, group))
    pickleDump(up, "../exports/%s/distributions/%s-open-local-up.pkl" % (d_path, group))
    pickleDump(q_ids_to_delete, "../exports/%s/q_ids_to_delete/%s-open-local.pkl" % (d_path, group))
    return og, up, trunc_og, trunc_up, q_ids_to_delete


def localOpenSortDelByVID(d_path, group):
    by_v_id = {}
    q_idx_to_del = pickleLoad("../exports/%s/q_ids_to_delete/%s-open-local.pkl" % (d_path, group))
    num = 0
    for lst in q_idx_to_del:
        for i in lst:
            for j in i:
                v_id = j[:5]

                if v_id not in by_v_id:
                    by_v_id[v_id] = []
                by_v_id[v_id].append(j)
                num += 1

    print("num deleted was", num)
    pickleDump(by_v_id, "../exports/%s/q_ids_to_delete/%s-open-local-byvid.pkl" % (d_path, group))


def deleteQuestions(group, step, start, stop, d_path):
    if step == 'after_glob':
        q_types = ['binary', 'open-global']
        src = 'all/'
    elif step == 'after_loc':
        q_types = ['open-local']
        src = 'smoothed/'
    else:
        print("invalid step", step)

    if group == "train":
        stsgs = train_stsgs
    elif group == "test":
        stsgs = test_stsgs
    #elif group == 'names':
    #    stsgs = names
    else:
        print("INVALID GROUP", group)
        return

    deleting = []
    for ans_type in q_types:
        deleting.append(pickleLoad("../exports/%s/q_ids_to_delete/%s-%s-byvid.pkl" % (d_path, group, ans_type)))

    cnt = 0
    num_deleted = 0
    for v_id in stsgs:
        if cnt < start:
            cnt = cnt + 1
            continue

        if cnt >= stop:
            break

        with open('../exports/%s/%s%s/%s.txt' % (d_path, src, group, v_id)) as json_file:
            QA = json.load(json_file)

        for to_delete in deleting:
            if v_id in to_delete:
                qs_to_del = to_delete[v_id]

                for q_id in qs_to_del:
                    if q_id in QA:
                        num_deleted = num_deleted + 1
                        del QA[q_id]

        with open('../exports/%s/smoothed/%s/%s.txt' % (d_path, group, v_id), 'w+') as json_file:
            json.dump(QA, json_file)

        if cnt % 100 == 0:
            print(cnt)
        cnt = cnt + 1
    print("the number deleted was ", num_deleted)
    print('finished', stop)


trunc_perc = .05
head_percent_of_x_axis = .2
max_head_percent_of_dist = .3
percent_og_to_retain = .1
b_val = 3 # will be raised as we get higher


if __name__ == '__main__':
    print("done imports")
    step = sys.argv[1:][2]
    group = sys.argv[1:][1]
    d_path = sys.argv[1:][0]
    valid = True

    jobs = []
    if group == 'test':
        if step in ['bin_glob_del', 'loc_del']:
            ranges = [(0, 303), (303, 555), (555, 807), (807, 1059), (1059, 1311), (1311, 1563), (1563, 1814)]
        elif step == 'bin_bal':
            ranges = [i for i in range(len(BINARY_GLOBAL_IDS))]
            print('looking at indices', ranges)
        else:
            ranges = [(0, len(test_stsgs))]
    elif group == 'train':
        if step in ['bin_glob_del', 'loc_del']:
            ranges = [(0, 1110), (1110, 2220), (2220, 3330), (3330, 4440), (4440, 5550), (5550, 6660), (6660, 7787)]

        elif step == 'bin_bal':
            ranges = [i for i in range(len(BINARY_GLOBAL_IDS))]
        else:
            ranges = [(0, len(train_stsgs))]
    else:
        print('D invalid group', group)
        valid = False

    if valid:
        for r in ranges:
            print("making range")
            if step == 'bin_glob_dict':
                p = Process(target=bs.getDictByQType, args=(group, r[0], r[1], d_path,))
            elif step == 'bin_bal':
                p = Process(target=balanceBinary, args=(group, False, r, d_path,))
            elif step == 'bin_by_vid':
                p = Process(target=binarySortDelByVID, args=(d_path, group,))
            elif step == 'glob_bal':
                p = Process(target=balanceGlobalOpen, args=(group, d_path,))
            elif step == 'glob_by_vid':
                openGlobSortDelByVID(d_path, group)
                p = None
            elif step == 'bin_glob_del':
                p = Process(target=deleteQuestions, args=(group, 'after_glob', r[0], r[1], d_path,))
            elif step == 'loc_dict':
                bs.getOpenLocalDict(group, d_path)
                p = None
            elif step == 'loc_bal':
                p = Process(target=balanceLocalOpen, args=(group, d_path,))
            elif step == 'loc_by_vid':
                localOpenSortDelByVID(d_path, group)
                p = None
            elif step == 'loc_del':
                p = Process(target=deleteQuestions, args=(group, 'after_loc', r[0], r[1], d_path,))
            else:
                print('invalid step', step)
                p = None
            if p is not None:
                jobs.append(p)
                p.start()
