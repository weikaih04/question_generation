import json
import random
#import seaborn as sns
import pandas as pd
#import matplotlib.pyplot as plt
import pickle
import grammar as g
import os

#infile = open('../data/videos_stsg.pkl', 'rb')
infile = open('../data/stsgs/train_stsgs.pkl', 'rb')
train_stsgs = pickle.load(infile)
infile.close()

infile = open('../data/stsgs/test_stsgs.pkl', 'rb')
test_stsgs = pickle.load(infile)
infile.close()

with open('../data/templ2global.txt', 'rb') as f:
    templ2global = json.load(f)


bny = {
    'objExists': 0,
    'objRelExists': 0,
    'relExists': 0,
    'actExists': 0,
    'andObjRelExists': 0,
    'xorObjRelExists': 0,
    'objFirstVerify': 0,
    'objLastVerify': 0,
    'actTime': 0,
    'relTime': 0,
    'objTime': 0,
    'actLengthLongerVerify': 0,
    'actLengthShorterVerify': 0,
    #'actCountChooseMore': 0,
    #'actCountChooseFewer': 0,
    #'actLengthLongerChoose': 0,
    'actLengthShorterChoose': 0,
    'objFirstChoose': 0,
    'objLastChoose': 0,
    'objWhatChoose': 0,
}
    
opn = {
    'objWhat': 0,
    'objWhatGeneral': 0,
    'objFirst': 0,
    #'relFirst': 0,
    'objLast': 0,
    #'relLast': 0,
    #'actCount': 0,
    'actWhatAfterAll': 0,
     'actWhatBefore': 0,
     'actLast': 0,
     'actFirst': 0,
     'actLongest': 0,
     'actShortest': 0,
}

def translateType(tp):
    if tp == 'query':
        return 'open'
    else:
        return 'binary'
    

def getVideoIDS(group):
    if group == 'train':
        return list(train_stsgs)
    elif group == 'test':
        return list(test_stsgs)
    
def loadJSON(path):
    with open(path) as json_file:
        QA = json.load(json_file)
    return QA

def getQA(d_path, group, bal_txt, v_id):
    with open('../exports/%s/%s/%s/%s.txt' % (d_path, bal_txt, group, v_id)) as json_file: #CHANGED
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
        
def pickleDump(var, destination):
    f = open(destination,"wb")
    pickle.dump(var,f)
    f.close() 
    
    
def pickleLoad(path):
    file = open(path, 'rb')
    info = pickle.load(file)
    file.close()
    return info


def getDF(qs):
    for q in qs:
        for i in q['attributes']:
            q[i] = q['attributes'][i]
            
    return pd.DataFrame(qs)

def mark(x):
    if x:
        return 1
    return 0


with open('../data/template_ids.txt') as json_file:
    templ_ids_dict = json.load(json_file)
    
templ_ids = []

for i in templ_ids_dict:
    templ_ids.append(i)


def getQA(d_path, v_id, group, getall=False):
    if getall: 
        bal_text = 'all'
    else:
        bal_text = 'balanced'
    with open('../exports/%s/%s/%s/%s.txt' % (d_path, bal_text, group, v_id)) as json_file:
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
    
def sums(dic):
    s = 0
    for i in dic:
        s = s + dic[i]
    return s

def total(dic):
    tot = 0
    for i in dic:
        tot = tot + dic[i]
    return tot

def perc(num, denom):
    if denom == 0:
        return 'denom 0'
    return round(num / denom  * 100, 2)
        
def findMax(ans):
    #print("finding max for ", ans)
    mx = 0
    tot = 0
    
    for a in ans:
        cnt = ans[a]
        tot = tot + cnt
        if cnt > mx:
            mx = cnt
            #print("Current Max: ", mx)
                
    return mx, tot

def randomChanceByTempl(by_templ):
    
    rand = {}
    for t in by_templ:
        mx, tot = findMax(by_templ[t])
        if tot == 0:
            #print("tot is 0 for template ", t)
            perc = 0
        else:
            perc = round(mx / tot, 3)
            
        rand[t] = (perc, mx, tot)
        
    return rand
        

def true(x):
    if x:
        return 1
    return 0

def combineSemantic(x):
    if x == 'objrel':
        return 'relation'
    else:
        return x


def getPredsList(path):
    print("getting preds from: ", path)
    with open(path) as f:
        preds = json.load(f)
    
    return preds

def getPredsDic(preds_list):
    preds_dic = {}
    preds_dic['Total_preds'] = {i['csv_q_id']: 1 for i in preds_list}
    for descr in preds_list[0]:
        if descr == 'question': 
            descr2 = 'words'
        elif descr == 'answer':
            descr2 = 'AGQA_ans'
        else:
            descr2 = descr
        preds_dic[descr2] = {i['csv_q_id']: i[descr] for i in preds_list}
    
    if 'id' in preds_dic:
        preds_dic.pop('id')

    return preds_dic

def qIsCorrect(equiv_id, mapping):
    if equiv_id not in mapping:
        return equiv_id
    elif mapping[equiv_id]:
        return 1
    else:
        return 0

# determine if each prediction had direct equiv correct
def getToDirectCorrect(df):
    # ake a dic of all the questions to if they are correct or not
    mapping = dict(zip(df.id, df.correct))

    # make a new column that does .apply(and then see if the direct is correct)

    print("DIRECT EQUIV PRESENT -1: %s" % ('direct_equiv' in df.columns))

    df['direct_correct'] = df['direct_equiv'].apply(qIsCorrect, args=(mapping,))


    print("DIRECT EQUIV PRESENT 0: %s" % ('direct_equiv' in df.columns))
    return df


def makePredsDF(path, metric, exploded_global=False):
    # get all predictions
    preds_list = getPredsList(path)

    # translate if in wrong format
    if model == 'hme':
        preds_list = translateHME(preds_list, 'dataset', metric)
    if model == 'psac':
        preds_list = translatePSAC(preds_list)

    
    # get data frame of all the stuff
    if exploded_global:
        df = df_qs_g
    else:
        df = df_qs
    dics = []
    
    start = 0
    split = 50000
    preds_dic = getPredsDic(preds_list)
    
    for i in preds_dic:
        df[i] = df['id'].map(preds_dic[i])

    df = df[df['Total_preds'] == 1]
    
    
    df.loc[:,'semantic'] = df['semantic'].apply(combineSemantic)
    df.loc[:,'correct'] = df['AGQA_ans'] == df['prediction']
    df.loc[:,'correct'] = df['correct'].apply(true)

    df = getToDirectCorrect(df)


    return df


def translateHME(preds, d_path, metric):
    if False:
        with open('../exports/%s/results/hme/%s/translation/idx2ans.pkl' % (d_path, metric), 'rb') as f_i2a:
            idx2ans = pickle.load(f_i2a)

            
        with open('../exports/%s/results/hme/%s/translation/word2idx.pkl' % (d_path, metric), 'rb') as f_i2a:
            word2idx = pickle.load(f_i2a)
            
        for pred in preds:
            if pred['prediction'] in ['Yes', "No"]:
                p = pred['prediction'].lower()
            else:
                p = pred['prediction']
            if True:
                if p == '.':
                    print('p is .')
                    eng_p = ''
                else:
                    idx_p = word2idx[p]
                    eng_p = idx2ans[idx_p]
                
            else: 
                eng_p = idx2ans[p]
                pred['answer'] = idx2ans[pred['answer']]
            
            pred['prediction'] = eng_p
            
            pred['video_name'] = pred['csv_q_id'][:5]
        
    return preds

def translatePSAC(preds):
    tr_preds = []
    
    for pred in preds:
        pred['video_name'] = pred['csv_q_id'][:5]
        
        tr_preds.append(pred)
        
    return tr_preds

def addCnt(correct_cnt, flag):
    if flag in correct_cnt:
        return correct_cnt[flag]
    else:
        return 0

def getResults(model, metric_overall, preds_path, output_path):
    # get preds
    preds = makePredsDF(preds_path, metric_overall, exploded_global=False)
    print('preds shape A', preds.shape)
    print('TESTING THIS FREAKING WORKS!!!')
    print("DIRECT EQUIV PRESENT A: %s" % ('direct_equiv' in preds.columns))

    store = {}
    store['perc_correct'] = {}
    store['cnt_correct'] = {}
    store['cnt_incorrect'] = {}
    perc = store['perc_correct']
    cnt_cor = store['cnt_correct']
    cnt_incor = store['cnt_incorrect']
    # size
    store['size'] = preds.shape[0]

    # total
    correct_cnt = preds.groupby(['correct']).sum().Total_preds.to_dict()
    correct_perc = preds.groupby(['Total_preds']).mean().correct.to_dict()

    perc['total'] = correct_perc[1]
    cnt_cor['total'] = correct_cnt[1]
    cnt_incor['total'] = correct_cnt[0]

    # for things with only 1 item
    for metric in ['novel_comp', 'nc_seq', 'nc_sup', 'nc_dur', 'nc_objrel', 'indirect', 'i_obj', 'i_act', 'i_temp', 'direct_correct', 'more_steps']:
        some_preds = preds[preds[metric] == 1]
        correct_cnt = some_preds.groupby(['correct']).sum().Total_preds.to_dict()
        correct_perc = some_preds.groupby([metric]).mean().correct.to_dict()
        if 1 in correct_perc:
            perc[metric] = correct_perc[1]
        else:
            perc[metric] = 0
        if 1 in cnt_cor:
            cnt_cor[metric] = correct_cnt[1]
        else:
            cnt_cor[metric] = 0
        if 0 in cnt_cor:
            cnt_incor[metric] = correct_cnt[0]
        else:
            cnt_incor[metric] = 0
        
        # each of these split by type
        correct_cnt = some_preds.groupby(['ans_type', 'correct']).sum().Total_preds.to_dict()
        correct_perc = some_preds.groupby(['ans_type']).mean().correct.to_dict()

        metric = '%s-tp' % metric
        perc[metric] = {}
        cnt_cor[metric] = {}
        cnt_incor[metric] = {}
        for tp in correct_perc:
            perc[metric][tp] = correct_perc[tp]
            cnt_cor[metric][tp] = addCnt(correct_cnt, (tp, 1))
            cnt_incor[metric][tp] = addCnt(correct_cnt, (tp, 0))

    # by ans_type
    for metric in ['ans_type', 'structural', 'semantic', 'type', 'steps']:
        correct_cnt = preds.groupby([metric, 'correct']).sum().Total_preds.to_dict()
        correct_perc = preds.groupby([metric]).mean().correct.to_dict()

        perc[metric] = {}
        cnt_cor[metric] = {}
        cnt_incor[metric] = {}
        for s in correct_perc:
            perc[metric][s] = correct_perc[s]
            cnt_cor[metric][s] = addCnt(correct_cnt, (s, 1))
            cnt_incor[metric][s] = addCnt(correct_cnt, (s, 0))
    # Semantic_split_ans-type

    correct_cnt = preds.groupby(['semantic', 'ans_type', 'correct']).sum().Total_preds.to_dict()
    correct_perc = preds.groupby(['semantic', 'ans_type']).mean().correct.to_dict()
    metric = 'semantic-tp'
    perc[metric] = {'action': {}, 'object': {}, 'relation': {}}
    cnt_cor[metric] = {'action': {}, 'object': {}, 'relation': {}}
    cnt_incor[metric] = {'action': {}, 'object': {}, 'relation': {}}
    for sem, tp in correct_perc:
        perc[metric][sem][tp] = correct_perc[(sem, tp)]
        cnt_cor[metric][sem][tp] = addCnt(correct_cnt, (sem, tp, 1))
        cnt_incor[metric][sem][tp] = addCnt(correct_cnt, (sem, tp, 0))


    # get global 
    print('preds shape B', preds.shape)
    preds_g = makePredsDF(preds_path, metric_overall, exploded_global=True)
    print('preds shape C', preds.shape)

    # set up dics & do normal globa
    correct_cnt = preds_g.groupby(['global', 'correct']).sum().Total_preds.to_dict()
    correct_perc = preds_g.groupby(['global']).mean().correct.to_dict()

    for metric in ['global', 'global-tp']:
        perc[metric] = {}
        cnt_cor[metric] = {}
        cnt_incor[metric] = {}

    metric = 'global'
    for s in correct_perc: 
        perc[metric][s] = correct_perc[s]
        cnt_cor[metric][s] = addCnt(correct_cnt, (s, 1))
        cnt_incor[metric][s] = addCnt(correct_cnt, (s, 0))

    # do global split by global type
    metric = 'global-tp'
    for glob in correct_perc: 
        perc[metric][glob] = {}
        cnt_cor[metric][glob] = {}
        cnt_incor[metric][glob] = {}

    
    correct_cnt = preds_g.groupby(['global', 'ans_type', 'correct']).sum().Total_preds.to_dict()
    correct_perc = preds_g.groupby(['global', 'ans_type']).mean().correct.to_dict()
    for sem, tp in correct_perc:
        perc[metric][sem][tp] = correct_perc[(sem, tp)]
        cnt_cor[metric][sem][tp] = addCnt(correct_cnt, (sem, tp, 1))
        cnt_incor[metric][sem][tp] = addCnt(correct_cnt, (sem, tp, 0))


    # see if direct_version is correct

    
    # save file
    print('saving to ', output_path)
    with open(output_path + '.json', 'w+') as f:
        json.dump(store, f)

    print('preds shape D', preds.shape)
    preds.to_csv(output_path + '-preds.csv')
    preds_g.to_csv(output_path + '-preds_g.csv')

    print("DIRECT EQUIV PRESENT B: %s" % ('direct_equiv' in preds.columns))

    return


def pathExists(path):
    return os.path.exists(path)

##########################################
#          Variables to Adjust           #
##########################################

# d_path and group
d_path = 'dataset'
group = 'test'

# Getting dataframe of questions
path = '../exports/%s/other_formats/%s-%s-agqa.csv'
path_g = '../exports/%s/other_formats/%s-%s-agqa-global.csv'
df_qs = pd.read_csv(path % (d_path, group, 'balanced'))
df_qs_g = pd.read_csv(path_g % (d_path, group, 'balanced'))


for model in ['hcrn']:#, 'psac']: #'hcrn', 
    for metric in ['blind']: #, 'balanced', 'blind', 'compo', 'steps_templ'
        for epoch in range(1):
            preds_path = '../exports/%s/results/%s_agqa_preds/preds_%s.json' % (d_path, metric, model)

            if pathExists(preds_path):
                output_path = '../exports/%s/results/organized/preds_%s_%s_%s' % (d_path, model, metric, epoch)
                getResults(model, metric, preds_path, output_path)
            else:
                print('Dont have results for: ', preds_path)



if False:
    for model in ['hcrn', 'hme', 'psac']:
        for metric in ['balanced', 'blind', 'compo', 'steps_templ']: #, 
            for epoch in range(1):
                preds_path = '../exports/%s/results/%s/%s/preds/preds_%s_%s.json' % (d_path, model, metric, metric, epoch)
                preds_path = '../exports/%s/results/%s/%s/preds/preds_%s_%s.json' % (d_path, model, metric, metric, epoch)
                #preds_path = '../../../Desktop/test_preds.json'

                if pathExists(preds_path):
                    output_path = '../exports/%s/results/organized/preds_%s_%s_%s' % (d_path, model, metric, epoch)
                    #output_path = '../../../Desktop/test_preds-organized.json'
                    getResults(model, metric, preds_path, output_path)

