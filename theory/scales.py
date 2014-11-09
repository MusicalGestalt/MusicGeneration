"""Tools for generating scales."""
import functools
import sys
from .harmonies import tone, semitone
middleC = 60

def note_for_semitones(num):
    """0 = C-1. 1=C#/Db0, 60=C4, etc."""
    notes = ["B#/C", "C#/Db", "D", "D#/Eb", "E", "E#/F", 
        "F#/Gb", "G", "G#/Ab", "A", "A#/Bb", "B/Cb"]
    note = num % 12
    octave = num // 12 - 1
    return "{0}{1}".format(notes[note],octave)

def notes_for_list(l):
    return list(map(note_for_semitones, l))



# TODO(remy): read below
# Should a scale of C contain a C note in 2 octaves? 
# It seems that this is true for major_intervals, but not for
# major_pentatonic_intervals (for example)
# Since it's always the case that a root note, x, and 'x+octave'
# are both in the scale, I think we can omit 'x+octave'. What do you think?
major_intervals = [tone, tone, semitone, tone, tone, tone, semitone]
natural_minor_intervals = [tone, semitone, tone, tone, semitone, tone, tone]
harmonic_minor_intervals = [tone, semitone, tone, tone, semitone, tone, semitone]
dorian_mode_intervals = [tone,semitone,tone,tone,tone,semitone,tone]
lydian_mode_intervals = [tone,tone,tone,semitone,tone,tone,semitone]
mixolydian_mode_intervals = [tone,tone,semitone,tone,tone,semitone,tone]
aeolian_mode_intervals = [tone,semitone,tone,tone,semitone,tone,tone]
locrian_mode_intervals = [semitone,tone,tone,semitone,tone,tone,tone]
major_pentatonic_intervals = [tone, tone, tone*2,tone]
minor_pentatonic_intervals = [tone + semitone, tone, tone, tone + semitone]
chromatic_scale_intervals = [semitone for _ in range(11)]

intervals = dict(
    major=major_intervals,
    natural_minor=natural_minor_intervals,
    harmonic_minor=harmonic_minor_intervals,
    dorian_mode=dorian_mode_intervals,
    lydian_mode=lydian_mode_intervals,
    mixolydian_mode=mixolydian_mode_intervals,
    aeolian_mode=aeolian_mode_intervals,
    locrian_mode=locrian_mode_intervals,
    chromatic=chromatic_scale_intervals,
    minor_pentatonic=minor_pentatonic_intervals,
    major_pentatonic=major_pentatonic_intervals
    )

def scale(root, intervals, num_notes=None):
    """Given a root note and a series of intervals, generate 
    a scale based on them. num_notes will allow you to select
    subset of the scale, or continue the scale into additonal
    octaves.

    >>> scale(60, major_intervals)
    [60, 62, 64, 65, 67, 69, 71, 72]
    >>> scale(60, natural_minor_intervals)
    [60, 62, 63, 65, 67, 68, 70, 72]
    """
    def scalify(accum,x):
        return accum + [accum[-1]+x]
    res = functools.reduce(scalify, intervals, [root])
    if num_notes == None: return res
    if num_notes <= len(res): return res[:num_notes]
    return res[:-1] + scale(res[-1],intervals,num_notes-len(res))


# lift the scales to modules
_mod = sys.modules[__name__]
for (name,intvs) in intervals.items():
    f = functools.partial(scale,intervals=intvs)
    f.__name__ = name
    f.__doc__ = """Returns a list of {0} notes 
    based on the root note""".format(name.replace("_", " "))
    setattr(_mod, name, f)
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()







