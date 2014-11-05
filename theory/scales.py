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
chromatic_scale_intervals = [semitone for _ in range(12)]

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

def scale(root, intervals):
    """Given a root note and a series of intervals, generate 
    a scale based on them.

    >>> scale(60, major_intervals)
    [60, 62, 64, 65, 67, 69, 71, 72]
    >>> scale(60, natural_minor_intervals)
    [60, 62, 63, 65, 67, 68, 70, 72]
    """
    def scalify(accum,x):
        if len(accum) > 0:
            return accum + [accum[-1]+x[1]]
        else:
            return accum + [x[0] + x[1]]
    return functools.reduce(scalify, [(root,intv) for intv in intervals], [])

# lift the scales to modules
_mod = sys.modules[__name__]
for (name,intvs) in _intervals.items():
    def curry(n,i):
        def f(root):
            return scale(root,i)
        f.__name__ = n
        f.__doc__ = """Returns a list of {0} notes 
        based on the root note""".format(n.replace("_", " "))
        return f
    setattr(_mod, name, curry(name,intvs))
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()







