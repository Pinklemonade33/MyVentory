import itertools


class T1:
    def __init__(self, length, width, height):
        self.length = length
        self.width = width
        self.height = height


a = T1(1, 5, 6)
b = T1(1, 1, 1)
c = T1(4, 4, 4)
lst = [a, b, c]


def check_list(combo, dims):
    pass


dd = {(x for x in itertools.permutations([y.length, y.width, y.height])) for y in lst}
d = list({x for y in lst for x in itertools.permutations([y.length, y.width, y.height])})
e = [list(itertools.combinations(d, x)) for x in range(len(lst), len(d))]
print(dd, sep='\n')
