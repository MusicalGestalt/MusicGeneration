"""Tools for generating scales."""
import functools
import sys
tone = 2
semitone = 1
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



# Should a scale of C contain a C note in 2 octaves?
# It seems that this is true for major_intervals, but not for
# major_pentatonic_intervals (for example)
# Since it's always the case that a root note, x, and 'x+octave'
# are both in the scale, I think we can omit 'x+octave'. What do you think?
major_intervals = [0, tone, tone, semitone, tone, tone, tone, semitone]
natural_minor_intervals = [0, tone, semitone, tone, tone, semitone, tone, tone]
harmonic_minor_intervals = [0, tone, semitone, tone, tone, semitone, tone, semitone]
dorian_mode_intervals = [0, tone,semitone,tone,tone,tone,semitone,tone]
lydian_mode_intervals = [0, tone,tone,tone,semitone,tone,tone,semitone]
mixolydian_mode_intervals = [0, tone,tone,semitone,tone,tone,semitone,tone]
aeolian_mode_intervals = [0, tone,semitone,tone,tone,semitone,tone,tone]
locrian_mode_intervals = [0, semitone,tone,tone,semitone,tone,tone,tone]
major_pentatonic_intervals = [0, tone, tone, tone*2,tone]
minor_pentatonic_intervals = [0, tone + semitone, tone, tone, tone + semitone]
# Should this also start with zero? (as I've modified it)
chromatic_scale_intervals = [0] + [semitone for _ in range(11)]
# [This let me shorten the scalify function (below)]
# If all lists start with 0, maybe we can remove the 0 from all lists, since it's a given
# that the root is a member of the interval.


_intervals = dict(
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


# I think it would also be nice to be able to generate N notes
# from a given scale. We could simply add another input parameter
# to scale: e.g scale(root, intervals, num_notes=None)
# If None, it will default to returning all notes in the intervals
# (as it currently does).

def scale(root, intervals):
    """Given a root note and a series of intervals, generate 
    a scale based on them.

    >>> scale(60, major_intervals)
    [60, 62, 64, 65, 67, 69, 71, 72]
    >>> scale(60, natural_minor_intervals)
    [60, 62, 63, 65, 67, 68, 70, 72]
    """
    def scalify(accum,x):
        return accum + [accum[-1]+x]
    return functools.reduce(scalify, intervals[1:], [root])

# lift the scales to modules
_mod = sys.modules[__name__]
for (name,intvs) in _intervals.items():
    f = functools.partial(scale,intervals=intvs)
    f.__name__ = name
    f.__doc__ = """Returns a list of {0} notes 
    based on the root note""".format(name.replace("_", " "))
    setattr(_mod, name, f)
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()







