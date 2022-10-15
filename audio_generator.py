from midiutil.MidiFile import MIDIFile
from chord_distribution_generator import load_json
from sequence_generator import is_half_cadence, is_perfect_authentic_cadence, generate_chord

baroque_markov_model_order_1_generated_sequence = load_json('baroque_markov_model_order_1_generated_sequence.json')
baroque_markov_model_order_2_generated_sequence = load_json('baroque_markov_model_order_2_generated_sequence.json')
chopin_markov_model_order_1_generated_sequence = load_json('chopin_markov_model_order_1_generated_sequence.json')
chopin_markov_model_order_2_generated_sequence = load_json('chopin_markov_model_order_2_generated_sequence.json')

# in order to print a progressions that is compatible with functional notation, we create the following dictionary:
midi_notation_to_functional_dictionary = {'0': '', '2': '/II', '5': '/IV', '7': '/V', '9': '/VI'}

# in order to create the complementary midi file, we create a dictionary that maps functional symbols to pitches:
c_modes_pitch_dictionary = {'I': [48, 64, 67, 72], 'I6': [52, 64, 67, 72], 'I64': [43, 64, 67, 72],
                            'I7': [48, 59, 64, 67], 'I9': [48, 62, 64, 72], 'I2': [47, 64, 67, 72],
                            'bI': [], 'bI64': [43, 63, 67, 72],
                            'V': [43, 62, 67, 71], 'V6': [47, 55, 67, 74], 'V7': [43, 62, 65, 71],
                            'V65': [47, 65, 67, 74], 'V43': [50, 65, 67, 71], 'V42': [53, 62, 67, 71],
                            'V9': [43, 57, 62, 71],
                            'VII6': [50, 62, 65, 71], 'VII7o/': [47, 65, 69, 74], 'VII7o': [47, 65, 68, 74],
                            'VII43o': [53, 62, 68, 71], 'VII': [47, 53, 62, 74], 'VII42o': [44, 62, 65, 71],
                            'VII4+o': [48, 65, 68, 71, 74], 'VII65o/': [50, 65, 69, 71],
                            'II': [50, 62, 65, 69], 'II6': [41, 62, 65, 69], 'II7': [50, 57, 65, 72],
                            'II65': [41, 62, 69, 72], 'II43': [45, 62, 65, 72], 'II42': [48, 65, 69, 74],
                            'II64': [45, 62, 65, 74],
                            'IV': [41, 65, 69, 72], 'IV6': [45, 57, 65, 72], 'IV64': [48, 65, 69, 72],
                            'IV7': [41, 64, 69, 72], 'IV42maj': [53, 57, 65, 72], 'IV7maj': [41, 69, 72, 76],
                            'bIV': [41, 65, 68, 72], 'bIV64': [48, 65, 68, 72],
                            'VI': [45, 57, 64, 72], 'VI6': [48, 57, 64, 69], 'VI9': [45, 60, 64, 71],
                            'VI7': [45, 64, 67, 72], 'VI65': [48, 57, 67, 69], 'VI43': [52, 64, 67, 72],
                            'VI42': [43, 64, 69, 72], '#VI': [45, 57, 64, 73],
                            'III': [40, 64, 67, 71], 'III6': [43, 55, 64, 71], 'III7': [52, 59, 67, 74],
                            'bIII': [39, 63, 67, 70],
                            'It+6': [44, 60, 66, 72], 'Fr+6': [44, 62, 66, 72], 'Ger+6': [44, 63, 66, 72]}


def generate_midi_sequence(generated_midi_notation_sequence, start_time=0, tempo=120, track=0, volume=100):
    # create MIDI object
    mf = MIDIFile(1)  # only 1 track
    mf.addTrackName(track, start_time, "Sample Track")
    mf.addTempo(track, start_time, tempo)

    # add some notes
    channel = 0
    onset_time = -2
    sequence_length = len(generated_midi_notation_sequence)

    for chord_index in range(sequence_length):
        chord = generated_midi_notation_sequence[chord_index]
        if 4 <= chord_index < sequence_length-1 \
                and is_half_cadence(seq=[generated_midi_notation_sequence[chord_index-2],
                                         generated_midi_notation_sequence[chord_index-1],
                                         generated_midi_notation_sequence[chord_index]]):
            current_onset = 4
            duration = 4
        elif is_perfect_authentic_cadence(seq=[generated_midi_notation_sequence[chord_index-2],
                                               generated_midi_notation_sequence[chord_index-1],
                                               generated_midi_notation_sequence[chord_index]]) \
                and chord_index >= 4:
            current_onset = 4
            duration = 4

        else:
            current_onset = 2
            duration = 2

        onset_time += current_onset

        chord_pitches = c_modes_pitch_dictionary[chord[1:]]

        # add the chord's notes (pitches) assign them volume. Bass gets higher volume.
        for pitch_index in range(len(chord_pitches)):
            pitch = chord_pitches[pitch_index]
            if pitch_index == 0:
                volume = volume*1.25
            else:
                volume = 100

            # tonicization to upwards than dominant may sound too high.
            if chord[0] > 7:
                pitch += int(chord[0]) - 12
            else:
                pitch += int(chord[0])

            mf.addNote(track, channel, pitch, onset_time, duration, volume)

    return mf


# the following function modifies the sequence to full functional notation using
# midi_notation_to_functional_dictionary (for pretty printing):
def midi_notation_to_functional(generated_midi_notation_sequence):
    generated_functional_notated_sequence = []
    for chord in generated_midi_notation_sequence:
        generated_functional_notated_sequence.append(chord[1:] + midi_notation_to_functional_dictionary[chord[0]])

    return generated_functional_notated_sequence


# first stage of results - spontaneous generation of progressions:
midifile_baroque_1 = generate_midi_sequence(baroque_markov_model_order_1_generated_sequence)
with open("baroque_output_order_1.mid", 'wb') as outf:
    midifile_baroque_1.writeFile(outf)

midifile_baroque_2 = generate_midi_sequence(baroque_markov_model_order_2_generated_sequence)
with open("baroque_output_order_2.mid", 'wb') as outf:
    midifile_baroque_2.writeFile(outf)

midifile_chopin_1 = generate_midi_sequence(chopin_markov_model_order_1_generated_sequence)
with open("chopin_output_order_1.mid", 'wb') as outf:
    midifile_chopin_1.writeFile(outf)

midifile_chopin_2 = generate_midi_sequence(chopin_markov_model_order_2_generated_sequence)
with open("chopin_output_order_2.mid", 'wb') as outf:
    midifile_chopin_2.writeFile(outf)

print('baroque order 1: ', midi_notation_to_functional(baroque_markov_model_order_1_generated_sequence))
print('baroque order 2: ', midi_notation_to_functional(baroque_markov_model_order_2_generated_sequence))
print('chopin order 1: ', midi_notation_to_functional(chopin_markov_model_order_1_generated_sequence))
print('chopin order 2: ', midi_notation_to_functional(chopin_markov_model_order_2_generated_sequence))


# # second stage of results - generating a chord w.r.t previous chord/s
# predicted_state = generate_chord(chopin_markov_model_generated_sequence, '??')
