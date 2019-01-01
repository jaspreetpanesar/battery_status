
"""
**Battery Status Display**

Displays battery information in long text form
or minimal visual display
"""


import os, sys, argparse, subprocess, time, logging


__author__  = "Jaspreet Panesar"
__version__ = 1


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

    ATTRIBUTES = { 
                    "capacity": "battery/capacity", 
                    "temp": "battery/temp", 
                    "health": "battery/health", 
                    "status": "battery/status", 
                    "chargeCounter": "battery/charge_counter", 
                    "currentNow": "battery/current_now", 
                    "technology": "battery/technology", 
                    "voltage": "battery/voltage_now"
                }


    def __init__(self, *args, **kwargs):
        for i in kwargs:
            setattr(self, i, kwargs[i])
        log.info("created battery object %s" %self)


    def read(self):
        """ """
        log.info("battery data read started")
        for i in Battery.ATTRIBUTES:
            filepath = os.path.dirname(os.path.realpath(
                            "/sys/class/power_supply" + Battery.ATTRIBUTES[i]) )
            try:
                data = readData(filepath)
            except IOError as e:
                log.error("'%s' data read unsuccessful with error: %s" %(i, e))
                continue
            if data:
                setattr(self, i, data)
                log.info("'%s' data read successful" %i)
            else:
                log.info("'%s' data read unsuccessful" %i)
            log.debug("'%s' = %s" %(i, data))

        log.info("battery data read complete")



    def showMinimal(self):
        """ """
        log.info("Battery.showMinimal called")
        return ""

    def showAll(self):
        """ """
        log.info("Battery.showAll called")
        return ""

    def __repr__(self):
        return "<Battery()>"





# TODO 
def readData(filepath):
    """returns the contents of file
    
    Args:
        filepath (string): full path of files to be read

    Raises:
    
    """
    # TODO
    try:
        with open(filepath) as f:
            content = f.readlines()
    except OSError as e:
        log.error("OS error occured: %s" %e)
        return None

    data = content.strip()
    return data



if __name__ == "__main__":
    pass









