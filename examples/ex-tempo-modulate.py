#!/usr/bin/env python3

#------------------------------------------------------------------------
# pylive: ex-tempo-modulate.py
#
# Slowly modulates the tempo of a Live set.
#------------------------------------------------------------------------
from live import *

import time
import math
import logging

logging.basicConfig(format="%(asctime)-15s %(message)s")
logging.getLogger("live").setLevel(logging.INFO)

#------------------------------------------------------------------------
# Don't need to scan the set for simple set-wide operations.
#------------------------------------------------------------------------
def main():
    set = Set()

    tempo_default = 120.0
    tempo_range = tempo_default * 0.5
    sleep = 0.01
    period = 10.0
    t = 0.0

    #------------------------------------------------------------------------
    # Change the set's tempo every 0.01s based on a smooth sinusoid,
    # giving a wave-like tempo modulation.
    #
    # The below are synonymous:
    #
    # set.tempo = 120.0
    # set.set_tempo(120.0)
    #------------------------------------------------------------------------
    print("Modulating tempo of Live set...")
    while True:
        set.tempo = tempo_default + (tempo_range * math.sin(math.pi * 2.0 * t / period))
        time.sleep(sleep)
        t += sleep

if __name__ == "__main__":
    main()
