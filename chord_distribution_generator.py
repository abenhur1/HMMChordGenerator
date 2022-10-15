import json


# function loads json:
def load_json(file_path, tuple_the_keys=False):
    json_file = open(file_path) # reading from json
    output = json.load(json_file) # array of arrays

    if tuple_the_keys:  # if order>1 we deal with string keys (since json.dump can't process tuples as keys) so we
                        # need to convert string back to tuple
        tuple_keys_output = {}
        for key, value in output.items():
            tuple_keys_output[tuple(key.split(','))] = value
        output = tuple_keys_output

    return output


# function merges all tracks in tracks_arrays:
def concatenate_tracks(tracks_arrays):
    corpus = []
    for track in tracks_arrays:
        for chord in track:
            corpus.append(chord)

    return corpus


# the following function initiates the probability distributions containers for markov model of order 1:
def create_markov_model_distributions(corpus, model_order):
    previous_states_dict = {}   # the keys of previous_states_dict are all the different
                                # past n chords (order n means key comprises n entities). the
                                # values are dictionaries. keys and values are next explained.
    if model_order == 1:
        distinct_corpus_chords = set(corpus)
        for chord in distinct_corpus_chords:
            previous_states_dict[chord] = {}    # the outer dictionary's value is also a dictionary.
                                                # its values are the distributions for all distinct
                                                # chords (every chord is a key) that happened to appear
                                                # after the outer dictionary's key. in actuality, they
                                                # are candidates for being generated as current_state.

            # the following for loop initiates the inner dictionaries with (only) the current_state
            # candidates (w.r.t. the given key - a chord), each gets a value of 0.
            for chord_index in range(len(corpus)-1):
                previous_check = corpus[chord_index]
                current_state = corpus[chord_index+1]
                if previous_check == chord:
                    previous_states_dict[chord][current_state] = 0

        # the following for loop populates the inner dictionaries with their distributions as current_state
        # candidates (w.r.t. the given key - a chord).
        for chord in distinct_corpus_chords:
            for chord_index in range(len(corpus)-1):
                previous_check = corpus[chord_index]
                current_state = corpus[chord_index+1]
                if previous_check == chord:
                    previous_states_dict[chord][current_state] += 1 / corpus.count(previous_check)

    if model_order == 2:
        corpus_pairs = [] # now a previous_state is a tuple
        for chord_index in range(len(corpus)-1):
            corpus_pairs.append((corpus[chord_index], corpus[chord_index+1]))

        distinct_corpus_pairs = set(corpus_pairs)
        for pair in distinct_corpus_pairs:
            previous_states_dict[pair] = {}
            for chord_index in range(len(corpus_pairs)-1):
                previous_check = corpus_pairs[chord_index]
                current_state = corpus[chord_index+2]
                if previous_check == pair:
                    previous_states_dict[pair][current_state] = 0

        for pair in distinct_corpus_pairs:
            for chord_index in range(len(corpus_pairs)-1):
                previous_check = corpus_pairs[chord_index]
                current_state = corpus[chord_index+2]
                if previous_check == pair:
                    previous_states_dict[pair][current_state] += 1 / corpus_pairs.count(previous_check)

        stringed_previous_states_dict = {} # convert tuple into string since json.dump can't process tuples as keys
        for key, value in previous_states_dict.items():
            stringed_previous_states_dict[','.join(key)] = value
        previous_states_dict = stringed_previous_states_dict # rename into original name so to align with order=1 dict

    return previous_states_dict


# writing into json (every corpus+order separately):
baroque_tracks_array = load_json('manual_baroque_tracks.json')
baroque_corpus = concatenate_tracks(baroque_tracks_array)

chopin_tracks_array = load_json('manual_chopin_tracks.json')
chopin_corpus = concatenate_tracks(chopin_tracks_array)

with open('baroque_markov_model_distributions_order_1.json', 'w') as f:
    json.dump(create_markov_model_distributions(baroque_corpus, model_order=1), f)

with open('baroque_markov_model_distributions_order_2.json', 'w') as f:
    json.dump(create_markov_model_distributions(baroque_corpus, model_order=2), f)

with open('chopin_markov_model_distributions_order_1.json', 'w') as f:
    json.dump(create_markov_model_distributions(chopin_corpus, model_order=1), f)

with open('chopin_markov_model_distributions_order_2.json', 'w') as f:
    json.dump(create_markov_model_distributions(chopin_corpus, model_order=2), f)
