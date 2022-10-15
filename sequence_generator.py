import json
import numpy as np
from operator import itemgetter
from chord_distribution_generator import load_json

current_state_sampling_dist = [0.4, 0.25, 0.1, 0.1, 0.1, 0.05]
baroque_markov_model_distributions_order_1 = load_json('baroque_markov_model_distributions_order_1.json')
baroque_markov_model_distributions_order_2 = load_json('baroque_markov_model_distributions_order_2.json',
                                                       tuple_the_keys=True)
chopin_markov_model_distributions_order_1 = load_json('chopin_markov_model_distributions_order_1.json')
chopin_markov_model_distributions_order_2 = load_json('chopin_markov_model_distributions_order_2.json',
                                                      tuple_the_keys=True)


# the following function identifies a perfect cadence:
def is_perfect_authentic_cadence(seq):
    if (seq[0] == '0II65' or seq[0] == '0II6' or seq[0] == '0I64') \
            and (seq[1] == '0V7' or seq[1] == '0V') and seq[2] == '0I':
        return True
    else:
        return False


# the following function identifies a half cadence:
def is_half_cadence(seq):
    if (seq[0] == '7V7' or seq[0] == '7V') and seq[1] == '0V' and seq[2] != '0I' and seq[2] != '0VI':
        return True
    else:
        return False


# the following function generates one chord (string). the argument previous_state can account for tuple of any length:
def generate_chord(markov_model_distributions_dictionary, previous_state):
    # first step is finding possible distribution of current_state candidates w.r.t a given previous state.
    dict_to_tuple_list = []
    for current_state_candidate, probability in markov_model_distributions_dictionary[previous_state].items():
        dict_to_tuple_list.append((current_state_candidate, probability))
    dict_to_tuple_list = sorted(dict_to_tuple_list, key=itemgetter(1), reverse=True)

    # second step is pulling the chords from the sorted chord-probability tuples.
    sorted_chord_list = []
    for current_state_probability_pair in dict_to_tuple_list:
        sorted_chord_list.append(current_state_probability_pair[0])

    # third step is making sure the sorted current_states list is compatible with the current_state
    # sampling distribution, and if the current_state sampling distribution is cut, then the values
    # should be normalized, so they add up to 1.
    compatible_sorted_chord_list = sorted_chord_list[:min(len(current_state_sampling_dist),
                                                          len(sorted_chord_list))]
    compatible_sampling_distribution = current_state_sampling_dist[:min(len(current_state_sampling_dist),
                                                                        len(sorted_chord_list))]
    compatible_normalized_sampling_distribution = compatible_sampling_distribution / \
                                                  np.sum(compatible_sampling_distribution)

    current_state = np.random.choice(compatible_sorted_chord_list, 1, p=compatible_normalized_sampling_distribution)

    return current_state[0]


# the following function generates a spontaneous progression based on a certain distribution (corpus), as long as it
# did not run into a perfect cadence:
def generate_sequence(markov_model_distributions, model_order):
    sequence = ['0I', '0IV', '0V']
    while not is_perfect_authentic_cadence(seq=[sequence[-3], sequence[-2], sequence[-1]]):
        if model_order == 1:
            generated_chord = generate_chord(markov_model_distributions, previous_state=sequence[-1])
        elif model_order == 2:
            generated_chord = generate_chord(markov_model_distributions, previous_state=(sequence[-2], sequence[-1]))
        else:
            generated_chord = generate_chord(markov_model_distributions, previous_state=(sequence[-3],
                                                                                         sequence[-2],
                                                                                         sequence[-1]))

        sequence.append(generated_chord)

    return sequence


with open('baroque_markov_model_order_1_generated_sequence.json', 'w') as f:
    json.dump(generate_sequence(baroque_markov_model_distributions_order_1, model_order=1), f)

with open('baroque_markov_model_order_2_generated_sequence.json', 'w') as f:
    json.dump(generate_sequence(baroque_markov_model_distributions_order_2, model_order=2), f)

with open('chopin_markov_model_order_1_generated_sequence.json', 'w') as f:
    json.dump(generate_sequence(chopin_markov_model_distributions_order_1, model_order=1), f)

with open('chopin_markov_model_order_2_generated_sequence.json', 'w') as f:
    json.dump(generate_sequence(chopin_markov_model_distributions_order_2, model_order=2), f)