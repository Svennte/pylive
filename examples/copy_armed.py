import live

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

def find_empty_clip_slot(track):
    """
    Finds the first empty clip slot in the given track.
    Returns the index of the empty slot, or None if all slots are occupied.
    """
    for index, clip in enumerate(track.clips):
        if clip is None:
            return index
    return None

def duplicate_playing_clip_to_empty_slot():
    """
    Duplicates the currently playing clip in the first armed track to an empty clip slot.
    """
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

if __name__ == "__main__":
    duplicate_playing_clip_to_empty_slot()
