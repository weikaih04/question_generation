import json
import pickle


with open('../data/train_video_names.txt', 'rb') as f:
    train_stsgs = json.load(f)


with open('../data/test_video_names.txt', 'rb') as f:
    test_stsgs = json.load(f)


def getDirect():
    """ make a dictionary of the direct equivalent to each question

    Args:

    Returns:
        saves a dictionary of the direct equivalent of each question
    """
    to_direct = {}
    total = 0

    for i, v_id in enumerate(test_stsgs):
        if i % 100 == 0:
            print(i, len(to_direct))

        # get video
        by_local = {}

        # get questions
        with open('../exports/dataset/all/test/%s.txt' % v_id, 'rb') as f:
            QA = json.load(f)

        total += len(QA)

        # for every question
        for q_id in QA:
            q = QA[q_id]

            loc = q['local'] + '-' + q['attributes']['type'] + '-' + q['metrics']['direct_args']

            if loc not in by_local:
                by_local[loc] = {
                    'direct': [],
                    'indirect': [],
                }

            indirects = q['metrics']['indirects'].count(True)

            if indirects == 0:
                if len(by_local[loc]['direct']) > 0:
                    print()
                    print("double direct!")
                    print(loc)
                    print(q['question'])
                    print(by_local[loc]['direct'][0]['question'])
                by_local[loc]['direct'].append(q_id)

            else:
                by_local[loc]['indirect'].append(q_id)

        this_to_direct = {}

        for loc in by_local:
            if len(by_local[loc]['direct']) == 0:
                continue
            d = by_local[loc]['direct'][0]
            this_to_direct[d] = d

            indirs = by_local[loc]['indirect']

            for i in indirs:
                this_to_direct[i] = d

        to_direct.update(this_to_direct)

    with open('../exports/dataset/to_direct.txt', 'w+') as f:
        json.dump(to_direct, f)


if __name__ == '__main__':
    getDirect()
