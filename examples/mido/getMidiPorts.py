import mido

print("Available MIDI Input Ports:")
print(mido.get_input_names())

print("Available MIDI Output Ports:")
print(mido.get_output_names())
