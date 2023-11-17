import pickle


def pickleLoad(path):
    f = open(path, 'rb')
    load = pickle.load(f)
    f.close()
    return load


IDX = pickleLoad('../../data/idx.pkl')
ENG = pickleLoad('../../data/eng.pkl')
PP = pickleLoad('../../data/pres_part.pkl')
ART = pickleLoad('../../data/article.pkl')
OBJ_ART = pickleLoad('../../data/object_with_article.pkl')
PRESENT = pickleLoad('../../data/present.pkl')
PAST = pickleLoad('../../data/past.pkl')


def vType(v):
    """ Find the type of vertex given index

    Args:
        v: an string index of a vertex

    Returns:
        string type of vertex
    """
    t = v[0]
    num = int(v[1:])
    if t == 'o' and num <= 36:
        return 'objects'
    elif t == 'c' and num <= 156:
        return 'actions'
    elif t == 'v' and num <= 32:
        return 'verb'
    elif t == 'r':
        if num <= 3:
            return 'attention'
        elif num <= 9:
            return 'spatial'
        elif num <= 26:
            return "contact"

    print('invalid tag', v)


def art(obj):
    # if its not direct, return phrase
    if type(obj) == dict:
        if obj['type'] != 'direct':
            return obj['phrase']
        obj = IDX[obj['phrase']]
    
    return OBJ_ART[obj]


def pres(verb):
    if type(verb) == dict:
        tp = verb['type']
        if tp != 'direct':
            if tp in ['longest', 'shortest']:
                minus_doing = verb['phrase'][5:]
                return "do" + minus_doing

            return verb['phrase']
        verb = IDX[verb['phrase']]

    return PRESENT[verb]


def past(verb):
    if type(verb) == dict:
        tp = verb['type']
        if tp != 'direct':
            if tp in ['longest', 'shortest']:
                minus_doing = verb['phrase'][5:]
                return "did" + minus_doing
            return verb['phrase']
        verb = IDX[verb['phrase']]

    return PAST[verb]


def pp(verb):
    if type(verb) == dict:
        if verb['type'] != 'direct':
            return verb['phrase']
        verb = IDX[verb['phrase']]

    return PP[verb]
