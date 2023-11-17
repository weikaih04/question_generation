

def find_char_location(verts, starts, phrases, order, q=None):
    sg = {}

    length = len(starts)
    for arg_idx in order:
        home_base = starts[arg_idx]
        phrase = phrases[arg_idx]
        max_e = -100
        for x in verts[arg_idx]:
            s, e = x
            v = verts[arg_idx][(s, e)]

            # This is when we don't hard code the phrase length
            # but it's not an "all video"
            if e == -1 and s != -1:
                e = len(phrase)
            # For the phrase "In the video"
            elif len(phrase) > 0 and phrase[0] == 'I':
                s = 0
                e = 12
            # These are to help with the start_phrase of times.
            if len(phrase) > 0 and phrase[0] != 'I':
                if len(phrase) < e:
                    e = len(phrase)
                if phrase[0:1].isupper():
                    s -= 1

            # Find start and end in whole sentence
            new_s = home_base + s
            new_e = new_s + (e - s)

            if prnt:
                print(home_base, s, e, new_s, new_e)

            sg[(new_s, new_e)] = v

            if max_e < e:
                max_e = e

        # if the phrase is nothing, don't adjust starts
        if phrase == '':
            continue
        for i in range(length):
            if i == arg_idx:
                continue
            if prnt:
                print()
                print('starts B', starts)
                print('sarts[i] ', starts[i], 'max_e', max_e)
                print("adjust starts[%s] to be %s" % (i, starts[i] + max_e))
            starts[i] += max_e

    return sg


prnt = False

verts = None
starts = None
phrases = None
order = None
q = None

if prnt:
    output = find_char_location(verts, starts, phrases, order)

    print(q)

    for s, e in output:
        print(s, e, e - s, len(q[s:e]), q[s:e], output[(s, e)])
