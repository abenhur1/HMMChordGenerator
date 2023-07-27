# the following code collects progressions, inserted into an array (array per track). insertion can be manual or using
# a specialized library. moreover, the code writes the arrays into a json file. each file dedicated to a corpus of a
# specific musical type.
# info about chord_extractor library and Chordino from: https://pypi.org/project/chord-extractor/

import json
# from chord_extractor.extractors import Chordino
#
#
# # Setup Chordino with one of several parameters that can be passed
# chordino = Chordino(roll_on=1)
#
# # Optional, only if we need to extract from a file that isn't accepted by librosa
# conversion_file_path = chordino.preprocess('/some_path/some_song.mid')
#
# # Run extraction. accepts only WAV for some reason. This is a Librosa issue probably
# chords = chordino.extract('C:/Users/user/Downloads/??.wav')

# The following arrays are a specific track's progression:
manual_cadences_sequences = ['0I', '0V', '0VI', '0III', '0IV', '0I', '0IV', '0V7', '0I', '0II7', '0V', '0VI',
                             '0II65', '0I64', '0V7', '0I', '0V', '0II', '0VI', '0IV', '0I', '0II65', '0I64', '0V7',
                             '0VI', '0IV6', '0VII', '0III6', '0VI', '0II6', '0V', '0I']

manual_bach_BWV_253 = ['0V6', '0I', '0IV', '5IV7', '5V', '0IV', '0I', '0V7', '0VI', '0IV', '0IV6', '0VII7o', '0I',
                       '0I6', '0V42', '0I6', '0V7', '0I', '0V7', '7V6', '7II7', '7V', '0V6', '7V65', '0V',
                       '9V', '9I', '0I64', '0IV6', '0I', '0V43', '0VI', '0I6', '0I64', '0V7', '0I']
manual_bach_BWV_401 = ['0V43', '0I6', '5V65', '0IV', '0V42', '0I6', '0VI65', '7V7', '0V', '0III', '0VI9', '0V7',
                       '0I', '0IV6', '0IV', '0I64', '0V7', '0I', '7IV', '7VI', '7V65', '9V6', '7II', '0V6', '7II65',
                       '7V42', '0V6', '5V65', '0IV', '0VII43o', '0I6', '0V', '0V6', '0I', '0IV64', '5V7',
                       '2VII7o/', '2I9', '2V43', '0II6', '7V65', '7I7', '0VI9', '0V7', '0I', '0I7', '0I6', '0I64',
                       '0II65',  '0V7', '0I']
manual_bach_BWV_255 = ['0V', '7V7', '0V', '5V7', '0IV', '0VI43', '0VII6', '0I', '0V', '7VII7o/', '0V6', '7V',
                       '0V', '7II65', '7V7', '0V', '0I6', '0VII6', '0I', '0V', '7IV', '7V43', '7VII6',
                       '0V', '7V65', '9VII7o/', '9I', '0II43', '0I64', '0V', '0V7', '0I']
manual_bach_BWV_779 = ['0V7', '7II6', '7V7', '0V', '0V43', '7IV', '7V7', '7VI', '7II7', '7V7', '0V', '0II65',
                       '0V7', '0I', '5V43', '0IV', '0V7', '0VI', '0II7', '0V7', '0I']
manual_bach_BWV_785 = ['0IV', '0V6', '0I', '0VI', '0II', '7V65', '0V',
                       '9VII7o', '9V7', '9I', '5V7', '0IV', '0II', '2VII7o', '2V7', '0II', '0V', '0I', '0IV', '0II',
                       '0VII6', '0V7', '0III', '0IV7', '0II', '0III7', '0I', '0II7', '0VII7o', '0I', '0IV64', '0V43',
                       '0I6', '0V', '0I']
manual_bach_BWV_854 = ['0IV64', '0I', '0II42', '0V65', '0I', '7V65', '0V', '7IV', '7II6', '7V7', '7III6',
                       '7VI7', '7II65', '7V7', '0V6', '7II43', '7V7', '7VI7', '7VII7o', '2VII7o/', '7V7', '0V',
                       '0VI', '0V7', '0I', '0IV64', '0I', '0II42', '0V65', '0I', '7V65', '0V', '7IV', '7II6',
                       '7V7', '7VI', '5V65', '0IV', '0VII7o', '0I']
manual_bach_BWV_860 = ['0IV64', '0VII6', '0I', '7IV', '7V42', '0V6', '7II7', '7V7', '0V', '7II7', '0V6', '7IV',
                       '0V6', '7II7', '0V', '0I', '5VII7o', '0IV', '0VII7o', '0III6', '0VI', '0II6', '0V', '0I6', '0IV',
                       '0VII6', '0III', '0VI6', '0II', '0V6', '0I', '0IV', '0V', '0I', '0IV6', '0II6', '0V7', '0I']
manual_bach_BWV_846 = ['0II42', '0V65', '0I', '7II6', '7V42', '7I6', '7IV42maj', '7II7', '7V7', '0V',
                       '2VII43o', '0II6', '0VII43o', '0I6', '0IV42maj', '0II7', '0V7', '0I', '5V7', '0IV7maj',
                       '7VII7o', '0VII42o', '7V7', '0V', '5V7', '0IV64', '0II42', '0V7', '0I']

manual_baroque_tracks = [manual_cadences_sequences, manual_bach_BWV_860, manual_bach_BWV_785, manual_bach_BWV_854,
                         manual_bach_BWV_779, manual_bach_BWV_401, manual_bach_BWV_255, manual_bach_BWV_253,
                         manual_bach_BWV_846]

manual_cadences_sequences2 = ['0I', '0IV', '0V7']

manual_chopin_op9_no2 = ['0I', '0VII4+o', '0I42', '2V7', '0II', '0V7', '9V65', '0VI', '7VII7o', '0V',
                         '7V6', '0I', '0IV', '0bIV', '0I', '7V65', '7V7', '7VI', '7II', '7V7', '0V',
                         '1V42', '1I6', '2V43', '7V7', '0V7', '0I', '5bI64', '5V', '0V43', '0I',
                         '7V65', '0V7', '0VI', '0bIV', '0I', '0V7', '9V65', '0VI', '7V65', '0V7', '0I']

manual_chopin_op28_no3 = ['7V7', '0V', '7V7', '0V7', '0I', '5V7', '0IV', '0II65', '0V7', '0I']

manual_chopin_op28_no7 = ['2V7', '0II7', '0V9', '0I', '2V7', '0II7', '0V9', '0I']

manual_chopin_op28_no9 = ['0IV', '0II', '0VII65o/', '0V', '0III6', '0VI7', '0II65', '0V', '0VI7', '7V7', '0V65', '0I',
                          '0V', '0bIII', '1V6', '1II64', '1V42', '0IV', '5VII7o', '5II64', '5VII42o', '5I64', '5V7',
                          '0IV', '0V7', '0I', '1III', '1I', '1V', '1I', '1IV', '1II', '3V', '0bIII', '0V', '0I']

manual_chopin_op28_no17 = ['0V7', '5V7', '0IV', '0V7', '2V7', '0II7', '0V7', '0I',
                           '1V7', '8IV', '8II', '5It+6', '5V7', '8VI', '8IV', '8It+6', '8V7', '4bVI', '4Fr+6', '4V',
                           '6bVI', '6Fr+6', '6V', '8Fr+6', '8I64', '8V7', '8I', '8bIV64',
                           '8III', '0bI', '7VII65o', '0V7', '5V7', '0IV', '0V', '2V7', '0II7', '0V7', '0I',
                           '8V65', '8I', '8V7', '8I', '0V', '6I', '5bIV64', '1IV42', '7Ger+6', '7I64', '7V7', '0V',
                           '0I', '5V7', '0IV6', '0V7', '5V43', '0IV64', '0V65', '5V7', '0IV6', '0bIV64', '0II42',
                           '0V65', '0I', '0II65', '0I64', '0V', '0I']

manual_chopin_op7_no2 = ['0bIV64', '0bI', '0V7', '0bI', '0bV64', '7V7', '0V', '0bIV64', '0bVI6',
                         '0bI', '0V7', '0bIV6', '0bVI', '1V7', '1I', '0V7', '0bI',
                         '3V6', '3Ger+6', '3V', '3Ger+6', '5VII43o', '5V43', '0IV', '0bI', '0V7', '0bVI',
                         '1V7', '1I', '0V7', '0bI', '0I', '5V7', '0IV', '0II6o', '0V7', '0I',
                         '0VI', '0VII42o/', '7V7', '0V', '5V7', '0IV', '0II6o', '0V7', '0I']

manual_chopin_op28_no20 = ['0Ib', '0bIV7', '0V7', '0bI', '8I', '8IV', '8V7', '8I', '0V7', '5V7', '0bIV', '0bI',
                           '7V7', '0V', '0bI', '0bVI6', '0VII7o', '0V6', '7II7o/', '0Fr+6', '0V', '0V42', '0bI6',
                           '0bIV', '0V65', '0bI', '0bVI', '1I', '0V7', '0bI']

manual_chopin_nouvelles_etudes_1 = ['0V65', '0bI', '3V65', '0bIII', '7V65', '0V7', '7bI', '7bIV7', '8I6',
                                    '7V7', '7bI', '8V6', '0bVI', '0V65', '0bI', '5V7', '0II42', '0bIV64', '0V7',
                                    '0bI', '0bVI6', '1I', '0V', '0bI']

manual_chopin_mazurka_op63_no2 = ['0bI64', '0V7', '0bI', '0bVI6', '3V65', '0bIII', '1I6', '0II65o/',
                                  '0bI64', '0V7', '0I', '0bI', '0bVI6', '3V7', '0bIII', '3VI', '7V', '3V7', '0bIII',
                                  '7bVI', '7II65o/', '7V', '2V', '7V', '0V43', '0bI', '0V', '0bVI', '1I6', '0II65o/',
                                  '0bI64', '0V7', '0I', '0bI']

manual_chopin_tracks = [manual_cadences_sequences2, manual_chopin_op9_no2 + manual_chopin_op28_no3 +
                        manual_chopin_op28_no7 + manual_chopin_op28_no9, manual_chopin_op28_no17,
                        manual_chopin_op7_no2, manual_chopin_op28_no20, manual_chopin_nouvelles_etudes_1,
                        manual_chopin_mazurka_op63_no2]

# writing into json (every corpus separately):
with open('manual_baroque_tracks.json', 'w') as f:
    json.dump(manual_baroque_tracks, f)
with open('manual_chopin_tracks.json', 'w') as f:
    json.dump(manual_chopin_tracks, f)
