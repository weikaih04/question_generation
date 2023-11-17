import grammar

IDX = grammar.IDX


def capitalize(phrases):
    capitalized = []

    for i in phrases:
        capitalized.append(i.capitalize())

    for i in capitalized:
        phrases.append(i)
    return phrases


BEFORE_COMP = [
        IDX["standing up"],
        IDX["playing with a phone"],
        IDX["throwing a broom somewhere"],
        IDX["walking through a doorway"],
        IDX["opening a laptop"],
        IDX["grasping onto a doorknob"],
    ]

FIRST_COMP = [
        IDX['behind'],
        IDX['holding'],
        IDX['in'],
        IDX['leaning on'],
        IDX['carrying'],
        IDX['on the side of'],
    ]

LONGER_COMP = [
        IDX["standing up"],
        IDX["playing with a phone"],
        IDX["throwing a broom somewhere"],
        IDX["walking through a doorway"],
        IDX["opening a laptop"],
        IDX["grasping onto a doorknob"],
    ]

REPETITION_COMP = [
        IDX['taking a cup from somewhere'],
        IDX['putting some food somewhere'],
    ]

# THese cannot be in actions
OBJREL_COMP = [
        (IDX['table'], IDX['wiping']),
        (IDX['dish'], IDX['wiping']),
        (IDX['table'], IDX['beneath']),
        (IDX['dish'], IDX['beneath']),
        (IDX['food'], IDX['in front of']),
        (IDX['book'], IDX['carrying']),
        (IDX['chair'], IDX['leaning on']),
    ]


def inPhrases(phrases, q):

    for c in phrases:
        if c in q:
            return True

    return False


def overlap(arr1, arr2):
    for i in arr1:
        for j in arr2:
            if i == j:
                return True

    return False


def includesNovelComp(metrics):
    before = metrics['before']
    first = metrics['first']
    longer = metrics['longer']
    repetition = metrics['repetition']
    objrel = metrics['objrel']

    novel_comp = [
        overlap(before, BEFORE_COMP),
        overlap(first, FIRST_COMP),
        overlap(longer, LONGER_COMP),
        overlap(repetition, REPETITION_COMP),
        overlap(objrel, OBJREL_COMP),
    ]
    return novel_comp


def makeMetrics(q_obj, o, a):
    metrics = q_obj['metrics'](o, a)
    novel_comp = includesNovelComp(metrics)
    direct_args = q_obj['direct'](a)
    direct_time = q_obj['time'](a)

    new_metrics = {
        'novel_comp': novel_comp,
        'indirects': metrics['indirects'],
        'direct_args': direct_args,
        'direct_time': direct_time,
    }

    return new_metrics
