import mido
import time

# Set your variables here
physicalMidi = 'Launchpad MK2'  # Name of the physical MIDI device
virtualOutputFromDAW = 'Launchpad_VIn'  # Virtual MIDI input (from DAW)
virtualInputToDAW = 'Launchpad_VOut'  # Virtual MIDI output (to DAW)

callbacks = {}  # Dictionary to store callbacks

def addCallback(value, callbackfunc):
    """
    Register a callback function for a specific MIDI value.
    :param value: The MIDI note or control value to trigger the callback.
    :param callbackfunc: The function to execute when the value is received.
    """
    callbacks[value] = callbackfunc
    print(f"Callback added for value {value}.")

def executeCallbacks(msg):
    """
    Check if the message triggers any registered callbacks and execute them.
    :param msg: The MIDI message to check.
    """
    if hasattr(msg, 'note') and msg.note in callbacks:
        print(f"Executing callback for note {msg.note}")
        callbacks[msg.note](msg)
    elif hasattr(msg, 'control') and msg.control in callbacks:
        print(f"Executing callback for control {msg.control}")
        callbacks[msg.control](msg)

def find_midi_port(port_name, available_ports):
    """
    Find a MIDI port that starts with the given port name, ignoring trailing numbers.
    """
    for port in available_ports:
        if port.startswith(port_name):
            return port
    raise ValueError(f"No MIDI port found matching name: {port_name}")

def StartMirrorMidi():
    """
    Start the MIDI mirroring process.
    """
    # Get the available MIDI ports
    available_inputs = mido.get_input_names()
    available_outputs = mido.get_output_names()

    try:
        # Find matching ports dynamically
        physical_input_port = find_midi_port(physicalMidi, available_inputs)
        physical_output_port = find_midi_port(physicalMidi, available_outputs)
        virtual_input_port = find_midi_port(virtualOutputFromDAW, available_inputs)
        virtual_output_port = find_midi_port(virtualInputToDAW, available_outputs)
    except ValueError as e:
        print(e)
        return

    # Open the ports non-exclusively if supported by mido
    with mido.open_input(physical_input_port) as physical_input, \
         mido.open_output(physical_output_port) as physical_output, \
         mido.open_input(virtual_input_port) as virtual_input, \
         mido.open_output(virtual_output_port) as virtual_output:

        print("Listening for MIDI messages...")

        while True:
            # Handle messages from the virtual input (DAW to physical device)
            for msg in virtual_input.iter_pending():
                print(f"[Virtual Port Input] Received: {msg}")
                executeCallbacks(msg)  # Check and execute callbacks
                physical_output.send(msg)  # Forward DAW messages to the physical device
                print(f"[Physical Port Output] Forwarded: {msg}")

            # Handle messages from the physical input (Physical device to DAW)
            for msg in physical_input.iter_pending():
                print(f"[Physical Port Input] Received: {msg}")
                executeCallbacks(msg)  # Check and execute callbacks
                virtual_output.send(msg)  # Forward physical messages to the DAW
                print(f"[Virtual Port Output] Forwarded: {msg}")

# Example callback function
def example_callback(msg):
    print(f"Callback triggered! Message: {msg}")

# Adding a test callback
addCallback(61, example_callback)  # Example: Trigger callback on MIDI note 60

# Uncomment the line below to start the mirror process when the script runs
StartMirrorMidi()
