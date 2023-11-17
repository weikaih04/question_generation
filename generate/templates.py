import grammar
import solve
import pickle

f = open('../data/validObjRel.pkl', 'rb')
validObjRel = pickle.load(f)
f.close()

f = open('../data/actionSV.pkl', 'rb')
ACTION_SV = pickle.load(f)
f.close()

f = open('../data/svAction.pkl', 'rb')
SV_ACTION = pickle.load(f)
f.close()

objRelActionCombos = list(ACTION_SV.values())

IDX = grammar.IDX
ENG = grammar.ENG
PP = grammar.PP
ART = grammar.ART
vType = grammar.vType
art = grammar.art
pres = grammar.pres
past = grammar.past
pp = grammar.pp

ALL_ACT = {'c000', 'c001', 'c002', 'c003', 'c004', 'c005', 'c006',
           'c007', 'c008', 'c009', 'c010', 'c011', 'c012', 'c013', 'c014',
           'c015', 'c016', 'c017', 'c018', 'c019', 'c020', 'c021', 'c022',
           'c023', 'c024', 'c025', 'c026', 'c027', 'c028', 'c029', 'c030',
           'c031', 'c032', 'c033', 'c034', 'c035', 'c036', 'c037', 'c038',
           'c039', 'c040', 'c041', 'c042', 'c043', 'c044', 'c045', 'c046',
           'c047', 'c048', 'c049', 'c050', 'c051', 'c052', 'c053', 'c054',
           'c055', 'c056', 'c057', 'c058', 'c059', 'c060', 'c061', 'c062',
           'c063', 'c064', 'c065', 'c066', 'c067', 'c068', 'c069', 'c070',
           'c071', 'c072', 'c073', 'c074', 'c075', 'c076', 'c077', 'c078',
           'c079', 'c080', 'c081', 'c082', 'c083', 'c084', 'c085', 'c086',
           'c087', 'c088', 'c089', 'c090', 'c091', 'c092', 'c093', 'c094',
           'c095', 'c096', 'c097', 'c098', 'c099', 'c100', 'c101', 'c102',
           'c103', 'c104', 'c105', 'c106', 'c107', 'c108', 'c109', 'c110',
           'c111', 'c112', 'c113', 'c114', 'c115', 'c116', 'c117', 'c118',
           'c119', 'c120', 'c121', 'c122', 'c123', 'c124', 'c125', 'c126',
           'c127', 'c128', 'c129', 'c130', 'c131', 'c132', 'c133', 'c134',
           'c135', 'c136', 'c137', 'c138', 'c139', 'c140', 'c141', 'c142',
           'c143', 'c144', 'c145', 'c146', 'c147', 'c148', 'c149', 'c150',
           'c151', 'c152', 'c153', 'c154', 'c155', 'c156'}

ALL_OBJ = {'o1', 'o10', 'o11', 'o12', 'o13', 'o14', 'o15', 'o16', 'o17',
           'o18', 'o19', 'o2', 'o20', 'o21', 'o22', 'o23', 'o24',
           'o25', 'o26', 'o27', 'o28', 'o29', 'o3', 'o30', 'o31', 'o32',
           'o33', 'o34', 'o35', 'o36', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9'}

ALL_AREL = {'r1', 'r2'}
ALL_SREL = {'r4', 'r5', 'r6', 'r7', 'r8', 'r9'}

ALL_CREL = {'r10', 'r11', 'r12', 'r13', 'r14', 'r15', 'r16', 'r17',
            'r18', 'r20', 'r21', 'r22', 'r23', 'r24', 'r25', 'r26'}


ALL_VREL = {'v000', 'v001', 'v002', 'v003', 'v006', 'v007', 'v009',
            'v011', 'v012', 'v013', 'v014', 'v015', 'v016', 'v019',
            'v021', 'v023', 'v024', 'v025', 'v026', 'v027', 'v028',
            'v029', 'v030', 'v031', 'v032'}


ALL_OBJ_INDIRECT = ['direct', 'first', 'last', 'whole']
ALL_REL_INDIRECT = ['direct', 'first']

ALL_ACT_INDIRECT = ['direct', 'longest', 'shortest', 'indir-obj', 'indir-verb']
ALL_TIME_INDIRECT = ['before', 'after', 'while', 'all', 'between']
COMP_TIME_INDIRECT = ['before', 'after', 'while', 'between']

# verbs that only have one associated objet
SINGLE_OBJ_VERBS = ['v024', 'v011', 'v013', 'v029', 'v027',
                    'v015', 'v007', 'v002']

# commonsense obj, rel combintions
commonsense_combos = [
    (IDX['floor'], IDX['standing_on']),
    (IDX['floor'], IDX['touching']),
    (IDX['floor'], IDX['behind']),
    (IDX['floor'], IDX['in front of']),
    (IDX['floor'], IDX['beneath']),
    (IDX['floor'], IDX['above']),
    (IDX['doorknob'], IDX['grasping']),
    (IDX['clothes'], IDX['touching']),
    (IDX['shoe'], IDX['touching']),
    (IDX['hair'], IDX['touching']),
    (IDX['clothes'], IDX['wearing']),
    (IDX['shoe'], IDX['wearing']),
]

same_obj = {
    'person': [], 'bag': [],
    'bed': ['chair', 'sofa'],
    'blanket': ['clothes', 'towel'],
    'book': ['paper', 'picture'],
    'box': [], 'broom': [],
    'chair': ['sofa', 'bed'],
    'closet': ['door', 'refrigerator'],
    'clothes': ['blanket', 'towel'],
    'cup': ['dish'],
    'dish': ['cup'],
    'door': ['refrigerator', 'closet'],
    'doorknob': [], 'doorway': [], 'floor': [],
    'food': ['sandwich', 'groceries', 'medicine'],
    'groceries': ['food', 'sandwich', 'medicine'],
    'laptop': [], 'light': [],
    'medicine': ['food', 'groceries', 'sandwich'],
    'mirror': [],
    'paper': ['book', 'picture'],
    'phone': [],
    'picture': ['paper', 'book'],
    'pillow': [],
    'refrigerator': ['door', 'closet'],
    'sandwich': ['food', 'groceries', 'medicine'],
    'shelf': ['table'],
    'shoe': [],
    'sofa': ['bed', 'chair'],
    'table': ['shelf'],
    'television': [],
    'towel': ['clothes', 'blanket'],
    'vacuum': [], 'window': [], 'hands': [], 'hair': [], 'None': [],
}


def transition(action):
    """ Indicates if the action has a transition verb

    Args:
        action: str (action code)

    Returns:
        True if action uses transition verb, false otherwise
    """
    if type(action) == dict:
        action = action['direct']

    if action == IDX['reaching for and grabbing a picture']:
        return True

    _, v = ACTION_SV[action]

    t_verbs = [IDX['taking'], IDX['putting'], IDX['throwing'],
               IDX['closing'], IDX['opening']]

    return v in t_verbs


def noAmbiguity(all_objs, output, potential_obj):
    """ Indicates if there are multiple objects annotated that are similar

    Args:
        all_objs: list (all objects in video)
        output: str ("Yes" or "No" answer to question)
        potential_obj: object referenced in question

    Returns:
        True if not ambiguous, False otherwise

    """

    # if the answer (output) is yes, return True
    if output == "Yes":
        return True

    if isIndirect(potential_obj):
        potential_obj = potential_obj['direct']

    # look at the potential object
    # if it (change to english) has synonyms, then ambiguous
    for syn in same_obj[ENG[potential_obj]]:
        if IDX[syn] in all_objs:
            return False
    return True


def isValidObjRel(obj, rel):
    """ Determines if this obj-rel pair can be used

    Args:
        obj: str (an object)
        rel: str (a relationship)

    Returns:
        True if can be used, false otherwise
    """

    # Can't ask: "Are they holding the object they were holding?"
    if isIndirect(obj):
        if obj['type'] != 'direct':
            if isIndirect(rel):
                direct_rel = rel['direct']
            else:
                direct_rel = rel
            if obj['args'][0] == direct_rel:
                return False
        obj = obj['direct']

    # Can't ask: "Are they doing what they did to the cup to the cup?"
    if isIndirect(rel):
        if rel['args'][0] == obj:
            return False
        rel = rel['direct']

    # it occurs enough times in the dataset
    if rel not in validObjRel[obj]:
        return False
    # There are multiple options of object for this relationship
    if rel in SINGLE_OBJ_VERBS:
        return False
    # Isn't actually just an action (though less important now?)
    #if (obj, rel) in objRelActionCombos:
    #    return False
    # Is not an obvious answer (are they above the floor)
    if (obj, rel) in commonsense_combos:
        return False
    return True


def combineMetrics(lst, items):
    """ Format the metrics of multiple inputs

    Args:
        lst: list of input metric
        items: another list of metrics

    Returns:
        a combined and formatted list of metrics

    """
    for item in items:
        if type(item) == dict:
            lst.append(item['direct'])
        else:
            lst.append(item)
    return lst


def combineObjRel(indirects, objs, rels):
    """ Format the obj-rel metrics of multiple inputs

    Args:
        indirects: lst (incoming object-relationship pair)
        objs: lst (existing objects)
        rels: lst (existing rels)

    Returns:
        a combined and formatted list of obj-rel metrics
    """
    new_obj = []
    new_rel = []

    for indirect in indirects:
        new_obj = new_obj + indirect['metrics']['objrel'][0]
        new_rel = new_rel + indirect['metrics']['objrel'][1]

    for obj in objs:
        if type(obj) is dict:
            obj = obj['direct']
        new_obj.append(obj)

    for rel in rels:
        if type(rel) is dict:
            rel = rel['direct']
        new_rel.append(rel)

    return objRelIndirect(new_obj, new_rel)


def combineIndirectMetrics(indirects):
    """ get all the indirect references metrics and combine

    Args:
        indirects: lst (indirect references)
    Returns:
        Formatted metrics for the indirect references
    """

    before = []
    first = []
    longer = []
    repetition = []

    new_indirect = []
    for i in range(4):
        nxt = False
        for item in indirects:
            if item['metrics']['indirects'][i]:
                nxt = True
                break
        new_indirect.append(nxt)

    for indirect in indirects:
        before = before + indirect['metrics']['before']
        first = first + indirect['metrics']['first']
        longer = longer + indirect['metrics']['longer']
        repetition = repetition + indirect['metrics']['repetition']

    return before, first, longer, repetition, new_indirect


def metrics(indirects, befores, firsts, longers, repetitions, objrels):
    """ combine new metrics from question with others

    Args:
        indirects: lst (existing metrics from previous questions)
        befores: lst (before metrics from this question)
        firsts: lst (first metrics from this question)
        longers: lst (longer metrics from this question)
        repetitions: lst (repetition metrics from this question)
        objrels: lst (objrel metrics from this question)

    Returns:
        formatted list of all metric types
    """
    # first combine indirects
    b, f, l, r, indirect_types = combineIndirectMetrics(indirects)

    # then combine with directs or with things in other ones
    before = combineMetrics(b, befores)
    first = combineMetrics(f, firsts)
    longer = combineMetrics(l, longers)
    repetition = combineMetrics(r, repetitions)
    objrel = combineObjRel(indirects, objrels[0], objrels[1])

    metrics = {
        'before': before,
        'first': first,
        'longer': longer,
        'repetition': repetition,
        'objrel': objrel,
        'indirects': indirect_types,
    }

    return metrics


def objRelIndirect(indirect_obj, indirect_rel):
    """ format objRel metrics with indirect refs

    Args:
        indirect_obj: list (indirect objects)
        indirect_rel: list (indirect relationships)

    Returns:
        formatted list of objrel metrics
    """
    obj_rel = []
    for obj in indirect_obj:
        for rel in indirect_rel:
            obj_rel.append((obj, rel))

    return obj_rel


def isValidRel(rel):
    """ relationship is ok to ask questions about

    Args:
        rel: str (relationship)

    Returns:
        True if valid relationship, false otherwise
    """

    # Not just one thing the relationship does
    if rel in SINGLE_OBJ_VERBS:
        return False

    # Not an obvious relationship
    if rel in [IDX['wearing'], IDX['standing on']]:
        return False
    return True


def isValidIndirect(indirect, rel):
    """ Does the indirect object reference the relationship?

    Args:
        indirect: an indirect object
        rel: str (relationship)

    Returns:
        True if the indirect object does not reference the relationship
        False otherwise
    """
    first_arg = indirect['args'][0]
    if first_arg is None:
        return True

    if type(first_arg) == dict:
        direct = first_arg['direct']
    else:
        direct = first_arg
    return rel != direct


def isValidObjCombo(obj1, obj2):
    """ Are objects for choose too similar?

    Args:
        obj1: str (object)
        obj2: str (object)

    Returns:
        True if objects are not too similar
        False otherwise
    """
    if isIndirect(obj1):
        obj1 = obj1['direct']
    if isIndirect(obj2):
        obj2 = obj2['direct']

    if obj1 == obj2:
        return False

    if obj1 == IDX['food'] and obj2 == IDX['sandwich']:
        return False

    if obj1 == IDX['sandwich'] and obj2 == IDX['food']:
        return False

    if obj1 == IDX['door'] and obj2 == IDX['doorway']:
        return False

    if obj1 == IDX['doorway'] and obj2 == IDX['door']:
        return False

    if obj1 == IDX['dish'] and obj2 == IDX['cup']:
        return False

    if obj1 == IDX['cup'] and obj2 == IDX['dish']:
        return False

    return True


def occursNo(comp, num, action, stsg):
    """ determines if an action occurred more of less times
        than a specified digit

    Args:
        comp: str ("more" or "les")
        num: int (the number compared to)
        action: str (action)
        stsg: a scene graph

    Returns:
        True if [action] occured [comp] than [num] times in [stsg]
        False otherwise
    """

    if isIndirect(action):
        action = action['direct']

    num_actions = len(stsg['actions'][action]['vertices'])

    if comp == "more":
        return num_actions <= num
    elif comp == "less":
        return num_actions >= num
    else:
        print("Incorrect comp argument ", comp)


def noActOverlapWithTime(act, time):
    """ Make sure not referring to the same thing

    Args:
        act: an action index 'c__'
        time: a time indirect object

    Returns:
        True if referencing different different actions:
    """
    # so if between can chech both
    for arg in time['args']:
        if arg is None:
            continue
        if arg['direct'] == act:
            return False
    return True


def isIndirect(item):
    """ determines if an item is indirect

    Args:
        item: any data

    Returns:
        True if the item is a dict, false otherwise
    """
    return type(item) == dict


def actFromObjRel(objs, rels):
    """ determine what actions occured based on objects and relations

    Args:
        objs: lst (objects)
        rels: lst (rels)

    Returns:
        list of actions using those objects and relationships
    """
    actions = []
    for obj in objs:
        if type(obj) == dict:
            obj = obj['direct']
        for rel in rels:
            if type(rel) == dict:
                rel = rel['direct']
            key = (obj, rel)
            if key in SV_ACTION:
                actions.append(SV_ACTION[key])
    return actions


def notInAction(sv, action):
    """ Determines if an object or relation is used in an action

    Args:
        sv: str (either a object or a relationship)
        action: str (action)

    Returns:
        True if [sv] is not in [action], False otherwise
        
    """
    if isIndirect(sv):
        sv = sv['direct']
    if isIndirect(action):
        if action['type'] in ALL_TIME_INDIRECT:
            if action['type'] == 'all':
                return True

            if action['type'] == 'between':
                if not notInAction(sv, action['args'][1]['direct']):
                    return False
            action = action['args'][0]['direct']
        else:
            action = action['direct']

    obj, verb = ACTION_SV[action]
    obj = IDX[ENG[obj]]
    verb = IDX[ENG[verb]]

    tp = grammar.vType(sv)

    if tp == 'objects':
        return obj != sv
    else:
        return verb != sv


def timeDirect(time):
    """ get the direct string of a time object

    Args:
        time: a time object

    Returns:
        the string reference to that time
    """
    tp = time['type']

    if tp == 'all':
        return ""

    if tp == 'between':
        a1 = time['args'][0]['direct']
        a2 = time['args'][1]['direct']
        return "%s-%s" % (a1, a2)

    return time['args'][0]['direct']


def getTemplatesForVideo(stsg):
    """ create templates based on spatio-temporal scene graphs

    Args:
        stsg: a spatio-temporal scene graph

    Returns:
        A dictionary of templates structured as such:

        'templateType': {
            'id': string id,
            'attributes': {
                'type': string templateType, #todo: storing this twice
                'structural': string verify, choose, logical...,
                'semantic': string object/relationship/action...,
                'ans_type': string binary/open,
                'video_id': string video id,
            },
            'global': string exists/first/last/etc,
            'local': lambda o, a: function,
            'questions': [ list of lambda a: functions ],
            'args': [... [number of this type, [direct], [indirec types]] ...],
            'program': lambda a: call to solve.type(stsg, a),
            'steps': integer number of compositional steps,
            'quals': [ list of lambda o, a: functions ],
            'package_ans': lambda o: how to process answer
        }
    """
    v_id = stsg['video_id']

    obj = stsg['obj_names']
    act = stsg['act_names']
    arel = []
    crel = stsg['crel_names']
    srel = stsg['srel_names']
    vrel = stsg['vrel_names']
    # get tags not in stsg
    abs_obj = list(ALL_OBJ - set(obj))
    abs_crel = list(ALL_CREL - set(crel))
    abs_vrel = list(ALL_VREL - set(vrel))


    templates = {
        ##########
        # EXISTS #
        ##########
        'objExists': {
            'id': 'objExists',
            'attributes': {
                'type': 'objExists',
                'structural': 'verify',
                'semantic': 'object',
                'ans_type': 'binary',
                'video_id': v_id,
            },
            'global': 'exists',
            'local': lambda o, a: a[0],
            'questions': [
                lambda a: "Does someone interact with %s%s?"
                          % (art(a[0]), a[1]['phrase']),
                lambda a: "Is there %s the person interacts with%s?"
                          % (art(a[0]), a[1]['phrase']),
                lambda a: "Were they interacting with %s%s?"
                          % (art(a[0]), a[1]['phrase']),
                lambda a: "%s, did they interact with %s?"
                          % (a[1]['start_phrase'], art(a[0])), 
                lambda a: "Was %s one of the things they were interacting with%s?"
                          % (art(a[0]), a[1]['phrase']),
            ],
            'starts': [
                [27, 27],
                [9, 35],
                [27, 27],
                [25, 0],
                [4, 49],
            ],
            'order': [
                [0, 1],
                [0, 1],
                [0, 1],
                [1, 0],
                [0, 1],
            ],
            'phrases': [
                lambda a: [art(a[0]), a[1]['phrase']],
                lambda a: [art(a[0]), a[1]['phrase']],
                lambda a: [art(a[0]), a[1]['phrase']],
                lambda a: [art(a[0]), a[1]['start_phrase']],
                lambda a: [art(a[0]), a[1]['phrase']],
            ],
            'args': [[1, obj + abs_obj, []],
                     [1, ['time'], ALL_TIME_INDIRECT]],
            'direct': lambda a: "%s" % (a[0]),
            'time': lambda a: (a[1]['type'], timeDirect(a[1])),
            'program': lambda a: solve.objExists(stsg, a),
            'steps': 1,
            'quals': [
                lambda o, a: notInAction(a[0], a[1]),
                lambda o, a: a[0] not in [IDX['clothes'], IDX['shoe'],
                                          IDX['light'], IDX['floor'],
                                          IDX['person'], IDX['doorway']],
                lambda o, a: noAmbiguity(obj, o, a[0]),
            ],
            'package_ans': lambda o: o,
            'metrics': lambda o, a: metrics([a[1]], [], [], [], [], [[a[0]], o[1]]),
            'str_program': lambda a: "Exists(%s, Iterate(%s, Filter(frame, [objects])))" % (ENG[a[0]], a[1]['tree']),
        },

        'objRelExists': {
            'id': 'objRelExists',
            'attributes': {
                'type': 'objRelExists',
                'structural': 'verify',
                'semantic': 'relation',
                'ans_type': 'binary',
                'video_id': v_id,
            },
            'global': 'exists',
            'local': lambda o, a: "%s-%s" % (a[0]['direct'], a[1]['direct']),
            'questions': [
                lambda a: "Was the person %s %s%s?" %
                          (pp(a[0]), art(a[1]), a[2]['phrase']),
                lambda a: "Did they %s %s%s?" %
                          (pres(a[0]), art(a[1]), a[2]['phrase']),
                lambda a: "%s, did they %s %s?" %
                          (a[2]['start_phrase'], pres(a[0]), art(a[1])),
            ],
            'starts': [
                [15, 16, 16],
                [9, 10, 10],
                [11, 12, 0],
            ],
            'order': [
                [0, 1, 2],
                [0, 1, 2],
                [2, 0, 1],
            ],
            'phrases': [
                lambda a: [pp(a[0]), art(a[1]), a[2]['phrase']],
                lambda a: [pres(a[0]), art(a[1]), a[2]['phrase']],
                lambda a: [pres(a[0]), art(a[1]), a[2]['start_phrase']],
            ],
            'args': [[1, arel + crel + vrel, ALL_REL_INDIRECT],
                     [1, obj, ALL_OBJ_INDIRECT],
                     [1, ['time'], ALL_TIME_INDIRECT]],
            'direct': lambda a: "%s-%s" % (a[0]['direct'], a[1]['direct']),
            'time': lambda a: (a[2]['type'], timeDirect(a[2])),
            'program': lambda a: solve.objRelExists(stsg, a),
            'steps': 1,
            'quals': [
                lambda o, a: a[0]['direct'] not in [IDX['not_contacting'],
                                                    IDX['not_looking_at']],
                lambda o, a: isValidIndirect(a[0], a[1]['direct']),
                lambda o, a: a[0]['direct'] != a[1]['args'][0],
                lambda o, a: isValidObjRel(a[1]['direct'], a[0]['direct']),
                lambda o, a: False if (a[0]['direct'] == IDX['touching'] and
                                       a[1]['args'][0] in crel) else True,
                lambda o, a: a[1]['args'][0] not in [IDX['not_contacting'],
                                                     IDX['not_looking_at']],
                lambda o, a: False if (a[2]['type'] in COMP_TIME_INDIRECT and
                                       IDX[ENG[ACTION_SV[a[2]['args'][0]['direct']][0]]] == a[1]['direct'])
                             else True,
            ],
            'package_ans': lambda o: o,
            'metrics': lambda o, a: metrics([a[0], a[1], a[2]], [], [], [], [], [[a[1]],[a[0]]]),
            'str_program': lambda a: "Exists(%s, Iterate(%s, Filter(frame, [relations, %s, objects])))" % (a[1]['tree'], a[2]['tree'], a[0]['tree']),
        },

        'relExists': {
            'id': 'relExists',
            'attributes': {
                'type': 'relExists',
                'structural': 'verify',
                'semantic': 'relation',
                'ans_type': 'binary',
                'video_id': v_id,
            },
            'global': 'exists',
            'local': lambda o, a: a[0],
            'questions': [
                lambda a: "Was the person %s something%s?" %
                          (pp(a[0]), a[1]['phrase']),
                lambda a: "Was the person %s anything%s?" %
                          (pp(a[0]), a[1]['phrase']),
                lambda a: "Did they %s something%s?" %
                          (pres(a[0]), a[1]['phrase']),
                lambda a: "Did they %s anything%s?" %
                          (pres(a[0]), a[1]['phrase']),
                lambda a: "Had they %s something%s?" %
                          (past(a[0]), a[1]['phrase']),
                lambda a: "Had the person %s anything%s?" %
                          (past(a[0]), a[1]['phrase']),
                lambda a: "%s, was the person %s something?" %
                          (a[1]['start_phrase'], pp(a[0])),
                lambda a: "%s, was the person %s anything?" %
                          (a[1]['start_phrase'], pp(a[0])),
                lambda a: "%s, did they %s something?" %
                          (a[1]['start_phrase'], pres(a[0])),
                lambda a: "%s, did they %s anything?" %
                          (a[1]['start_phrase'], pres(a[0])),
            ],
            'starts': [
                [15, 25],
                [15, 24],
                [9, 19],
                [9, 18],
                [9, 19],
                [15, 24],
                [17, 0],
                [17, 0],
                [11, 0],
                [11, 0],
            ],
            'order': [
                [0, 1],
                [0, 1],
                [0, 1],
                [0, 1],
                [0, 1],
                [0, 1],
                [1, 0],
                [1, 0],
                [1, 0],
                [1, 0],
            ],
            'phrases': [
                lambda a: [pp(a[0]), a[1]['phrase']],
                lambda a: [pp(a[0]), a[1]['phrase']],
                lambda a: [pres(a[0]), a[1]['phrase']],
                lambda a: [pres(a[0]), a[1]['phrase']],
                lambda a: [past(a[0]), a[1]['phrase']],
                lambda a: [past(a[0]), a[1]['phrase']],
                lambda a: [pp(a[0]), a[1]['start_phrase']],
                lambda a: [pp(a[0]), a[1]['start_phrase']],
                lambda a: [pres(a[0]), a[1]['start_phrase']],
                lambda a: [pres(a[0]), a[1]['start_phrase']],
            ],
            'args': [[1, crel + abs_crel + vrel + abs_vrel, []],
                     [1, ['time'], ALL_TIME_INDIRECT]],
            'direct': lambda a: "%s" % (a[0]),
            'time': lambda a: (a[1]['type'], timeDirect(a[1])),
            'program': lambda a: solve.relExists(stsg, a),
            'steps': 1,
            'quals': [
                lambda o, a: a[0] not in [IDX['not_contacting'],
                                          IDX['not_looking_at'],
                                          'v030', 'v006', 'v009',
                                          'v017', 'r20', 'v019',
                                          'v020', 'v022'],
                lambda o, a: False if (a[0] == IDX['touching'] and not o and
                                       len(crel) != 0) else True,
                lambda o, a: isValidRel(a[0]),
                lambda o, a: notInAction(a[0], a[1])
            ],
            'package_ans': lambda o: o,
            'metrics': lambda o, a: metrics([a[1]], [], [], [], [], [o[1],[a[0]]]),
            'str_program': lambda a: "Exists(%s, Iterate(%s, Filter(frame, [relations])))" % (ENG[a[0]], a[1]['tree']),
        },

        'andObjRelExists': {
            'id': 'andObjRelExists',
            'attributes': {
                'type': 'andObjRelExists',
                'structural': 'logic',
                'semantic': 'relation',
                'ans_type': 'binary',
                'video_id': v_id,
            },
            'global': 'exists',
            'local': lambda o, a: "and-%s-%s-%s" %
                                  (a[0]['direct'], a[2]['direct'],
                                   a[3]['direct']),
            'questions': [
                lambda a: "Were they %s both %s and %s%s?" %
                          (pp(a[0]), art(a[2]),
                           art(a[3]), a[1]['phrase']),
                lambda a: "Did the person %s both %s and %s%s?" %
                          (pres(a[0]), art(a[2]),
                           art(a[3]), a[1]['phrase']),
                lambda a: "%s, was the person %s both %s and %s?" %
                          (a[1]['start_phrase'], pp(a[0]), art(a[2]),
                           art(a[3])),
                lambda a: "%s, did they %s both %s and %s?" %
                          (a[1]['start_phrase'], pres(a[0]), art(a[2]),
                           art(a[3])),
                #lambda a: "Was the person %s %s and %s %s%s?" %
                #          (pp(a[0]), art(a[2]), pp(a[0]),
                #           art(a[3]), a[1]['phrase']),
                #lambda a: "Did they %s %s and %s %s%s?" %
                #          (pres(a[0]), art(a[2]), pres(a[0]),
                #           art(a[3]), a[1]['phrase']),
                #lambda a: "%s, were they %s %s and %s %s?" %
                #          (a[1]['start_phrase'], pp(a[0]), art(a[2]), pp(a[0]),
                #           art(a[3])),
                #lambda a: "%s, did the person %s %s and %s %s?" %
                #          (a[1]['start_phrase'], pres(a[0]), art(a[2]), pres(a[0]),
                #           art(a[3])),
            ],
            'starts': [
                [10, 21, 16, 21],
                [15, 26, 21, 26],
                [17, 0, 23, 28],
                [11, 0, 17, 22]
            ],
            'order': [
                [0, 2, 3, 1],
                [0, 2, 3, 1],
                [1, 0, 2, 3],
                [1, 0, 2, 3],
            ],
            'phrases': [
                lambda a: [pp(a[0]), a[1]['phrase'], art(a[2]),
                           art(a[3])],
                lambda a: [pres(a[0]), a[1]['phrase'], art(a[2]),
                           art(a[3])],
                lambda a: [pp(a[0]), a[1]['start_phrase'], art(a[2]),
                           art(a[3])],
                lambda a: [pres(a[0]), a[1]['start_phrase'], art(a[2]),
                           art(a[3])],
            ],
            'args': [[1, arel + crel + vrel, ALL_REL_INDIRECT],
                     [1, ['time'], ALL_TIME_INDIRECT],
                     [2, obj, ALL_OBJ_INDIRECT]],
            'direct': lambda a: "and-%s-%s-%s" % (a[0]['direct'],
                                                  a[2]['direct'],
                                                  a[3]['direct']),
            'time': lambda a: (a[1]['type'], timeDirect(a[1])),
            'program': lambda a: solve.andObjRelExists(stsg, a),
            'steps': 3,
            'quals': [
                lambda o, a: a[0]['direct'] not in [IDX['not_contacting'],
                                                    IDX['not_looking_at']],
                lambda o, a: isValidObjRel(a[2]['direct'], a[0]['direct']),
                lambda o, a: isValidObjRel(a[3]['direct'], a[0]['direct']),
                # TODO: same as below? (but doesn't work)
                lambda o, a: False if (a[0]['direct'] == IDX['touching'] and
                                       a[2]['args'][0] in crel) else True,
                lambda o, a: False if (a[0]['direct'] == IDX['touching'] and
                                       a[3]['args'][0] in crel) else True,
                lambda o, a: notInAction(a[2], a[1]),
                lambda o, a: notInAction(a[3], a[1]),
                lambda o, a: isValidObjCombo(a[2], a[3])
            ],
            'package_ans': lambda o: o,
            'metrics': lambda o, a: metrics(a, [], [], [], [], [[a[2], a[3]], [a[0]]]),
            'str_program': lambda a: "AND(Exists(%s, Iterate(%s, Filter(frame, [relation, %s, objects]))), Exists(%s, Iterate(%s, Filter(frame, [relation, %s, objects]))))" 
                            % (a[2]['tree'], a[1]['tree'], a[0]['tree'], a[3]['tree'], a[1]['tree'], a[0]['tree'])
        },

        'xorObjRelExists': {
            'id': 'xorObjRelExists',
            'attributes': {
                'type': 'xorObjRelExists',
                'structural': 'logic',
                'semantic': 'relation',
                'ans_type': 'binary',
                'video_id': v_id,
            },
            'global': 'exists',
            'local': lambda o, a: "xor-%s-%s-%s" %
                                  (a[0]['direct'],
                                   a[2]['direct'],
                                   a[3]['direct']),
            'questions': [
                lambda a: "Was the person %s %s but not %s%s?" %
                          (pp(a[0]), art(a[2]),
                           art(a[3]), a[1]['phrase']),
                lambda a: "Did they %s %s but not %s%s?" %
                          (pres(a[0]), art(a[2]),
                           art(a[3]), a[1]['phrase']),
                lambda a: "%s, were they %s %s but not %s?" %
                          (a[1]['start_phrase'], pp(a[0]), art(a[2]),
                           art(a[3])),
                lambda a: "%s, did they %s %s but not %s?" %
                          (a[1]['start_phrase'], pres(a[0]), art(a[2]),
                           art(a[3])),
            ],
            'starts': [
                [15, 25, 16, 25],
                [9, 19, 10, 19],
                [12, 0, 13, 22],
                [11, 0, 12, 21]
            ],
            'order': [
                [0, 2, 3, 1],
                [0, 2, 3, 1],
                [1, 0, 2, 3],
                [1, 0, 2, 3],
            ],
            'phrases': [
                lambda a: [pp(a[0]), a[1]['phrase'], art(a[2]),
                           art(a[3])],
                lambda a: [pres(a[0]), a[1]['phrase'], art(a[2]),
                           art(a[3])],
                lambda a: [pp(a[0]), a[1]['start_phrase'], art(a[2]),
                           art(a[3])],
                lambda a: [pres(a[0]), a[1]['start_phrase'], art(a[2]),
                           art(a[3])],
            ],
            'args': [[1, arel + crel + vrel, ALL_REL_INDIRECT],
                     [1, ['time'], ALL_TIME_INDIRECT],
                     [2, obj, ALL_OBJ_INDIRECT]],
            'direct': lambda a: "xor-%s-%s-%s" % (a[0]['direct'],
                                                  a[2]['direct'],
                                                  a[3]['direct']),
            'time': lambda a: (a[1]['type'], timeDirect(a[1])),
            'program': lambda a: solve.xorObjRelExists(stsg, a),
            'steps': 3,
            'quals': [
                lambda o, a: a[0]['direct'] not in [IDX['not_contacting'],
                                                    IDX['not_looking_at']],
                lambda o, a: isValidObjRel(a[2]['direct'], a[0]['direct']),
                lambda o, a: isValidObjRel(a[3]['direct'], a[0]['direct']),
                lambda o, a: False if (a[0]['direct'] == IDX['touching'] and
                                       a[2]['args'][0] in crel) else True,
                lambda o, a: False if (a[0]['direct'] == IDX['touching'] and
                                       a[3]['args'][0] in crel) else True,
                lambda o, a: notInAction(a[2], a[1]),
                lambda o, a: notInAction(a[3], a[1]),
                lambda o, a: isValidObjCombo(a[2], a[3]),
            ],
            'package_ans': lambda o: o,
            'metrics': lambda o, a: metrics(a, [], [], [], [], [[a[2], a[3]], [a[0]]]),
            'str_program': lambda a: "XOR(Exists(%s, Iterate(%s, Filter(frame, [relation, %s, objects]))), Exists(%s, Iterate(%s, Filter(frame, [relation, %s, objects]))))" 
                            % (a[2]['tree'], a[1]['tree'], a[0]['tree'], a[3]['tree'], a[1]['tree'], a[0]['tree'])
        },

        #########
        #  FLA  #
        #########

        'objWhatGeneral': {
            'id': 'objWhatGeneral',
            'attributes': {
                'type': 'objWhatGeneral',
                'structural': 'query',
                'semantic': 'object',
                'ans_type': 'open',
                'video_id': v_id,
            },
            'global': 'what',
            'local': lambda o, a: 'object',
            'questions': [
                lambda a: "Which object were they interacting with%s?" %
                          (a[0]['phrase']),
                lambda a: "What was the person interacting with%s?" %
                          (a[0]['phrase']),
                lambda a: "Which object did the person interact with%s?" %
                          (a[0]['phrase']),
                lambda a: "What did they interact with%s?" %
                          (a[0]['phrase']),
                lambda a: "%s, which object were they interacting with?" %
                          (a[0]['start_phrase']),
                lambda a: "%s, what was the person interacting with?" %
                          (a[0]['start_phrase']),
                lambda a: "%s, which object did the person interact with?" %
                          (a[0]['start_phrase']),
                lambda a: "%s, what did they interact with?" %
                          (a[0]['start_phrase']),
            ],
            'starts': [
                [39], [36], [41], [27], [0], [0], [0], [0],
            ],
            'order': [
                [0], [0], [0], [0], [0], [0], [0], [0]
            ],
            'phrases': [
                lambda a: [a[0]['phrase']],
                lambda a: [a[0]['phrase']],
                lambda a: [a[0]['phrase']],
                lambda a: [a[0]['phrase']],
                lambda a: [a[0]['start_phrase']],
                lambda a: [a[0]['start_phrase']],
                lambda a: [a[0]['start_phrase']],
                lambda a: [a[0]['start_phrase']],
            ],
            'args': [[1, ['time'],
                     ['before', 'after', 'all', 'while', 'between']]],
            'direct': lambda a: "",
            'time': lambda a: (a[0]['type'], timeDirect(a[0])),
            'program': lambda a: solve.objFLAInteracting(stsg, a),
            'steps': 1,
            'quals': [
                lambda o, a: len(o) == 1,
                lambda o, a: notInAction(o[0], a[0]),
            ],
            'package_ans': lambda o: ENG[o[0]],
            'metrics': lambda o, a: metrics(a, [], [], [], [], [[], []]),
            'str_program': lambda a: "Query(class, OnlyItem(Iterate(%s, Filter(frame, [objects]))))" % a[0]['tree']
        },

        'objWhat': {
            'id': 'objWhat',
            'attributes': {
                'type': 'objWhat',
                'structural': 'query',
                'semantic': 'object',
                'ans_type': 'open',
                'video_id': v_id,
            },
            'global': 'what',
            'local': lambda o, a: a[0]['direct'],
            'questions': [
                lambda a: "Which object were they %s%s?" %
                          (pp(a[0]), a[1]['phrase']),
                lambda a: "What was the person %s%s?" %
                          (pp(a[0]), a[1]['phrase']),
                lambda a: "Which object did the person %s%s?" %
                          (pres(a[0]), a[1]['phrase']),
                lambda a: "What did they %s%s?" %
                          (pres(a[0]), a[1]['phrase']),
                lambda a: "%s, which object were they %s?" %
                          (a[1]['start_phrase'], pp(a[0])),
                lambda a: "%s, what was the person %s?" %
                          (a[1]['start_phrase'], pp(a[0])),
                lambda a: "%s, which object did the person %s?" %
                          (a[1]['start_phrase'], pres(a[0])),
                lambda a: "%s, what did they %s?" %
                          (a[1]['start_phrase'], pres(a[0])),
            ],
            'starts': [
                [23, 23],
                [20, 20],
                [28, 28],
                [14, 14],
                [25, 0],
                [22, 0],
                [30, 0],
                [16, 0],
            ],
            'order': [
                [0, 1], [0, 1], [0, 1], [0, 1], [1, 0], [1, 0], [1, 0], [1, 0]
            ],
            'phrases': [
                lambda a: [pp(a[0]), a[1]['phrase']],
                lambda a: [pp(a[0]), a[1]['phrase']],
                lambda a: [pres(a[0]), a[1]['phrase']],
                lambda a: [pres(a[0]), a[1]['phrase']],
                lambda a: [pp(a[0]), a[1]['start_phrase']],
                lambda a: [pp(a[0]), a[1]['start_phrase']],
                lambda a: [pres(a[0]), a[1]['start_phrase']],
                lambda a: [pres(a[0]), a[1]['start_phrase']],
            ],
            'args': [[1, crel + arel + srel + vrel, ALL_REL_INDIRECT],
                     [1, ['time'],
                      ['before', 'after', 'all', 'while', 'between']]],
            'direct': lambda a: "%s" % (a[0]['direct']),
            'time': lambda a: (a[1]['type'], timeDirect(a[1])),
            'program': lambda a: solve.objFLA(stsg, a),
            'steps': 2,
            'quals': [
                lambda o, a: len(o) == 1,
                lambda o, a: a[0]['direct'] not in [IDX[
                    'not_contacting'], IDX['not_looking_at']],
                lambda o, a: notInAction(o[0], a[1]),
                lambda o, a: notInAction(a[0], a[1]),
                lambda o, a: isValidIndirect(a[0], o[0])
            ],
            'package_ans': lambda o: ENG[o[0]],
            'metrics': lambda o, a: metrics(a, [], [], [], [], [[o[0][0]], [a[0]]]),
            'str_program': lambda a: "Query(class, OnlyItem(Iterate(%s, Filter(frame, [relations, %s, objects]))))" 
                        % (a[1]['tree'], a[0]['tree'])
        },

        'objWhatChoose': {
            'id': 'objWhatChoose',
            'attributes': {
                'type': 'objWhatChoose',
                'structural': 'choose',
                'semantic': 'object',
                'ans_type': 'binary',
                'video_id': v_id,
            },
            'global': 'what',
            'local': lambda o, a: "%s-%s-%s" % (a[0]['direct'],
                                                a[2]['direct'],
                                                a[3]['direct']),
            'questions': [
                lambda a: "Which were they %s%s, %s or %s?" %
                          (pp(a[0]), a[1]['phrase'],
                           art(a[2]), art(a[3])),
                lambda a: "Which did they %s%s, %s or %s?" %
                          (pres(a[0]), a[1]['phrase'],
                           art(a[2]), art(a[3])),
                lambda a: "Was %s or %s the thing they %s%s?" %
                          (art(a[2]), art(a[3]), past(a[0]), a[1]['phrase']),
                lambda a: "Were they %s %s or %s%s?" %
                          (pp(a[0]), art(a[2]), art(a[3]), a[1]['phrase']),
                lambda a: "%s, which was the person %s, %s or %s?" %
                          (a[1]['start_phrase'], pp(a[0]),
                           art(a[2]), art(a[3])),
                lambda a: "%s, which did they %s, %s or %s?" %
                          (a[1]['start_phrase'], pres(a[0]),
                           art(a[2]), art(a[3])),
                lambda a: "%s, was %s or %s the thing they %s?" %
                          (a[1]['start_phrase'], art(a[2]),
                           art(a[3]), past(a[0])),
                lambda a: "%s, did they %s %s or %s?" %
                          (a[1]['start_phrase'], pres(a[0]),
                           art(a[2]), art(a[3])),
            ],
            'starts': [
                [16, 16, 18, 22],
                [15, 15, 17, 21],
                [24, 24, 4, 8],
                [10, 15, 11, 15],
                [23, 0, 25, 29],
                [17, 0, 19, 23],
                [26, 0, 6, 10],
                [11, 0, 12, 16],
            ],
            'order': [
                [0, 1, 2, 3],
                [0, 1, 2, 3],
                [2, 3, 0, 1],
                [0, 2, 3, 1],
                [1, 0, 2, 3],
                [1, 0, 2, 3],
                [1, 2, 3, 0],
                [1, 0, 2, 3],
            ],
            'phrases': [
                lambda a: [pp(a[0]), a[1]['phrase'],
                           art(a[2]), art(a[3])],
                lambda a: [pres(a[0]), a[1]['phrase'],
                           art(a[2]), art(a[3])],
                lambda a: [past(a[0]), a[1]['phrase'],
                           art(a[2]), art(a[3])],
                lambda a: [pp(a[0]), a[1]['phrase'],
                           art(a[2]), art(a[3])],
                lambda a: [pp(a[0]), a[1]['start_phrase'],
                           art(a[2]), art(a[3])],
                lambda a: [pres(a[0]), a[1]['start_phrase'],
                           art(a[2]), art(a[3])],
                lambda a: [past(a[0]), a[1]['start_phrase'],
                           art(a[2]), art(a[3])],
                lambda a: [pres(a[0]), a[1]['start_phrase'],
                           art(a[2]), art(a[3])],
            ],
            'args': [[1, crel + arel + srel + vrel, ALL_REL_INDIRECT],
                     [1, ['time'],
                      ['before', 'after', 'all', 'while', 'between']],
                     [2, obj, ['direct', 'last']]],
            'direct': lambda a: "%s-%s-%s" % (a[0]['direct'],
                                              a[2]['direct'],
                                              a[3]['direct']),
            'time': lambda a: (a[1]['type'], timeDirect(a[1])),
            'program': lambda a: solve.objWhatChoose(stsg, a),
            'steps': 3,
            'quals': [
                lambda o, a: o is not None,
                lambda o, a: len(o) != 0,
                lambda o, a: a[0]['direct'] not in [IDX[
                    'not_contacting'], IDX['not_looking_at']],
                lambda o, a: isValidObjRel(a[2], a[0]),
                lambda o, a: isValidObjRel(a[3], a[0]),
                lambda o, a: isValidObjCombo(a[2], a[3]),
                lambda o, a: notInAction(a[0], a[1]),
                lambda o, a: notInAction(a[2], a[1]),
                lambda o, a: notInAction(a[3], a[1]),
                lambda o, a: not (a[2]['direct'] in solve.objFLAQual(stsg, a) and a[3]['direct'] in solve.objFLAQual(stsg, a)),
            ],
            'package_ans': lambda o: ENG[o],
            'metrics': lambda o, a: metrics(a, [], [], [], [], [[a[2], a[3]], [a[0]]]),
            'str_program': lambda a: "Choose(%s, %s, Query(class, OnlyItem(Iterate(%s, Filter(frame, [relations, %s, objects])))))" 
                        % (a[2]['tree'], a[3]['tree'], a[1]['tree'], a[0]['tree'])
        },

        'actWhatAfterAll': {
            'id': 'actWhatAfterAll',
            'attributes': {
                'type': 'actWhatAfterAll',
                'structural': 'query',
                'semantic': 'action',
                'ans_type': 'open',
                'video_id': v_id,
            },
            'global': 'what',
            'local': lambda o, a: timeDirect(a[0]),
            'questions': [
                lambda a: "What did the person do%s?" % a[0]['phrase'],
                lambda a: "What did they do%s?" % a[0]['phrase'],
                lambda a: "What was the person doing%s?" % a[0]['phrase'],
                lambda a: "What were they doing%s?" % a[0]['phrase'],
                lambda a: "What is the thing they did%s?" % a[0]['phrase'],
                lambda a: "%s, what did the person do?" % a[0]['start_phrase'],
                lambda a: "%s, what did they do?" % a[0]['start_phrase'],
                lambda a: "%s, what was the person doing?" % a[0]['start_phrase'],
                lambda a: "%s, what were they doing?" % a[0]['start_phrase'],
                lambda a: "%s, what is the thing they did?" % a[0]['start_phrase'],
            ],
            'starts': [
                [22], [16], [25], [20], [26], [0], [0], [0], [0], [0], 
            ],
            'order': [
                [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]
            ],
            'phrases': [
                lambda a: [a[0]['phrase']],
                lambda a: [a[0]['phrase']],
                lambda a: [a[0]['phrase']],
                lambda a: [a[0]['phrase']],
                lambda a: [a[0]['phrase']],
                lambda a: [a[0]['start_phrase']],
                lambda a: [a[0]['start_phrase']],
                lambda a: [a[0]['start_phrase']],
                lambda a: [a[0]['start_phrase']],
                lambda a: [a[0]['start_phrase']],
            ],
            'args': [[1, ['time'], ['after', 'all']]],
            'direct': lambda a: "",
            'time': lambda a: (a[0]['type'], timeDirect(a[0])),
            'program': lambda a: solve.actAfterAllFLA(stsg, a),
            'steps': 1,
            'quals': [
                lambda o, a: len(o) == 1,
                lambda o, a: noActOverlapWithTime(o[0], a[0])
            ],
            'package_ans': lambda o: ENG[o[0]],
            'metrics': lambda o, a: metrics(a, [], [], [], [], [[], []]),
            'str_program': lambda a: "Query(class, OnlyItem(Iterate(%s, Filter(frame, [actions]))))" 
                        % (a[0]['tree'])
        },

        'actWhatBefore': {
            'id': 'actWhatBefore',
            'attributes': {
                'type': 'actWhatBefore',
                'structural': 'query',
                'semantic': 'action',
                'ans_type': 'open',
                'video_id': v_id,
            },
            'global': 'what',
            'local': lambda o, a: timeDirect(a[0]),
            'questions': [
                lambda a: "What did the person do%s?" % a[0]['phrase'],
                lambda a: "What did they do%s?" % a[0]['phrase'],
                lambda a: "What was the person doing%s?" % a[0]['phrase'],
                lambda a: "What were they doing%s?" % a[0]['phrase'],
                lambda a: "What is the thing they did%s?" % a[0]['phrase'],
                lambda a: "%s, what did the person do?" % a[0]['start_phrase'],
                lambda a: "%s, what did they do?" % a[0]['start_phrase'],
                lambda a: "%s, what was the person doing?" % a[0]['start_phrase'],
                lambda a: "%s, what were they doing?" % a[0]['start_phrase'],
                lambda a: "%s, what is the thing they did?" % a[0]['start_phrase'],
            ],
            'starts': [
                [22], [16], [25], [20], [26], [0], [0], [0], [0], [0], 
            ],
            'order': [
                [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]
            ],
            'phrases': [
                lambda a: [a[0]['phrase']],
                lambda a: [a[0]['phrase']],
                lambda a: [a[0]['phrase']],
                lambda a: [a[0]['phrase']],
                lambda a: [a[0]['phrase']],
                lambda a: [a[0]['start_phrase']],
                lambda a: [a[0]['start_phrase']],
                lambda a: [a[0]['start_phrase']],
                lambda a: [a[0]['start_phrase']],
                lambda a: [a[0]['start_phrase']],
            ],
            'args': [[1, ['time'], ['before']]],
            'direct': lambda a: "",
            'time': lambda a: (a[0]['type'], timeDirect(a[0])),
            'program': lambda a: solve.actBeforeFLA(stsg, a),
            'steps': 1,
            'quals': [
                lambda o, a: len(o) == 1,
                lambda o, a: noActOverlapWithTime(o[0], a[0])
            ],
            'package_ans': lambda o: ENG[o[0]],
            'metrics': lambda o, a: metrics(a, [], [], [], [], [[], []]),
            'str_program': lambda a: "Query(class, OnlyItem(Iterate(%s, Filter(frame, [actions]))))" 
                        % (a[0]['tree'])
        },


        #########
        # FIRST #
        #########

        'objFirst': {
            'id': 'objFirst',
            'attributes': {
                'type': 'objFirst',
                'structural': 'query',
                'semantic': 'object',
                'ans_type': 'open',
                'video_id': v_id,
            },
            'global': 'first',
            'local': lambda o, a: a[0]['direct'],
            'questions': [
                lambda a: "Which object were they %s first%s?" %
                          (pp(a[0]), a[1]['phrase']),
                lambda a: "What was the person %s first%s?" %
                          (pp(a[0]), a[1]['phrase']),
                lambda a: "Which object did the person %s first%s?" %
                          (pres(a[0]), a[1]['phrase']),
                lambda a: "What did they %s first%s?" %
                          (pres(a[0]), a[1]['phrase']),
                lambda a: "%s, which object were they %s first?" %
                          (a[1]['start_phrase'], pp(a[0])),
                lambda a: "%s, what was the person %s first?" %
                          (a[1]['start_phrase'], pp(a[0])),
                lambda a: "%s, which object did the person %s first?" %
                          (a[1]['start_phrase'], pres(a[0])),
                lambda a: "%s, what did they %s first?" %
                          (a[1]['start_phrase'], pres(a[0])),
            ],
            'starts': [
                [23, 29],
                [20, 26],
                [28, 34],
                [14, 20],
                [25, 0],
                [22, 0],
                [30, 0],
                [16, 0],
            ],
            'order': [
                [0, 1], [0, 1], [0, 1], [0, 1],
                [1, 0], [1, 0], [1, 0], [1, 0]
            ],
            'phrases': [
                lambda a: [pp(a[0]), a[1]['phrase']],
                lambda a: [pp(a[0]), a[1]['phrase']],
                lambda a: [pres(a[0]), a[1]['phrase']],
                lambda a: [pres(a[0]), a[1]['phrase']],
                lambda a: [pp(a[0]), a[1]['start_phrase']],
                lambda a: [pp(a[0]), a[1]['start_phrase']],
                lambda a: [pres(a[0]), a[1]['start_phrase']],
                lambda a: [pres(a[0]), a[1]['start_phrase']],
            ],
            'args': [[1, crel + arel + srel + vrel, ALL_REL_INDIRECT],
                     [1, ['time'], ['after', 'all', 'while', 'between']]],
            'direct': lambda a: "%s" % (a[0]['direct']),
            'time': lambda a: (a[1]['type'], timeDirect(a[1])),
            'program': lambda a: solve.objFirst(stsg, a),
            'steps': 2,
            'quals': [
                lambda o, a: o is not None,
                lambda o, a: len(o) == 1,
                lambda o, a: a[0]['direct'] not in [IDX[
                    'not_contacting'], IDX['not_looking_at']],
                lambda o, a: notInAction(o[0], a[1]),
                lambda o, a: notInAction(a[0], a[1]),
                lambda o, a: isValidIndirect(a[0], o[0]),
                lambda o, a: len(solve.objFLAQual(stsg, a)) > 1,
                lambda o, a: isValidObjRel(o[0], a[0]),
            ],
            'package_ans': lambda o: ENG[o[0]],
            'metrics': lambda o, a: metrics(a, [], [a[0]], [], [], [[o[0][0]], [a[0]]]),
            'str_program': lambda a: "Query(class, OnlyItem(IterateUntil(forward, %s, Exists(%s, Filter(frame, [relations])), Filter(frame, [relations, %s, objects]))))"
                        % (a[1]['tree'], a[0]['tree'], a[0]['tree'])
        },

        'objFirstChoose': {
            'id': 'objFirstChoose',
            'attributes': {
                'type': 'objFirstChoose',
                'structural': 'choose',
                'semantic': 'object',
                'ans_type': 'binary',
                'video_id': v_id,
            },
            'global': 'first',
            'local': lambda o, a: "%s-%s-%s" % (a[0]['direct'],
                                                a[2]['direct'],
                                                a[3]['direct']),
            'questions': [
                lambda a: "Which were they %s first%s, %s or %s?" %
                          (pp(a[0]), a[1]['phrase'],
                           art(a[2]), art(a[3])),
                lambda a: "Which did they %s first%s, %s or %s?" %
                          (pres(a[0]), a[1]['phrase'],
                           art(a[2]), art(a[3])),
                lambda a: "Was %s or %s the first thing they %s%s?" %
                          (art(a[2]), art(a[3]), past(a[0]), a[1]['phrase']),
                lambda a: "Were they %s %s or %s first%s?" %
                          (pp(a[0]), art(a[2]), art(a[3]), a[1]['phrase']),
                lambda a: "Of all the items they %s%s, was the first one %s or %s?" %
                          (past(a[0]), a[1]['phrase'], art(a[2]), art(a[3])),
                lambda a: "%s, which was the person %s first, %s or %s?" %
                          (a[1]['start_phrase'], pp(a[0]),
                           art(a[2]), art(a[3])),
                lambda a: "%s, which did they %s first, %s or %s?" %
                          (a[1]['start_phrase'], pres(a[0]),
                           art(a[2]), art(a[3])),
                lambda a: "%s, was %s or %s the first thing they %s?" %
                          (a[1]['start_phrase'], art(a[2]),
                           art(a[3]), past(a[0])),
                lambda a: "%s, did they %s %s or %s first?" %
                          (a[1]['start_phrase'], pres(a[0]),
                           art(a[2]), art(a[3])),
                lambda a: "%s, of all the items they %s, was the first one %s or %s?" %
                          (a[1]['start_phrase'], past(a[0]),
                           art(a[2]), art(a[3])),
            ],
            'starts': [
                [16, 22, 24, 28],
                [15, 21, 23, 27],
                [30, 30, 4, 8],
                [10, 21, 11, 15],
                [22, 22, 42, 46],
                [23, 0, 31, 35],
                [17, 0, 25, 29],
                [32, 0, 6, 10],
                [11, 0, 12, 16],
                [24, 0, 44, 48],
            ],
            'order': [
                [0, 1, 2, 3],
                [0, 1, 2, 3],
                [2, 3, 0, 1],
                [0, 2, 3, 1],
                [0, 1, 2, 3],
                [1, 0, 2, 3],
                [1, 0, 2, 3],
                [1, 2, 3, 0],
                [1, 0, 2, 3],
                [1, 0, 2, 3],
            ],
            'phrases': [
                lambda a: [pp(a[0]), a[1]['phrase'], art(a[2]), art(a[3])],
                lambda a: [pres(a[0]), a[1]['phrase'], art(a[2]), art(a[3])],
                lambda a: [past(a[0]), a[1]['phrase'], art(a[2]), art(a[3])],
                lambda a: [pp(a[0]), a[1]['phrase'], art(a[2]), art(a[3])],
                lambda a: [past(a[0]), a[1]['phrase'], art(a[2]), art(a[3])],
                lambda a: [pp(a[0]), a[1]['start_phrase'], art(a[2]), art(a[3])],
                lambda a: [pres(a[0]), a[1]['start_phrase'], art(a[2]), art(a[3])],
                lambda a: [past(a[0]), a[1]['start_phrase'], art(a[2]), art(a[3])],
                lambda a: [pres(a[0]), a[1]['start_phrase'], art(a[2]), art(a[3])],
                lambda a: [past(a[0]), a[1]['start_phrase'], art(a[2]), art(a[3])],
            ],
            'args': [[1, crel + arel + srel + vrel, ALL_REL_INDIRECT],
                     [1, ['time'], ['after', 'all', 'while', 'between']],
                     [2, obj, ['direct', 'last']]],
            'direct': lambda a: "%s-%s-%s" % (a[0]['direct'],
                                              a[2]['direct'],
                                              a[3]['direct']),
            'time': lambda a: (a[1]['type'], timeDirect(a[1])),
            'program': lambda a: solve.objFirstChoose(stsg, a),
            'steps': 3,
            'quals': [
                lambda o, a: o is not None,
                lambda o, a: a[0]['direct'] not in [IDX[
                    'not_contacting'], IDX['not_looking_at']],
                lambda o, a: isValidObjRel(a[2], a[0]),
                lambda o, a: isValidObjRel(a[3], a[0]),
                lambda o, a: isValidObjCombo(a[2], a[3]),
                lambda o, a: notInAction(a[0], a[1]),
                lambda o, a: notInAction(a[2], a[1]),
                lambda o, a: notInAction(a[3], a[1]),
                lambda o, a: a[2]['direct'] in solve.objFLAQual(stsg, a) and a[3]['direct'] in solve.objFLAQual(stsg, a),
                lambda o, a: len(solve.objFirst(stsg, a)[0]) == 1,#solve.objFirst(stsg, a)[0] in [a[2]['direct'], a[3]['direct']],

                # I made it such that it's [0]
                lambda o, a: solve.objFirst(stsg, a)[0][0] in [a[2]['direct'], a[3]['direct']],
            ],
            'package_ans': lambda o: ENG[o],
            'metrics': lambda o, a: metrics(a, [], [a[0]], [], [], [[a[2], a[3]], [a[0]]]),
            'str_program': lambda a: "Choose(%s, %s, IterateUntil(forward, %s, XOR(Exists(%s, Filter(frame, [relations, %s, objects])), Exists(%s, Filter(frame, [relations, %s, objects]))), Filter(frame, [relations, %s, objects])))"
                        % (a[2]['tree'], a[3]['tree'], a[1]['tree'], a[2]['tree'], a[0]['tree'], a[3]['tree'], a[0]['tree'], a[0]['tree'])
        },

        'objFirstVerify': {
            'id': 'objFirstVerify',
            'attributes': {
                'type': 'objFirstVerify',
                'structural': 'verify',
                'semantic': 'object',
                'ans_type': 'binary',
                'video_id': v_id,
            },
            'global': 'first',
            'local': lambda o, a: "%s-%s" % (a[0]['direct'], a[2]['direct']),
            'questions': [
                lambda a: "Was %s the first thing they were %s%s?" %
                          (art(a[2]), pp(a[0]), a[1]['phrase']),
                lambda a: "Did they %s %s first%s?" %
                          (pres(a[0]), art(a[2]), a[1]['phrase']),
                lambda a: "Of everything they %s%s, was the first %s?" %
                          (past(a[0]), a[1]['phrase'], art(a[2])),
                lambda a: "Of all the things the person was %s%s, was the first %s?" %
                          (pp(a[0]), a[1]['phrase'], art(a[2])),
                lambda a: "%s, was %s the first thing they %s?" %
                          (a[1]['start_phrase'], art(a[2]), past(a[0])),
                lambda a: "%s, were they %s %s first?" %
                          (a[1]['start_phrase'], pp(a[0]), art(a[2])),
                lambda a: "%s, of everything the person %s, was the first %s?" %
                          (a[1]['start_phrase'], past(a[0]), art(a[2])),
                lambda a: "%s, of all the things the person was %s, was the first %s?" %
                          (a[1]['start_phrase'], pp(a[0]), art(a[2])),
            ],
            'starts': [
                [31, 31, 4],
                [9, 16, 10],
                [19, 19, 35],
                [33, 33, 49],
                [28, 0, 6],
                [12, 0, 13],
                [27, 0, 43],
                [35, 0, 51],
            ],
            'order': [
                [2, 0, 1],
                [0, 2, 1],
                [0, 1, 2],
                [0, 1, 2],
                [1, 2, 0],
                [1, 0, 2],
                [1, 0, 2],
                [1, 0, 2],
            ],
            'phrases': [
                lambda a: [pp(a[0]), a[1]['phrase'], art(a[2])],
                lambda a: [pres(a[0]), a[1]['phrase'], art(a[2])],
                lambda a: [past(a[0]), a[1]['phrase'], art(a[2])],
                lambda a: [pp(a[0]), a[1]['phrase'], art(a[2])],
                lambda a: [past(a[0]), a[1]['start_phrase'], art(a[2])],
                lambda a: [pp(a[0]), a[1]['start_phrase'], art(a[2])],
                lambda a: [past(a[0]), a[1]['start_phrase'], art(a[2])],
                lambda a: [pp(a[0]), a[1]['start_phrase'], art(a[2])],
            ],
            'args': [[1, crel + arel + srel + vrel, ALL_REL_INDIRECT],
                     [1, ['time'], ['after', 'all', 'while', 'between']],
                     [1, obj, ['direct', 'last']]],
            'direct': lambda a: "%s-%s" % (a[0]['direct'], a[2]['direct']),
            'time': lambda a: (a[1]['type'], timeDirect(a[1])),
            'program': lambda a: solve.objFirstVerify(stsg, a),
            'steps': 3,
            'quals': [
                lambda o, a: o is not None,
                lambda o, a: a[0]['direct'] not in [IDX[
                    'not_contacting'], IDX['not_looking_at']],
                lambda o, a: isValidObjRel(a[2], a[0]),
                lambda o, a: isValidRel(a[0]),
                lambda o, a: notInAction(a[0], a[1]),
                lambda o, a: notInAction(a[2], a[1]),
                lambda o, a: len(solve.objFLA(stsg, a)) > 1,
            ],
            'package_ans': lambda o: o,
            'metrics': lambda o, a: metrics(a, [], [a[0]], [], [], [[a[2]], [a[0]]]),
            'str_program': lambda a: "Equals(%s, OnlyItem(IterateUntil(forward, %s, Exists(%s, Filter(frame, [relations])), Filter(frame, [relations, %s, objects]))))"
                        % (a[2]['tree'], a[1]['tree'], a[0]['tree'], a[0]['tree'])
        },

        'actFirst': {
            'id': 'actFirst',
            'attributes': {
                'type': 'actFirst',
                'structural': 'query',
                'semantic': 'action',
                'ans_type': 'open',
                'video_id': v_id,
            },
            'global': 'first',
            'local': lambda o, a: timeDirect(a[0]),
            'questions': [
                lambda a: "What did the person start doing first%s?" %
                          (a[0]['phrase']),
                lambda a: "What did they start to do first%s?" %
                          (a[0]['phrase']),
                lambda a: "What was the person starting to do first%s?" %
                          (a[0]['phrase']),
                lambda a: "What did they start doing first%s?" %
                          (a[0]['phrase']),
                lambda a: "What is the first thing they started to do%s?" %
                          (a[0]['phrase']),
                lambda a: "%s, what did the person start to do first?" %
                          (a[0]['start_phrase']),
                lambda a: "%s, what did they start to do first?" %
                          (a[0]['start_phrase']),
                lambda a: "%s, what did the person start doing first?" %
                          (a[0]['start_phrase']),
                lambda a: "%s, what were they starting to do first?" %
                          (a[0]['start_phrase']),
                lambda a: "%s, what is the first thing they started?" %
                          (a[0]['start_phrase']),
            ],
            'starts': [
                [37], [31], [40], [31], [42], [0], [0], [0], [0], [0]
            ],
            'order': [
                [0], [0], [0], [0], [0], [0], [0], [0], [0], [0],
            ],
            'phrases': [
                lambda a: [a[0]['phrase']],
                lambda a: [a[0]['phrase']],
                lambda a: [a[0]['phrase']],
                lambda a: [a[0]['phrase']],
                lambda a: [a[0]['phrase']],
                lambda a: [a[0]['start_phrase']],
                lambda a: [a[0]['start_phrase']],
                lambda a: [a[0]['start_phrase']],
                lambda a: [a[0]['start_phrase']],
                lambda a: [a[0]['start_phrase']],
            ],
            'args': [[1, ['time'], ['after', 'all']]],
            'direct': lambda a: "",
            'time': lambda a: (a[0]['type'], timeDirect(a[0])),
            'program': lambda a: solve.actFirst(stsg, a),
            'steps': 1,
            'quals': [
                lambda o, a: len(o) == 1,
                lambda o, a: len(solve.actAfterAllFLAQual(stsg, a)) > 1,
                lambda o, a: o[0] != a[0]['direct'],
                lambda o, a: ACTION_SV[o[0]][1] != IDX['taking'],
            ],
            'package_ans': lambda o: ENG[o[0]],
            'metrics': lambda o, a: metrics(a, [], [], [], [], [[], []]),
            'str_program': lambda a: "Query(class, OnlyItem(IterateUntil(forward, %s, HasItem(Filter(frame, [actions])), Filter(frame, [actions]))))"
                        % (a[0]['tree'])
        },

        #########
        # LAST  #
        #########

        'objLast': {
            'id': 'objLast',
            'attributes': {
                'type': 'objLast',
                'structural': 'query',
                'semantic': 'object',
                'ans_type': 'open',
                'video_id': v_id,
            },
            'global': 'last',
            'local': lambda o, a: a[0]['direct'],
            'questions': [
                lambda a: "Which object were they %s last%s?" %
                          (pp(a[0]), a[1]['phrase']),
                lambda a: "What was the person %s last%s?" %
                          (pp(a[0]), a[1]['phrase']),
                lambda a: "Which object did the person %s last%s?" %
                          (pres(a[0]), a[1]['phrase']),
                lambda a: "What did they %s last%s?" %
                          (pres(a[0]), a[1]['phrase']),
                lambda a: "%s, which object were they %s last?" %
                          (a[1]['start_phrase'], pp(a[0])),
                lambda a: "%s, what was the person %s last?" %
                          (a[1]['start_phrase'], pp(a[0])),
                lambda a: "%s, which object did the person %s last?" %
                          (a[1]['start_phrase'], pres(a[0])),
                lambda a: "%s, what did they %s last?" %
                          (a[1]['start_phrase'], pres(a[0])),
            ],
            'starts': [
                [23, 28],
                [20, 25],
                [28, 33],
                [14, 19],
                [25, 0],
                [22, 0],
                [30, 0],
                [16, 0],
            ],
            'order': [
                [0, 1], [0, 1], [0, 1], [0, 1],
                [1, 0], [1, 0], [1, 0], [1, 0]
            ],
            'phrases': [
                lambda a: [pp(a[0]), a[1]['phrase']],
                lambda a: [pp(a[0]), a[1]['phrase']],
                lambda a: [pres(a[0]), a[1]['phrase']],
                lambda a: [pres(a[0]), a[1]['phrase']],
                lambda a: [pp(a[0]), a[1]['start_phrase']],
                lambda a: [pp(a[0]), a[1]['start_phrase']],
                lambda a: [pres(a[0]), a[1]['start_phrase']],
                lambda a: [pres(a[0]), a[1]['start_phrase']],
            ],
            'args': [[1, crel + arel + srel + vrel, ALL_REL_INDIRECT],
                     [1, ['time'], ['before', 'all', 'while', 'between']]],
            'direct': lambda a: "%s" % (a[0]['direct']),
            'time': lambda a: (a[1]['type'], timeDirect(a[1])),
            'program': lambda a: solve.objLast(stsg, a),
            'steps': 2,
            'quals': [
                lambda o, a: o is not None,
                lambda o, a: len(o) == 1,
                lambda o, a: a[0]['direct'] not in [IDX[
                    'not_contacting'], IDX['not_looking_at']],
                lambda o, a: notInAction(o[0], a[1]),
                lambda o, a: notInAction(a[0], a[1]),
                lambda o, a: isValidIndirect(a[0], o[0]),
                lambda o, a: len(solve.objFLAQual(stsg, a)) > 1,
                lambda o, a: isValidObjRel(o[0], a[0]),
            ],
            'package_ans': lambda o: ENG[o[0]],
            'metrics': lambda o, a: metrics(a, [], [], [], [], [[o[0][0]], [a[0]]]),
            'str_program': lambda a: "Query(class, OnlyItem(IterateUntil(backward, %s, Exists(%s, Filter(frame, [relations])), Filter(frame, [relations, %s, objects]))))"
                        % (a[1]['tree'], a[0]['tree'], a[0]['tree'])
        },

        'objLastChoose': {
            'id': 'objLastChoose',
            'attributes': {
                'type': 'objLastChoose',
                'structural': 'choose',
                'semantic': 'object',
                'ans_type': 'binary',
                'video_id': v_id,
            },
            'global': 'last',
            'local': lambda o, a: "%s-%s-%s" % (a[0]['direct'],
                                                a[2]['direct'],
                                                a[3]['direct']),
            'questions': [
                lambda a: "Which were they %s last%s, %s or %s?" %
                          (pp(a[0]), a[1]['phrase'],
                           art(a[2]), art(a[3])),
                lambda a: "Which did they %s last%s, %s or %s?" %
                          (pres(a[0]), a[1]['phrase'],
                           art(a[2]), art(a[3])),
                lambda a: "Was %s or %s the last thing they %s%s?" %
                          (art(a[2]), art(a[3]), past(a[0]), a[1]['phrase']),
                lambda a: "Were they %s %s or %s last%s?" %
                          (pp(a[0]), art(a[2]), art(a[3]), a[1]['phrase']),
                lambda a: "Of all the items they %s%s, was the last one %s or %s?" %
                          (past(a[0]), a[1]['phrase'], art(a[2]), art(a[3])),
                lambda a: "%s, which was the person %s last, %s or %s?" %
                          (a[1]['start_phrase'], pp(a[0]),
                           art(a[2]), art(a[3])),
                lambda a: "%s, which did they %s last, %s or %s?" %
                          (a[1]['start_phrase'], pres(a[0]),
                           art(a[2]), art(a[3])),
                lambda a: "%s, was %s or %s the last thing they %s?" %
                          (a[1]['start_phrase'], art(a[2]), art(a[3]), past(a[0])),
                lambda a: "%s, did they %s %s or %s last?" %
                          (a[1]['start_phrase'], pres(a[0]), art(a[2]), art(a[3])),
                lambda a: "%s, of all the items they %s, was the last one %s or %s?" %
                          (a[1]['start_phrase'], past(a[0]), art(a[2]), art(a[3])),
            ],
            'starts': [
                [16, 21, 23, 27],
                [15, 20, 22, 26],
                [29, 29, 4, 8],
                [10, 20, 11, 15],
                [22, 22, 41, 45],
                [23, 0, 30, 34],
                [17, 0, 24, 28],
                [31, 0, 6, 10],
                [11, 0, 12, 16],
                [24, 0, 43, 47],
            ],
            'order': [
                [0, 1, 2, 3],
                [0, 1, 2, 3],
                [2, 3, 0, 1],
                [0, 2, 3, 1],
                [0, 1, 2, 3],
                [1, 0, 2, 3],
                [1, 0, 2, 3],
                [1, 2, 3, 0],
                [1, 0, 2, 3],
                [1, 0, 2, 3],
            ],
            'phrases': [
                lambda a: [pp(a[0]), a[1]['phrase'], art(a[2]), art(a[3])],
                lambda a: [pres(a[0]), a[1]['phrase'], art(a[2]), art(a[3])],
                lambda a: [past(a[0]), a[1]['phrase'], art(a[2]), art(a[3])],
                lambda a: [pp(a[0]), a[1]['phrase'], art(a[2]), art(a[3])],
                lambda a: [past(a[0]), a[1]['phrase'], art(a[2]), art(a[3])],
                lambda a: [pp(a[0]), a[1]['start_phrase'],
                           art(a[2]), art(a[3])],
                lambda a: [pres(a[0]), a[1]['start_phrase'],
                           art(a[2]), art(a[3])],
                lambda a: [past(a[0]), a[1]['start_phrase'],
                           art(a[2]), art(a[3])],
                lambda a: [pres(a[0]), a[1]['start_phrase'],
                           art(a[2]), art(a[3])],
                lambda a: [past(a[0]), a[1]['start_phrase'],
                           art(a[2]), art(a[3])],
            ],
            'args': [[1, crel + arel + srel + vrel, ALL_REL_INDIRECT],
                     [1, ['time'], ['before', 'all', 'while', 'between']],
                     [2, obj, ['direct', 'first']]],
            'direct': lambda a: "%s-%s-%s" % (a[0]['direct'],
                                              a[2]['direct'],
                                              a[3]['direct']),
            'time': lambda a: (a[1]['type'], timeDirect(a[1])),
            'program': lambda a: solve.objLastChoose(stsg, a),
            'steps': 3,
            'quals': [
                lambda o, a: o is not None,
                lambda o, a: a[0]['direct'] not in [IDX[
                    'not_contacting'], IDX['not_looking_at']],
                lambda o, a: isValidObjRel(a[2], a[0]),
                lambda o, a: isValidObjRel(a[3], a[0]),
                lambda o, a: isValidObjCombo(a[2], a[3]),
                lambda o, a: notInAction(a[0], a[1]),
                lambda o, a: notInAction(a[2], a[1]),
                lambda o, a: notInAction(a[3], a[1]),
                lambda o, a: a[2]['direct'] in solve.objFLAQual(stsg, a) and a[3]['direct'] in solve.objFLAQual(stsg, a),
                #lambda o, a: solve.objLast(stsg, a) in [a[2]['direct'], a[3]['direct']],

                lambda o, a: len(solve.objLast(stsg, a)[0]) == 1,#solve.objFirst(stsg, a)[0] in [a[2]['direct'], a[3]['direct']],

                # I made it such that it's [0]
                lambda o, a: solve.objLast(stsg, a)[0][0] in [a[2]['direct'], a[3]['direct']],
            ],
            'package_ans': lambda o: ENG[o],
            'metrics': lambda o, a: metrics(a, [], [], [], [], [[a[2], a[3]],[a[0]]]),
            'str_program': lambda a: "Choose(%s, %s, IterateUntil(backward, %s, XOR(Exists(%s, Filter(frame, [relations, %s, objects])), Exists(%s, Filter(frame, [relations, %s, objects]))), Filter(frame, [relations, %s, objects])))"
                        % (a[2]['tree'], a[3]['tree'], a[1]['tree'], a[2]['tree'], a[0]['tree'], a[3]['tree'], a[0]['tree'], a[0]['tree'])
        },

        'objLastVerify': {
            'id': 'objLastVerify',
            'attributes': {
                'type': 'objLastVerify',
                'structural': 'verify',
                'semantic': 'object',
                'ans_type': 'binary',
                'video_id': v_id,
            },
            'global': 'last',
            'local': lambda o, a: "%s-%s" % (a[0]['direct'], a[2]['direct']),
            'questions': [
                lambda a: "Was %s the last thing they were %s%s?" %
                          (art(a[2]), pp(a[0]), a[1]['phrase']),
                lambda a: "Did they %s %s last%s?" %
                          (pres(a[0]), art(a[2]), a[1]['phrase']),
                lambda a: "Of everything they %s%s, was the last %s?" %
                          (past(a[0]), a[1]['phrase'], art(a[2])),
                lambda a: "Of all the things the person was %s%s, was the last %s?" %
                          (pp(a[0]), a[1]['phrase'], art(a[2])),
                lambda a: "%s, was %s the last thing they %s?" %
                          (a[1]['start_phrase'], art(a[2]), past(a[0])),
                lambda a: "%s, were they %s %s last?" %
                          (a[1]['start_phrase'], pp(a[0]), art(a[2])),
                lambda a: "%s, of everything the person %s, was the last %s?" %
                          (a[1]['start_phrase'], past(a[0]), art(a[2])),
                lambda a: "%s, of all the things the person was %s, was the last %s?" %
                          (a[1]['start_phrase'], pp(a[0]), art(a[2])),
            ],
            'starts': [
                [30, 30, 4],
                [9, 15, 10],
                [19, 19, 34],
                [33, 33, 48],
                [27, 0, 6],
                [12, 0, 13],
                [27, 0, 42],
                [35, 0, 50],
            ],
            'order': [
                [2, 0, 1],
                [0, 2, 1],
                [0, 1, 2],
                [0, 1, 2],
                [1, 2, 0],
                [1, 0, 2],
                [1, 0, 2],
                [1, 0, 2],
            ],
            'phrases': [
                lambda a: [pp(a[0]), a[1]['phrase'], art(a[2])],
                lambda a: [pres(a[0]), a[1]['phrase'], art(a[2])],
                lambda a: [past(a[0]), a[1]['phrase'], art(a[2])],
                lambda a: [pp(a[0]), a[1]['phrase'], art(a[2])],
                lambda a: [past(a[0]), a[1]['start_phrase'], art(a[2])],
                lambda a: [pp(a[0]), a[1]['start_phrase'], art(a[2])],
                lambda a: [past(a[0]), a[1]['start_phrase'], art(a[2])],
                lambda a: [pp(a[0]), a[1]['start_phrase'], art(a[2])],
            ],
            'args': [[1, crel + arel + srel + vrel, ALL_REL_INDIRECT],
                     [1, ['time'], ['before', 'all', 'while', 'between']],
                     [1, obj, ['direct', 'first']]],
            'direct': lambda a: "%s-%s" % (a[0]['direct'], a[2]['direct']),
            'time': lambda a: (a[1]['type'], timeDirect(a[1])),
            'program': lambda a: solve.objLastVerify(stsg, a),
            'steps': 3,
            'quals': [
                lambda o, a: o is not None,
                lambda o, a: a[0]['direct'] not in [IDX[
                    'not_contacting'], IDX['not_looking_at']],
                lambda o, a: isValidObjRel(a[2], a[0]),
                lambda o, a: isValidRel(a[0]),
                lambda o, a: notInAction(a[0], a[1]),
                lambda o, a: notInAction(a[2], a[1]),
                lambda o, a: len(solve.objFLA(stsg, a)) > 1,
            ],
            'package_ans': lambda o: o,
            'metrics': lambda o, a: metrics(a, [], [], [], [], [[a[2]], [a[0]]]),
            'str_program': lambda a: "Equals(%s, OnlyItem(IterateUntil(backward, %s, Exists(%s, Filter(frame, [relations])), Filter(frame, [relations, %s, objects]))))"
                        % (a[2]['tree'], a[1]['tree'], a[0]['tree'], a[0]['tree'])
        },     

        'actLast': {
            'id': 'actLast',
            'attributes': {
                'type': 'actLast',
                'structural': 'query',
                'semantic': 'action',
                'ans_type': 'open',
                'video_id': v_id,
            },
            'global': 'last',
            'local': lambda o, a: "action",
            'questions': [
                lambda a: "What did the person do last%s?" % a[0]['phrase'],
                lambda a: "What did they do last%s?" % a[0]['phrase'],
                lambda a: "What was the person doing last%s?" % a[0]['phrase'],
                lambda a: "What were they doing last%s?" % a[0]['phrase'],
                lambda a: "What is the last thing they did%s?" % a[0]['phrase'],
                lambda a: "%s, what did the person do last?" % a[0]['start_phrase'],
                lambda a: "%s, what did they do last?" % a[0]['start_phrase'],
                lambda a: "%s, what was the person doing last?" % a[0]['start_phrase'],
                lambda a: "%s, what were they doing last?" % a[0]['start_phrase'],
                lambda a: "%s, what is the last thing they did?" % a[0]['start_phrase'],
            ],
            'starts': [
                [27], [21], [30], [25], [31], [0], [0], [0], [0], [0]
            ],
            'order': [
                [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], 
            ],
            'phrases': [
                lambda a: [a[0]['phrase']],
                lambda a: [a[0]['phrase']],
                lambda a: [a[0]['phrase']],
                lambda a: [a[0]['phrase']],
                lambda a: [a[0]['phrase']],
                lambda a: [a[0]['start_phrase']],
                lambda a: [a[0]['start_phrase']],
                lambda a: [a[0]['start_phrase']],
                lambda a: [a[0]['start_phrase']],
                lambda a: [a[0]['start_phrase']],
            ],
            'args': [[1, ['time'], ['before', 'all']]],
            'direct': lambda a: "",
            'time': lambda a: (a[0]['type'], timeDirect(a[0])),
            'program': lambda a: solve.actLast(stsg, a),
            'steps': 1,
            'quals': [
                lambda o, a: len(o) == 1,
                lambda o, a: len(solve.actBeforeFLAQual(stsg, a)) > 1,
                lambda o, a: o[0] != a[0]['direct'],
                lambda o, a: ACTION_SV[o[0]][1] != IDX['putting'],
            ],
            'package_ans': lambda o: ENG[o[0]],
            'metrics': lambda o, a: metrics(a, [], [], [], [], [[], []]),
            'str_program': lambda a: "Query(class, OnlyItem(IterateUntil(backward, %s, HasItem(Filter(frame, [actions])), Filter(frame, [actions]))))"
                        % (a[0]['tree'])
        },


        ##########
        # Length #
        ##########
        'actLengthLongerChoose': {
            'id': 'actLengthLongerChoose',
            'attributes': {
                'type': 'actLengthLongerChoose',
                'structural': 'compare',
                'semantic': 'action',
                'ans_type': 'binary',
                'video_id': v_id,
            },
            'global': 'length',
            'local': lambda o, a: "longer-%s-%s" % (a[0]['direct'],
                                                    a[1]['direct']),
            'questions': [
                lambda a: "Was the person %s or %s for longer?" %
                          (pp(a[0]), pp(a[1])),
                lambda a: "Did they %s or %s for longer?" %
                          (pres(a[0]), pres(a[1])),
                lambda a: "Was the person %s or %s for a longer amount of time?" %
                          (pp(a[0]), pp(a[1])),
                lambda a: "Did they %s or %s for a longer amount of time?" %
                          (pres(a[0]), pres(a[1])),
                lambda a: "Do they take a longer amount of time %s or %s?" %
                          (pp(a[0]), pp(a[1])),
                lambda a: "Is %s or %s the activity that takes longer?" %
                          (pp(a[0]), pp(a[1])),
                lambda a: "Was the person %s or %s for more time?" %
                          (pp(a[0]), pp(a[1])),
                lambda a: "Did they %s or %s for more time?" %
                          (pres(a[0]), pres(a[1])),
                lambda a: "Was the person %s or %s for a larger amount of time?" %
                          (pp(a[0]), pp(a[1])),
                lambda a: "Did they %s or %s for a larger amount of time?" %
                          (pres(a[0]), pres(a[1])),
                lambda a: "Do they spend more time %s or %s?" %
                          (pp(a[0]), pp(a[1])),
                lambda a: "Is %s or %s the activity that takes more time?" %
                          (pp(a[0]), pp(a[1])),
                lambda a: "Which did they do for longer, %s or %s?" %
                          (pp(a[0]), pp(a[1])),
            ],
            'starts': [
                [15, 19],
                [9, 13],
                [15, 19],
                [9, 13],
                [37, 41],
                [3, 7],
                [15, 19],
                [9, 13],
                [15, 19],
                [9, 13],
                [24, 28],
                [3, 7],
                [30, 34],
            ],
            'order': [
                [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1],
                [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1]
            ],
            'phrases': [
                lambda a: [pp(a[0]), pp(a[1])],
                lambda a: [pres(a[0]), pres(a[1])],
                lambda a: [pp(a[0]), pp(a[1])],

                lambda a: [pres(a[0]), pres(a[1])],
                lambda a: [pp(a[0]), pp(a[1])],
                lambda a: [pp(a[0]), pp(a[1])],

                lambda a: [pp(a[0]), pp(a[1])],
                lambda a: [pres(a[0]), pres(a[1])],
                lambda a: [pp(a[0]), pp(a[1])],

                lambda a: [pres(a[0]), pres(a[1])],
                lambda a: [pp(a[0]), pp(a[1])],
                lambda a: [pp(a[0]), pp(a[1])],
                lambda a: [pp(a[0]), pp(a[1])],
            ],
            'args': [[2, act, ['direct']]],
            'direct': lambda a: "longer-%s-%s" % (a[0]['direct'],
                                                  a[1]['direct']),
            'time': lambda a: ('all', ""),
            'program': lambda a: solve.actLengthLongerChoose(stsg, a),
            'steps': 5,
            'quals': [
                lambda o, a: o is not None,
                lambda o, a: a[0]['direct'] != a[1]['direct'],
                lambda o, a: occursNo('more', 1, a[0], stsg),
                lambda o, a: occursNo('more', 1, a[1], stsg),
                lambda o, a: not transition(a[0]),
                lambda o, a: not transition(a[1]),
            ],
            'package_ans': lambda o: ENG[o],
            'metrics': lambda o, a: metrics(a, [], [], a, [], [[], []]),
            'str_program': lambda a: "Superlative(max, [Filter(video, [actions, %s]), Filter(video, [actions, %s])], Subtract(Query(end, action), Query(start, action)))"
                                        % (a[0]['tree'], a[1]['tree'])
        },

        'actLengthShorterChoose': {
            'id': 'actLengthShorterChoose',
            'attributes': {
                'type': 'actLengthShorterChoose',
                'structural': 'compare',
                'semantic': 'action',
                'ans_type': 'binary',
                'video_id': v_id,
            },
            'global': 'length',
            'local': lambda o, a: "shorter-%s-%s" % (a[0]['direct'],
                                                     a[1]['direct']),
            'questions': [
                lambda a: "Was the person %s or %s for less time?" %
                          (pp(a[0]), pp(a[1])),
                lambda a: "Did they %s or %s for less time?" %
                          (pres(a[0]), pres(a[1])),
                lambda a: "Was the person %s or %s for a shorter amount of time?" %
                          (pp(a[0]), pp(a[1])),
                lambda a: "Did they %s or %s for a shorter amount of time?" %
                          (pres(a[0]), pres(a[1])),
                lambda a: "Do they take a shorter amount of time %s or %s?" %
                          (pp(a[0]), pp(a[1])),
                lambda a: "Is %s or %s the activity that they do for less time?" %
                          (pp(a[0]), pp(a[1])),
                lambda a: "Was the person %s or %s for less time?" %
                          (pp(a[0]), pp(a[1])),
                lambda a: "Did they %s or %s for less time?" %
                          (pres(a[0]), pres(a[1])),
                lambda a: "Was the person %s or %s for a shorter amount of time?" %
                          (pp(a[0]), pp(a[1])),
                lambda a: "Did they %s or %s for a shorter amount of time?" %
                          (pres(a[0]), pres(a[1])),
                lambda a: "Do they spend less time %s or %s?" %
                          (pp(a[0]), pp(a[1])),
                lambda a: "Is %s or %s the activity that takes less time?" %
                          (pp(a[0]), pp(a[1])),
                lambda a: "Which did they do for less time, %s or %s?" %
                          (pp(a[0]), pp(a[1])),
            ],
            'starts': [
                [15, 19],
                [9, 13],
                [15, 19],
                [9, 13],
                [38, 42],
                [3, 7],
                [15, 19],
                [9, 13],
                [15, 19],
                [9, 13],
                [24, 28],
                [3, 7],
                [33, 37],
            ],
            'order': [
                [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1],
                [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1],
            ],
            'phrases': [
                lambda a: [pp(a[0]), pp(a[1])],
                lambda a: [pres(a[0]), pres(a[1])],
                lambda a: [pp(a[0]), pp(a[1])],

                lambda a: [pres(a[0]), pres(a[1])],
                lambda a: [pp(a[0]), pp(a[1])],
                lambda a: [pp(a[0]), pp(a[1])],

                lambda a: [pp(a[0]), pp(a[1])],
                lambda a: [pres(a[0]), pres(a[1])],
                lambda a: [pp(a[0]), pp(a[1])],

                lambda a: [pres(a[0]), pres(a[1])],
                lambda a: [pp(a[0]), pp(a[1])],
                lambda a: [pp(a[0]), pp(a[1])],
                lambda a: [pp(a[0]), pp(a[1])],
            ],
            'args': [[2, act, ['direct']]],
            'direct': lambda a: "shorter-%s-%s" % (a[0]['direct'],
                                                   a[1]['direct']),
            'time': lambda a: ('all', ""),
            'program': lambda a: solve.actLengthShorterChoose(stsg, a),
            'steps': 5,
            'quals': [
                lambda o, a: o is not None,
                lambda o, a: a[0]['direct'] != a[1]['direct'],
                lambda o, a: occursNo('more', 1, a[0], stsg),
                lambda o, a: occursNo('more', 1, a[1], stsg),
                lambda o, a: not transition(a[0]),
                lambda o, a: not transition(a[1]),
            ],
            'package_ans': lambda o: ENG[o],
            'metrics': lambda o, a: metrics(a, [], [], [], [], [[], []]),
            'str_program': lambda a: "Superlative(min, [Filter(video, [actions, %s]), Filter(video, [actions, %s])], Subtract(Query(end, action), Query(start, action)))"
                                        % (a[0]['tree'], a[1]['tree'])
        },

        'actLengthLongerVerify': {
            'id': 'actLengthLongerVerify',
            'attributes': {
                'type': 'actLengthLongerVerify',
                'structural': 'compare',
                'semantic': 'action',
                'ans_type': 'binary',
                'video_id': v_id,
            },
            'global': 'length',
            'local': lambda o, a: "longer-%s-%s" % (a[0]['direct'],
                                                    a[1]['direct']),
            'questions': [
                lambda a: "Was the person %s for longer than they were %s?" %
                          (pp(a[0]), pp(a[1])),
                lambda a: "Did they %s for longer than they spent %s?" %
                          (pres(a[0]), pp(a[1])),
                lambda a: "Did the person spend a longer amount of time %s than %s?" %
                          (pp(a[0]), pp(a[1])),
                lambda a: "Was %s something they spent longer doing than %s?" %
                          (pp(a[0]), pp(a[1])),
                lambda a: "Compared to %s, did they %s for longer?" %
                          (pp(a[1]), pres(a[0])),
                lambda a: "Was the person %s for more time than they were %s?" %
                          (pp(a[0]), pp(a[1])),
                lambda a: "Did they %s for more time than they spent %s?" %
                          (pres(a[0]), pp(a[1])),
                lambda a: "Did the person spend more time %s than %s?" %
                          (pp(a[0]), pp(a[1])),
                lambda a: "Was %s something they spent more time doing than %s?" %
                          (pp(a[0]), pp(a[1])),
                lambda a: "Compared to %s, did the person %s for longer?" %
                          (pp(a[1]), pres(a[0])),
            ],
            'starts': [
                [15, 42],
                [9, 37],
                [45, 51],
                [4, 44],
                [23, 12],
                [15, 45],
                [9, 40],
                [31, 37],
                [4, 47],
                [29, 12],
            ],
            'order': [
                [0, 1], [0, 1], [0, 1], [0, 1], [1, 0],
                [0, 1], [0, 1], [0, 1], [0, 1], [1, 0],
            ],
            'phrases': [
                lambda a: [pp(a[0]), pp(a[1])],
                lambda a: [pres(a[0]), pp(a[1])],
                lambda a: [pp(a[0]), pp(a[1])],
                lambda a: [pp(a[0]), pp(a[1])],
                lambda a: [pres(a[0]), pp(a[1])],
                lambda a: [pp(a[0]), pp(a[1])],
                lambda a: [pres(a[0]), pp(a[1])],
                lambda a: [pp(a[0]), pp(a[1])],
                lambda a: [pp(a[0]), pp(a[1])],
                lambda a: [pres(a[0]), pp(a[1])],
            ],
            'args': [[2, act, ['direct']]],
            'direct': lambda a: "longer-%s-%s" % (a[0]['direct'],
                                                  a[1]['direct']),
            'time': lambda a: ('all', ""),
            'program': lambda a: solve.actLengthLongerVerify(stsg, a),
            'steps': 5,
            'quals': [
                lambda o, a: o is not None,
                lambda o, a: a[0]['direct'] != a[1]['direct'],
                lambda o, a: occursNo('more', 1, a[0], stsg),
                lambda o, a: occursNo('more', 1, a[1], stsg),
                lambda o, a: not transition(a[0]),
                lambda o, a: not transition(a[1]),
            ],
            'package_ans': lambda o: o,
            'metrics': lambda o, a: metrics(a, [], [], a, [], [[], []]),
            'str_program': lambda a: "Equals(%s, Superlative(max, [Filter(video, [actions, %s]), Filter(video, [actions, %s])], Subtract(Query(end, action), Query(start, action))))"
                                        % (a[0]['tree'], a[0]['tree'], a[1]['tree'])
        },

        'actLengthShorterVerify': {
            'id': 'actLengthShorterVerify',
            'attributes': {
                'type': 'actLengthShorterVerify',
                'structural': 'compare',
                'semantic': 'action',
                'ans_type': 'binary',
                'video_id': v_id,
            },
            'global': 'length',
            'local': lambda o, a: "shorter-%s-%s" %
                                  (a[0]['direct'],
                                   a[1]['direct']),
            'questions': [
                lambda a: "Was the person %s for less time than they were %s?" %
                          (pp(a[0]), pp(a[1])),
                lambda a: "Did they %s for less time than they spent %s?" %
                          (pres(a[0]), pp(a[1])),
                lambda a: "Did the person spend a smaller amount of time %s than %s?" %
                          (pp(a[0]), pp(a[1])),
                lambda a: "Was %s something they spent less time doing than %s?" %
                          (pp(a[0]), pp(a[1])),
                lambda a: "Compared to %s, did they %s for less time?" %
                          (pp(a[1]), pres(a[0])),
                lambda a: "Were they %s for a shorter amount of time than they were %s?" %
                          (pp(a[0]), pp(a[1])),
                lambda a: "Did the person %s for a shorter amount of time than they spent %s?" %
                          (pres(a[0]), pp(a[1])),
                lambda a: "Did the person spend a shorter amount of time %s than they spent %s?" %
                          (pp(a[0]), pp(a[1])),
                lambda a: "Was %s something they spent a shorter amount of time doing than they spent %s?" %
                          (pp(a[0]), pp(a[1])),
                lambda a: "Compared to %s, did the person %s for a shorter amount of time?" %
                          (pp(a[1]), pres(a[0])),
            ],
            'starts': [
                [15, 45],
                [9, 40],
                [46, 52],
                [4, 47],
                [23, 12],
                [10, 55],
                [15, 61],
                [46, 63],
                [4, 73],
                [29, 12],
            ],
            'order': [
                [0, 1], [0, 1], [0, 1], [0, 1], [1, 0], [0, 1],
                [0, 1], [0, 1], [0, 1], [1, 0],
            ],
            'phrases': [
                lambda a: [pp(a[0]), pp(a[1])],
                lambda a: [pres(a[0]), pp(a[1])],
                lambda a: [pp(a[0]), pp(a[1])],
                lambda a: [pp(a[0]), pp(a[1])],
                lambda a: [pres(a[0]), pp(a[1])],
                lambda a: [pp(a[0]), pp(a[1])],
                lambda a: [pres(a[0]), pp(a[1])],
                lambda a: [pp(a[0]), pp(a[1])],
                lambda a: [pp(a[0]), pp(a[1])],
                lambda a: [pres(a[0]), pp(a[1])],
            ],
            'args': [[2, act, ['direct']]],
            'direct': lambda a: "shorter-%s-%s" % (a[0]['direct'],
                                                   a[1]['direct']),
            'time': lambda a: ('all', ""),
            'program': lambda a: solve.actLengthShorterVerify(stsg, a),
            'steps': 5,
            'quals': [
                lambda o, a: o is not None,
                lambda o, a: a[0]['direct'] != a[1]['direct'],
                lambda o, a: occursNo('more', 1, a[0], stsg),
                lambda o, a: occursNo('more', 1, a[1], stsg),
                lambda o, a: not transition(a[0]),
                lambda o, a: not transition(a[1]),
            ],
            'package_ans': lambda o: o,
            'metrics': lambda o, a: metrics(a, [], [], [], [], [[], []]),
            'str_program': lambda a: "Equals(%s, Superlative(min, [Filter(video, [actions, %s]), Filter(video, [actions, %s])], Subtract(Query(end, action), Query(start, action))))"
                                        % (a[0]['tree'], a[0]['tree'], a[1]['tree'])
        },


        'actLongest': {
            'id': 'actLongest',
            'attributes': {
                'type': 'actLongest',
                'structural': 'query',
                'semantic': 'action',
                'ans_type': 'open',
                'video_id': v_id,
            },
            'global': 'length',
            'local': lambda o, a: "longest",
            'questions': [
                lambda a: "What was the person doing for the longest amount of time?",
                lambda a: "What did the person spend the longest amount of time doing?",
                lambda a: "What was the person doing for the most time?",
                lambda a: "What did the person spend the most amount of time doing?",
                lambda a: "What were they doing for the longest amount of time?",
                lambda a: "What did they spend the longest amount of time doing?",
                lambda a: "What were they doing for the most time?",
                lambda a: "What did they spend the most amount of time doing?",
            ],
            'starts': [
                [], [], [], [], [], [], [], [], 
            ],
            'order': [
                [], [], [], [], [], [], [], [], 
            ],
            'phrases': [
                lambda a: '', lambda a: '', lambda a: '',
                lambda a: '', lambda a: '',
                lambda a: '', lambda a: '', lambda a: '',
                lambda a: '', lambda a: '',
            ],
            'args': [],
            'direct': lambda a: "longest",
            'time': lambda a: ('all', ""),
            'program': lambda a: solve.findLongestTemplate(stsg, 7),
            'steps': 2,
            'quals': [
                lambda o, a: o is not None,
                lambda o, a: not transition(o),
            ],
            'package_ans': lambda o: ENG[o],
            'metrics': lambda o, a: metrics(a, [], [], [o[0]], [], [[], []]),
            'str_program': lambda a: "Superlative(max, Filter(video, [actions]), Subtract(Query(end, action), Query(start, action)))"
        },


        'actShortest': {
            'id': 'actShortest',
            'attributes': {
                'type': 'actShortest',
                'structural': 'query',
                'semantic': 'action',
                'ans_type': 'open',
                'video_id': v_id,
            },
            'global': 'length',
            'local': lambda o, a: "shortest",
            'questions': [
                lambda a: "What was the person doing for the shortest amount of time?",
                lambda a: "What did the person spend the shortest amount of time doing?",
                lambda a: "What was the person doing for the least time?",
                lambda a: "What did the person spend the least amount of time doing?",
                lambda a: "What were they doing for the shortest amount of time?",
                lambda a: "What did they spend the shortest amount of time doing?",
                lambda a: "What were they doing for the least time?",
                lambda a: "What did they spend the least amount of time doing?",
            ],
            'starts': [
                [], [], [], [], [], [], [], [], 
            ],
            'order': [
                [], [], [], [], [], [], [], [], 
            ],
            'phrases': [
                lambda a: '', lambda a: '', lambda a: '',
                lambda a: '', lambda a: '',
                lambda a: '', lambda a: '', lambda a: '',
                lambda a: '', lambda a: '',
            ],
            'args': [],
            'direct': lambda a: "shortest",
            'time': lambda a: ('all', ""),
            'program': lambda a: solve.findShortestTemplate(stsg, 7),
            'steps': 2,
            'quals': [
                lambda o, a: o is not None,
                lambda o, a: not transition(o),
            ],
            'package_ans': lambda o: ENG[o],
            'metrics': lambda o, a: metrics(a, [], [], [], [], [[], []]),
            'str_program': lambda a: "Superlative(min, Filter(video, [actions]), Subtract(Query(end, action), Query(start, action)))"
        },

        ##########
        #  Time  #
        ##########
        'actTime': {
            'id': 'actTime',
            'attributes': {
                'type': 'actTime',
                'structural': 'compare',
                'semantic': 'action',
                'ans_type': 'binary',
                'video_id': v_id,
            },
            'global': 'time',
            'local': lambda o, a: "%s-%s" % (a[0]['direct'], a[1]['direct']),
            'questions': [
                lambda a: "Was the person %s before or after %s?" %
                          (pp(a[0]), pp(a[1])),
                lambda a: "Did they %s before or after %s?" %
                          (pres(a[0]), pp(a[1])),
                lambda a: "Did they %s before or after they %s?" %
                          (pres(a[0]), past(a[1])),
                lambda a: "Was %s something they did before or after they %s?" %
                          (pp(a[0]), past(a[1])),
            ],
            'starts': [
                [15, 32], [9, 26], [9, 31], [4, 45],
            ],
            'order': [
                [0,1], [0,1], [0,1], [0,1], 
            ],
            'phrases': [
                lambda a: [pp(a[0]), pp(a[1])],
                lambda a: [pres(a[0]), pp(a[1])],
                lambda a: [pres(a[0]), past(a[1])],
                lambda a: [pp(a[0]), past(a[1])],
            ],
            'args': [[2, act, ALL_ACT_INDIRECT]],
            'direct': lambda a: "%s-%s" % (a[0]['direct'], a[1]['direct']),
            'time': lambda a: ('all', ""),
            'program': lambda a: solve.actTime(stsg, a),
            'steps': 5,
            'quals': [
                lambda o, a: o is not None,
                lambda o, a: a[0]['direct'] != a[1]['direct'],
            ],
            'package_ans': lambda o: o,
            'metrics': lambda o, a: metrics(a, a, [], [], [], [[], []]),
            'str_program': lambda a: "Compare([before, after], Exists(%s, Iterate(Localize(temporal tag, %s), Filter(frame, [actions]))))" % (a[0]['tree'], a[1]['tree'])
        },

        'relTime': {
            'id': 'relTime',
            'attributes': {
                'type': 'relTime',
                'structural': 'compare',
                'semantic': 'relation',
                'ans_type': 'binary',
                'video_id': v_id,
            },
            'global': 'time',
            'local': lambda o, a: "%s-%s" % (a[0]['direct'], a[1]['direct']),
            'questions': [
                lambda a: "Was the person %s something before or after %s?" %
                          (pp(a[0]), pp(a[1])),
                lambda a: "Did they %s anything before or after %s?" %
                          (pres(a[0]), pp(a[1])),
                lambda a: "Did they %s something before or after they %s?" %
                          (pres(a[0]), past(a[1])),
                lambda a: "Was %s an object something they did before or after they %s?" %
                          (pp(a[0]), past(a[1])),
            ],
            'starts': [
                [15, 42], [9, 35], [9, 41], [4, 55],
            ],
            'order': [
                [0,1], [0,1], [0,1], [0,1],
            ],
            'phrases': [
                lambda a: [pp(a[0]), pp(a[1])],
                lambda a: [pres(a[0]), pp(a[1])],
                lambda a: [pres(a[0]), past(a[1])],
                lambda a: [pp(a[0]), past(a[1])],
            ],
            'args': [[1, crel + vrel, ALL_REL_INDIRECT],
                     [1, act, ALL_ACT_INDIRECT]],
            'direct': lambda a: "%s-%s" % (a[0]['direct'], a[1]['direct']),
            'time': lambda a: ('all', ""),
            'program': lambda a: solve.relTime(stsg, a),
            'steps': 5,
            'quals': [
                lambda o, a: o is not None,
                lambda o, a: notInAction(a[0], a[1]),
                lambda o, a: a[0]['direct'] != IDX['not_contacting'],
                # these are verbs where there are actions mapping to verb --> None
                lambda o, a: a[0]['direct'] not in ['v016', 'r20', 'v030',
                                                'v006', 'v000', 'v017',
                                                'v019', 'v020', 'v022',
                                                'r13'],
            ],
            'package_ans': lambda o: o,
            'metrics': lambda o, a: metrics(a, actFromObjRel(o[1], [a[0]]) + [a[1]], [], [], [], [[], []]),
            'str_program': lambda a: "Compare([before, after], Exists(%s, Iterate(Localize(temporal tag, %s), Filter(frame, [relations]))))" % (a[0]['tree'], a[1]['tree'])
        },

        'objTime': {
            'id': 'objTime',
            'attributes': {
                'type': 'objTime',
                'structural': 'compare',
                'semantic': 'object',
                'ans_type': 'binary',
                'video_id': v_id,
            },
            'global': 'time',
            'local': lambda o, a: "%s-%s" % (a[0]['direct'], a[1]['direct']),
            'questions': [
                lambda a: "Did the person interact with %s before or after %s?" %
                          (art(a[0]), pp(a[1])),
                lambda a: "Did the person interact with %s before or after they %s?" %
                          (art(a[0]), past(a[1])),
                lambda a: "Was interacting with %s something they did before or after they %s?" %
                          (art(a[0]), past(a[1])),
                lambda a: "Were they interacting with %s before or after %s?" %
                          (art(a[0]), pp(a[1])),
                lambda a: "Were they interacting with %s before or after they %s?" %
                          (art(a[0]), past(a[1])),
            ],
            'starts': [
                [29, 46],
                [29, 41],
                [21, 62],
                [27, 44],
                [27, 49]
            ],
            'order': [
                [0,1], [0,1], [0,1], [0,1], [0,1],
            ],
            'phrases': [
                lambda a: [art(a[0]), pp(a[1])],
                lambda a: [art(a[0]), past(a[1])],
                lambda a: [art(a[0]), past(a[1])],
                lambda a: [art(a[0]), pp(a[1])],
                lambda a: [art(a[0]), past(a[1])],
            ],
            'args': [[1, obj, ALL_OBJ_INDIRECT],
                     [1, act, ALL_ACT_INDIRECT]],
            'direct': lambda a: "%s-%s" % (a[0]['direct'], a[1]['direct']),
            'time': lambda a: ('all', ""),
            'program': lambda a: solve.objTime(stsg, a),
            'steps': 5,
            'quals': [
                lambda o, a: o is not None,
                lambda o, a: notInAction(a[0], a[1]),
                lambda o, a: a[0] not in [IDX['clothes'], IDX['shoe'],
                                          IDX['light'], IDX['floor'],
                                          IDX['person'], IDX['doorway']],
            ],
            'package_ans': lambda o: o,

            'metrics': lambda o, a: metrics(a, actFromObjRel([a[0]], o[1]) + [a[1]], [], [], [], [[], []]),
            'str_program': lambda a: "Compare([before, after], Exists(%s, Iterate(Localize(temporal tag, %s), Filter(frame, [objects]))))" % (a[0]['tree'], a[1]['tree'])
        },

    }

    return templates

######################################################################
######################################################################
####################### TEMPLATE GRAVEYARD ###########################
######################################################################
######################################################################
# 'actExists': {
        #     'id': 'actExists',
        #     'attributes': {
        #         'type': 'actExists',
        #         'structural': 'verify',
        #         'semantic': 'action',
        #         'ans_type': 'binary',
        #         'video_id': v_id,
        #     },
        #     'global': 'exists',
        #     'local': lambda o, a: a[0],
        #     'questions': [
        #         lambda a: "Was the person %s%s?" % (pp(a[0]), a[1]['phrase']),
        #         lambda a: "Were they %s%s?" % (pp(a[0]), a[1]['phrase']),
        #         lambda a: "%s, was the person %s?" % (a[1]['start_phrase'], pp(a[0])),
        #         lambda a: "%s, were they %s?" % (a[1]['start_phrase'], pp(a[0])),

        #         lambda a: "Did the person %s%s?" % (pres(a[0]), a[1]['phrase']),
        #         lambda a: "Did they %s%s?" % (pres(a[0]), a[1]['phrase']),
        #         lambda a: "%s, did the person %s?" % (a[1]['start_phrase'], pres(a[0])),
        #         lambda a: "%s, did they %s?" % (a[1]['start_phrase'], pres(a[0])),

        #         lambda a: "Had the person %s%s?" % (past(a[0]), a[1]['phrase']),
        #         lambda a: "Have they %s%s?" % (past(a[0]), a[1]['phrase']),
        #         lambda a: "%s, had the person %s?" % (a[1]['start_phrase'], past(a[0])),
        #         lambda a: "%s, had they %s?" % (a[1]['start_phrase'], past(a[0])),

        #         lambda a: "Was %s one of the things they did%s?" % (pp(a[0]), a[1]['phrase']),
        #         lambda a: "Was %s something a person did%s?" % (pp(a[0]), a[1]['phrase']),

        #         #lambda a: "%s, had the person %s?" % (a[1]['start_phrase'], past(a[0])),
        #         lambda a: "%s, was there a point where they %s?" % (a[1]['start_phrase'], past(a[0])),
        #         lambda a: "%s, was there a point where someone %s?" % (a[1]['start_phrase'], past(a[0])),
        #     ],
        #     'starts': [
        #         [15, 15],
        #         [10, 10],
        #         [17, 0],
        #         [12, 0],

        #         [15, 15],
        #         [9, 9],
        #         [17, 0],
        #         [11, 0],

        #         [15, 15],
        #         [10, 10],
        #         [17, 0],
        #         [11, 0],

        #         [4, 31],
        #         [4, 27],

        #         [31, 0],
        #         [34, 0],
        #     ],
        #     'order': [
        #         [0, 1],
        #         [0, 1],
        #         [1, 0],
        #         [1, 0],

        #         [0, 1],
        #         [0, 1],
        #         [1, 0],
        #         [1, 0],

        #         [0, 1],
        #         [0, 1],
        #         [1, 0],
        #         [1, 0],

        #         [0, 1],
        #         [0, 1],

        #         [1, 0],
        #         [1, 0],
        #     ],
        #     'phrases': [
        #         lambda a: [pp(a[0]), a[1]['phrase']],
        #         lambda a: [pp(a[0]), a[1]['phrase']],
        #         lambda a: [pp(a[0]), a[1]['start_phrase']],
        #         lambda a: [pp(a[0]), a[1]['start_phrase']],

        #         lambda a: [pres(a[0]), a[1]['phrase']],
        #         lambda a: [pres(a[0]), a[1]['phrase']],
        #         lambda a: [pres(a[0]), a[1]['start_phrase']],
        #         lambda a: [pres(a[0]), a[1]['start_phrase']],

        #         lambda a: [past(a[0]), a[1]['phrase']],
        #         lambda a: [past(a[0]), a[1]['phrase']],
        #         lambda a: [past(a[0]), a[1]['start_phrase']],
        #         lambda a: [past(a[0]), a[1]['start_phrase']],


        #         lambda a: [pp(a[0]), a[1]['phrase']],
        #         lambda a: [pp(a[0]), a[1]['phrase']],

        #         lambda a: [past(a[0]), a[1]['start_phrase']],
        #         lambda a: [past(a[0]), a[1]['start_phrase']],

        #     ],
        #     'args': [[1, ALL_ACT, []],
        #              [1, ['time'], ALL_TIME_INDIRECT]],
        #     'direct': lambda a: "%s" % (a[0]),
        #     'time': lambda a: (a[1]['type'], timeDirect(a[1])),
        #     'program': lambda a: solve.actExists(stsg, a),
        #     'steps': 1,
        #     'quals': [
        #         lambda o, a: noActOverlapWithTime(a[0], a[1]), 
        #         lambda o, a: ACTION_SV[a[0]][0] in obj or ACTION_SV[a[0]][1] in rel,
        #     ],
        #     'package_ans': lambda o: o,
        #     'metrics': lambda o, a: metrics([a[1]], [], [], [], [], [[],[]]),
        #     'str_program': lambda a: "Exists(%s, Iterate(%s, Filter(frame, [actions])))" % (ENG[a[0]], a[1]['tree']),
        # },


#'relFirst': {
        #     'id': 'relFirst',
        #     'attributes': {
        #         'type': 'relFirst',
        #         'structural': 'query',
        #         'semantic': 'relation',  # todo: is this object?
        #         'ans_type': 'open',
        #         'video_id': v_id,
        #     },
        #     'global': 'first',
        #     'local': lambda o, a: a[0],
        #     'questions': [
        #         lambda a: "What did the person do to %s first?"
        #                   % art(a[0]),
        #         lambda a: "What was the first thing they did to %s?"
        #                   % art(a[0]),
        #         lambda a: "What were they doing to %s first?"
        #                   % art(a[0]),
        #         lambda a: "What was the first thing the person was doing to %s?"
        #                   % art(a[0]),
        #     ],
        #     'args': [[1, obj, []]],
        #     'direct': lambda a: "%s" % (a[0]),
        #     'time': lambda a: ('all', ""),
        #     'program': lambda a: solve.relFirst(stsg, a),
        #     'steps': 1,
        #     'quals': [
        #         lambda o, a: len(o) == 1,
        #         lambda o, a: o[0] not in [IDX[
        #             'not_contacting'], IDX['not_looking_at']],
        #         lambda o, a: isValidObjRel(a[0], o[0])
        #     ],
        #     'package_ans': lambda o: ENG[o[0]],
        #     'metrics': lambda o, a: metrics([], [], [o[0]], [], [], [[a[0]],[o[0]]])
        # },


        # 'relLast': {
        #     'id': 'relLast',
        #     'attributes': {
        #         'type': 'relLast',
        #         'structural': 'query',
        #         'semantic': 'relation',  # todo: is this object?
        #         'ans_type': 'open',
        #         'video_id': v_id,
        #     },
        #     'global': 'last',
        #     'local': lambda o, a: a[0],
        #     'questions': [
        #         lambda a: "What did the person do to %s last?"
        #                   % art(a[0]),
        #         lambda a: "What was the last thing they did to %s?"
        #                   % art(a[0]),
        #         lambda a: "What were they doing to %s last?"
        #                   % art(a[0]),
        #         lambda a: "What was the last thing the person was doing to %s?"
        #                   % art(a[0]),
        #     ],
        #     'args': [[1, obj, []]],
        #     'direct': lambda a: "%s" % (a[0]),
        #     'time': lambda a: ('all', ""),
        #     'program': lambda a: solve.relLast(stsg, a),
        #     'steps': 2,
        #     'quals': [
        #         lambda o, a: len(o) == 1,
        #         lambda o, a: o[0] not in [IDX[
        #             'not_contacting'], IDX['not_looking_at']],
        #     ],
        #     'package_ans': lambda o: ENG[o[0]],
        #     'metrics': lambda o, a: metrics([], [], [], [], [], [[a[0]],[o[0]]])
        # },


        ##########
        # #  What #
        # #########

        # 'actWhatStart': {
        #     'id': 'actWhatStart',
        #     'attributes': {
        #         'type': 'actWhatStart',
        #         'structural': 'query',
        #         'semantic': 'action',
        #         'ans_type': 'open',
        #         'video_id': v_id,
        #     },
        #     'global': 'what',
        #     'local': lambda o, a: "start",
        #     'questions': [
        #         lambda a: "What else was the person doing when they began %s?" %
        #                 pp(a[0]),
        #         lambda a: "When they began %s, what else was the person doing?" %
        #                 pp(a[0]),
        #         lambda a: "What were they doing at the same time as when they started to %s?" %
        #                 pres(a[0]),
        #         lambda a: "As the person was starting to %s, what other activity were they doing?" %
        #                 pres(a[0]),
        #     ],
        #     'args': [[1, act, ALL_ACT_INDIRECT]],
        #     'direct': lambda a: "%s" % (a[0]['direct']),
        #     'time': lambda a: ("all", ""),
        #     'program': lambda a: solve.actWhatStart(stsg, a),
        #     'steps': 2,
        #     'quals': [
        #         lambda o, a: o is not None,
        #         lambda o, a: len(o) == 1,
        #     ],
        #     'package_ans': lambda o: ENG[o[0]],
        #     'metrics': lambda o, a: metrics(a, [], [], [], [], [[], []]),
        # },

        # 'actWhatEnd': {
        #     'id': 'actWhatEnd',
        #     'attributes': {
        #         'type': 'actWhatEnd',
        #         'structural': 'query',
        #         'semantic': 'action',
        #         'ans_type': 'open',
        #         'video_id': v_id,
        #     },
        #     'global': 'what',
        #     'local': lambda o, a: "end",
        #     'questions': [
        #         lambda a: "What else was the person doing when they finished %s?" %
        #                 pp(a[0]),
        #         lambda a: "When they finished %s, what else was the person doing?" %
        #                 pp(a[0]),
        #         lambda a: "What were they doing at the same time as when they stopped %s?" %
        #                 pp(a[0]),
        #         lambda a: "As the person stopped %s, what other activity were they doing?" %
        #                 pp(a[0]),
        #     ],
        #     'args': [[1, act, ALL_ACT_INDIRECT]],
        #     'direct': lambda a: "%s" % (a[0]['direct']),
        #     'time': lambda a: ("all", ""),
        #     'program': lambda a: solve.actWhatEnd(stsg, a),
        #     'steps': 2,
        #     'quals': [
        #         lambda o, a: o is not None,
        #         lambda o, a: len(o) == 1
        #     ],
        #     'package_ans': lambda o: ENG[o[0]],
        #     'metrics': lambda o, a: metrics(a, [], [], [], [], [[], []]),
        # },

        # 'actWhatBetweenWhileStartOneFirst': {
        #     'id': 'actWhatBetweenWhileStartOneFirst',
        #     'attributes': {
        #         'type': 'actWhatBetweenWhileStartOneFirst',
        #         'structural': 'query',
        #         'semantic': 'action',
        #         'ans_type': 'open',
        #         'video_id': v_id,
        #     },
        #     'global': 'what',
        #     'local': lambda o, a: a[0]['type'],
        #     'questions': [
        #         lambda a: "What is the first thing they started doing%s?" %
        #                    a[0]['phrase'],
        #         lambda a: "What is the first thing they began%s?" %
        #                    a[0]['phrase'],
        #         lambda a: "What is the first thing,%s, that the person started doing?" %
        #                    a[0]['phrase'],
        #         lambda a: "What is the first thing,%s, that they began doing?" %
        #                    a[0]['phrase'],
        #         lambda a: "%s, what is the first thing the person started doing?" %
        #                    a[0]['start_phrase'],
        #         lambda a: "%s, what is the first thing they began?" %
        #                    a[0]['start_phrase'],
        #     ],
        #     'args': [[1, ['time'], ['between', 'while']]],
        #     'direct': lambda a: "",
        #     'time': lambda a: (a[0]['type'], timeDirect(a[0])),
        #     'program': lambda a: solve.actWhatBetweenWhileStartOneFirst(stsg, a),
        #     'steps': 2,
        #     'quals': [
        #         lambda o, a: o is not None,
        #     ],
        #     'package_ans': lambda o: ENG[o],
        #     'metrics': lambda o, a: metrics(a, [], [], [], [], [[], []]),
        # },

        # 'actWhatBetweenWhileStartOneLast': {
        #     'id': 'actWhatBetweenWhileStartOneLast',
        #     'attributes': {
        #         'type': 'actWhatBetweenWhileStartOneLast',
        #         'structural': 'query',
        #         'semantic': 'action',
        #         'ans_type': 'open',
        #         'video_id': v_id,
        #     },
        #     'global': 'what',
        #     'local': lambda o, a: a[0]['type'],
        #     'questions': [
        #         lambda a: "What is the last thing they started doing%s?" %
        #                    a[0]['phrase'],
        #         lambda a: "What is the last thing they began%s?" %
        #                    a[0]['phrase'],
        #         lambda a: "What is the last thing,%s, that the person started doing?" %
        #                    a[0]['phrase'],
        #         lambda a: "What is the last thing,%s, that they began doing?" %
        #                    a[0]['phrase'],
        #         lambda a: "%s, what is the last thing the person started doing?" %
        #                    a[0]['start_phrase'],
        #         lambda a: "%s, what is the last thing they began?" %
        #                    a[0]['start_phrase'],
        #     ],
        #     'args': [[1, ['time'], ['between', 'while']]],
        #     'program': lambda a: solve.actWhatBetweenWhileStartOneLast(stsg, a),
        #     'direct': lambda a: "",
        #     'time': lambda a: (a[0]['type'], timeDirect(a[0])),
        #     'steps': 2,
        #     'quals': [
        #         lambda o, a: o is not None,
        #     ],
        #     'package_ans': lambda o: ENG[o],
        #     'metrics': lambda o, a: metrics(a, [], [], [], [], [[], []]),
        # },

        # 'actWhatBetweenWhileEndOneFirst': {
        #     'id': 'actWhatBetweenWhileEndOneFirst',
        #     'attributes': {
        #         'type': 'actWhatBetweenWhileEndOneFirst',
        #         'structural': 'query',
        #         'semantic': 'action',
        #         'ans_type': 'open',
        #         'video_id': v_id,
        #     },
        #     'global': 'what',
        #     'local': lambda o, a: a[0]['type'],
        #     'questions': [
        #         lambda a: "What is the first thing the person stopped doing%s?" %
        #                    a[0]['phrase'],
        #         lambda a: "What is the first thing they finished%s?" %
        #                    a[0]['phrase'],
        #         lambda a: "What is the first thing,%s, that they stopped doing?" %
        #                    a[0]['phrase'],
        #         lambda a: "What is the first thing,%s, that the person finished doing?" %
        #                    a[0]['phrase'],
        #         lambda a: "%s, what is the first thing the person stopped doing?" %
        #                    a[0]['start_phrase'],
        #         lambda a: "%s, what is the first thing they finished?" %
        #                    a[0]['start_phrase'],
        #     ],
        #     'args': [[1, ['time'], ['between', 'while']]],
        #     'program': lambda a: solve.actWhatBetweenWhileEndOneFirst(stsg, a),
        #     'direct': lambda a: "",
        #     'time': lambda a: (a[0]['type'], timeDirect(a[0])),
        #     'steps': 2,
        #     'quals': [
        #         lambda o, a: o is not None,
        #     ],
        #     'package_ans': lambda o: ENG[o],
        #     'metrics': lambda o, a: metrics(a, [], [], [], [], [[], []]),
        # },

        # 'actWhatBetweenWhileEndOneLast': {
        #     'id': 'actWhatBetweenWhileEndOneLast',
        #     'attributes': {
        #         'type': 'actWhatBetweenWhileEndOneLast',
        #         'structural': 'query',
        #         'semantic': 'action',
        #         'ans_type': 'open',
        #         'video_id': v_id,
        #     },
        #     'global': 'what',
        #     'local': lambda o, a: a[0]['type'],
        #     'questions': [
        #         lambda a: "What is the last thing the person stopped doing%s?" %
        #                    a[0]['phrase'],
        #         lambda a: "What is the last thing they finished%s?" %
        #                    a[0]['phrase'],
        #         lambda a: "What is the last thing,%s, that they stopped doing?" %
        #                    a[0]['phrase'],
        #         lambda a: "What is the last thing,%s, that the person finished doing?" %
        #                    a[0]['phrase'],
        #         lambda a: "%s, what is the last thing the person stopped doing?" %
        #                    a[0]['start_phrase'],
        #         lambda a: "%s, what is the last thing they finished?" %
        #                    a[0]['start_phrase'],
        #     ],
        #     'args': [[1, ['time'], ['between', 'while']]],
        #     'direct': lambda a: "",
        #     'time': lambda a: (a[0]['type'], timeDirect(a[0])),
        #     'program': lambda a: solve.actWhatBetweenWhileEndOneLast(stsg, a),
        #     'steps': 2,
        #     'quals': [
        #         lambda o, a: o is not None,
        #     ],
        #     'package_ans': lambda o: ENG[o],
        #     'metrics': lambda o, a: metrics(a, [], [], [], [], [[], []]),
        # },

        # #########
        # # Count #
        # #########

        # 'actCount': {
        #     'id': 'actCount',
        #     'attributes': {
        #         'type': 'actCount',
        #         'structural': 'query',
        #         'semantic': 'action',
        #         'ans_type': 'open',
        #         'video_id': v_id,
        #     },
        #     'global': 'count',
        #     'local': lambda o, a: a[0],
        #     'questions': [
        #         lambda a: "How many times were they %s%s?" %
        #                 (pp(a[0]), a[1]['phrase']),
        #         lambda a: "How many times does the person %s%s?" %
        #                 (pres(a[0]), a[1]['phrase']),
        #         lambda a: "How many times did they %s%s?" %
        #                 (pres(a[0]), a[1]['phrase']),
        #         lambda a: "What is the number of times they were %s%s?" %
        #                 (pp(a[0]), a[1]['phrase']),
        #         lambda a: "What is the number of times they person was %s%s?" %
        #                 (pp(a[0]), a[1]['phrase']),
        #         lambda a: "What is the number of times they %s%s?" %
        #                 (past(a[0]), a[1]['phrase']),
        #         lambda a: "How many times%s were they %s?" %
        #                 (a[1]['phrase'], pp(a[0])),
        #         lambda a: "How many times%s does the person %s?" %
        #                 (a[1]['phrase'], pres(a[0])),
        #         lambda a: "How many times%s did they %s?" %
        #                 (a[1]['phrase'], pres(a[0])),
        #         lambda a: "%s, what is the number of times they were %s?" %
        #                 (a[1]['start_phrase'], pp(a[0])),
        #         lambda a: "%s, what is the number of times they person was %s?" %
        #                 (a[1]['start_phrase'], pp(a[0])),
        #         lambda a: "%s, what is the number of times they %s?" %
        #                 (a[1]['start_phrase'], past(a[0])),
        #         lambda a: "%s, how many times were they %s?" %
        #                 (a[1]['start_phrase'], pp(a[0])),
        #         lambda a: "%s, how many times does the person %s?" %
        #                 (a[1]['start_phrase'], pres(a[0])),
        #         lambda a: "%s, how many times did they %s?" %
        #                 (a[1]['start_phrase'], pres(a[0])),
        #     ],
        #     'args': [[1, act, []],
        #              [1, ['time'], ALL_TIME_INDIRECT]],
        #     'direct': lambda a: "%s" % (a[0]),
        #     'time': lambda a: (a[1]['type'], timeDirect(a[1])),
        #     'program': lambda a: solve.actCount(stsg, a),
        #     'steps': 1,
        #     'quals': [
        #         lambda o, a: o == 0, # AC o != 0
        #         lambda o, a: noActOverlapWithTime(a[0], a[1]),
        #         lambda o, a: a[0] not in ILLEGAL_REP,
        #     ],
        #     'package_ans': lambda o: o,
        #     'metrics': lambda o, a: metrics([a[1]], [], [], [], [a[0]], [[], []]),
        # },

        # 'actCountChooseMore': {
        #     'id': 'actCountChooseMore',
        #     'attributes': {
        #         'type': 'actCountChooseMore',
        #         'structural': 'compare',
        #         'semantic': 'action',
        #         'ans_type': 'open',
        #         'video_id': v_id,
        #     },
        #     'global': 'count',
        #     'local': lambda o, a: "%s-%s" % (a[0], a[1]),
        #     'questions': [
        #         lambda a: "Were they %s or %s more times%s?" %
        #             (pp(a[0]), pp(a[1]), a[2]['phrase']),
        #         lambda a: "Did they %s or %s more times%s?" %
        #             (pres(a[0]), pres(a[1]), a[2]['phrase']),
        #         lambda a: "Was the number of times they %s or %s greater%s?" %
        #             (past(a[0]), past(a[1]), a[2]['phrase']),
        #         lambda a: "Was %s or %s the activity they did more often%s?" %
        #             (pp(a[0]), pp(a[1]), a[2]['phrase']),
        #         lambda a: "Did they %s or %s a greater number of times%s?" %
        #             (pres(a[0]), pres(a[1]), a[2]['phrase']),
        #         lambda a: "%s, were they %s or %s more times?" %
        #             (a[2]['start_phrase'], pp(a[0]), pp(a[1])),
        #         lambda a: "%s, did they %s or %s more times?" %
        #             (a[2]['start_phrase'], pres(a[0]), pres(a[1])),
        #         lambda a: "%s, was the number of times they %s or %s greater?" %
        #             (a[2]['start_phrase'], past(a[0]), past(a[1])),
        #         lambda a: "%s, was %s or %s the activity they did more often?" %
        #             (a[2]['start_phrase'], pp(a[0]), pp(a[1])),
        #         lambda a: "%s, did they %s or %s a greater number of times?" %
        #             (a[2]['start_phrase'], pres(a[0]), pres (a[1])),
        #     ],
        #     'args': [[2, act, []],
        #              [1, ['time'], ALL_TIME_INDIRECT]],
        #     'direct': lambda a: "%s-%s" % (a[0], a[1]),
        #     'time': lambda a: (a[2]['type'], timeDirect(a[2])),
        #     'program': lambda a: solve.actCountChooseMore(stsg, a),
        #     'steps': 3,
        #     'quals': [
        #         lambda o, a: o is not None,
        #         lambda o, a: noActOverlapWithTime(a[0], a[2]),
        #         lambda o, a: noActOverlapWithTime(a[1], a[2]),
        #         lambda o, a: a[0] not in ILLEGAL_REP,
        #         lambda o, a: a[1] not in ILLEGAL_REP,
        #     ],
        #     'package_ans': lambda o: ENG[o],
        #     'metrics': lambda o, a: metrics([a[2]], [], [], [], [a[0], a[1]], [[], []]),
        # },

        # 'actCountChooseFewer': {
        #     'id': 'actCountChooseFewer',
        #     'attributes': {
        #         'type': 'actCountChooseFewer',
        #         'structural': 'compare',
        #         'semantic': 'action',
        #         'ans_type': 'open',
        #         'video_id': v_id,
        #     },
        #     'global': 'count',
        #     'local': lambda o, a: "%s-%s" % (a[0], a[1]),
        #     'questions': [
        #         lambda a: "Were they %s or %s fewer times%s?" %
        #             (pp(a[0]), pp(a[1]), a[2]['phrase']),
        #         lambda a: "Did they %s or %s fewer times%s?" %
        #             (pres(a[0]), pres(a[1]), a[2]['phrase']),
        #         lambda a: "Was the number of times they %s or %s smaller%s?" %
        #             (past(a[0]), past(a[1]), a[2]['phrase']),
        #         lambda a: "Was %s or %s the activity they did less often%s?" %
        #             (pp(a[0]), pp(a[1]), a[2]['phrase']),
        #         lambda a: "Did they %s or %s a smaller number of times%s?" %
        #             (pres(a[0]), pres(a[1]), a[2]['phrase']),
        #         lambda a: "%s, were they %s or %s fewer times?" %
        #             (a[2]['start_phrase'], pp(a[0]), pp(a[1])),
        #         lambda a: "%s, did they %s or %s fewer times?" %
        #             (a[2]['start_phrase'], pres(a[0]), pres(a[1])),
        #         lambda a: "%s, was the number of times they %s or %s smaller?" %
        #             (a[2]['start_phrase'], past(a[0]), past(a[1])),
        #         lambda a: "%s, was %s or %s the activity they did less often?" %
        #             (a[2]['start_phrase'], pp(a[0]), pp(a[1])),
        #         lambda a: "%s, did they %s or %s a smaller number of times?" %
        #             (a[2]['start_phrase'], pres(a[0]), pres (a[1])),
        #     ],
        #     'args': [[2, act, []],
        #              [1, ['time'], ALL_TIME_INDIRECT]],
        #     'direct': lambda a: "%s-%s" % (a[0], a[1]),
        #     'time': lambda a: (a[2]['type'], timeDirect(a[2])),
        #     'program': lambda a: solve.actCountChooseFewer(stsg, a),
        #     'steps': 3,
        #     'quals': [
        #         lambda o, a: o is not None, 
        #         lambda o, a: noActOverlapWithTime(a[0], a[2]),
        #         lambda o, a: noActOverlapWithTime(a[1], a[2]),
        #         lambda o, a: a[0] not in ILLEGAL_REP,
        #         lambda o, a: a[1] not in ILLEGAL_REP,
        #     ],
        #     'package_ans': lambda o: ENG[o],
        #     'metrics': lambda o, a: metrics([a[2]], [], [], [], [a[0], a[1]], [[], []]),
        # },