import matplotlib.pyplot as plt
import numpy as np


print(np.random.choice(['I', 'IV', 'V', 'VI', 'III', 'III6'], 1, p=[0.4, 0.2, 0.1, 0.1, 0.1, 0.1]))

# sequence = ['0I']
# n = 0
# while n < 10:
#     sequence.append(max(markov_model_distributions[sequence[n]], key=markov_model_distributions[sequence[n]].get))
#     n += 1
#
# print(sequence)

dictionary = {"0I, 7II6": {"7V42": 1.0}, "0VI, 0II65": {"0V7": 1.0}, "0IV, 0VII7o": {"0I": 1.0}}
a = []
for key in dictionary.keys():
    a.append(tuple(key.split(',')))
print(a)
for key in a:
    print(len(key), type(key))
