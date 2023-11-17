import program_modules as pm
import grammar as g
import solve
import pickle
import random
import templates
from locate_char import find_char_location
import json

f = open('../data/idx.pkl', 'rb')
IDX = pickle.load(f)
f.close()

f = open('../data/actionSV.pkl', 'rb')
ACTION_SV = pickle.load(f)
f.close()

f = open('../data/past.pkl', 'rb')
PAST = pickle.load(f)
f.close()

f = open('../data/present.pkl', 'rb')
PRES = pickle.load(f)
f.close()

f = open('../data/object_with_article.pkl', 'rb')
ART_OBJ= pickle.load(f)
f.close()

SINGLE_OBJ_VERBS = ['v024', 'v011', 'v013', 'v029', 'v027', 'v015', 'v007', 'v002']

with open('../data/multi_subj_verbs', 'rb') as f:
    multi_subj_verbs = json.load(f)

def makeIndirect(stsg):
    """
    Args:
        stsg: a spatio-temporal scene graph

    Returns:
        A dictionary of indirect references.
    """

    obj = stsg['obj_names']
    act = stsg['act_names']
    arel = stsg['arel_names']
    crel = stsg['crel_names']
    srel = stsg['srel_names']
    vrel = stsg['vrel_names']

    refs = {}

    metrics = {
        'before': [],
        'first': [],
        'longer': [],
        'repetition': [],
        'objrel': [[], []],
        'indirects': [False] * 4
    }

    refs['time'] = {}
    refs = addAllTime(stsg, refs)
    refs = addObjects(stsg, obj, arel, crel, srel, vrel, refs, metrics)
    refs = addRelations(stsg, obj, arel, crel, srel, vrel, refs, metrics)
    refs = addActions(stsg, act, obj, refs, metrics)
    refs = addTime(stsg, act, refs, metrics)

    return refs


def addObjects(stsg, obj, arel, crel, srel, vrel, refs, metrics):
    """ Create indirect objects references

    Args:
        stsg: the spatiotemporal scene graph
        obj: a list of all objects in video
        arel: a list of all attention relationships in video
        crel: a list of all contact relationships in video
        srel: a list of all spatial relationships in video
        vrel: a list of all verb relationships in video
        refs: current indirect reference dictionary

    Returns:
        An updated reference dictionary.
        Dictionary includes "object they were <reference> first" objects
    """

    metrics['indirects'] = [False] * 4

    for o in obj:
        refs[o] = {
            'direct': [makeRef(g.ENG[o], lambda a: a[0], 0,
                       [o], 'direct', False, metrics, g.ENG[o], {})]
        }

    all_time = refs['time']['all'][0]
    rels = crel + srel + vrel
    exactly_one = []
    more_than_one = []
    for rel in rels:
        rel_objs = solve.relRef(stsg, [rel, all_time])[0]
        if len(rel_objs) == 1:
            exactly_one.append(rel)
        else:
            more_than_one.append(rel)

    refs = addFirstObjRef(stsg, obj, arel, more_than_one, [], [], refs)
    refs = addLastObjRef(stsg, obj, arel,  more_than_one, [], [], refs)
    # refs = addTimeObjRef(stsg, obj, arel,  more_than_one, [], [], refs)
    refs = addSingleObjRef(stsg, obj, arel,  exactly_one, [], [], refs)

    for o in obj:
        for tp in refs[o]:
            if len(refs[o][tp]) > 3:
                refs[o][tp] = random.sample(refs[o][tp], k=3)

    return refs


def addRelations(stsg, obj, arel, crel, srel, vrel, refs, metrics):
    """ Create indirect objects references

    Args:
        stsg: the spatiotemporal scene graph
        obj: a list of all objects in video
        arel: a list of all attention relationships in video
        crel: a list of all contact relationships in video
        srel: a list of all spatial relationships in video
        vrel: a list of all verb relationships in video
        refs: current indirect reference dictionary

    Returns:
        An updated reference dictionary.
        Dictionary includes "first thing they did to <object>" objects
    """
    rels = crel + srel + vrel

    metrics['indirects'] = [False] * 4

    sg_verts = {(0, -1): []}

    for r in rels:
        if r not in g.PP:
            continue
        refs[r] = {
            'direct': [makeRef(g.PP[r], lambda a: a[0], 0,
                       [r], 'direct', False, metrics, g.PP[r], sg_verts)]
        }

    #refs = addFirstRelRef(stsg, obj, arel, crel, srel, vrel, refs)

    return refs


def addActions(stsg, act, obj, refs, metrics):
    """ Create indirect action references

    Args:
        stsg: the spatiotemporal scene graph=
        act: list of action names
        obj: a list of object names
        refs: current indirect reference dictionary

    Returns:
        An updated reference dictionary with action references
    """

    metrics['indirects'] = [False] * 4

    for a in act:
        refs[a] = {
            'direct': [makeRef(g.ENG[a], lambda a: a[0], 0,
                       [a], 'direct', False, metrics, g.ENG[a],
                       sg_verts={(0, -1): [a + '/1']})]
        }

    # refs = addLongest(stsg, act, error_margin, refs)
    # refs = addShortest(stsg, act, error_margin, refs)

    refs = addActionWithIndirectObject(stsg, act, refs)

    return refs


def addTime(stsg, act, refs, metrics):
    """ Create indirect time references

    Args:
        stsg: the spatiotemporal scene graph=
        act: list of actions
        refs: current indirect reference dictionary

    Returns:
        An updated reference dictionary with time objets
    """

    refs = addBefore(stsg, act, refs)
    refs = addAfter(stsg, act, refs)
    refs = addWhile(stsg, act, refs)
    # refs = addBetween(stsg, act, refs) # changed this, see how it effects

    return refs


def add(refs, direct, tp, phrase, program, steps,
        args, metrics, tree, sg_verts=['FAKE']):
    """ Adds a new indirect ref to references

    Args:
        refs: current reference dictionary
        direct: the direct idx referenced by this indirect phrase
        tp: string type of indirect reference
        phrase: string phrase associated with indirect reference
        program: the function associated with the indirect reference
        steps: the number of compositional steps to make the indirect reference
        args: an array of arguments used in the program

    Returns:
        A dictionary of references incorporating this new reference

    """
    if (direct not in refs):
        print(direct, " not in refs")
        return refs
    if (tp not in refs[direct]):
        refs[direct][tp] = []
    new_ref = makeRef(phrase, program, steps, args, tp,
                      direct == 'time', metrics, tree, sg_verts)

    refs[direct][tp].append(new_ref)
    return refs


def makeRef(phrase, program, steps, args, tp,
            direct_type, metrics, tree, sg_verts):
    """ Creates a new reference dictionary object

    Args:
        phrase: string phrase associated with indirect reference
        program: the function associated with the indirect reference
        steps: the number of compositional steps to make the indirect reference
        args: an array of arguments used in the program
        tp:
        direct_type: object, time, rel, action etc

    Returns:
        A new reference dictionary object incorporating the arguments
    """
    new_ref = {
        'phrase': phrase,
        'direct': program(args),
        'program': program,
        'steps': steps,
        'args': args,
        'type': tp,
        'metrics': metrics,
        'tree': tree,
        'sg_verts': sg_verts,
    }

    if direct_type:
        if len(phrase) == 0:
            new_ref['start_phrase'] = "In the video"
        else:
            new_ref['start_phrase'] = phrase[1:].capitalize()

    return new_ref


def combineIndirectMetrics(items, idx):
    new_indirect = []

    for i in range(4):
        nxt = False
        for item in items:
            if item['metrics']['indirects'][i]:
                nxt = True
                break

        new_indirect.append(nxt)

    new_indirect[idx] = True

    return new_indirect


def combineMetrics(items, tp):
    new_list = []

    for item in items:
        if type(item) == dict:
            new_list = new_list + item['metrics'][tp]
        else:
            new_list.append(item)

    return new_list


def combineObjRel(indirects, objs, rels):
    new_obj = []
    new_rel = []

    for indirect in indirects:
        new_obj = new_obj + indirect['metrics']['objrel'][0]
        new_rel = new_rel + indirect['metrics']['objrel'][1]

    for obj in objs:
        new_obj.append(obj)

    for rel in rels:
        new_rel.append(rel)

    return [new_obj, new_rel]


def pickPhrase(phrases):
    length = len(phrases)
    rand = random.randint(0, length - 1)
    return phrases[rand]


##################
#     Actions    #
##################

def addActionWithIndirectObject(stsg, act, refs):
    """ TODO
    """

    args = [None]
    for direct in act:
        if direct == 'c044':
            continue
        # find the associated object
        s, v = ACTION_SV[direct]
        # see if the object has indirect refs
        if s in refs:
            if v not in multi_subj_verbs:
                continue
            if direct not in multi_subj_verbs[v]:
                continue
            if s == g.IDX['picture']:
                continue
            for tp in refs[s]:
                # dont want to replace direct reference with direct reference
                if tp == 'direct':
                    continue
                for subj_indir in refs[s][tp]:
                    if v in subj_indir['args']:
                        continue

                    metrics = {
                        'before': [],
                        'first': [],
                        'longer': [direct],
                        'repetition': [],
                        'objrel': [[], []],
                        'indirects': [True, False, False, False],
                    }
                    # will have to adjust this b/c articles
                    phrase = g.PP[direct]
                    phrase = phrase.replace("%s of something" % g.art(s),
                                            subj_indir['phrase'])
                    phrase = phrase.replace("%ss" % g.art(s),
                                            subj_indir['phrase'])
                    phrase = phrase.replace(g.art(s),
                                            subj_indir['phrase'])
                    phrase = phrase.replace("%ss" % g.ENG[s],
                                            subj_indir['phrase'])
                    phrase = phrase.replace(g.ENG[s], subj_indir['phrase'])

                    # ok so just index the first part of the string
                    if phrase.find(subj_indir['phrase']) == -1:
                        continue

                    sg_verts = {}

                    for start, end in subj_indir['sg_verts']:
                        sub_phrase = subj_indir['phrase'][start:end]

                        first_idx = phrase.find(sub_phrase)

                        if first_idx == -1:
                            continue
                        last_idx = first_idx + len(sub_phrase) + 1

                        sg_verts = {
                            (first_idx, last_idx): subj_indir['sg_verts'][(start, end)],
                        }
                    sg_verts[(0, -1)] = [direct + '/1']
                    tree = "ToAction(%s, %s)" % (g.PP[v], subj_indir['tree'])

                    refs = add(refs, direct, 'indir-obj', phrase,
                               lambda a: direct, subj_indir['steps'],
                               args, metrics, tree, sg_verts)

    return refs


def addLongest(stsg, act, error_margin, refs):
    """ TODO
    """

    args = [None]
    direct = solve.findLongest(stsg, error_margin)

    if direct is None:
        return refs

    phrases = [
        "doing the action they did the longest",
        "doing the longest action",
        "doing the thing they spent the longest amount of time doing",
    ]
    # Will need to be args when say "before/after"

    metrics = {
        'before': [],
        'first': [],
        'longer': [direct],
        'repetition': [],
        'objrel': [[], []],
        'indirects': [False, False, True, False],
    }

    tree = 'Superlative(max, Filter(video, [actions]), Subtract(Query(end, action), Query(start, action)))'

    # figure out frames of action
    to_select = ['actions', direct, 'vertices', 0, 'all_f']
    act_frames = pm.select(stsg, to_select)
    act_frames = [direct + '/' + i for i in act_frames]

    # make sg verts
    phrase = pickPhrase(phrases)

    sg_verts = {
        (0, len(phrase)): act_frames
    }

    refs = add(refs, direct, 'longest', phrase,
               lambda a: solve.findLongest(stsg, error_margin),
               1, args, metrics, tree, sg_verts)

    return refs


def addShortest(stsg, act, error_margin, refs):
    """ TODO
    """

    args = [None]
    direct = solve.findShortest(stsg, error_margin)

    if direct is None:
        return refs

    phrases = [
        "doing the action they did the fastest",
        "doing the fastest action",
        "doing the thing they spent the least amount of time doing",
    ]
    # Will need to be args when say "before/after"

    metrics = {
        'before': [],
        'first': [],
        'longer': [],
        'repetition': [],
        'objrel': [[], []],
        'indirects': [False, False, True, False],
    }

    tree = 'Superlative(min, Filter(video, [actions]), Subtract(Query(end, action), Query(start, action)))'

    # figure out frames of action
    to_select = ['actions', direct, 'vertices', 0, 'all_f']
    act_frames = pm.select(stsg, to_select)
    act_frames = [direct + '/' + i for i in act_frames]

    # make sg verts
    phrase = pickPhrase(phrases)

    sg_verts = {
        (0, len(phrase)): act_frames
    }

    refs = add(refs, direct, 'shortest', phrase,
               lambda a: solve.findShortest(stsg, error_margin),
               1, args, metrics, tree, sg_verts)

    return refs


##################
#      Time      #
##################
def addBefore(stsg, act, refs):
    """ Create indirect objects referencing what happened before

    Args:
        stsg: the spatiotemporal scene graph
        act: a list of all actions in video
        refs: current indirect reference dictionary

    Returns:
        An updated reference dictionary.
        Dictionary includes "before <action>" objects
    """

    # eventually add rels too TODO
    video_first_frame = stsg['ordered_frames'][0]

    for action_id in act:
        if action_id == 'c044':
            continue
        for tp in refs[action_id]:
            for indirect in refs[action_id][tp]:
                args = [indirect]
                test = solve.framesBefore(stsg, args)

                if len(test) == 0:
                    continue

                to_select = ['actions', action_id, 'vertices', 0, 'all_f']
                act_frames = pm.select(stsg, to_select)
                first_frame = act_frames[0]

                if (first_frame != video_first_frame):
                    phrases = [
                        " before %s" % (indirect['phrase']),
                    ]

                    metrics = {
                        'before': combineMetrics([indirect, action_id],
                                                 'before'),
                        'first': indirect['metrics']['first'],
                        'longer': indirect['metrics']['longer'],
                        'repetition': indirect['metrics']['repetition'],
                        'objrel': indirect['metrics']['objrel'],
                        'indirects': combineIndirectMetrics([indirect], 3),
                    }

                    tree = 'Localize(before, %s)' % indirect['tree']

                    starts = [[8]]
                    sg_phrases = [[indirect['phrase']]]

                    # take a random number!
                    length = len(phrases)
                    rand = random.randint(0, length - 1)
                    phrase = phrases[rand]
                    starts = starts[rand]
                    sg_phrases = sg_phrases[rand]
                    order = [0]

                    verts = {
                            0: indirect['sg_verts'],
                    }

                    sg_verts = find_char_location(verts, starts,
                                                  sg_phrases, order)

                    sg_verts[(1, -1)] = test

                    refs = add(refs, 'time', 'before', phrase,
                               lambda a: solve.framesBefore(stsg, a),
                               2 + indirect['steps'], args, metrics,
                               tree, sg_verts)

    return refs


def addAfter(stsg, act, refs):
    """ Create indirect objects referencing what happened before

    Args:
        stsg: the spatiotemporal scene graph
        act: a list of all actions in video
        refs: current indirect reference dictionary

    Returns:
        An updated reference dictionary.
        Dictionary includes "after <action>" objects
    """

    video_last_frame = stsg['ordered_frames'][-1]

    for action_id in act:
        if action_id == 'c044':
            continue
        for tp in refs[action_id]:
            for indirect in refs[action_id][tp]:
                args = [indirect]
                test = solve.framesAfter(stsg, args)
                if len(test) == 0:
                    continue

                to_select = ['actions', action_id, 'vertices', 0, 'all_f']
                act_frames = pm.select(stsg, to_select)
                last_frame = act_frames[-1]

                metrics = {
                    'before': indirect['metrics']['before'],
                    'first': indirect['metrics']['first'],
                    'longer': indirect['metrics']['longer'],
                    'repetition': indirect['metrics']['repetition'],
                    'objrel': indirect['metrics']['objrel'],
                    'indirects': combineIndirectMetrics([indirect], 3),
                }
                tree = 'Localize(after, %s)' % indirect['tree']
                if (last_frame != video_last_frame):
                    phrase = " after %s" % (indirect['phrase'])

                    starts = [7]
                    sg_phrases = [indirect['phrase']]
                    order = [0]

                    verts = {
                            0: indirect['sg_verts'],
                    }

                    sg_verts = find_char_location(verts, starts,
                                                  sg_phrases, order)

                    sg_verts[(1, -1)] = test

                    refs = add(refs, 'time', 'after', phrase,
                               lambda a: solve.framesAfter(stsg, a),
                               2 + indirect['steps'], args, metrics,
                               tree, sg_verts)

    return refs


def addWhile(stsg, act, refs):
    """ Create indirect objects referencing what happened concurrently

    Args:
        stsg: the spatiotemporal scene graph
        act: a list of all actions in video
        refs: current indirect reference dictionary

    Returns:
        An updated reference dictionary.
        Dictionary includes "qhile <action>" objects
    """
    for action_id in act:
        if action_id == 'c044':
            continue
        for tp in refs[action_id]:
            for indirect in refs[action_id][tp]:
                args = [indirect]
                phrase = " while %s" % (indirect['phrase'])

                to_select = ['actions', action_id, 'vertices', 0, 'all_f']
                act_frames = pm.select(stsg, to_select)

                metrics = {
                    'before': indirect['metrics']['before'],
                    'first': indirect['metrics']['first'],
                    'longer': indirect['metrics']['longer'],
                    'repetition': indirect['metrics']['repetition'],
                    'objrel': indirect['metrics']['objrel'],
                    'indirects': combineIndirectMetrics([indirect], 3),
                }

                tree = 'Localize(while, %s)' % indirect['tree']

                starts = [7]
                sg_phrases = [indirect['phrase']]
                order = [0]

                verts = {
                        0: indirect['sg_verts'],
                }

                sg_verts = find_char_location(verts, starts, sg_phrases, order)

                sg_verts[(1, -1)] = act_frames

                refs = add(refs, 'time', 'while', phrase,
                           lambda a: solve.framesWhile(stsg, a),
                           2 + indirect['steps'], args, metrics,
                           tree, sg_verts)

    return refs


def addBetween(stsg, act, refs):
    """ Create indirect objects referencing beetween two actions

    Args:
        stsg: the spatiotemporal scene graph
        act: a list of all actions in video
        refs: current indirect reference dictionary

    Returns:
        An updated reference dictionary.
        Dictionary includes "between" objects
    """

    for a_id1 in act:
        if a_id1 == 'c044':
            continue
        for tp in refs[a_id1]:
            for indirect1 in refs[a_id1][tp]:
                for a_id2 in act:
                    if a_id2 == 'c044':
                        continue
                    for tp in refs[a_id2]:
                        for indirect2 in refs[a_id2][tp]:
                            args = [indirect1, indirect2]
                            test = solve.framesBetween(stsg, args)

                            if len(test) == 0:
                                continue

                            phrases = [
                                " before %s but after %s" % (indirect2['phrase'], indirect1['phrase']),
                                " between %s and %s" % (indirect1['phrase'], indirect2['phrase']),
                            ]

                            metrics = {
                                'before': combineMetrics([indirect1, indirect2, a_id1], 'before'),
                                'first': combineMetrics([indirect1, indirect2], 'first'),
                                'longer': combineMetrics([indirect1, indirect2], 'longer'),
                                'repetition': combineMetrics([indirect1, indirect2], 'repetition'),
                                'objrel': combineObjRel([indirect1, indirect2], [], []),
                                'indirects': combineIndirectMetrics([indirect1, indirect2], 3),
                            }

                            tree = 'Localize(between, [%s, %s])' % (indirect1['tree'], indirect2['tree'])

                            starts = [[19, 8], [9, 14]]

                            sg_phrases = [[indirect1['phrase'], indirect2['phrase']],
                                          [indirect1['phrase'], indirect2['phrase']]]

                            order = [[1, 0], [0, 1]]

                            # take a random number!
                            length = len(phrases)
                            rand = random.randint(0, length - 1)
                            phrase = phrases[rand]
                            starts = starts[rand]
                            sg_phrases = sg_phrases[rand]
                            order = order[rand]

                            verts = {
                                    0: {(0, -1): [indirect1['direct'] + '/1']},
                                    1: {(0, -1): [indirect2['direct'] + '/1']},
                            }

                            verts = {
                                    0: indirect1['sg_verts'],
                                    1: indirect2['sg_verts'],
                            }
                            sg_verts = find_char_location(verts, starts,
                                                          sg_phrases, order)

                            sg_verts[(1, -1)] = test


                            refs = add(refs, 'time', 'between', phrase,
                                       lambda a: solve.framesBetween(stsg, a),
                                       3 + indirect1['steps'] + indirect2['steps'],
                                       args, metrics, tree, sg_verts)

    return refs


def addAllTime(stsg, refs):
    """ Create indirect objects referencing entire video

    Args:
        stsg: the spatiotemporal scene graph
        refs: current indirect reference dictionary

    Returns:
        An updated reference dictionary.
        Dictionary includes "whole vide" objects
    """
    phrase = ""

    all_frames = stsg['ordered_frames']

    metrics = {
        'before': [],
        'first': [],
        'longer': [],
        'repetition': [],
        'objrel': [[], []],
        'indirects': [False, False, False, False],
    }

    sg_verts = {(-1, -1): all_frames}

    tree = 'video'

    refs = add(refs, 'time', 'all', phrase,
               lambda a: all_frames, 0, [None], metrics, tree, sg_verts)
    return refs


##################
#     Objects    #
##################

def addFirstObjRef(stsg, obj, arel, crel, srel, vrel, refs):
    """ Create indirect objects of the form "object they were <reference> first"

    Args:
        stsg: the spatiotemporal scene graph
        obj: a list of all objects in video
        arel: a list of all attention relationships in video
        crel: a list of all contact relationships in video
        srel: a list of all spatial relationships in video
        refs: current indirect reference dictionary

    Returns:
        An updated reference dictionary.
        Dictionary includes "object they were <reference> first<time>" objects
    """
    rels = crel + srel + vrel

    for tp in ['all']:
        for indirect in refs['time'][tp]:
            for r in rels:

                if r in [IDX['not_contacting'],
                         IDX['unsure'],
                         IDX['not_looking_at']]:
                    continue

                if r in SINGLE_OBJ_VERBS:
                    continue

                args = [r, indirect]
                if not templates.notInAction(r, indirect):
                    continue
                test, rel_verts = solve.firstObjCompRef(stsg, args)

                if len(test) != 1:
                    continue

                def program_first(a): return solve.firstObjCompRef(stsg, a)[0][0]

                direct = program_first(args)

                if indirect['args'][0] is not None:
                    action_ref = indirect['args'][0]['direct']

                    obj, _ = ACTION_SV[action_ref]
                    if direct == obj:
                        continue

                    if len(indirect['args']) == 2:
                        action_ref = indirect['args'][1]['direct']

                        obj, _ = ACTION_SV[action_ref]
                        if direct == obj:
                            continue

                if not templates.notInAction(direct, indirect):
                    continue

                metrics = {
                    'before': indirect['metrics']['before'],
                    'first': combineMetrics([indirect, r], 'first'),
                    'longer': indirect['metrics']['longer'],
                    'repetition': indirect['metrics']['repetition'],
                    'objrel': combineObjRel([indirect], [test[0]], [r]),
                    'indirects': combineIndirectMetrics([indirect], 0),
                }

                phrases = [
                    "the object they were %s first%s" % (g.PP[r], indirect['phrase']),
                    "the first thing they %s%s" % (PAST[r], indirect['phrase']),
                ]
                
                tree = "Query(class, OnlyItem(IterateUntil(forward, %s, Exists(%s, Filter(frame, [relations])), Filter(frame, [relations, %s, objects]))))" % (indirect['tree'], g.ENG[r], g.ENG[r])

                # get the scene graph vertices
                # treating the relationship as arg 0 and the time as arg 1
                starts = [
                    [21],
                    [21]]

                sg_phrases = [
                    [g.PP[r]],
                    [PAST[r]]]

                # take a random number!
                length = len(phrases)
                rand = random.randint(0, length - 1)
                phrase = phrases[rand]
                starts = starts[rand]
                sg_phrases = sg_phrases[rand]
                order = [0]

                verts = {
                        0: {(0, -1): rel_verts},
                }

                sg_verts = find_char_location(verts, starts, sg_phrases, order)

                rel_verts_frames = [i.split('/')[1] for i in rel_verts]
                # In the normal one, this is commented, out but here need for indirect act
                sg_verts[(0, -1)] = [direct + '/' + f for f in rel_verts_frames]

                refs = add(refs, direct, 'first', phrase,
                           lambda a: solve.firstObjCompRef(stsg, a)[0][0],
                           1, args, metrics, tree, sg_verts)

    return refs


def addLastObjRef(stsg, obj, arel, crel, srel, vrel, refs):
    """ Create indirect objects of the form "object they were <reference> last"

    Args:
        stsg: the spatiotemporal scene graph
        obj: a list of all objects in video
        arel: a list of all attention relationships in video
        crel: a list of all contact relationships in video
        srel: a list of all spatial relationships in video
        refs: current indirect reference dictionary

    Returns:
        An updated reference dictionary.
        Dictionary includes "object they were <reference> last" objects
    """
    rels = crel + srel + vrel  # + arel

    for tp in ['all']:  # refs['time']:
        for indirect in refs['time'][tp]:
            for r in rels:
                if r in [IDX['not_contacting'],
                         IDX['unsure'],
                         IDX['not_looking_at']]:
                    continue
                if r in SINGLE_OBJ_VERBS:
                    continue
                args = [r, indirect]
                if not templates.notInAction(r, indirect):
                    continue
                test, rel_verts = solve.lastObjCompRef(stsg, args)

                if len(test) != 1:
                    continue

                def program_last(a): return solve.lastObjCompRef(stsg, args)[0][0]

                direct = program_last(args)

                if indirect['args'][0] is not None:
                    action_ref = indirect['args'][0]['direct']

                    obj, _ = ACTION_SV[action_ref]
                    if direct == obj:
                        continue

                    if len(indirect['args']) == 2:
                        action_ref = indirect['args'][1]['direct']

                        obj, _ = ACTION_SV[action_ref]
                        if direct == obj:
                            continue

                if not templates.notInAction(direct, indirect):
                    continue

                metrics = {
                    'before': indirect['metrics']['before'],
                    'first': indirect['metrics']['first'],
                    'longer': indirect['metrics']['longer'],
                    'repetition': indirect['metrics']['repetition'],
                    'objrel': combineObjRel([indirect], [test[0]], [r]),
                    'indirects': combineIndirectMetrics([indirect], 0),
                }

                phrases = [
                    "the object they were %s last%s" % (g.PP[r], indirect['phrase']),
                    "the last thing they %s%s" % (PAST[r], indirect['phrase']),
                ]

                tree = "Query(class, OnlyItem(IterateUntil(backward, %s, Exists(%s, Filter(frame, [relations])), Filter(frame, [relations, %s, objects]))))" % (indirect['tree'], g.ENG[r], g.ENG[r])

                # get the scene graph vertices
                # treating the relationship as arg 0 and the time as arg 1
                starts = [
                    [21],
                    [20]]

                sg_phrases = [
                    [g.PP[r]],
                    [PAST[r]]]

                # take a random number!
                length = len(phrases)
                rand = random.randint(0, length - 1)
                phrase = phrases[rand]
                starts = starts[rand]
                sg_phrases = sg_phrases[rand]
                order = [0]

                verts = {
                        0: {(0, -1): rel_verts},
                }

                sg_verts = find_char_location(verts, starts, sg_phrases, order)

                # I am doing this here, unlike in
                rel_verts_frames = [i.split('/')[1] for i in rel_verts]
                # In the normal one, this is commented
                # out but here need for indirect act
                sg_verts[(0, -1)] = [direct + '/' + f for f in rel_verts_frames]

                refs = add(refs, direct, 'last', phrase,
                           lambda a: solve.lastObjCompRef(stsg, a)[0][0],
                           1, args, metrics, tree, sg_verts)

    return refs


def addTimeObjRef(stsg, obj, arel, crel, srel, vrel, refs):
    """ Create indirect objects of the form "object they were <reference>"

    Args:
        stsg: the spatiotemporal scene graph
        obj: a list of all objects in video
        arel: a list of all attention relationships in video with multiple objs
        crel: a list of all contact relationships in video
        srel: a list of all spatial relationships in video
        refs: current indirect reference dictionary

    Returns:
        An updated reference dictionary.
        Dictionary includes "object they were <reference>" objects
    """
    rels = crel + srel + vrel

    for tp in refs['time']:
        if tp == 'all':
            continue
        for indirect in refs['time'][tp]:
            for r in rels:
                if r in [IDX['not_contacting'], IDX['unsure']]:
                    continue
                if r in SINGLE_OBJ_VERBS:
                    continue

                if not templates.notInAction(r, indirect['args'][0]['direct']):
                    continue

                args = [r, indirect]
                if not templates.notInAction(r, indirect):
                    continue
                test, rel_verts = solve.relRef(stsg, args)

                if len(test) != 1:
                    continue

                direct = test[0]

                if not templates.notInAction(direct, indirect):
                    continue
                phrases = [
                    "the object they were %s%s" % (g.PP[r],
                                                   indirect['phrase']),
                    "the thing they %s%s" % (PAST[r], indirect['phrase']),
                ]

                metrics = {
                    'before': indirect['metrics']['before'],
                    'first': indirect['metrics']['first'],
                    'longer': indirect['metrics']['longer'],
                    'repetition': indirect['metrics']['repetition'],
                    'objrel': combineObjRel([indirect], [test[0]], [r]),
                    'indirects': combineIndirectMetrics([indirect], 0),
                }

                starts = [
                    [21, 21],
                    [15, 15]]

                sg_phrases = [
                    [g.PP[r], indirect['phrase']],
                    [PAST[r], indirect['phrase']]]

                # take a random number!
                length = len(phrases)
                rand = random.randint(0, length - 1)
                phrase = phrases[rand]
                starts = starts[rand]
                sg_phrases = sg_phrases[rand]
                order = [0, 1]

                verts = {
                        0: {(0, -1): rel_verts},
                        1: indirect['sg_verts']
                }

                sg_verts = find_char_location(verts, starts, sg_phrases, order)
                rel_verts_frames = [i.split('/')[1] for i in rel_verts]
                # In the normal one, this is commented,
                # out but here need for indirect act
                sg_verts[(0, -1)] = [direct + '/' + f for f in rel_verts_frames]

                tree = "Query(class, OnlyItem(Iterate(%s, Filter(frame, [relations, %s, objects]))))" % (indirect['tree'], g.ENG[r])

                refs = add(refs, direct, 'whole', phrase,
                        lambda a: solve.relRef(stsg, a)[0][0], 1,
                        args, metrics, tree, sg_verts)

    return refs


def addSingleObjRef(stsg, obj, arel, crel, srel, vrel, refs):
    """ Create indirect objects of the form "object they were <reference>"

    Args:
        stsg: the spatiotemporal scene graph
        obj: a list of all objects in video with multiple instances
        arel: a list of all attention relationships in video with one obj
        crel: a list of all contact relationships in video
        srel: a list of all spatial relationships in video
        refs: current indirect reference dictionary

    Returns:
        An updated reference dictionary.
        Dictionary includes "object they were <reference>" objects
    """
    rels = crel + srel + vrel
    indirect = refs['time']['all'][0]

    for r in rels:
        if r in [IDX['not_contacting'], IDX['unsure']]:
            continue
        if r in SINGLE_OBJ_VERBS:
            continue

        args = [r, indirect]
        if not templates.notInAction(r, indirect):
            continue

        test, rel_verts = solve.relRef(stsg, args)

        if len(test) != 1:
            continue

        direct = test[0]

        if not templates.notInAction(direct, indirect):
            continue

        phrases = [
            "the object they were %s" % (g.PP[r]),
            "the thing they %s" % (PAST[r]),
        ]

        metrics = {
            'before': [],
            'first': [],
            'longer': [],
            'repetition': [],
            'objrel': [[test[0]], [r]],
            'indirects': [True, False, False, False],
        }

        starts = [
            [21],
            [15]]

        sg_phrases = [
            [g.PP[r]],
            [PAST[r]]]

        # take a random number!
        length = len(phrases)
        rand = random.randint(0, length - 1)
        phrase = phrases[rand]
        starts = starts[rand]
        sg_phrases = sg_phrases[rand]
        order = [0]

        verts = {
                0: {(0, -1): rel_verts},
        }

        sg_verts = find_char_location(verts, starts, sg_phrases, order)

        rel_verts_frames = [i.split('/')[1] for i in rel_verts]
        # In the normal one, this is commented,
        # out but here need for indirect act
        sg_verts[(0, -1)] = [direct + '/' + f for f in rel_verts_frames]

        tree = "Query(class, OnlyItem(Iterate(video, Filter(frame, [relations, %s, objects]))))" % g.ENG[r]

        refs = add(refs, direct, 'whole', phrase,
                   lambda a: solve.relRef(stsg, a)[0][0],
                   1, args, metrics, tree, sg_verts)

    return refs


##################
#    Relations   #
##################

def addFirstRelRef(stsg, obj, arel, crel, srel, vrel, refs):
    """ Create indirect objects of the form "object they were <reference> first"

    Args:
        stsg: the spatiotemporal scene graph
        obj: a list of all objects in video
        rels: a list of all attention relationships in video
        crel: a list of all contact relationships in video
        srel: a list of all spatial relationships in video
        vrel: a list of all verb relationships in video
        refs: current indirect reference dictionary

    Returns:
        An updated reference dictionary.
        Dictionary includes "the first thing they did to <obj>" objects
    """

    for o in obj:
        test = solve.firstRelRef(stsg, [o])

        to_remove = set()
        for rel in test:
            if g.vType(rel) == 'spatial':
                to_remove.add(rel)

        for rem in to_remove:
            test.remove(rem)

        if len(test) != 1:
            continue

        if test[0] in [IDX['not_contacting'],
                       IDX['unsure'],
                       IDX['not_looking_at']]:
            continue

        def program_first(a):
            return solve.firstRelRef(stsg, a)[0]

        args = [o]
        direct = program_first(args)

        metrics = {
                    'before': [],
                    'first': [test[0]],
                    'longer': [],
                    'repetition': [],
                    'objrel': [[o], [test[0]]],
                    'indirects': [False, True, False, False]
                }

        phrases = [
            "doing the first thing they did to the %s" % (g.ENG[o]),
        ]
        phrase = pickPhrase(phrases)

        refs = add(refs, direct, 'first', phrase,
                   program_first, 1, args, metrics)

    return refs


ids = ['T3R3K', 'W97NR', 'Y7CGN']


# f = open('../data/stsgs/test_stsgs.pkl', 'rb')
# STSG = pickle.load(f)
# f.close()

STSG = {}


def printDic(dic):
    """ Print a compositional ref dictionary

    Args: dic: compositional ref dictionary
    """
    for i in dic:
        print(i)
        for j in dic[i]:
            print(" "*4, j)
            for k in dic[i][j]:
                print(" "*8, 'phrase: ', k['phrase'])
                if 'start_phrase' in k:
                    print(" "*8, 'start phrase: ', k['start_phrase'])
                print(" "*8, 'direct: ', k['direct'])
                print(" "*8, 'program: ', k['program'])
                print(" "*8, 'steps: ', k['steps'])
                print(" "*8, 'args: ', k['args'])
                print(" "*8, 'type: ', k['type'])
                print(" "*8, 'metrics: ')
                for lee in k['metrics']:
                    print(" " * 12, lee, k['metrics'][lee])
                print()
        print()


def printSGVert():
    for video_id in ids:
        print(video_id)
        printSGV(makeIndirect(STSG[video_id]))


def printSGV(dic):
    """ Print a compositional ref dictionary

    Args: dic: compositional ref dictionary
    """
    for i in dic:
        print(i)
        for j in dic[i]:
            print(" "*4, j)
            for k in dic[i][j]:
                print()
                phrase = k['phrase']
                print('     phrase: ', phrase)
                sg = k['sg_verts']
                for x in sg:
                    if type(x) == str:
                        continue
                    s, e = x
                    print(" "*8, s, e, phrase[s:e])
                    print(" "*16, sg)


def printPhrase(dic):
    """ Print a compositional ref dictionary

    Args: dic: compositional ref dictionary
    """
    for i in dic:
        for j in dic[i]:
            for k in dic[i][j]:
                print(" "*8, i, 'phrase: ', k['phrase'])


def printAll():
    for video_id in ids:
        print(video_id)
        printDic(makeIndirect(STSG[video_id]))


def printAllPhrases():
    for video_id in ids[:3]:
        print(video_id)
        printPhrase(makeIndirect(STSG[video_id]))


#ids = ['N1E7A']
#printAllPhrases()

def findCompoRefDistr(group):
    if group == 'test':
        infile = open('../data/test_videos_stsg.pkl', 'rb')
        stsgs = pickle.load(infile)
        infile.close()
    elif group == 'train':
        infile = open('../data/videos_stsg.pkl', 'rb')
        stsgs = pickle.load(infile)
        infile.close()

    refs = {}
    cnt = 0
    for s_idx in stsgs:
        if cnt % 100 == 0:
            print(cnt)
        cnt += 1
        indirect = makeIndirect(stsgs[s_idx])

        for direct in indirect:
            # only looking at objects for noe
            if direct[:1] != 'o':
                continue
            for ref_type in indirect[direct]:
                if ref_type == 'direct':
                    continue
                for ind_obj in indirect[direct][ref_type]:
                    ref = ind_obj['args'][0]
                    if ref not in refs:
                        refs[ref] = {}
                    if direct not in refs[ref]:
                        refs[ref][direct] = 0
                    refs[ref][direct] += 1
    with open('../data/dicOfRefs-%s.txt' % group, 'w+') as f:
        json.dump(refs, f)
