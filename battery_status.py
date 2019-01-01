
"""
*Battery Status Display*

Returns battery information in long text form
or minimal visual display
"""


import os, sys, argparse, subprocess, time, logging

# ----- LOGGING SETUP -----
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# file logging
fh = logging.FileHandler("logs/battery_status.log")
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
log.addHandler(fh)

# console logging
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
ch.setFormatter(formatter)
log.addHandler(ch)
# --- END LOGGING SETUP ---


class Battery(object):
    """storage for battery status data

    Attributes:
        -- data --
        capacity (int): reads the current charge  of the battery
        temp (int): reads the currrent temperature of the battery
        health (string): describes the health of the battery
        status (string): describes whether the battery is discharging or charging
        
        -- information --
        chargeCounter (int): max charge cycle count
        current_now (int): current charge cycle count
        technology (string): type of battery
        voltage (int): current voltage

    """

    ATTRIBUTES = ["capacity", "temp", "health", "status", "chargeCounter", 
                    "current_now", "technology", "voltage"]

    def __init__(self, *args, **kwargs):
        for i in kwargs:
            setattr(self, i, kwargs[i])
        log.info("created battery object %s" %self)




    def showMinimal(self):
        return ""

    def howAll(self):
        return ""

    def __repr__(self):
        return "<Battery()>"



if __name__ == "__main__":
    pass






