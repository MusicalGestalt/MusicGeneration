"""DrumComposer Objects compuse music for drums."""
from MusicGeneration.composers import EventSender, EventReceiver, BaseComposer
from MusicGeneration.music import Phrase
from MusicGeneration.composers import SimpleComposer
from MusicGeneration.rhythm import fourfour
from MusicGeneration.rhythm.interval_sequences import PatternIntervalGenerator
from MusicGeneration.theory.tone_sequences import ConstantMelodyGenerator
import itertools
import random

# Main drum types
BASS = 1
SNARE = 2
TOM_SMALL = 3
TOM_BIG = 4
TOM_FLOOR = 5
HIHAT_OPEN = 6
HIHAT_CLOSED = 7
CRASH = 8
RIDE = 9
CLICK = 10

# Sound attributes
QUIET = 100
LOUD = 101

# Mapping the default drum WAV files to drum types
DEFAULT_DRUMS = {
    1: (CLICK),
    7: (CLICK),
    9: (CLICK),
    # 14: Click, knock?
    # 16: CLAP
    2: (SNARE, QUIET),
    # 3 = DRUM ROLL?
    # 5, 6 = DRUM ROLL?
    4: (SNARE, QUIET),
    10: (BASS),
    8: (SNARE, LOUD),
    11: (SNARE, LOUD),
    15: (SNARE, LOUD),
    17: (SNARE, LOUD),
    12: (BASS),
    13: (BASS),
    24: (TOM_SMALL),
    25: (TOM_SMALL),
    27: (TOM_SMALL),
    18: (TOM_BIG),
    20: (TOM_BIG),
    22: (TOM_FLOOR),
    19: (HIHAT_OPEN),
    23: (HIHAT_OPEN),
    21: (HIHAT_CLOSED),
    31: (HIHAT_CLOSED),
    26: (CRASH),
    32: (CRASH),
    34: (CRASH),
    28: (RIDE),
    30: (RIDE),
    36: (RIDE),
}

class DrumComposer(BaseComposer):
    """Base class for Composers that create drum music."""
    def __init__(self, drum_type_mapping=None):
        # TODO(oconaire): Finish work on this class
        if drum_type_mapping is None:
          self.note_to_drum_type = DEFAULT_DRUMS
        else:
          self.note_to_drum_type = drum_type_mapping
        # Setup the inverse mapping: drum_type --> note_num
        self.drum_type_to_notes = {}
        for (note, drum_type) in self.note_to_drum_type.items():
          if drum_type in self.drum_type_to_notes:
            self.drum_type_to_notes[drum_type].append(note)
          else:
            self.drum_type_to_notes[drum_type] = [note]

    def getDrumNote(self, drum_type, selection=-1):
        if selection < 0:
            return random.choice(self.drum_type_to_notes[drum_type])
        return self.drum_type_to_notes[drum_type][selection]


class SimpleDrumComposer(SimpleComposer, DrumComposer):
    def __init__(self, pattern, drum_type, drum_type_mapping=None, time_signature=fourfour):
        DrumComposer.__init__(self, drum_type_mapping)
        interval_generator = PatternIntervalGenerator(pattern, time_signature=time_signature)
        drum_note = self.getDrumNote(drum_type)
        melody_generator = ConstantMelodyGenerator(drum_note)
        SimpleComposer.__init__(self, interval_generator, melody_generator,
                                default_time_sig=time_signature, default_duration=time_signature.eighth_note)

