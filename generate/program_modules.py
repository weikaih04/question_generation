import grammar


def applyGrammar(lst, gram):
    """ TODO
    """
    new_list = []
    for i in lst:
        new_list.append(gram[i])
    
    return new_list


def addSegmentationErrorMargin(stsg, frames):
    return frames


def inMarginOfError(error_margin, data, idx1, idx2):
    """ TODO
    """

    num1 = data[idx1]
    num2 = data[idx2]

    return abs(num1 - num2) <= error_margin


def makeDict(keys, values):
    """ TODO
    """
    if len(keys) != len(values):
        print("Invalid arguments to make dict")
        return

    new_dict = {}
    for i in range(len(keys)):
        new_dict[keys[i]] = values[i]

    return new_dict


def makeListOfTuples(items1, items2):
    """ TODO
    """
    if len(items1) != len(items2):
        print("Invalid arguments to make dict")
        return

    new_list = []
    for i in range(len(items1)):
        new_list.append((items1[i], items2[i]))

    return new_list


def sort(data, idx):
    """ TODO
    """

    data.sort(key=lambda x: x[idx])
    return data


def select(data, attrs):
    """ Navigates the data structure given a list of attributes

    Args:
        data: a data structure
        attrs: an array of attributes mapping thorughout that data structure

    Returns:
        The data structure found while navigating.
    """
    if len(attrs) != 1:
        data = select(data, attrs[:-1])

    return data[attrs[-1]]


def getFrameIds(stsg, f_id, relation):
    """ Gets all the frame ids with the given relation to a specified id

    Args:
        stsg: spatiotemporal scene graph
        f_id: frame id
        relation: type of relationship to frame
            after: gets frames after f_id
            before: gets frames before f_id

    Returns:
        A list of frames before/after f_id
    """

    all_f = select(stsg, ['ordered_frames'])

    idx = all_f.index(f_id)

    if relation == 'after':
        return all_f[idx + 1:]
    elif relation == 'before':
        return all_f[:idx]
    else:
        print("Incorrect relation argument ", relation)


def exists(data, metric, val):
    """ Confirms if a data structure contains an object with a certain attribute

    Args:
        data: the data structure to search
        metric: the part of the data objects to reference
        val: the value we are looking for

    Returns:
        True if an object with this value exists, false otherwise
    """

    if data is None:
        return False

    if val is None:
        return len(data) != 0

    if metric is None:
        for i in data:
            if i == val:
                return True
    else:
        for i in data:
            if i[metric] == val:
                return True

    return False


def existsReturnItem(data, metric, val):
    # This is so it also returns the item that caused truth
    """ Confirms if a data structure contains an object with a certain attribute

    Args:
        data: the data structure to search
        metric: the part of the data objects to reference
        val: the value we are looking for

    Returns:
        True if an object with this value exists, false otherwise
    """

    if data is None:
        return False, None

    if val is None:
        return len(data) != 0, data

    if metric is None:
        for i in data:
            if i == val:
                return True, i
    else:
        for i in data:
            if i[metric] == val:
                return True, i

    return False, None


def overlap(list1, list2):
    """ Confirms if there is overlap betwene 2 lists

    Args:
        list1: a list
        list2: a list

    Returns:
        True overlap between lists, False otherwise
    """

    for i in list1:
        if i in list2:
            return True

    return False


def containedIn(list1, list2):
    """ Confirms list1 is contained in list2

    Args:
        list1: a list
        list2: a list

    Returns:
        True if list 1 contaned in list 2, False otherwise
    """

    for i in list1:
        if i not in list2:
            return False

    return True


def editList(oldList, metric):
    """ Replaces every object in list with a part of that object

    Args:
        oldList: a list of objects with some metric
        metric: the part of the data objects to reference

    Returns:
        List with metric values of every obj on old list
    """

    newList = []
    for i in oldList:
        newList.append(i[metric])

    return newList


def removeFromList(lst, item, metric):
    """ Deletes something from list, if it exists

    Args:
        lst: a list of items
        item: an item of the same type as the list
        metric: the metric to search for

    Returns:
        List with every element but the specified item
    """

    for i in lst:
        if metric is not None:
            list_item = i[metric]
        else:
            list_item = i

        if list_item == item:
            lst.remove(i)
            break

    return lst


def objInRelList(rel_list, obj_id):
    """ Finds if obj is in list of rels
    Args:
        rel_list: a list of relation vertices
        obj: and object id

    Returns:
        True if obj in list of rels, false ow
    """

    for rel in rel_list:
        if select(rel, ['class']) in ['r18', 'r19', 'r1', 'r2', 'r3']:
            continue

        objs = select(rel, ['objects'])
        for obj in objs:
            if select(obj, ['class']) == obj_id:
                return True

    return False


def verify(b):
    """ Processes answer from bool
    Args:
        b: a boolean value

    Returns:
        "Yes" if bool is true, "No" otherwise
    """

    if b:
        return "Yes"
    return "No"


def equals(item1, item2):
    """ Sees if items are equal
    Args:
        item1: an item
        item2: an item

    Returns:
        True if items are equal, False otherwise
    """

    return item1 == item2


def isEmpty(data):
    """ Finds if the length of a datastruct is zero
    Args:
        data: a data strucutre

    Returns:
        True if length of lst is zero, false ow
    """

    return len(data) == 0


def lengthOne(lst):
    """ Finds if the length of a list is one
    Args:
        lst: a list

    Returns:
        True if length of lst is 1, false ow
    """

    return len(lst) == 1


def length(lst):
    """ Finds if the length of a list
    Args:
        lst: a list

    Returns:
        length of list
    """

    return len(lst)


def onlyActionInstance(stsg, a_id):
    return len(stsg['actions'][a_id]['vertices']) == 1


def iterate(data, func, num, args):
    """ Iterates through a data structure

    Args:
        data: an iterable data structure
        func: a function that returns true or false
        num: an integer i. i=...
            None: iterate entire datastructure
            1: return first time func(data[_]) = true
            2: return second time func(data[_]) = true
            -1: return last time func(data[_]) = true
        args: any extra arguments to func

    Returns:
        Either a list of all instances in which the item satisfies
        the function requirements, or the num item to satify the
        function requirements
    """

    true = []

    cnt = 0
    for datum in data:
        if func(datum, args):
            true.append(datum)

            cnt = cnt + 1
            if cnt == num:
                break

    if num is None:
        return true

    if num > 0:
        num = num - 1

    if abs(num) >= len(true):
        return

    return true[num]


def getVertex(stsg, v_class, frame):
    """ Returns the vertex associated with a class and frame

    Args:
        stsg: the spatio-temporal scene graph
        v_class: the class (ex: o9)
        frame: the frame number

    Returns:
        The corresponding vertex object
    """

    v_id = "%s/%s" % (v_class, frame)
    tp = grammar.vType(v_class)

    return stsg['stsg'][tp][v_id]


def getVertexList(stsg, ids, node_type):
    """ Turns every vertex id into a vertex

    Args:
        stsg: the spatio-temporal scene graph
        ids: a list of object ids
        node_type: the type of node (ex: 'action')

    Returns:
        A list of the corresponding vertices for each id
    """
    vertex_list = []

    for v_id in ids:
        vertex = stsg['stsg'][node_type][v_id]
        vertex_list.append(vertex)

    return vertex_list


def AND(items):
    """ Determines if all bools in an array are true

    Args:
        items: a list of booleans

    Returns: true if all items in the list are true, else false
    """
    for boolean in items:
        if not boolean:
            return False

    return True


def XOR(b1, b2):
    """ Determines if exactly one of two items is true

    Args:
        b1: a boolean
        b2: a boolean

    Returns: true exactly one boolean is true, else false
    """

    return b1 ^ b2


def comparative(first, second, comparative_type, metric):
    """ Returns the larger or smaller item

    Args:
        first: first item
        second: second item
        comparative_type: string type of comparison
            "less": return the smaller
            "more": return the larger
        metric: the part of the data objects to reference

    Returns: item with more or less, or item 1 if equal
    """
    if comparative_type != 'less' and comparative_type != 'more':
        print("Comparative: invalid type argument")

    if metric is not None:
        item1 = first[metric]
        item2 = second[metric]
    else:
        item1 = first
        item2 = second

    if item1 == item2:
        return first

    if comparative_type == "less":
        if item1 < item2:
            return first
        else:
            return second
    else:
        if item1 < item2:
            return second
        else:
            return first


def superlative(items, superlative_type, metric):
    """ Returns the largest or smallest item

    Args:
        items: a list of items to compare
        superlative_type: string type of comparison
            "least": return the smaller
            "most": return the larger
        metric: the part of the data objects to reference

    Returns: a list of items with the largest or smallest amount
    """
    if superlative_type != 'least' and superlative_type != 'most':
        print("Superlative: invalid type argument: ", superlative_type)

    if metric is None:
        items_by_metric = items
    else:
        items_by_metric = editList(items, metric)

    if superlative_type == 'least':
        lowest_value = 99999999
        lowest = []

        for idx in range(len(items_by_metric)):
            val = items_by_metric[idx]
            if val == lowest_value:
                lowest.append(items[idx])
            elif val < lowest_value:
                lowest_value = val
                lowest = [items[idx]]
        return lowest
    else:
        highest_value = -99999999
        highest = []

        for idx in range(len(items_by_metric)):
            val = items_by_metric[idx]
            if val == highest_value:
                highest.append(items[idx])
            elif val > highest_value:
                highest_value = val
                highest = [items[idx]]
        return highest


def objRelExists(stsg, f_id, obj, rel):
    """ TODO:

    Args:

    Returns:
    """

    rels = select(stsg, ['frames', f_id, grammar.vType(rel), 'vertices'])

    if not exists(rels, 'class', rel):
        return False

    rel_vertex = getVertex(stsg, rel, f_id)

    objs_in_rel = select(rel_vertex, ['objects'])

    return exists(objs_in_rel, 'class', obj)


def chooseOne(data, possibles):
    """ Finds which is present in list
    TODO:

    Args:

    Returns: None if more or less than one is present
    """

    def equals(name, args):
        return name in possibles

    exist = iterate(data, equals, None, None)

    if len(exist) != 1:
        return

    return exist[0]
