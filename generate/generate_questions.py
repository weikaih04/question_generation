from fill_templates import iterateTemplate, iterateTemplateActionIndirect
from templates import getTemplatesForVideo
import templates_action_indirect
import compositional_refs as cr
import compositional_refs_action
import pickle
import json

infile = open('../data/stsgs/test_stsgs.pkl', 'rb')
test_stsgs = pickle.load(infile)
infile.close()

infile = open('../data/stsgs/train_stsgs.pkl', 'rb')
train_stsgs = pickle.load(infile)
infile.close()

infile = open('../data/video_names.txt', 'rb')
video_names = json.load(infile)
infile.close()


banned_templates = ['actWhatBetweenWhileEndOneLast',
                    'actWhatBetweenWhileStartOneLast',
                    'actWhatBetweenWhileEndOneFirst',
                    'actWhatBetweenWhileStartOneFirst',
                    'actWhatStart',
                    'actWhatEnd',
                    'actCountChooseMore',
                    'actCountChooseFewer',
                    'actCount'
                    'relFirst',
                    'relLast',
                    'actExists']

good_templates = [
    'objExists', 'objRelExists', 'relExists',
    'andObjRelExists', 'xorObjRelExists',
    'objWhatGeneral', 'objWhat', 'objWhatChoose',
    'actWhatAfterAll', 'actWhatBefore', 'objFirst',
    'objFirstChoose', 'objFirstVerify', 'actFirst',
    'objLast', 'objLastChoose', 'objLastVerify', 'actLast',
    'actLengthLongerChoose', 'actLengthShorterChoose',
    'actLengthLongerVerify', 'actLengthShorterVerify',
    'actLongest', 'actShortest', 'actTime', 'relTime', 'objTime'
]


def generateQuestions(group, start, stop, save, adding):
    """ generates AGQA questions

    Args:
           group: str (train or test)
           start: int (starting scene graph index)
           stop: int (ending scene graph index)
           save: str (`save` if want to save)
           adding: str ('add' if want to add to existing file)

    Returns:
        saves generated questions if indicated
    """
    v_ids = []
    cnt = 0

    if group == 'train':
        stsgs = train_stsgs
    elif group == 'test':
        stsgs = test_stsgs
    else:
        print("Invalid group ", group)
        return

    total = 0
    print("Begin generation for %s-%s" % (start, stop))



    # ADDED
    breaks_on = {}

    # Iterate through all videos
    for s_idx in stsgs:
        if cnt < start:
            cnt = cnt + 1
            continue
        if cnt >= stop:
            break

        # set up blank templates and indirects
        templates = getTemplatesForVideo(stsgs[s_idx])
        indirect = cr.makeIndirect(stsgs[s_idx])

        if adding == 'add':
            # pull out existing questions
            video_path = "../exports/dataset/all/%s/%s.txt" % (group, s_idx)
            with open(video_path, 'rb') as infile:
                video_qa = json.load(infile)
            stsg_cnt = int(list(video_qa.keys())[-1].split('-')[1])

        else:
            video_qa = {}
            stsg_cnt = 0

        # Iterate through each template and generate questions

        # CHANGED
        for t_idx in good_templates:
            if (t_idx in banned_templates) or (t_idx == 'actCount'):
                continue
            # ADDED
            temp, templ_cnt, breaks_on = iterateTemplate(templates[t_idx],
                                              indirect, stsg_cnt, breaks_on)
            stsg_cnt = stsg_cnt + templ_cnt
            video_qa.update(temp)

        # Save to file if saving
        if save:
            video_path = "../exports/dataset/all_without_indirect/%s/%s.txt" % (group, s_idx)
            with open(video_path, 'w+') as outfile:
                json.dump(dict(video_qa), outfile)

        total += len(video_qa)

        v_ids.append((s_idx, cnt))
        cnt = cnt + 1

        if cnt % 25 == 0:
            print(cnt)

    print("Done %s-%s: generated %s questions" % (start, stop, total))
    # ADDED
    print(breaks_on)


def generateQuestionsIndirect(group, start, stop, save):
    """ generates AGQA questions with an indirect object in action

    Args:
           group: str (train or test)
           start: int (starting scene graph index)
           stop: int (ending scene graph index)
           save: str (`save` if want to save)

    Returns:
        saves generated questions if indicated
    """
    v_ids = []
    cnt = 0

    if group == 'train':
        stsgs = train_stsgs
    elif group == 'test':
        stsgs = test_stsgs
    else:
        print("Invalid group ", group)
        return

    total = 0

    for s_idx in stsgs:
        if cnt < start:
            cnt = cnt + 1
            continue
        if cnt >= stop:
            break

        # Load existing dataset
        video_path = "../exports/dataset/all_without_indirect/%s/%s.txt" % (group, s_idx)
        with open(video_path, 'rb') as infile:
            video_qa = json.load(infile)

        if len(video_qa) == 0:
            if save:
                video_path = "../exports/dataset/all/%s/%s.txt" % (group, s_idx)
                with open(video_path, 'w+') as outfile:
                    json.dump(dict(video_qa), outfile)

            continue

        # set up blank templates and indirects
        templs = templates_action_indirect.getTemplatesForVideo(stsgs[s_idx])
        indirect = compositional_refs_action.makeIndirect(stsgs[s_idx])

        stsg_cnt = int(list(video_qa.keys())[-1].split('-')[1])

        for t_idx in ['objFirstChoose', 'objLastChoose', 'relTime', 'actTime']: #good_templates:
            if (t_idx in banned_templates) or (t_idx == 'actCount'):
                continue

            temp, templ_cnt = iterateTemplateActionIndirect(templs[t_idx],
                                                            indirect, stsg_cnt)
            stsg_cnt = stsg_cnt + templ_cnt
            video_qa.update(temp)

        # Sve if indicated
        if save:
            video_path = "../exports/dataset/all/%s/%s.txt" % (group, s_idx)
            with open(video_path, 'w+') as outfile:
                json.dump(dict(video_qa), outfile)

        total += len(video_qa)
        v_ids.append((s_idx, cnt))
        cnt = cnt + 1

        if cnt % 25 == 0:
            print(cnt)

    print("Done %s-%s: generated %s questions" % (start, stop, total))


# CHANGED
#generateQuestionsIndirect('test', 0, 100, 'save')


def saveTemplateIds():
    """ saves all the used templates and the number of
        natural language questions

    Args:

    Returns:
        saves the used templates
    """

    t_ids = {}
    num_nl = 0
    for s_idx in test_stsgs:
        templates = getTemplatesForVideo(test_stsgs[s_idx])
        for t_id in good_templates:
            if t_id in banned_templates:
                continue
            t_ids[t_id] = 0
            num_nl += len(templates[t_id]['questions'])

        break

    print("Numer of natural language templates", num_nl)
    with open("../data/template_ids.txt", 'w') as outfile:
        json.dump(dict(t_ids), outfile)

saveTemplateIds()