import json
import pickle
import random
import math


with open('../data/train_video_names.txt', 'rb') as f:
    train_stsgs = json.load(f)


with open('../data/test_video_names.txt', 'rb') as f:
    test_stsgs = json.load(f)

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


def getValueCount(dic):
    cnt = {}
    for i in dic:
        tot = 0
        for tt in dic[i]:
            tot += len(dic[i][tt])
        cnt[i] = tot
    return cnt


def getTemporalType(group, d_path, balanced):
    with open('../exports/%s/metrics/%s/%s/temporalChangeAns.txt' % (d_path, balanced, group), 'rb') as f:
        one = json.load(f)
    f.close()

    return one


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


def getTempTypeDic():
    dic = {
        'no_temporal': [],
        'same_ans': [],
        'diff_ans': [],
        'no_direct': [],
    }
    return dic


def getTemporalValue(temp_type, v_id, q_id):
    if v_id in temp_type and q_id in temp_type[v_id]:
        temporal = temp_type[v_id][q_id]
    else:
        temporal = 'no_time'

    return temporal


def getDictByQType(group, start, stop, d_path):
    print("dpath is ", d_path)

    opn = {}
    bny = {}

    temp_type = getTemporalType(group, d_path, 'all')

    for glob in OPEN_GLOBAL_IDS:
        opn[glob] = {}
    for glob in BINARY_GLOBAL_IDS:
        bny[glob] = {}

    for glob in bny:
        bny[glob]['all'] = {}

    if group == "train":
        stsgs = train_stsgs
    elif group == "test":
        stsgs = test_stsgs
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
            struct = q['attributes']['structural']
            if struct == 'query':
                ans_type = 'open'
            else:
                ans_type = 'binary'

            ans = str(q['answer'])

            if ans_type == 'binary':
                loc = getBinaryCat(q)
                category = bny[glob]['all']
                if loc not in category:
                    category[loc] = {}
                if ans not in category[loc]:
                    category[loc][ans] = getTempTypeDic()

                temporal = temp_type[v_id][q_id]
                category[loc][ans][temporal].append(q_id)
            if ans_type == 'open':
                if glob == 'count' and type(q['answer']) == int:
                    glob = 'count-int'
                if ans not in opn[glob]:
                    opn[glob][ans] = getTempTypeDic()
                temporal = temp_type[v_id][q_id]
                opn[glob][ans][temporal].append(q_id)
        cnt = cnt + 1

        if cnt % 100 == 0:
            print("finished", cnt)

    print("Saving to: ", "../exports/%s/by_q_type/binary/%s-%s-%s.pkl" % (d_path, group, start, stop))
    pickleDump(bny, "../exports/%s/by_q_type/binary/%s-%s-%s.pkl" % (d_path, group, start, stop))
    pickleDump(opn, "../exports/%s/by_q_type/open_global/%s-%s-%s.pkl" % (d_path, group, start, stop))


def sumsToDel(to_del):
    tot = 0
    for i in to_del:
        x = to_del[i]
        if type(x) != int:
            print("type of i does not equal list")
            print(i, 'is the thing thats not a lost')
        tot += x
    return tot


def getIdsToDelete(ans, cnt):
    a = splitIdsToDelete(ans, cnt)

    to_del = a[0]
    leftovers = a[1]
    if leftovers != 0:
        print("LEFTOVERS ARE NOT 0")
        print(to_del)

    # make sure deleting rom both (do that in func above)
    updated_to_del = {}
    q_ids = []

    for i in to_del:
        # what if - i dont let it do this until its all of them
        # so if its ==, delete all
        # if its >, add to leftovers
        # afterwards, use all leftovers to deleter where posisble
        num_to_del = to_del[i]
        if num_to_del > len(ans[i]):
            leftovers += num_to_del - len(ans[i])
            num_to_del = len(ans[i])
        updated_to_del[i] = num_to_del

    if leftovers > 1:
        half = math.floor(leftovers / 2)
        if half <= len(ans['same_ans']) and half <= len(ans['diff_ans']):
            to_del['same_ans'] += half
            to_del['diff_ans'] += half
            leftovers -= 2 * half
        else:
            1+1

    if leftovers == 1:
        # try to put in one or other, ow put in 1
        leftovers -= 1

    for i in updated_to_del:
        if type(ans[i]) == str:
            print('SAMPLING FROM STRING!')
        q_ids.append(random.sample(ans[i], k=updated_to_del[i]))

    if sumsToDel(to_del) != cnt:
        print('sum of to_del', sumsToDel(to_del), 'does not equal count!', cnt)
    if sumsToDel(updated_to_del) != cnt:
        print('sum of updatedto_del', sumsToDel(updated_to_del),
              'does not equal count!', cnt)

    if type(q_ids) != list:
        print('q-ids not a list')
    for i in q_ids:
        if type(i) != list:
            print("THING IN QIDS IS NOT A LIST IS A ", type(i))
        for j in i:
            if len(j) < 6:
                print("Length of item in list of lists is less than 6")
                print('it is', j)
    return q_ids


def splitIdsToDelete(ans, cnt):
    no_temporal = ans['no_temporal']
    same = ans['same_ans']
    diff = ans['diff_ans']
    no_direct = ans['no_direct']

    len_no_temporal = len(no_temporal)
    len_same = len(same)
    len_diff = len(diff)
    len_no_direct = len(no_direct)

    to_del = {
            'no_temporal': 0,
            'same_ans': 0,
            'diff_ans': 0,
            'no_direct': 0,
        }
    sums = 0
    for i in ans:
        sums += len(ans[i])

    if cnt >= sums:
        for i in ans:
            to_del[i] = len(ans[i])
        cnt -= sums
        return to_del, cnt

    if len_same != len_diff:
        dif_btwn_dics = abs(len_diff - len_same)
        if len_diff < len_same:
            bigger = 'same_ans'

            if cnt <= dif_btwn_dics:
                to_del[bigger] = cnt
                len_same -= cnt
                cnt -= cnt
            else:
                to_del[bigger] = dif_btwn_dics
                len_same -= dif_btwn_dics

                cnt -= dif_btwn_dics
        else:
            bigger = 'diff_ans'

            if cnt <= dif_btwn_dics:
                to_del[bigger] = cnt
                len_diff = 0
                cnt -= cnt
            else:
                to_del[bigger] = dif_btwn_dics
                len_diff -= dif_btwn_dics
                cnt -= dif_btwn_dics

    if cnt == 0:
        return to_del, cnt

    if len_same != len_no_direct:
        dif_btwn_dics = abs(len_same - len_no_direct)
        if len_no_direct < len_same:

            half_cnt = math.floor(cnt / 2)

            if half_cnt <= dif_btwn_dics:
                to_del['same_ans'] += half_cnt
                len_same -= half_cnt
                to_del['diff_ans'] += half_cnt
                len_diff -= half_cnt
                cnt -= 2 * half_cnt

            else:
                # so here, deleting all the rest of count
                # would drop same/diff below no_direct
                # so instead split dif_btwn_dics in half. or no!
                half_diff_len = dif_btwn_dics
                to_del['same_ans'] += half_diff_len
                len_same -= half_diff_len
                to_del['diff_ans'] += half_diff_len
                len_diff -= half_diff_len

                cnt -= 2 * half_diff_len
        else:
            # so here, no direct has more than the other 2
            if cnt <= dif_btwn_dics:
                to_del['no_direct'] += cnt
                len_no_direct -= cnt
                cnt -= cnt
            else:
                to_del['no_direct'] += dif_btwn_dics
                len_no_direct -= dif_btwn_dics
                cnt -= dif_btwn_dics

    if cnt == 0:
        return to_del, cnt

    if len_same != len_no_temporal:
        # split into 3 and see if can delete
        # take the floor & then left overs get del from no direct
        dif_btwn_dics = abs(len_no_temporal - len_same)
        if len_no_temporal < len_same:
            third_cnt = math.floor(cnt / 3)

            if third_cnt <= dif_btwn_dics:
                to_del['same_ans'] += third_cnt
                len_same -= third_cnt
                to_del['diff_ans'] += third_cnt
                len_diff -= third_cnt
                to_del['no_direct'] += third_cnt
                len_no_direct -= third_cnt

                cnt -= 3 * third_cnt

            else:
                third_diff_len = dif_btwn_dics
                to_del['same_ans'] += third_diff_len
                len_same -= third_diff_len
                to_del['diff_ans'] += third_diff_len
                len_diff -= third_diff_len
                to_del['no_direct'] += third_diff_len
                len_no_direct -= third_diff_len

                cnt -= 3 * third_diff_len

        else:
            if cnt < dif_btwn_dics:
                to_del['no_temporal'] += cnt
                len_no_temporal -= cnt
                cnt -= cnt
            else:
                to_del['no_temporal'] += dif_btwn_dics
                len_no_temporal -= dif_btwn_dics
                cnt -= dif_btwn_dics

    if cnt == 0:
        return to_del, cnt

    fourth_cnt = math.floor(cnt / 4)

    # so here is an issue b/c not necesarily
    leftovers = cnt % 4
    if len_same >= fourth_cnt:
        to_del['same_ans'] += fourth_cnt
        len_same -= fourth_cnt
        cnt -= fourth_cnt
    else:
        to_del['same_ans'] += len_same
        leftovers += (fourth_cnt + len_same)
        cnt -= len_same
        len_same = 0
    if len_diff >= fourth_cnt:
        to_del['diff_ans'] += fourth_cnt
        len_diff -= fourth_cnt
        cnt -= fourth_cnt
    else:
        to_del['diff_ans'] += len_diff
        leftovers += (fourth_cnt + len_diff)
        cnt -= len_diff
        len_diff = 0
    if len_no_direct >= fourth_cnt:
        to_del['no_direct'] += fourth_cnt
        len_no_direct -= fourth_cnt
        cnt -= fourth_cnt
    else:
        to_del['no_direct'] += len_no_direct
        leftovers += (fourth_cnt + len_no_direct)
        cnt -= len_no_direct
        len_no_direct = 0
    if len_no_temporal >= fourth_cnt:
        to_del['no_temporal'] += fourth_cnt
        len_no_temporal -= fourth_cnt
        cnt -= fourth_cnt
    else:
        to_del['no_temporal'] += len_no_temporal
        leftovers += (fourth_cnt + len_no_temporal)
        cnt -= len_no_temporal
        len_no_temporal = 0

    # so here and above, only del if smaler then the len ow. take fro elsewhere
    if leftovers < len_no_temporal:
        to_del['no_temporal'] += leftovers

        cnt -= leftovers
    else:
        to_del['no_temporal'] += len_no_temporal
        leftovers -= len_no_temporal
        cnt -= len_no_temporal
        len_no_temporal = 0

        if leftovers >= 2:
            # this should be the even?
            half_left = math.floor(leftovers / 2)
            min_group_len = min(len_same, len_diff)

            if half_left < min_group_len:
                to_del['same_ans'] += half_left
                len_same -= half_left
                to_del['diff_ans'] += half_left
                len_diff -= half_left
                leftovers -= 2 * half_left
                cnt -= 2 * half_left
            else:
                to_del['same_ans'] += min_group_len
                len_same -= min_group_len
                to_del['diff_ans'] += min_group_len
                len_diff -= min_group_len
                leftovers -= 2 * min_group_len
                cnt -= 2 * min_group_len

        if len_no_direct < leftovers:
            to_del['same_ans'] += 1
            cnt -= 1

        elif leftovers == 1:
            to_del['no_direct'] += 1
            cnt -= 1
    return to_del, cnt


def getOpenLocalDict(group, d_path):
    opn = {}

    temp_type = getTemporalType(group, d_path, 'all')

    # separate all by global categories
    for glob in OPEN_GLOBAL_IDS:
        opn[glob] = {}

    if group == "train":
        stsgs = train_stsgs
    elif group == "test":
        stsgs = test_stsgs
    else:
        print("INVALID GROUP", group)
        return

    cnt = 0
    for v_id in stsgs:
        with open('../exports/%s/smoothed/%s/%s.txt' % (d_path, group, v_id)) as json_file:
            QA = json.load(json_file)
        for q_id in QA:
            q = QA[q_id]

            struct = q['attributes']['structural']
            if struct == 'query':
                ans_type = 'open'
            else:
                ans_type = 'binary'

            if ans_type == 'binary':
                continue

            glob = q['global']
            loc = q['local']

            ans = str(q['answer'])
            if ans_type == 'open':
                if glob == 'count' and type(q['answer']) == int:
                    glob = 'count-int'
                if loc not in opn[glob]:
                    opn[glob][loc] = {}
                loc_dict = opn[glob][loc]
                if ans not in loc_dict:
                    loc_dict[ans] = getTempTypeDic()
                temporal = temp_type[v_id][q_id]
                loc_dict[ans][temporal].append(q_id)
        if cnt % 100 == 0:
            print(cnt)
        cnt = cnt + 1

    pickleDump(opn, "../exports/%s/by_q_type/open_local/%s-%s-%s.pkl" % (d_path, group, 0, len(stsgs)))
    return opn
