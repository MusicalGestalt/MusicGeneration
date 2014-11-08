# TODO(remy): Why is a quarter_note = 32?
# Also, how are "beats" related to ticks?
# e.g. if we have 100 bpm (beats/min), then do we have 3200 ticks/min?
# When you originally mentioned 32, I thought you were referring to
# 32 ticks in a 'bar', so we could fit 32 notes into a bar (at most)
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
