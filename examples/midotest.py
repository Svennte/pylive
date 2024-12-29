import mido

print("Available MIDI ports:")
print(mido.get_input_names())
print(mido.get_output_names())
