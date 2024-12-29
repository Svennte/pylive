import mido
import live
from virtual_midi import VirtualMidiHandler

def duplicate_playing_clip(message):
    """
    Callback function to handle MIDI messages and trigger duplication.
    """
    if message.type == 'note_on': #and message.note == 7:  # Check for the mapped MIDI note
        print(f"Triggered duplication for note: {message.note}")
        duplicate_playing_clip_to_empty_slot()  # Call your duplication function here
        
def get_playing_clip_in_armed_track():
    """
    Identifies the currently playing clip in the first armed track.
    Returns the playing clip, its track index, and clip index.
    """
    set = live.Set(scan=True)
    for track in set.tracks:
        if hasattr(track, 'arm') and track.arm:
            print(f"Armed Track Found: {track.name}")
            playing_clip = track.clip_playing
            if playing_clip:
                print(f"Playing Clip: {playing_clip} (Track: {track.index}, Clip: {playing_clip.index})")
                return playing_clip, track.index, playing_clip.index, track
            else:
                print(f"No clip is playing in the armed track: {track.name}.")
                return None, None, None, None
    print("No armed tracks found.")
    return None, None, None, None

def duplicate_playing_clip_to_empty_slot():
    try:
        # Step 1: Get the playing clip and its indices
        playing_clip, track_index, clip_index, track = get_playing_clip_in_armed_track()
        if not playing_clip or not track:
            print("No playing clip found to copy.")
            return

        # Step 2: Find an empty slot in the track
        empty_slot = find_empty_clip_slot(track)
        if empty_slot is None:
            print("No empty slots available to copy the clip.")
            return

        print(f"Found empty slot at index {empty_slot}")

        # Step 3: Duplicate the clip to the empty slot
        live.cmd("/live/clip_slot/duplicate_clip_to", (track_index, clip_index, track_index, empty_slot))
        print(f"Duplicated clip from slot {clip_index} to slot {empty_slot}.")

    except live.exceptions.LiveConnectionError as e:
        print(f"Connection error with Ableton Live: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def listen_for_midi(midi_port_name, mapped_note):
    """
    Listens for MIDI input and triggers the duplication function when the mapped key is pressed.

    Args:
        midi_port_name (str): Name of the MIDI port to listen to.
        mapped_note (int): MIDI note number to trigger the script.
    """
    print(f"Listening for MIDI input on port: {midi_port_name}")
    with mido.open_input(midi_port_name) as midi_port:
        for message in midi_port:
            if message.type == 'note_on' and message.note == mapped_note:
                print(f"MIDI key pressed: {message.note}. Triggering script...")
                duplicate_playing_clip_to_empty_slot()

if __name__ == "__main__":
    input_port_name = "Launchpad MK2 1"
    virtual_output_port_name = "LaunchpadVirtual 3"

    # Initialize the MIDI handler
    midi_handler = VirtualMidiHandler(input_port_name, virtual_output_port_name)

    # Add the duplication callback
    midi_handler.add_callback(duplicate_playing_clip)

    # Start the MIDI handler
    midi_handler.start()

    try:
        while True:
            pass  # Keep the main thread alive
    except KeyboardInterrupt:
        midi_handler.stop()
        print("Stopped MIDI handler.")