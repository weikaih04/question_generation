import metrics
from itertools import combinations
import random
from locate_char import find_char_location
import grammar as g


ALL_TIME_INDIRECT = ['before', 'after', 'while', 'all', 'between']


def appendPerm(perms, p_lists, p_list):
    """ Given lists of permutations, concatenate those lists in all possible ways

    Args:
        perms: lists of lists of permutations
        p_lists: collection of all combined permutations so far
        p_list: current permutation list being built

    Returns:
        collection of all permutation combinations

    """

    # base case where add to lists
    if len(perms) == 0:
        p_lists.append(p_list)
        return p_lists

    for i in perms[0]:
        temp_p_list = p_list.copy()
        temp_p_list = temp_p_list + i
        p_lists = appendPerm(perms[1:], p_lists, temp_p_list)

    return p_lists


def createPermutations(args):  # Note, now combinations
    """ Given possible arguments and a num each type, create all
        permutations of lists with that num of each type

    Args:
        args: [... ['arg_type':(num, [arguments of arg_type]), [] ...]

    Returns:
        A list of all permutations of the arguments with the
        specified number of each type
    """

    perms = []
    for i in args:
        # p = permutations(i[1], i[0])
        p = combinations(i[1], i[0])
        p_type = []

        # turn permutation itertools into list format
        for j in p:
            p_ex = []
            for k in j:
                p_ex.append(k)
            p_type.append(p_ex)
        perms.append(p_type)

    # create permutations of the permutations
    return appendPerm(perms, [], [])


def addIndirectRefs(tpl, refs):
    """ Replace a template's direct references with indirect ones

    Args:
        tpl: the template object
        refs: a dictionary of all indirect references for this video
    """

    # add in all indirect references to possible args lists of valid types
    for arg in tpl['args']:
        newArgs = []
        for tp in arg[2]:  # look at what type of arguent they're looking for
            for direct in arg[1]:
                if direct not in refs:  # these two avoid errors
                    # print(direct + " not in refs")
                    continue
                if tp not in refs[direct]:
                    # print(tp, " not in refs for ", direct)
                    continue
                for ref in refs[direct][tp]:
                    newArgs.append(ref)

        if len(arg[2]) != 0:
            arg[1] = newArgs


def cumulativeSteps(args, tpl):
    """ Find number of steps needed for a particular question

    Args:
        args: the arguments used to fill this version of the template
        tpl: the question template

    Returns:
        An integer number of compositional steps needed to answer the question
    """

    steps = tpl['steps']

    for arg in args:
        if type(arg) == dict:
            steps = steps + arg['steps']
    return steps


def createQuestion(question, answer, tpl, local, id, steps,
                   args, metrics, str_program, sg_verts):
    """ Creates a question dictionary object with relevant attributes

    Args:
        question: the string question about the video
        answer: the string answer to that question
        tpl: the question template
        local: the question's "local" value
        id: the queston-specific id
        steps: the number of compositional steps needed to solve answer
        args: the arguments that were used to fill out question

    Returns:
        A question object dictionary
    """

    # CHANGED
    if metrics['indirects'].count(True) == 0 and answer == 'Yes':
        print()
        print(question)

    newQ = {
        'question': question,
        'answer': answer,
        'attributes': tpl['attributes'],
        'global': tpl['global'],
        'local': local,
        'steps': steps,
        'id': id,
        'metrics': metrics,
        'program': str_program,
        'sg_grounding': sg_verts,
    }

    return newQ


def atLeastOneNewIndir(p_list):
    atLeastOne = False

    for arg in p_list:
        if type(arg) != dict:
            continue
        if (arg['type'] not in ALL_TIME_INDIRECT and g.vType(arg['direct']) != 'actions'):
            continue
        indir = arg['metrics']['indirects']

        if indir[0] or indir[1]:
            atLeastOne = True
            break

    return atLeastOne


def appendPermActionIndirect(perms, p_lists, p_list):
    """ Given lists of permutations, concatenate those lists in all possible ways

    Args:
        perms: lists of lists of permutations
        p_lists: collection of all combined permutations so far
        p_list: current permutation list being built

    Returns:
        collection of all permutation combinations

    """

    # base case where add to lists
    if len(perms) == 0:
        if atLeastOneNewIndir(p_list):
            p_lists.append(p_list)
        return p_lists

    for i in perms[0]:
        temp_p_list = p_list.copy()
        temp_p_list = temp_p_list + i
        p_lists = appendPermActionIndirect(perms[1:], p_lists, temp_p_list)

    return p_lists


def createPermutationsActionIndirect(args):  # Note, now combinations
    """ Given possible arguments and a num each type, create all
        permutations of lists with that num of each type

    Args:
        args: [... ['arg_type':(num, [arguments of arg_type]), [] ...]

    Returns:
        A list of all permutations of the arguments with the
        specified number of each type
    """

    perms = []
    for i in args:
        p = combinations(i[1], i[0])
        p_type = []

        # turn permutation itertools into list format
        for j in p:
            p_ex = []
            for k in j:
                p_ex.append(k)
            p_type.append(p_ex)

        perms.append(p_type)
    # create permutations of the permutations
    return appendPermActionIndirect(perms, [], [])


def iterateTemplateActionIndirect(tpl, indirect, count):
    """ Creates all possible questions from a template

    Args:
        tpl: a tmeplate object
        indirect: a dictionary of all indirect references for this video

    Returns:
        A dictionary mapping question ids to questions
    """
    addIndirectRefs(tpl, indirect)

    perms = createPermutationsActionIndirect(tpl['args'])

    # create a question using each argument formulation
    questBank = {}
    cnt = 0
    num_nl_q = len(tpl['questions']) - 1
    for args in perms:
        output = tpl['program'](args)
        # make sure valid answer
        valid = True
        for qual in tpl['quals']:
            if not qual(output[0], args):
                valid = False
                break
        if not valid:
            continue
        else:
            answer = tpl['package_ans'](output[0])

        rand_q_int = random.randint(0, num_nl_q)
        q_tpl = tpl['questions'][rand_q_int]
        q_id = "%s-%d" % (tpl['attributes']['video_id'], count)
        steps = cumulativeSteps(args, tpl)
        q = q_tpl(args)

        metric_flags = metrics.makeMetrics(tpl, output, args)

        starts = tpl['starts'][rand_q_int].copy()

        phrases = tpl['phrases'][rand_q_int](args)
        order = tpl['order'][rand_q_int]

        sg_verts = find_char_location(output[-1], starts, phrases, order)

        new_sg_verts = {}

        for s, e in sg_verts:
            key = '%s-%s' % (s, e)
            new_sg_verts[key] = sg_verts[(s, e)]
            if s < 0 or e < 0:
                print(key, new_sg_verts[key])
                print("STILL GETTING NEGATIVEs", key)
            else:
                1+1
#                print('   ', q[s:e])

        question = createQuestion(q, answer, tpl,
                                  tpl['local'](output[0], args),
                                  q_id, steps, args, metric_flags,
                                  tpl['str_program'](args), new_sg_verts)
        questBank[q_id] = question
        cnt = cnt + 1
        count = count + 1

    return questBank, cnt



# ADDED
def iterateTemplate(tpl, indirect, count, breaks_on):
    """ Creates all possible questions from a template

    Args:
        tpl: a tmeplate object
        indirect: a dictionary of all indirect references for this video

    Returns:
        A dictionary mapping question ids to questions
    """

    addIndirectRefs(tpl, indirect)

    # TODO: think if want permutation or combination
    perms = createPermutations(tpl['args'])

    # create a question using each argument formulation
    questBank = {}
    cnt = 0
    num_nl_q = len(tpl['questions']) - 1


    for args in perms:
        output = tpl['program'](args)
        # make sure valid answer
        valid = True

        for i, qual in enumerate(tpl['quals']):
            if not qual(output[0], args):
                valid = False

                # ADDED
                if i not in breaks_on:
                    breaks_on[i] = 0
                breaks_on[i] += 1

                break

        if not valid:
            continue
        else:
            answer = tpl['package_ans'](output[0])

            # ADDED
            i = -1
            if i not in breaks_on:
                breaks_on[i] = 0
            breaks_on[i] += 1



        rand_q_int = random.randint(0, num_nl_q)
        q_tpl = tpl['questions'][rand_q_int]
        q_id = "%s-%d" % (tpl['attributes']['video_id'], count)
        steps = cumulativeSteps(args, tpl)
        q = q_tpl(args)

        metric_flags = metrics.makeMetrics(tpl, output, args)

        starts = tpl['starts'][rand_q_int].copy()

        phrases = tpl['phrases'][rand_q_int](args)
        order = tpl['order'][rand_q_int]

        sg_verts = find_char_location(output[-1], starts, phrases, order)

        new_sg_verts = {}

        for s, e in sg_verts:
            key = '%s-%s' % (s, e)
            new_sg_verts[key] = sg_verts[(s, e)]

        question = createQuestion(q, answer, tpl,
                                  tpl['local'](output, args),
                                  q_id, steps, args, metric_flags,
                                  tpl['str_program'](args), new_sg_verts)

        # check if it's greater than or equal to 9 steps
        if question['steps'] >= 9:
            continue
        questBank[q_id] = question
        cnt = cnt + 1
        count = count + 1


    # ADDED
    return questBank, cnt, breaks_on
