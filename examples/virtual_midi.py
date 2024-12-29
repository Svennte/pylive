import mido
import threading


class VirtualMidiHandler:
    def __init__(self, input_port_name, virtual_output_port_name):
        """
        Initialize the MIDI handler.

        Args:
            input_port_name (str): Name of the physical MIDI input port (e.g., "Launchpad MK2 1").
            virtual_output_port_name (str): Name of the virtual MIDI output port to create (e.g., "VirtualMIDI").
        """
        self.input_port_name = input_port_name
        self.virtual_output_port_name = virtual_output_port_name
        self.callbacks = []  # List of functions to call on MIDI events
        self.running = True

        # Open input and output ports
        self.input_port = mido.open_input(self.input_port_name)
        self.virtual_output_port = mido.open_output(self.virtual_output_port_name)

    def add_callback(self, callback):
        """
        Add a callback function to handle MIDI messages.

        Args:
            callback (function): Function to handle MIDI messages. Takes a `mido.Message` as argument.
        """
        self.callbacks.append(callback)

    def forward_midi(self, message):
        """
        Forward MIDI messages to the virtual output port and invoke callbacks.

        Args:
            message (mido.Message): The MIDI message received.
        """
        # Send to the virtual output port
        self.virtual_output_port.send(message)

        # Call all registered callbacks
        for callback in self.callbacks:
            callback(message)

    def start(self):
        """
        Start listening for MIDI messages.
        """
        self.flush_input()  # Ensure the input is clean before starting
        def listen():
            print(f"Listening for MIDI input on port: {self.input_port_name}")
            for message in self.input_port:
                if not self.running:
                    break
                print(f"Received MIDI message: {message}")
                self.forward_midi(message)

        self.thread = threading.Thread(target=listen, daemon=True)
        self.thread.start()

    def stop(self):
        """
        Stop listening for MIDI messages.
        """
        self.running = False
        self.thread.join()
        self.input_port.close()
        self.virtual_output_port.close()
        
    def flush_input(self):
        """
        Flushes all pending messages from the input port.
        """
        for _ in self.input_port.iter_pending():
            pass
        print("Input flushed.")


