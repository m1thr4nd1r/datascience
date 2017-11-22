from collections import Counter
from functools import reduce

import collections
import numpy as np
import pandas as pd
import math

"""

atributo-valor

Quanto menos opções de valor de atributo mais rápido
No caso de Brasil podemos classificar por estado, mas também seria interessante usar por região.

"""
print("Árvore de decisão - ID3\n")

class defaultdict(collections.defaultdict):
    def __missing__(self, key):
        _obj = defaultdict()
        _obj[key] = 0
        return _obj[key];

def gain(storage, attr, attr_objective, DEBUG=False):

    if DEBUG:
        print(storage, attr, attr_objective)
    counter_class = Counter(tennis_data[attr_objective])
    total = len(storage[attr_objective])
    """
    Entropia -> quão balanceado está a base. Quanto maior a entropia menos balanceado está.
     0 - Todos na mesma classe
     1 - Totalmente balanceada
     (0,1) - Valores diferentes
    """
    kk = []
    for name in counter_class:
        if counter_class[name] != total and total != 0:
            kk.append(counter_class[name] / total)
        elif total == 0:
            kk.append(counter_class[name])
        else:
            kk.append(total)

    kkkk = [value * math.log(value, 2) for value in kk]
    goal_entropy = reduce(lambda x, y: - x - y, kkkk)

    classes = storage[attr].unique()
    if DEBUG:
        print('classes', classes)
    dict_sum = {
        'individual': {key: defaultdict() for key in classes},
        'total': defaultdict()
    }
    if DEBUG:
        print('dict_sum',dict_sum)
    for value in storage[attr_objective].unique():

        if DEBUG:
            print('value',value)
        data = storage[storage[attr_objective] == value]
        counter_class = Counter(data[attr])

        for item in counter_class:
            try:
                dict_sum['individual'][item][value] += counter_class[item]
                if DEBUG:
                    print('individual', dict_sum['individual'])
            except:
                dict_sum['individual']['NA'] = dict_sum['individual']['NA'] if 'NA' in dict_sum['individual'] else defaultdict()
                dict_sum['individual']['NA'][value] += counter_class[item]
            dict_sum['total'][item] += counter_class[item]

    if DEBUG:
        print('dict_sum',dict_sum, 'total', total)
    percentage = {item: dict_sum['total'][item] / total for item in dict_sum['total']}
    if DEBUG:
        print('percentage', percentage)
    gain = goal_entropy
    if DEBUG:
        print('goal_entropy', goal_entropy)
    if DEBUG:
        print('\n')
    for item in dict_sum['individual']:
        entropy = 0
        for key in dict_sum['individual'][item]:
            x = dict_sum['individual'][item][key] / dict_sum['total'][item]
            entropy += - x * math.log(x,2)
        gain -= percentage[item] * entropy

    return gain

if __name__ == "__main__":
    tennis_data = pd.read_csv("dataset/tennis.csv", index_col=0)
    attr_objective = tennis_data.columns[-1]
    best = -math.inf
    b_key = None
    for attr in tennis_data.columns[:-1]:
        value = gain(tennis_data, attr, attr_objective)
        print('Gain "%s" related to "%s": %.4f' % (attr, attr_objective, value))
        if value > best:
            best, b_key = value, attr
    print('\n"%s" is the best attribute: %.3f' % (b_key, best))
