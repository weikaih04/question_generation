import generate_questions
from multiprocessing import Process
import sys


if __name__ == '__main__':
    print("done imports")
    group = sys.argv[1:][0]
    adding = sys.argv[1:][1]
    version = sys.argv[1:][2]
    print("Group:", group, "Adding:", adding, 'Version:', version)

    jobs = []
    if group == 'test':
        ranges = [(0, 303), (303, 555), (555, 807), (807, 1059),
                  (1059, 1311), (1311, 1563), (1563, 1814)]
        ranges = [(0, 555), (555, 1059),
                  (1059, 1563), (1563, 1814)]
        #ranges = [(5, 10), (10, 15), (15,20), (20,25), (25, 30)]
        #ranges = [(0, 1)]
    elif group == 'train':
        ranges = [(0, 1110), (1110, 2220), (2220, 3330), (3330, 4440),
                  (4440, 5550), (5550, 6660), (6660, 7787)]
        ranges = [(0, 2220), (2220, 4440),
                  (4440, 6660), (6660, 7787)]

    else:
        print("Invalid group", group)

    for r in ranges:
        if version == 'general':
            p = Process(target=generate_questions.generateQuestions,
                        args=(group, r[0], r[1], True, adding,))
        elif version == 'actionIndirect':
            p = Process(target=generate_questions.generateQuestionsIndirect,
                        args=(group, r[0], r[1], True,))
        else:
            print("invalid version", version)
        jobs.append(p)
        p.start()
