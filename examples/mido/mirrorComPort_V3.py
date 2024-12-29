import mido
import time
import live

class MidiMirror:
    def __init__(self, physicalMidi, virtualOutputFromDAW, virtualInputToDAW):
        self.physicalMidi = physicalMidi
        self.virtualOutputFromDAW = virtualOutputFromDAW
        self.virtualInputToDAW = virtualInputToDAW
        self.callbacks = {}  # Dictionary to store callbacks

    def addCallback(self, value, callbackfunc):
        """
        Register a callback function for a specific MIDI value.
        :param value: The MIDI note or control value to trigger the callback.
        :param callbackfunc: The function to execute when the value is received.
        """
        self.callbacks[value] = callbackfunc
        print(f"Callback added for value {value}.")

    def executeCallbacks(self, msg):
        """
        Check if the message triggers any registered callbacks and execute them.
        :param msg: The MIDI message to check.
        """
        if hasattr(msg, 'note') and msg.note in self.callbacks:
            print(f"Executing callback for note {msg.note}")
            self.callbacks[msg.note](msg)
        elif hasattr(msg, 'control') and msg.control in self.callbacks:
            print(f"Executing callback for control {msg.control}")
            self.callbacks[msg.control](msg)

    def find_midi_port(self, port_name, available_ports):
        """
        Find a MIDI port that starts with the given port name, ignoring trailing numbers.
        """
        for port in available_ports:
            if port.startswith(port_name):
                return port
        raise ValueError(f"No MIDI port found matching name: {port_name}")

    def StartMirrorMidi(self):
        """
        Start the MIDI mirroring process.
        """
        # Get the available MIDI ports
        available_inputs = mido.get_input_names()
        available_outputs = mido.get_output_names()

        try:
            # Find matching ports dynamically
            physical_input_port = self.find_midi_port(self.physicalMidi, available_inputs)
            physical_output_port = self.find_midi_port(self.physicalMidi, available_outputs)
            virtual_input_port = self.find_midi_port(self.virtualOutputFromDAW, available_inputs)
            virtual_output_port = self.find_midi_port(self.virtualInputToDAW, available_outputs)
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
                    self.executeCallbacks(msg)  # Check and execute callbacks
                    physical_output.send(msg)  # Forward DAW messages to the physical device
                    print(f"[Physical Port Output] Forwarded: {msg}")

                # Handle messages from the physical input (Physical device to DAW)
                for msg in physical_input.iter_pending():
                    print(f"[Physical Port Input] Received: {msg}")
                    self.executeCallbacks(msg)  # Check and execute callbacks
                    virtual_output.send(msg)  # Forward physical messages to the DAW
                    print(f"[Virtual Port Output] Forwarded: {msg}")

## Adding callback to duplicate playing clip in Ableton Live
#def duplicate_clip_callback(msg):
#    try:
#        if msg.type == 'note_on' and msg.note == 107 and msg.velocity == 127:
#            set = live.Set(scan=True)
#            for track in set.tracks:
#                if hasattr(track, 'arm') and track.arm:
#                    playing_clip = track.clip_playing
#                    if playing_clip:
#                        print(f"Playing Clip Found: {playing_clip} in Track {track.index}")
#                        empty_slot = next((i for i, clip in enumerate(track.clips) if clip is None), None)
#                        if empty_slot is not None:
#                            live.cmd("/live/clip_slot/duplicate_clip_to", (track.index, playing_clip.index, track.index, empty_slot))
#                            print(f"Duplicated clip to slot {empty_slot}.")
#                        else:
#                            print("No empty slot available.")
#                    return
#    except live.exceptions.LiveConnectionError as e:
#        print(f"Connection error with Ableton Live: {e}")
#    except Exception as e:
#        print(f"Unexpected error: {e}")
#
## Example usage
#midi_mirror = MidiMirror(physicalMidi='Launchpad MK2', virtualOutputFromDAW='Launchpad_VIn', virtualInputToDAW='Launchpad_VOut')
#midi_mirror.addCallback(107, duplicate_clip_callback)  # Trigger duplication on MIDI note 107

# Uncomment the line below to start the mirror process
#midi_mirror.StartMirrorMidi()
