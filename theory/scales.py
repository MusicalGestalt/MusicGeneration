"""Tools for generating scales."""

from functools import reduce
import sys

chromatic_scale = ["A", "A#", "B", 
    "C", "C#", "D", "D#", "E", 
    "F", "F#", "G", "G#"]

major_intervals = [1, 1, 0.5, 1, 1, 1, 0.5]
natural_minor_intervals = [1, 0.5, 1, 1, 0.5, 1, 1]
harmonic_minor_intervals = [1, 0.5, 1, 1, 0.5, 1.5, 0.5]
dorian_mode_intervals = [1,0.5,1,1,1,0.5,1]
lydian_mode_intervals = [1,1,1,0.5,1,1,0.5]
mixolydian_mode_intervals = [1,1,0.5,1,1,0.5,1]
aeolian_mode_intervals = [1,0.5,1,1,0.5,1,1]
locrian_mode_intervals = [0.5,1,1,0.5,1,1,1]

_intervals = dict(
    major=major_intervals,
    natural_minor=natural_minor_intervals,
    harmonic_minor=harmonic_minor_intervals,
    dorian_mode=dorian_mode_intervals,
    lydian_mode=lydian_mode_intervals,
    mixolydian_mode=mixolydian_mode_intervals,
    aeolian_mode=aeolian_mode_intervals,
    locrian_mode=locrian_mode_intervals
    )


def sharpify(note):
    """For simplicity in defining a scale, we're not going to use flats.
    Sharpify removes flats from a note and replaces it with the same tone,
    spelled as a #

    >>> sharpify("Bb")
    'A#'
    >>> sharpify("C#")
    'C#'
    >>> sharpify("D")
    'D'
    """
    if "b" in note:
        idx = chromatic_scale.index(note[0])
        return chromatic_scale[idx - 1]
    return note

def scale(root, intervals):
    """Given a root note and a series of intervals, generate 
    a scale based on them.

    >>> scale("C", major_intervals)
    ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C', None]
    """
    root = sharpify(root)
    idx = chromatic_scale.index(root)
    scale = [root]
    totalSteps = 0
    for step in reversed(intervals):
        totalSteps += int(step * -2)
        scale += [chromatic_scale[idx+totalSteps]]
    # scale += [None] #add rests to all scales
    return list(reversed(scale[1:]))

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
    








