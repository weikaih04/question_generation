import program_modules as pm
import pickle
import grammar as g

with open('../data/actionSV.pkl', 'rb') as f:
    actionSV = pickle.load(f)

REL_TYPES = ['attention', 'spatial', 'contact', 'verb']

##################
# For compo refs #
##################

##################
#     objects    #
##################

def firstObjCompRef(stsg, a):
    """ Finds the object they were ____ from first.

    Args:
        stsg: the spatio-temporal scene graph
        a: an list of arguments [relationship x]

    Returns:
        A list of objects they did x to first
    """
    return objFirst(stsg, a)[0:2]


def lastObjCompRef(stsg, a):
    """ Finds the object they were ____ from last.

    Args:
        stsg: the spatio-temporal scene graph
        a: an list of arguments [relationship x]

    Returns:
        A list of objects they did x to last
    """
    return objLast(stsg, a)[0:2]


def relRef(stsg, a):
    """ Finds the object they were ____

    Args:
        stsg: the spatio-temporal scene graph
        a: an list of arguments [relationship x, time y]

    Returns:
        A list of objects they did x to
    """
    x = relExists(stsg, a)
    return x[1], x[2]


##################
#   relations    #
##################


def firstRelRef(stsg, a):
    """ Finds the thing they did first to ____.

    Args:
        stsg: the spatio-temporal scene graph
        a: an list of arguments [object x]

    Returns:
        A list of the first things they did to x
    """

    to_select = ['objects', a[0], 'names']
    list_of_first = pm.select(stsg, to_select)
    classes = list_of_first
 
    return classes


##################
#     actions    #
##################
def findLengths(stsg):
    """ TODO
    """

    # TODO: make sure this works when multiple actions

    action_ids = pm.select(stsg, ['stsg', 'actions'])

    actions = pm.getVertexList(stsg, action_ids, 'actions')

    action_ids = pm.editList(actions, 'charades')

    lengths = pm.editList(actions, 'length')

    len2act = pm.makeListOfTuples(lengths, action_ids)
    act2len = pm.makeDict(action_ids, lengths)

    return pm.sort(len2act, 0), act2len


def findLongest(stsg, error_margin):
    """ TODO
    """

    lengths = pm.select(findLengths(stsg), [0])

    just_lengths = [pair[0] for pair in lengths]

    if len(lengths) > 1:
        if pm.inMarginOfError(error_margin, just_lengths, -1, -2):
            return None

    else:
        # if only 1 action, ignore
        return None

    return pm.select(lengths, [-1, 1])


def findShortest(stsg, error_margin):
    """ TODO
    """

    lengths = pm.select(findLengths(stsg), [0])

    just_lengths = [pair[0] for pair in lengths]

    if len(lengths) > 1:
        if pm.inMarginOfError(error_margin, list(just_lengths), 0, 1):
            return None
    else:
        # if only 1 action, ignore
        return None

    return pm.select(lengths, [0, 1])


def findLongestTemplate(stsg, error_margin):
    """ TODO
    """

    lengths = pm.select(findLengths(stsg), [0])

    just_lengths = [pair[0] for pair in lengths]

    if len(lengths) > 1:
        if pm.inMarginOfError(error_margin, just_lengths, -1, -2):
            return None, None

    else:
        # if only 1 action, ignore
        return None, None

    return pm.select(lengths, [-1, 1]), {}


def findShortestTemplate(stsg, error_margin):
    """ TODO
    """

    lengths = pm.select(findLengths(stsg), [0])

    just_lengths = [pair[0] for pair in lengths]

    if len(lengths) > 1:
        if pm.inMarginOfError(error_margin, list(just_lengths), 0, 1):
            return None, None
    else:
        # if only 1 action, ignore
        return None, None

    return pm.select(lengths, [0, 1]), {}


##################
#      time      #
##################
def framesBefore(stsg, a):
    """ Find frames that occur before some action

    Args:
        stsg: the spatio-temporal scene graph
        a: an list of arguments [indirect action x]

    Returns:
        List of frames occuring before action x
    """
    action_id = a[0]['direct']
    to_select = ['actions', action_id, 'vertices', 0, 'all_f']
    first_frame = pm.select(stsg, to_select)[0]

    last_idx = stsg['ordered_frames'].index(first_frame)
    frame_list = stsg['ordered_frames'][:(last_idx + 1)]
    frame_list = pm.addSegmentationErrorMargin(stsg, frame_list)
    return frame_list


def framesAfter(stsg, a):
    """ Find frames that occur after some action

    Args:
        stsg: the spatio-temporal scene graph
        a: an list of arguments [indirect action x]

    Returns:
        List of frames occuring after action x
    """
    action_id = a[0]['direct']
    to_select = ['actions', action_id, 'vertices', 0, 'all_f']
    last_frame = pm.select(stsg, to_select)[-1]

    first_idx = stsg['ordered_frames'].index(last_frame) + 1

    frame_list = stsg['ordered_frames'][first_idx:]
    frame_list = pm.addSegmentationErrorMargin(stsg, frame_list)
    return frame_list


def framesWhile(stsg, a):
    """ Find frames that occur during some action

    Args:
        stsg: the spatio-temporal scene graph
        a: an list of arguments [action x]

    Returns:
        List of frames occuring during action x
    """
    action_id = a[0]['direct']
    to_select = ['actions', action_id, 'vertices', 0, 'all_f']
    first_frame = pm.select(stsg, to_select)[0]
    last_frame = pm.select(stsg, to_select)[-1]

    first_idx = stsg['ordered_frames'].index(first_frame)
    last_idx = stsg['ordered_frames'].index(last_frame)
    frame_list = stsg['ordered_frames'][(first_idx):(last_idx + 1)]
    frame_list = pm.addSegmentationErrorMargin(stsg, frame_list)
    return frame_list


def framesBetween(stsg, a):
    """ Find frames that occur between two actions

    Args:
        stsg: the spatio-temporal scene graph
        a: an list of arguments [indirect action x, indirect action y]

    Returns:
        List of frames occuring during action x
    """
    a_id1 = a[0]['direct']
    a_id2 = a[1]['direct']

    first_frame = pm.select(stsg,
                            ['actions', a_id1, 'vertices', -1, 'all_f'])[-1]
    last_frame = pm.select(stsg, ['actions', a_id2, 'vertices', 0, 'all_f'])[0]

    if int(first_frame) >= int(last_frame):
        return []

    first_idx = stsg['ordered_frames'].index(first_frame)
    last_idx = stsg['ordered_frames'].index(last_frame)
    frame_list = stsg['ordered_frames'][(first_idx + 1):(last_idx)]
    frame_list = pm.addSegmentationErrorMargin(stsg, frame_list)
    return frame_list


#################
# For templates #
#################

##################
#     Exists     #
##################
def objExists(stsg, a):
    """ Determines if a person interacts with an object

    Args:
        stsg: the spatio-temporal scene graph
        a: an list of arguments [object x]

    Returns:
        Yes if they interact with x, No otherwise
    """
    frames = a[1]['direct']

    rels = []

    o_verts = []

    def vertex_func(c_vertex, args):
        if pm.select(c_vertex, ['class']) == g.IDX['not_contacting']:
            return False
        objects = pm.select(c_vertex, ['objects'])
        ans, obj = pm.existsReturnItem(objects, 'class', a[0])
        if ans:
            rels.append(pm.select(c_vertex, ['class']))
            o_verts.append(obj['id'])

        return ans

    # return true if frame contains action false ow
    def frames_func(f_id, args):
        contact = pm.select(stsg, ['frames', f_id, 'contact', 'vertices'])
        return pm.iterate(contact, vertex_func, 1, None)

    exists = pm.iterate(frames, frames_func, None, None)

    # enure that the freaking vertices are all in the dictionary we want!
    sg_verts = {
        0: {(0, -1): list(set(o_verts))},  # object
        1: a[1]['sg_verts']
    }

    return pm.verify(exists), rels, sg_verts


def objRelExists(stsg, a):
    """ Determines if a person did a relationship on an object

    Args:
        stsg: the spatio-temporal scene graph
        a: an list of arguments
           [relationship x, indirect obj y, indirect time z]

    Returns:
        Yes if they did do x on y, No otherwise
    """

    list_of_frames = a[2]['direct']
    rel = a[0]['direct']
    object = a[1]['direct']

    obj_frames = []
    rel_frames = []

    def to_iterate(datum, args):
        tp = g.vType(rel)
        to_select = ['frames', datum, tp, 'vertices']
        vertices_in_frame = pm.select(stsg, to_select)

        combo_exists = False
        for contact_vert in vertices_in_frame:
            if contact_vert['class'] != rel:
                continue
            objs = pm.select(contact_vert, ['objects'])
            ans, obj = pm.existsReturnItem(objs, 'class', object)
            if ans:
                rel_frames.append(contact_vert['id'])
                obj_frames.append(obj['id'])
                combo_exists = True

        return combo_exists

    exists = pm.iterate(list_of_frames, to_iterate, None, None)

    #  update
    obj_verts = a[1]['sg_verts']
    obj_verts[(0, -1)] = obj_frames

    #  update
    rel_verts = a[0]['sg_verts']
    rel_verts[(0, -1)] = rel_frames

    # enure that the freaking vertices are all in the dictionary we want!
    sg_verts = {
        0: rel_verts,
        1: obj_verts,
        2: a[2]['sg_verts'],
    }

    return pm.verify(len(exists) != 0), sg_verts


def relExists(stsg, a):
    """ Determines if a person performs some contact relationship

    Args:
        stsg: the spatio-temporal scene graph
        a: an list of arguments [c/vrel x]

    Returns:
        Yes if they are x with something, No otherwise
    """
    frames = a[1]['direct']
    rel = a[0]
    objs = set()
    rel_verts = []

    # return true if frame contains action false ow
    def frames_func(f_id, args):
        frame = pm.select(stsg, ['frames', f_id])
        names = pm.select(frame, [g.vType(rel), 'names'])
        ans = pm.exists(names, None, rel)

        if ans:
            for obj in pm.select(frame, ['objects', 'names']):
                if pm.objRelExists(stsg, f_id, obj, rel):
                    objs.add(obj)
                    rel_verts.append(rel + '/' + f_id)
        return ans

    exists = pm.iterate(frames, frames_func, None, None)

    sg_verts = {
        0: {(0, -1): rel_verts},
        1: a[1]['sg_verts'],
    }

    return pm.verify(exists), list(objs), rel_verts, sg_verts


def actExists(stsg, a):
    """ Determines if a person performs some action

    Args:
        stsg: the spatio-temporal scene graph
        a: an list of arguments [action x, time]

    Returns:
        Yes if they perform x, No otherwise
    """
    frames = a[1]['direct']

    # return true if frame contains action false ow
    def frames_func(f_id, args):
        actions = pm.select(stsg, ['frames', f_id, 'actions', 'names'])
        return pm.exists(actions, None, a[0])

    exists = pm.iterate(frames, frames_func, 1, None)

    if exists:
        to_select = ['actions', a[0], 'vertices']
        act_verts = pm.select(stsg, to_select)
        act_verts = [a['id'] for a in act_verts]
    else:
        act_verts = []

    sg_verts = {
        0: {(0, -1): act_verts},
        1: a[1]['sg_verts'],
    }
    return pm.verify(exists), sg_verts


def andObjRelExists(stsg, a):
    """ Determines if a person did a relationship on an object

    Args:
        stsg: the spatio-temporal scene graph
        a: an list of arguments
           [indirectrelationship x, indirect time y,
           indirect object a, indirect object b]

    Returns:
        Yes if they did do x on a and b, No otherwise
    """
    list_of_frames = a[1]['direct']
    rel = a[0]['direct']
    o1 = a[2]['direct']
    o2 = a[3]['direct']

    rel_frames = []
    obj_frames = {
        o1: [],
        o2: []
    }

    def to_iterate(f_id, obj):
        tp = g.vType(rel)
        to_select = ['frames', f_id, tp, 'vertices']
        vertices_in_frame = pm.select(stsg, to_select)

        for contact_vert in vertices_in_frame:
            if contact_vert['class'] != rel:
                continue
            objs = pm.select(contact_vert, ['objects'])
            ans, return_obj = pm.existsReturnItem(objs, 'class', obj)

            if ans:
                rel_frames.append(contact_vert['id'])
                obj_frames[obj].append(return_obj['id'])
                return True
        return False

    exists1 = pm.exists(pm.iterate(list_of_frames, to_iterate,
                        1, a[2]['program'](a[2]['args'])), None, None)

    exists2 = pm.exists(pm.iterate(list_of_frames, to_iterate,
                        1, a[3]['program'](a[3]['args'])), None, None)

    #  update
    obj_verts1 = a[2]['sg_verts']
    obj_verts1[(0, -1)] = obj_frames[o1]

    obj_verts2 = a[3]['sg_verts']
    obj_verts2[(0, -1)] = obj_frames[o2]

    #  update
    rel_verts = a[0]['sg_verts']
    rel_verts[(0, -1)] = rel_frames

    # enure that the freaking vertices are all in the dictionary we want!
    sg_verts = {
        0: rel_verts,
        1: a[1]['sg_verts'],
        2: obj_verts1,
        3: obj_verts2,
    }

    return pm.verify(pm.AND([exists1, exists2])), sg_verts


def xorObjRelExists(stsg, a):
    """ Determines if a person did a relationship on an object

    Args:
        stsg: the spatio-temporal scene graph
        a: an list of arguments
           [relationship x, indirect time y,
           indirect object a, indirect object b]

    Returns:
        Yes if they did do x on a and b, No otherwise
    """
    list_of_frames = a[1]['direct']
    rel = a[0]['direct']
    o1 = a[2]['direct']
    o2 = a[3]['direct']

    rel_frames = []
    obj_frames = {
        o1: [],
        o2: []
    }

    def to_iterate(f_id, obj):
        tp = g.vType(rel)
        to_select = ['frames', f_id, tp, 'vertices']
        vertices_in_frame = pm.select(stsg, to_select)

        for contact_vert in vertices_in_frame:
            if contact_vert['class'] != rel:
                continue
            objs = pm.select(contact_vert, ['objects'])

            ans, return_obj = pm.existsReturnItem(objs, 'class', obj)
            if ans:
                rel_frames.append(contact_vert['id'])
                obj_frames[obj].append(return_obj['id'])
                return True
        return False

    exists1 = pm.exists(pm.iterate(list_of_frames, to_iterate,
                        1, a[2]['program'](a[2]['args'])), None, None)
    exists2 = pm.exists(pm.iterate(list_of_frames, to_iterate,
                        1, a[3]['program'](a[3]['args'])), None, None)

    #  update
    obj_verts1 = a[2]['sg_verts']
    obj_verts1[(0, -1)] = obj_frames[o1]

    obj_verts2 = a[3]['sg_verts']
    obj_verts2[(0, -1)] = obj_frames[o2]

    #  update
    rel_verts = a[0]['sg_verts']
    rel_verts[(0, -1)] = rel_frames

    # enure that the freaking vertices are all in the dictionary we want!
    sg_verts = {
        0: rel_verts,
        1: a[1]['sg_verts'],
        2: obj_verts1,
        3: obj_verts2,
    }

    # TODO: is this legal, or should I be outsourcing to pm?
    if exists2:
        return pm.verify(not exists2), sg_verts
    return pm.verify(exists1), sg_verts


###########################
#      First/Last/All     #
###########################


def objFLAInteracting(stsg, a):
    """ Finds the objects they were ___.

    Args:
        stsg: the spatio-temporal scene graph
        a: an list of arguments [relationship x, time y]

    Returns:
        A list of objects they did x to first
    """

    frame_ids = a[0]['direct']

    possible_answers = set()

    for frame in frame_ids:
        classes = pm.select(stsg, ['frames', frame, 'objects', 'names'])
        for cla in classes:
            possible_answers.add(cla)

    sg_verts = {
        0: a[0]['sg_verts'],
    }

    return list(possible_answers), sg_verts


def objFLA(stsg, a):
    """ Finds the objects they were ___.

    Args:
        stsg: the spatio-temporal scene graph
        a: an list of arguments [relationship x, time y]

    Returns:
        A list of objects they did x to first
    """

    frame_ids = a[1]['direct']
    if type(a[0]) == dict:
        rel = a[0]['program'](a[0]['args'])
    else:
        rel = a[0]

    def to_iterate_frame(datum, args):
        names = pm.select(stsg, ['frames', datum, g.vType(rel), 'names'])
        ex = pm.exists(names, None, rel)
        return ex

    frames = pm.iterate(frame_ids, to_iterate_frame, None, None)
    if frames is None:
        return [], None

    possible_answers = set()

    for frame in frames:
        vertex = pm.getVertex(stsg, rel, frame)
        objects = pm.select(vertex, ['objects'])
        classes = pm.editList(objects, 'class')
        for cla in classes:
            possible_answers.add(cla)

    rel_verts = a[0]['sg_verts']
    rel_verts[(0, -1)] = [rel + '/' + f for f in frames]
    sg_verts = {
        0: rel_verts,
        1: a[1]['sg_verts'],
    }

    return list(possible_answers), sg_verts


def objFLAQual(stsg, a):
    """ Finds the objects they were ___.

    Args:
        stsg: the spatio-temporal scene graph
        a: an list of arguments [relationship x, time y]

    Returns:
        A list of objects they did x to first
    """

    frame_ids = a[1]['direct']
    if type(a[0]) == dict:
        rel = a[0]['program'](a[0]['args'])
    else:
        rel = a[0]

    def to_iterate_frame(datum, args):
        names = pm.select(stsg, ['frames', datum, g.vType(rel), 'names'])
        ex = pm.exists(names, None, rel)
        return ex

    frames = pm.iterate(frame_ids, to_iterate_frame, None, None)
    if frames is None:
        return []

    possible_answers = set()

    for frame in frames:
        vertex = pm.getVertex(stsg, rel, frame)
        objects = pm.select(vertex, ['objects'])
        classes = pm.editList(objects, 'class')
        for cla in classes:
            possible_answers.add(cla)

    return list(possible_answers)


def relFLA(stsg, a):
    """ Finds the object they were ____ from first.

    Args:
        stsg: the spatio-temporal scene graph
        a: an list of arguments [relationship x]

    Returns:
        A list of objects they did x to first
    """

    list_of_first = []
    for rel_type in REL_TYPES:
        to_select = ['objects', a[0], 'vertices', 0, rel_type]
        relations = pm.select(stsg, to_select)
        if relations:
            list_of_first = list_of_first + relations

    classes = pm.editList(list_of_first, 'class')

    return classes


def objWhatChoose(stsg, a):
    """ Chooses the object they were ____ first.

    Args:
        stsg: the spatio-temporal scene graph
        a: an list of arguments [relationship x, time y]

    Returns:
        The object they did x to first
    """
    frame_ids = a[1]['direct']
    rel = a[0]['direct']

    def to_iterate_frame(f_id, args):
        o1Exists = pm.objRelExists(stsg, f_id, a[2]['direct'], rel)
        o2Exists = pm.objRelExists(stsg, f_id, a[3]['direct'], rel)

        return o1Exists or o2Exists

    frame_verts = pm.iterate(frame_ids, to_iterate_frame, None, None)
    if len(frame_verts) == 0:
        return [], None

    first_frame_id = frame_verts[0]
    if pm.objRelExists(stsg, first_frame_id, a[2]['direct'], rel):
        item = a[2]['direct'].split('/')[0]
    else:
        item = a[3]['direct'].split('/')[0]

    idx_first = frame_ids.index(first_frame_id)

    def to_iterate_frame_not(f_id, args):
        return pm.objRelExists(stsg, f_id, item, rel) == False

    last_frame_id = pm.iterate(frame_ids[idx_first:],
                               to_iterate_frame_not, 1, None)
    if last_frame_id is None:
        return None, None

    idx_last = frame_ids.index(last_frame_id)
    frame_group = frame_ids[idx_first:min(idx_last + 1, len(frame_ids))]

    all_objs = set()

    for frame_id in frame_group:
        tp = g.vType(rel)
        vertex_id = "%s/%s" % (rel, frame_id)
        if vertex_id not in stsg['stsg'][tp]:
            continue

        vertex = pm.getVertex(stsg, rel, frame_id)
        objects = pm.select(vertex, ['objects'])
        classes = pm.editList(objects, 'class')

        for i in classes:
            all_objs.add(i)

    if a[2]['direct'] in all_objs and a[3]['direct'] in all_objs:
        return None, None

    vertex = pm.getVertex(stsg, rel, first_frame_id)
    objects = pm.select(vertex, ['objects'])
    classes = pm.editList(objects, 'class')
    answer = pm.chooseOne(classes, [a[2]['direct'], a[3]['direct']])

    if answer is None:
        return answer, None

    rel_verts = a[0]['sg_verts']
    rel_verts[(0, -1)] = [rel + '/' + f for f in frame_verts]

    o1_verts = a[2]['sg_verts']
    o2_verts = a[3]['sg_verts']

    if item == a[2]['direct']:
        o1_verts[(0, -1)] = [item + '/' + f for f in frame_verts]
        o2_verts[(0, -1)] = []

    elif item == a[3]['direct']:
        o2_verts[(0, -1)] = [item + '/' + f for f in frame_verts]
        o1_verts[(0, -1)] = []

    else:
        print('Problem: direct is not working as comparison')
    sg_verts = {
        0: rel_verts,
        1: a[1]['sg_verts'],
        2: o1_verts,
        3: o2_verts
    }

    return answer, sg_verts


def actAfterAllFLA(stsg, a):
    """ Finds the first action they did.

    Args:
        stsg: the spatio-temporal scene graph
        a: an list of arguments []

    Returns:
        A list of the actions occuring after
    """

    list_of_frames = a[0]['direct']

    first_frame = list_of_frames[0]

    # NEW BLACKLISTING
    actions = pm.select(stsg, ['frames', first_frame, 'actions', 'names'])
    if len(actions) > 1:
        return [], None

    frames = pm.addSegmentationErrorMargin(stsg, [first_frame], )
    first_frame = pm.select(frames, [0])
    first_valid_time = pm.select(stsg, ['frames', first_frame, 'secs'])

    # NEW BLACKLISTING
    actions = pm.select(stsg, ['frames', first_frame, 'actions', 'names'])
    if len(actions) > 1:
        return [], None

    if first_frame == pm.select(stsg, ['ordered_frames', 0]):
        first_valid_time = 0.0
    else:
        first_valid_time = first_valid_time - 1

    def findActionsAfter(action_vertex, args):
        # Note! So I changed this so that it just looks at
        # everything that ends after it ends
        # Still going to blackilst this though
        end_time = pm.select(action_vertex, ['end'])

        first = pm.comparative(first_valid_time, float(end_time),
                               "less", None)
        return first == first_valid_time

    all_action_ids = pm.select(stsg, ['stsg', 'actions'])
    all_actions = pm.getVertexList(stsg, all_action_ids, 'actions')
    actions_after = pm.iterate(all_actions, findActionsAfter, None, None)

    actions_after = pm.editList(actions_after, 'charades')

    sg_verts = {
        0: a[0]['sg_verts'],
    }

    return actions_after, sg_verts


def actAfterAllFLAQual(stsg, a):
    """ Finds the first action they did.

    Args:
        stsg: the spatio-temporal scene graph
        a: an list of arguments []

    Returns:
        A list of the actions occuring after
    """

    list_of_frames = a[0]['direct']

    first_frame = list_of_frames[0]

    # NEW BLACKLISTING
    actions = pm.select(stsg, ['frames', first_frame, 'actions', 'names'])
    if len(actions) > 1:
        return [], None

    frames = pm.addSegmentationErrorMargin(stsg, [first_frame], )
    first_frame = pm.select(frames, [0])
    first_valid_time = pm.select(stsg, ['frames', first_frame, 'secs'])

    # NEW BLACKLISTING
    actions = pm.select(stsg, ['frames', first_frame, 'actions', 'names'])
    if len(actions) > 1:
        return [], None

    if first_frame == pm.select(stsg, ['ordered_frames', 0]):
        first_valid_time = 0.0
    else:
        first_valid_time = first_valid_time - 1  # so can be in first frame

    def findActionsAfter(action_vertex, args):
        # Note! So I changed this so that it just
        # looks at everything that ends after it ends
        # Still going to blackilst this though
        end_time = pm.select(action_vertex, ['end'])

        first = pm.comparative(first_valid_time, float(end_time),
                               "less", None)
        return first == first_valid_time

    all_action_ids = pm.select(stsg, ['stsg', 'actions'])
    all_actions = pm.getVertexList(stsg, all_action_ids, 'actions')
    actions_after = pm.iterate(all_actions, findActionsAfter, None, None)

    actions_after = pm.editList(actions_after, 'charades')

    return actions_after


def actBeforeFLA(stsg, a):
    """ Finds the last action they did.

    Args:
        stsg: the spatio-temporal scene graph
        a: an list of arguments [time]

    Returns:
        A last of the first actions
    """

    list_of_frames = a[0]['direct']

    last_frame = list_of_frames[-1]
    last_valid_time = pm.select(stsg, ['frames', last_frame, 'secs'])

    # NEW BLACKLISTING
    actions = pm.select(stsg, ['frames', last_frame, 'actions', 'names'])
    if len(actions) > 1:
        return [], None

    if last_frame == pm.select(stsg, ['ordered_frames', -1]):
        last_valid_time = 999999

    def findActionsAfter(action_vertex, args):
        end_time = pm.select(action_vertex, ['end'])
        last = pm.comparative(last_valid_time, float(end_time),
                              "more", None)
        return last != end_time

    all_action_ids = pm.select(stsg, ['stsg', 'actions'])
    all_actions = pm.getVertexList(stsg, all_action_ids, 'actions')
    actions_after = pm.iterate(all_actions, findActionsAfter, None, None)

    actions_after = pm.editList(actions_after, 'charades')

    sg_verts = {
        0: a[0]['sg_verts'],
    }

    return actions_after, sg_verts


def actBeforeFLAQual(stsg, a):
    """ Finds the last action they did.

    Args:
        stsg: the spatio-temporal scene graph
        a: an list of arguments [time]

    Returns:
        A last of the first actions
    """

    list_of_frames = a[0]['direct']

    last_frame = list_of_frames[-1]
    last_valid_time = pm.select(stsg, ['frames', last_frame, 'secs'])

    # NEW BLACKLISTING
    actions = pm.select(stsg, ['frames', last_frame, 'actions', 'names'])
    if len(actions) > 1:
        return []

    if last_frame == pm.select(stsg, ['ordered_frames', -1]):
        last_valid_time = 999999

    def findActionsAfter(action_vertex, args):
        end_time = pm.select(action_vertex, ['end'])
        last = pm.comparative(last_valid_time, float(end_time),
                              "more", None)
        return last != end_time

    all_action_ids = pm.select(stsg, ['stsg', 'actions'])
    all_actions = pm.getVertexList(stsg, all_action_ids, 'actions')
    actions_after = pm.iterate(all_actions, findActionsAfter, None, None)

    actions_after = pm.editList(actions_after, 'charades')

    return actions_after


##################
#      First     #
##################


def objFirst(stsg, a):
    """ Finds the object they were ____ first.

    Args:
        stsg: the spatio-temporal scene graph
        a: an list of arguments [relationship x, time y]

    Returns:
        A list of objects they did x to first
    """

    frame_ids = a[1]['direct']
    if type(a[0]) == dict:
        rel = a[0]['program'](a[0]['args'])
        rel_verts = a[0]['sg_verts']
    else:
        rel = a[0]
        rel_verts = {}

    def to_iterate_frame(datum, args):
        names = pm.select(stsg, ['frames', datum, g.vType(rel), 'names'])
        return pm.exists(names, None, rel)

    def to_iterate_frame_not(datum, args):
        names = pm.select(stsg, ['frames', datum, g.vType(rel), 'names'])
        return not pm.exists(names, None, rel)

    first_frame_id = pm.iterate(frame_ids, to_iterate_frame, 1, None)
    if first_frame_id is None:
        return [], None, None

    idx_first = frame_ids.index(first_frame_id)
    last_frame_id = pm.iterate(frame_ids[idx_first:],
                               to_iterate_frame_not, 1, None)
    if last_frame_id is None:
        return [], None, None

    idx_last = frame_ids.index(last_frame_id)
    frame_group = frame_ids[idx_first:min(idx_last + 1, len(frame_ids))]

    all_objs = set()

    rel_vertices = []
    for frame_id in frame_group:
        tp = g.vType(rel)
        vertex_id = "%s/%s" % (rel, frame_id)
        if vertex_id not in stsg['stsg'][tp]:
            continue

        vertex = pm.getVertex(stsg, rel, frame_id)
        objects = pm.select(vertex, ['objects'])
        classes = pm.editList(objects, 'class')

        rel_vertices.append(vertex['id'])

        for i in classes:
            all_objs.add(i)

    rel_verts[(0, -1)] = [rel + '/' + first_frame_id]

    sg_verts = {
        0: rel_verts,
        1: a[1]['sg_verts'],
    }

    return list(all_objs), rel_vertices, sg_verts


def objFirstChoose(stsg, a):
    """ Chooses the object they were ____ first.

    Args:
        stsg: the spatio-temporal scene graph
        a: an list of arguments [relationship x, time y]

    Returns:
        The object they did x to first
    """
    frame_ids = a[1]['direct']
    rel = a[0]['direct']

    def to_iterate_frame(f_id, args):
        o1Exists = pm.objRelExists(stsg, f_id, a[2]['direct'], rel)
        o2Exists = pm.objRelExists(stsg, f_id, a[3]['direct'], rel)

        return o1Exists or o2Exists

    first_frame_id = pm.iterate(frame_ids, to_iterate_frame, 1, None)
    if first_frame_id is None:
        return [], None

    if pm.objRelExists(stsg, first_frame_id, a[2]['direct'], rel):
        item = a[2]['direct'].split('/')[0]
    else:
        item = a[3]['direct'].split('/')[0]

    idx_first = frame_ids.index(first_frame_id)

    def to_iterate_frame_not(f_id, args):
        return not pm.objRelExists(stsg, f_id, item, rel)

    last_frame_id = pm.iterate(frame_ids[idx_first:],
                               to_iterate_frame_not, 1, None)
    if last_frame_id is None:
        return None, None

    idx_last = frame_ids.index(last_frame_id)
    frame_group = frame_ids[idx_first:min(idx_last + 1, len(frame_ids))]

    all_objs = set()

    for frame_id in frame_group:
        tp = g.vType(rel)
        vertex_id = "%s/%s" % (rel, frame_id)
        if vertex_id not in stsg['stsg'][tp]:
            continue

        vertex = pm.getVertex(stsg, rel, frame_id)
        objects = pm.select(vertex, ['objects'])
        classes = pm.editList(objects, 'class')

        for i in classes:
            all_objs.add(i)

    if a[2]['direct'] in all_objs and a[3]['direct'] in all_objs:
        return None, None

    vertex = pm.getVertex(stsg, rel, first_frame_id)
    objects = pm.select(vertex, ['objects'])
    classes = pm.editList(objects, 'class')
    answer = pm.chooseOne(classes, [a[2]['direct'], a[3]['direct']])

    if answer is None:
        return answer, None

    rel_verts = a[0]['sg_verts']
    rel_verts[(0, -1)] = [rel + '/' + first_frame_id]

    o1_verts = a[2]['sg_verts']
    o2_verts = a[3]['sg_verts']

    if item == a[2]['direct']:
        o1_verts[(0, -1)] = [item + '/' + first_frame_id]
        o2_verts[(0, -1)] = []

    elif item == a[3]['direct']:
        o2_verts[(0, -1)] = [item + '/' + first_frame_id]
        o1_verts[(0, -1)] = []

    else:
        print('Problem: direct is not working as comparison')
    sg_verts = {
        0: rel_verts,
        1: a[1]['sg_verts'],
        2: o1_verts,
        3: o2_verts
    }

    return answer, sg_verts


def objFirstVerify(stsg, a):
    """ Verifies the object they were ____ first.

    Args:
        stsg: the spatio-temporal scene graph
        a: an list of arguments [relationship x, time y, object z]

    Returns:
        Yes if they xed z first, No otherwise
    """
    first_obj, _, sg_verts_old = objFirst(stsg, a)
    if len(first_obj) != 1:
        return None, None

    first_rel = sg_verts_old[0][(0, -1)][0]
    frame = first_rel.split('/')[1]

    same = first_obj[0] == a[2]['direct']

    if same:
        sg_verts = {
            0: {(0, -1): [first_rel]},
            1: a[1]['sg_verts'],
            2: a[2]['sg_verts']
        }

        sg_verts[2][(0, -1)] = [a[2]['direct'] + '/' + frame]
    else:
        sg_verts = {
            0: {(0, -1): []},
            1: a[1]['sg_verts'],
            2: a[2]['sg_verts']
        }

        sg_verts[2][(0, -1)] = []

    return pm.verify(same), sg_verts


def relFirst(stsg, a):
    """ Finds the object they were ____ from first.

    Args:
        stsg: the spatio-temporal scene graph
        a: an list of arguments [relationship x]

    Returns:
        A list of objects they did x to first
    """

    list_of_first = []
    for rel_type in REL_TYPES:
        to_select = ['objects', a[0], 'vertices', 0, rel_type]
        relations = pm.select(stsg, to_select)
        if relations:
            list_of_first = list_of_first + relations

    classes = pm.editList(list_of_first, 'class')

    return classes


def actFirst(stsg, a):
    """ Finds the first action they did.

    Args:
        stsg: the spatio-temporal scene graph
        a: an list of arguments []

    Returns:
        A list of the first actions
    """

    list_of_frames = a[0]['direct']
    first_frame = list_of_frames[0]
    actions = set()

    frames = pm.addSegmentationErrorMargin(stsg, [first_frame])
    first_frame = pm.select(frames, [0])
    first_valid_time = pm.select(stsg, ['frames', first_frame, 'secs'])

    buffer_end = first_valid_time + 5
    secs = first_valid_time
    i = 0
    while secs < buffer_end and i < len(list_of_frames):
        secs = pm.select(stsg, ['frames', list_of_frames[i], 'secs'])
        if secs > buffer_end:
            break

        acts = pm.select(stsg, ['frames', list_of_frames[i],
                                'actions', 'names'])
        for act in acts:
            actions.add(act)
        i += 1

    if len(actions) > 1:
        return [], None

    # NEW BLACKLISTING - so if there's more than one thing happening its a nope
    actions = pm.select(stsg, ['frames', first_frame, 'actions', 'names'])
    if len(actions) > 1:
        return [], None

    if first_frame == pm.select(stsg, ['ordered_frames', 0]):
        first_valid_time = 0.0
    else:
        first_valid_time = first_valid_time - 1  # so can be in first frame

    def findActionsAfter(action_vertex, args):
        start_time = pm.select(action_vertex, ['start'])

        first = pm.comparative(first_valid_time, float(start_time),
                               "less", None)
        return first == first_valid_time

    all_action_ids = pm.select(stsg, ['stsg', 'actions'])
    all_actions = pm.getVertexList(stsg, all_action_ids, 'actions')
    actions_after = pm.iterate(all_actions, findActionsAfter, None, None)

    first = pm.superlative(actions_after, 'least', 'start')
    first = pm.editList(first, 'charades')

    sg_verts = {
        0: a[0]['sg_verts'],
    }

    return first, sg_verts


##################
#      Last      #
##################


def objLast(stsg, a):
    """ Finds the object they were ____ last.

    Args:
        stsg: the spatio-temporal scene graph
        a: an list of arguments [relationship x, time y]

    Returns:
        A list of objects they did x to last
    """
    frame_ids = a[1]['direct']
    if type(a[0]) == dict:
        rel = a[0]['program'](a[0]['args'])
        rel_verts = a[0]['sg_verts']
    else:
        rel = a[0]
        rel_verts = {}

    def to_iterate_frame(datum, args):
        names = pm.select(stsg, ['frames', datum, g.vType(rel), 'names'])
        return pm.exists(names, None, rel)

    last_frame_id = pm.iterate(frame_ids, to_iterate_frame, -1, None)
    if last_frame_id is None:
        return [], None, None

    def to_iterate_frame_not(datum, args):
        names = pm.select(stsg, ['frames', datum, g.vType(rel), 'names'])
        return not pm.exists(names, None, rel)

    idx_last = frame_ids.index(last_frame_id)
    previous_frames = frame_ids[:idx_last + 1]
    previous_frames.reverse()
    first_frame_id = pm.iterate(previous_frames, to_iterate_frame_not, 1, None)
    if first_frame_id is None:
        return [], None, None

    idx_first = frame_ids.index(first_frame_id)

    frame_group = frame_ids[max(idx_first - 2, 0):idx_last + 1]

    all_objs = set()
    rel_vertices = []
    for frame_id in frame_group:

        tp = g.vType(rel)
        vertex_id = "%s/%s" % (rel, frame_id)
        if vertex_id not in stsg['stsg'][tp]:
            continue

        vertex = pm.getVertex(stsg, rel, frame_id)
        objects = pm.select(vertex, ['objects'])
        classes = pm.editList(objects, 'class')

        for i in classes:
            all_objs.add(i)

        rel_vertices.append(vertex['id'])

    rel_verts[(0, -1)] = [rel + '/' + last_frame_id]

    sg_verts = {
        0: rel_verts,
        1: a[1]['sg_verts'],
    }

    return list(all_objs), rel_vertices, sg_verts


def objLastChoose(stsg, a):
    """ Chooses the object they were ____ last.

    Args:
        stsg: the spatio-temporal scene graph
        a: an list of arguments [relationship x, time y, obj a, obj b]

    Returns:
        A the object they did x to last, a or b
    """
    frame_ids = a[1]['direct']
    rel = a[0]['direct']

    def to_iterate_frame(f_id, args):
        o1Exists = pm.objRelExists(stsg, f_id, a[2]['direct'], rel)
        o2Exists = pm.objRelExists(stsg, f_id, a[3]['direct'], rel)
        return o1Exists or o2Exists

    last_frame_id = pm.iterate(frame_ids, to_iterate_frame, -1, None)
    if last_frame_id is None:
        return None, None

    if pm.objRelExists(stsg, last_frame_id, a[2]['direct'], rel):
        item = a[2]['direct'].split('/')[0]
    else:
        item = a[3]['direct'].split('/')[0]

    idx_last = frame_ids.index(last_frame_id)

    def to_iterate_frame_not(f_id, args):
        return not pm.objRelExists(stsg, f_id, item, rel)

    idx_last = frame_ids.index(last_frame_id)
    previous_frames = frame_ids[:idx_last + 1]
    previous_frames.reverse()
    first_frame_id = pm.iterate(previous_frames, to_iterate_frame_not, 1, None)

    if first_frame_id is None:
        return None, None

    idx_first = frame_ids.index(first_frame_id)
    frame_group = frame_ids[idx_first:min(idx_last + 1, len(frame_ids))]

    all_objs = set()

    for frame_id in frame_group:
        tp = g.vType(rel)
        vertex_id = "%s/%s" % (rel, frame_id)
        if vertex_id not in stsg['stsg'][tp]:
            continue

        vertex = pm.getVertex(stsg, rel, frame_id)
        objects = pm.select(vertex, ['objects'])
        classes = pm.editList(objects, 'class')

        for i in classes:
            all_objs.add(i)

    if a[2]['direct'] in all_objs and a[3]['direct'] in all_objs:
        return None, None

    vertex = pm.getVertex(stsg, rel, last_frame_id)
    objects = pm.select(vertex, ['objects'])
    classes = pm.editList(objects, 'class')
    answer = pm.chooseOne(classes, [a[2]['direct'], a[3]['direct']])

    rel_verts = a[0]['sg_verts']
    rel_verts[(0, -1)] = [rel + '/' + last_frame_id]

    o1_verts = a[2]['sg_verts']
    o2_verts = a[3]['sg_verts']

    if item == a[2]['direct']:
        o1_verts[(0, -1)] = [item + '/' + last_frame_id]
        o2_verts[(0, -1)] = []

    elif item == a[3]['direct']:
        o2_verts[(0, -1)] = [item + '/' + last_frame_id]
        o1_verts[(0, -1)] = []

    else:
        print('Problem: direct is not working as comparison')
    sg_verts = {
        0: rel_verts,
        1: a[1]['sg_verts'],
        2: o1_verts,
        3: o2_verts
    }

    if answer is None:
        return answer, None

    return answer, sg_verts


def objLastVerify(stsg, a):
    """ Verifies the object they were ____ last.

    Args:
        stsg: the spatio-temporal scene graph
        a: an list of arguments [relationship x, time y, object z]

    Returns:
        Yes if they xed z last, No otherwise
    """

    last_obj, _, sg_verts_old = objLast(stsg, a)

    if len(last_obj) != 1:
        return None, None

    last_rel = sg_verts_old[0][(0, -1)][-1]
    frame = last_rel.split('/')[1]

    same = last_obj[0] == a[2]['direct']

    if same:
        sg_verts = {
            0: {(0, -1): [last_rel]},
            1: a[1]['sg_verts'],
            2: a[2]['sg_verts']
        }

        sg_verts[2][(0, -1)] = [a[2]['direct'] + '/' + frame]
    else:
        sg_verts = {
            0: {(0, -1): []},
            1: a[1]['sg_verts'],
            2: a[2]['sg_verts']
        }

        sg_verts[2][(0, -1)] = []

    return pm.verify(same), sg_verts


def relLast(stsg, a):
    """ Finds the object they were ____ from last.

    Args:
        stsg: the spatio-temporal scene graph
        a: an list of arguments [relationship x]

    Returns:
        A list of objects they did x to last
    """

    list_of_last = []
    for rel_type in REL_TYPES:
        to_select = ['objects', a[0], 'vertices', -1, rel_type]
        relations = pm.select(stsg, to_select)
        if relations:
            list_of_last = list_of_last + relations

    classes = pm.editList(list_of_last, 'class')

    return classes


def actLast(stsg, a):
    """ Finds the last action they did.

    Args:
        stsg: the spatio-temporal scene graph
        a: an list of arguments [time]

    Returns:
        A last of the first actions
    """

    list_of_frames = a[0]['direct']

    last_frame = list_of_frames[-1]
    last_valid_time = pm.select(stsg, ['frames', last_frame, 'secs'])

    actions = set()

    if last_frame == pm.select(stsg, ['ordered_frames', -1]):
        last_valid_time = 999999
        last_valid_time = pm.select(stsg, ['frames', last_frame, 'secs'])

    buffer_start = last_valid_time - 5
    secs = last_valid_time
    i = -1
    while secs > buffer_start and i > (len(list_of_frames) * -1):
        secs = pm.select(stsg, ['frames', list_of_frames[i], 'secs'])
        if secs < buffer_start:
            break

        acts = pm.select(stsg, ['frames', list_of_frames[i],
                                'actions', 'names'])
        for act in acts:
            actions.add(act)
        i -= 1

    if len(actions) > 1:
        return [], None

    all_ends = []

    def findActionsAfter(action_vertex, args):
        end_time = pm.select(action_vertex, ['end'])
        last = pm.comparative(last_valid_time, float(end_time),
                              "more", None)
        all_ends.append(end_time)
        return last != end_time

    all_action_ids = pm.select(stsg, ['stsg', 'actions'])
    all_actions = pm.getVertexList(stsg, all_action_ids, 'actions')
    actions_after = pm.iterate(all_actions, findActionsAfter, None, None)

    first = pm.superlative(actions_after, 'most', 'end')

    sg_verts = {
        0: a[0]['sg_verts'],
    }

    first = pm.editList(first, 'charades')
    return first, sg_verts


##################
#      What      #
##################


def actWhatAfterAll(stsg, a):
    """ Finds all things they started doing after finishing an action

    Args:
        stsg: the spatio-temporal scene graph
        a: an list of arguments [indirect action]

    Returns:
        The first action to occur after finishing action
    """

    # find last frame of action
    a_id = a[0]['program'](a[0]['args'])
    all_acts = pm.select(stsg, ['actions', a_id, 'vertices'])

    if not pm.lengthOne(all_acts):
        return

    end_frame_id = pm.select(all_acts, [0, 'all_f', -1])
    frames = pm.addSegmentationErrorMargin(stsg, [end_frame_id])
    end_frame_id = pm.select(frames, [0])

    first_valid_time = pm.select(stsg, ['frames', end_frame_id, 'secs'])

    def findActionsAfter(action_vertex, args):
        start_time = pm.select(action_vertex, ['start'])
        first = pm.comparative(first_valid_time, float(start_time),
                               "less", None)
        return first == first_valid_time

    all_action_ids = pm.select(stsg, ['stsg', 'actions'])
    all_actions = pm.getVertexList(stsg, all_action_ids, 'actions')
    actions_after = pm.iterate(all_actions, findActionsAfter, None, None)

    actions_after = pm.editList(actions_after, 'charades')

    return actions_after


def actWhatBeforeAll(stsg, a):
    """ Finds all things they ended doing before finishing an action

    Args:
        stsg: the spatio-temporal scene graph
        a: an list of arguments [indirect action]

    Returns:
        The actions to occur before starting action
    """

    # find last frame of action
    a_id = a[0]['program'](a[0]['args'])
    all_acts = pm.select(stsg, ['actions', a_id, 'vertices'])

    if not pm.lengthOne(all_acts):
        return

    start_frame_id = pm.select(all_acts, [0, 'all_f', 0])
    frames = pm.addSegmentationErrorMargin(stsg, [start_frame_id])
    start_frame_id = pm.select(frames, [-1])

    last_valid_time = pm.select(stsg, ['frames', start_frame_id, 'secs'])

    def findActionsBefore(action_vertex, args):
        end_time = pm.select(action_vertex, ['end'])
        end = pm.comparative(last_valid_time, float(end_time),
                             "more", None)
        return end == last_valid_time

    all_action_ids = pm.select(stsg, ['stsg', 'actions'])
    all_actions = pm.getVertexList(stsg, all_action_ids, 'actions')
    actions_after = pm.iterate(all_actions, findActionsBefore, None, None)

    actions_after = pm.editList(actions_after, 'charades')

    return actions_after


##################
#     Length     #
##################
def actLengthLongerChoose(stsg, a):
    """ Finds which happened longer

    Args:
        stsg: the spatio-temporal scene graph
        a: an list of arguments [action, action]

    Returns:
        Which action occured for longer
    """

    act2len = pm.select(findLengths(stsg), [1])
    a_id1 = a[0]['direct']
    a_id2 = a[1]['direct']
    len1 = pm.select(act2len, [a_id1])
    len2 = pm.select(act2len, [a_id2])

    error_margin = 7

    if pm.inMarginOfError(error_margin, [len1, len2], 0, 1):
        return None, None

    longer = pm.comparative(len1, len2, 'more', None)

    sg_verts = {
        0: a[0]['sg_verts'],
        1: a[1]['sg_verts'],
    }

    if pm.equals(longer, len1):
        return a_id1, sg_verts
    elif pm.equals(longer, len2):
        return a_id2, sg_verts
    else:
        print("Something's wrong")
        return None, []


def actLengthShorterChoose(stsg, a):
    """ Finds which happened for less time

    Args:
        stsg: the spatio-temporal scene graph
        a: an list of arguments [action, action]

    Returns:
        Which action occured for shorter
    """

    act2len = pm.select(findLengths(stsg), [1])
    a_id1 = a[0]['direct']
    a_id2 = a[1]['direct']
    len1 = pm.select(act2len, [a_id1])
    len2 = pm.select(act2len, [a_id2])

    error_margin = 7

    if pm.inMarginOfError(error_margin, [len1, len2], 0, 1):
        return None, None

    shorter = pm.comparative(len1, len2, 'less', None)

    sg_verts = {
        0: a[0]['sg_verts'],
        1: a[1]['sg_verts'],
    }

    if pm.equals(shorter, len1):
        return a_id1, sg_verts
    elif pm.equals(shorter, len2):
        return a_id2, sg_verts
    else:
        print("Something's wrong")
        return None, None


def actLengthLongerVerify(stsg, a):
    """ Confirms if an action happened for longer than another

    Args:
        stsg: the spatio-temporal scene graph
        a: an list of arguments [action x, action y]

    Returns:
        True if action x happened longer than y, False otherwise
    """

    act2len = pm.select(findLengths(stsg), [1])
    a_id1 = a[0]['direct']
    a_id2 = a[1]['direct']
    len1 = pm.select(act2len, [a_id1])
    len2 = pm.select(act2len, [a_id2])

    error_margin = 7

    if pm.inMarginOfError(error_margin, [len1, len2], 0, 1):
        return None, None

    longer = pm.comparative(len1, len2, 'more', None)

    sg_verts = {
        0: a[0]['sg_verts'],
        1: a[1]['sg_verts'],
    }

    return pm.verify(pm.equals(longer, len1)), sg_verts


def actLengthShorterVerify(stsg, a):
    """ Confirms if an action happened for less time than another

    Args:
        stsg: the spatio-temporal scene graph
        a: an list of arguments [action x, action y]

    Returns:
        True if action x happened for less time than y, False otherwise
    """

    act2len = pm.select(findLengths(stsg), [1])
    a_id1 = a[0]['direct']
    a_id2 = a[1]['direct']
    len1 = pm.select(act2len, [a_id1])
    len2 = pm.select(act2len, [a_id2])

    error_margin = 7

    if pm.inMarginOfError(error_margin, [len1, len2], 0, 1):
        return None, None

    shorter = pm.comparative(len1, len2, 'less', None)

    sg_verts = {
        0: a[0]['sg_verts'],
        1: a[1]['sg_verts'],
    }

    return pm.verify(pm.equals(shorter, len1)), sg_verts


##################
#      Time      #
##################
def actTime(stsg, a):
    """ Finds if one action occurred before or after another

    Args:
        stsg: the spatio-temporal scene graph
        a: an list of arguments [action, action]

    Returns:
        If the action occured before or after
    """
    # make sure no multiple instances
    if (not pm.onlyActionInstance(stsg, a[0]['direct']) or
       not pm.onlyActionInstance(stsg, a[1]['direct'])):
        return None, None

    # find the frames of action 2
    outer_frames = pm.select(stsg, ['actions', a[1]['direct'],
                                    'vertices', 0, 'all_f'])

    # get all frame sbefore and afer
    before_frames = pm.getFrameIds(stsg, pm.select(outer_frames, [0]),
                                   'before')
    after_frames = pm.getFrameIds(stsg, pm.select(outer_frames, [-1]), 'after')

    # add error margin
    before_frames = pm.addSegmentationErrorMargin(stsg, before_frames)
    after_frames = pm.addSegmentationErrorMargin(stsg, after_frames)

    # find frames of action1
    inner_frames = pm.select(stsg, ['actions', a[0]['direct'],
                                    'vertices', 0, 'all_f'])

    if pm.containedIn(inner_frames, outer_frames):
        return None, None

    sg_verts = {
        0: a[0]['sg_verts'],
        1: a[1]['sg_verts'],
    }

    a1 = a[0]['direct']
    # see if their contained before, after or neithr
    if pm.containedIn(inner_frames, before_frames):
        # If action is in actionSV
        if a1 in actionSV:
            # Find the object and relationship
            obj, rel = actionSV[a1]
            # Then for each f_id in after_frames do pm.objRelExists() with the args:
            for f_id in after_frames:
                # stsg, f_id, obj, rel
                if pm.objRelExists(stsg, f_id, obj, rel):
                    # if the obj-rel combination exists in any of these frames, 
                    # Return None, None
                    return None, None
            # MAKE SURE to make the same changes in solve_action_indirect
            # Do the same thing for the elif where it returns after
        return "before", sg_verts
    elif pm.containedIn(inner_frames, after_frames):
        # If action is in actionSV
        if a1 in actionSV:
            obj, rel = actionSV[a1]
            # Then for each f_id in after_frames do pm.objRelExists() with the args:
            for f_id in before_frames:
                # stsg, f_id, obj, rel
                if pm.objRelExists(stsg, f_id, obj, rel):
                    # if the obj-rel combination exists in any of these frames, 
                    # Return None, None
                    return None, None
        return "after", sg_verts
    else:
        return None, None


def relTime(stsg, a):
    """ Finds if a relation occurred before or after an action

    Args:
        stsg: the spatio-temporal scene graph
        a: an list of arguments [rel, action]

    Returns:
        If the rel occured before or after
    """

    # make sure no multiple instances
    if not pm.onlyActionInstance(stsg, a[1]['direct']):
        return None, None, None

    # find the frames of action 2
    outer_frames = pm.select(stsg, ['actions', a[1]['direct'],
                                    'vertices', 0, 'all_f'])

    # get all frame sbefore and afer
    before_frames = pm.getFrameIds(stsg,
                                   pm.select(outer_frames, [0]), 'before')
    after_frames = pm.getFrameIds(stsg, pm.select(outer_frames, [-1]), 'after')

    # add error margin
    before_frames = pm.addSegmentationErrorMargin(stsg, before_frames)
    after_frames = pm.addSegmentationErrorMargin(stsg, after_frames)

    rel_frames = []

    tp = g.vType(a[0]['direct'])

    # iterate before and after frames to see if held something in each
    def relInFrame(f_id, args):
        rels = pm.select(stsg, ['frames', f_id, tp, 'names'])

        exists = pm.exists(rels, None, a[0]['direct'])

        if exists:
            rel_frames.append(f_id)
        return exists

    before = pm.iterate(before_frames, relInFrame, None, None)
    objs = []
    after = pm.iterate(after_frames, relInFrame, None, None)
    occurred_before = not pm.isEmpty(before)
    occurred_after = not pm.isEmpty(after)

    # during is new
    during = pm.iterate(outer_frames, relInFrame, None, None)
    occurred_during = not pm.isEmpty(during)

    if occurred_during:
        return None, None, None

    rel_verts = a[0]['sg_verts']
    rel_verts[(0, -1)] = [a[0]['direct'] + '/' + f for f in rel_frames]

    sg_verts = {
        0: rel_verts,
        1: a[1]['sg_verts'],
    }

    if not pm.XOR(occurred_before, occurred_after):
        return None, None, None
    elif occurred_before:
        for f_id in before:
            for obj in pm.select(stsg, ['frames', f_id, 'objects', 'names']):
                if pm.objRelExists(stsg, f_id, obj, a[0]['direct']):
                    objs.append(obj)
        return "before", objs, sg_verts
    else:
        for f_id in after:
            for obj in pm.select(stsg, ['frames', f_id, 'objects', 'names']):
                if pm.objRelExists(stsg, f_id, obj, a[0]['direct']):
                    objs.append(obj)
        return "after", objs, sg_verts


def objTime(stsg, a):
    """ Finds if someon contacted x occurred before or after an action

    Args:
        stsg: the spatio-temporal scene graph
        a: an list of arguments [rel, action]

    Returns:
        If the obj was contacted occured before or after
    """

    # make sure no multiple instances
    if not pm.onlyActionInstance(stsg, a[1]['direct']):
        return None, None, None

    # find the frames of action 2
    outer_frames = pm.select(stsg, ['actions', a[1]['direct'],
                                    'vertices', 0, 'all_f'])

    # get all frame sbefore and afer
    before_frames = pm.getFrameIds(stsg, pm.select(outer_frames, [0]),
                                   'before')
    after_frames = pm.getFrameIds(stsg, pm.select(outer_frames, [-1]), 'after')

    # add error margin
    before_frames = pm.addSegmentationErrorMargin(stsg, before_frames)
    after_frames = pm.addSegmentationErrorMargin(stsg, after_frames)

    obj_frames = []

    # iterate before and after frames to see if held something in each
    def objContactedInFrame(f_id, args):
        rels = pm.select(stsg, ['frames', f_id, 'contact', 'vertices'])
        exists = pm.objInRelList(rels, a[0]['direct'])
        if exists:
            obj_frames.append(f_id)
        return exists

    before = pm.iterate(before_frames, objContactedInFrame, None, None)
    after = pm.iterate(after_frames, objContactedInFrame, None, None)

    # during is new
    during = pm.iterate(outer_frames, objContactedInFrame, None, None)
    occurred_during = not pm.isEmpty(during)

    occurred_before = not pm.isEmpty(before)
    occurred_after = not pm.isEmpty(after)

    rels = set()

    if occurred_during:
        return None, None, None

    obj_verts = a[0]['sg_verts']
    obj_verts[(0, -1)] = [a[0]['direct'] + '/' + f for f in obj_frames]

    sg_verts = {
        0: obj_verts,
        1: a[1]['sg_verts'],
    }

    if not pm.XOR(occurred_before, occurred_after):
        return None, None, None
    elif occurred_before:
        for f_id in before:
            for rel in pm.select(stsg, ['frames', f_id, 'contact', 'names']):
                if pm.objRelExists(stsg, f_id, a[0]['direct'], rel):
                    rels.add(rel)
        return "before", list(rels), sg_verts
    else:
        for f_id in after:
            for rel in pm.select(stsg, ['frames', f_id, 'contact', 'names']):
                if pm.objRelExists(stsg, f_id, a[0]['direct'], rel):
                    rels.add(rel)
        return "after", list(rels), sg_verts
