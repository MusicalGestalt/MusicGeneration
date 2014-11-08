# Here's the logic- a single "beat", musically, can sub-divided indefinitely
# The smallest you'll usually see marked in music is 32nd notes.
# Hence, 32 beats per quarter note (assuming a quarter note gets one beat)
# Long term, we'll probably replace these with functions so we can do things
# like 2/2 time (half note gets one beat), and 6/8 time (eight note gets one beat)
# This version covers the most common case, though.
# Rememeber, just because there are 32 ticks per beat, they're just POTENTIAL ticks
# We only need to track the ticks on which an event happens.
ticks_per_beat = 32
quarter_note = ticks_per_beat
eight_note = quarter_note / 2
sixteenth_note = quarter_note / 4
thirty_second_note = quarter_note / 8
half_note = quarter_note * 2
whole_note = quarter_note * 4
quarter_note_triplet = half_note / 3
eight_note_triplet = quarter_note / 3
sixtheenth_note_triplet = eight_note / 3
thirty_second_note_triplet = sixteenth_note_triplet / 3
