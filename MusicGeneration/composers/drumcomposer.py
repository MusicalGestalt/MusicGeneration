"""DrumComposers compuse music for drums."""
from . import EventSender, EventReceiver, BaseComposer
from MusicGeneration.music import Phrase
import itertools

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
default_drums = {
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
          drum_type_mapping = default_drums
        else:
          self.drum_type_mapping = drum_type_mapping

