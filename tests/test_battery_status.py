
from battery_status import *
import unittest

# ----- LOGGING SETUP -----
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# file logging
fh = logging.FileHandler("logs/test.log")
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
log.addHandler(fh)

# console logging
# ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)
# ch.setFormatter(formatter)
# log.addHandler(ch)
# --- END LOGGING SETUP ---


class ReadDataTest(unittest.TestCase):

    def test_readCapacity(self):
        filepath = "/sys/class/power_supply/battery/capacity"
        data = readData(filepath)
        if not data:
            self.fail()


    def test_wrong_filepath(self):
        filepath = "/incorrect/file/path"
        data = readData(filepath)
        if data:
            self.fail()


class BatteryTest(unittest.TestCase):

    def test_read(self):
        b = Battery()
        b.read()


    def test_getattr(self):
        b = Battery()
        b.read()

        for i in Battery.ATTRIBUTES:
            if not getattr(b, i, None):
                self.fail()

    def test_getfancyattr(self):
        b = Battery()
        b.read()

        try:
            val = b.getFancyFormatAttr("capacity")
            log.info("fancyattr result = %s" %val)
        except Exception as e:
            self.fail()


    def showAll(self):
        b = Battery()
        b.read()
        try:
            log.info(b.viewAll())
        except Exception as e:
            log.error(e)
            f.fail()



if __name__ == "__main__":
    unittest.main()
