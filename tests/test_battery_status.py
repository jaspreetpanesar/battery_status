
from battery_status import *
import unittest


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





if __name__ == "__main__":
    unittest.main()
