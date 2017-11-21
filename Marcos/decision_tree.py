from collections import Counter
# from functools import reduce

import numpy as np
import pandas as pd
import math

"""

atributo-valor

Quanto menos opções de valor de atributo mais rápido
No caso de Brasil podemos classificar por estado, mas também seria interessante usar por região.

Entropia -> quão balanceado está a base. Quanto maior a entropia menos balanceado está.
 0 - Todos na mesma classe
 1 - Totalmente balanceada
 (0,1) - Valores diferentes

"""
print("Árvore de decisão - ID3\n")

tennis_data = pd.read_csv("dataset/tennis.csv", index_col=0)

print('Columns: ',list(tennis_data.columns))

counter_class = Counter(tennis_data['play'])
print(counter_class)

# total = reduce((lambda x, y: x + y), map(lambda x: int(counter_class[x]), counter_class))
total = len(tennis_data['play'])
print('Total: ', total)

entropy = [- value * math.log(value, 2) for value in (counter_class[name] / total for name in counter_class)]
print('Entropy: ', entropy)
