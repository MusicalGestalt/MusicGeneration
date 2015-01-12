"""To run from command line, use: python -m [directory_name]"""


# This code is broken, but checking it in to be fixed later.
# Need to figure out how to import modules together (wavefile and sample_generators)

# from wavefile import WaveFile
# from sample_generators import generators, envelopes

# print("Running main code")



# def test(self):
#     saw_gen = generators.SawtoothWaveGenerator(330)
#     delay_gen = generators.DelayedGenerator(source=saw_gen, start_time=0.0)
#     # Total note length of 1 second
#     vol_env = envelopes.StandardEnvelope(
#         source=delay_gen,
#         peak=0.9,
#         level=0.8,
#         attack=0.1,
#         decay=0.1,
#         sustain=0.6,
#         release=0.2)
#     data = vol_env.get(5 * SAMPLING_RATE)
#     with WaveFile("tone1.wav") as wave_file:
#         wave_file.writeData(data)


# test()
