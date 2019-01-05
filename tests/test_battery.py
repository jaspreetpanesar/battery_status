
import unittest
import sys
import os

try:
    from battery_status import *
except ImportError:
    from ...battery_status import *

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



class Read_test(unittest.TestCase):

    def test_successful(self):
        b = Battery()
        b.read()
        for i in Battery.ATTRIBUTES:
            if not getattr(b, i, None):
                log.error("battery_read_test fail on %s" %i)
                self.fail()



class getAttr_test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """runs before each test class"""
        cls.b = Battery()
        cls.b.read()


    def test_string(self):
        value = self.b.getAttr("health")
        if not value:
            self.fail()


    def test_none(self):
        attr = self.b.getAttr("incorrectattribute")
        if attr != None:
            self.fail()


    def test_int(self):
        value = self.b.getAttr("capacity")
        if value:
            if isinstance(value, int):
                return
        self.fail()


class readData_test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """runs before each test class"""
        pass

    def setUp(self):
        """runs before each test case"""
        pass



class getFancyFormatAttr_test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """runs before each test class"""
        cls.b = Battery()
        cls.b.read()

    def setUp(self):
        """runs before each test case"""
        pass

    def test_capacity_correct(self):
        """test case"""
        value = self.b.getFancyFormatAttr("capacity")
        if not value.endswith("%"):
            log.debug("fancy attribute test fail: new val = %s" %value)
            self.fail()
        log.debug("fancy attribute correct: new val = %s" %value)


    def test_all(self):
        log.info("fancy attr all test")
        for i in Battery.ATTRIBUTES:
            log.info("fancy attr %s" %i)
            try:
                value = self.b.getFancyFormatAttr(i)
                log.debug("Attribute: %s = %s" %(i, value))
                if not value:
                    self.fail()
            except Exception as e:
                log.error("fancy attr all test fail: %s" %e)
                continue

    def test_decimal(self):
        log.info("fancy decimal test")
        value = self.b.getFancyFormatAttr("temp")
        if not value[1] == ".":
            log.debug("fancy attribute test fail: new val = %s" %value)
            self.fail()
        log.debug("fancy attribute correct: new val = %s" %value)




if __name__ == "__main__":
    unittest.main()
