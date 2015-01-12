"""Misc theory functions."""

def ToneToFrequency(tone):
    """Convert a tone to a frequency."""
    # 60=C4 ==> 261.63Hz
    # 69=A4 ==> 440Hz
    return 440.0 * (2.0 ** (1.0/12.0)) ** (tone - 69)

