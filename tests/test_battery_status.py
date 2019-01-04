
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



class Battery_read_test(unittest.TestCase):

    def test_successful(self):
        b = Battery()
        b.read()
        for i in Battery.ATTRIBUTES:
            if not getattr(b, i, None):
                log.error("battery_read_test fail on %s" %i)
                self.fail()



class Battery_getAttr_test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """runs before each test class"""
        cls.b = Battery()
        cls.b.read()


    def test_string_return(self):
        value = self.b.getAttr("health")
        if not value:
            self.fail()


    def test_none_return(self):
        attr = self.b.getAttr("incorrectattribute")
        if attr != None:
            self.fail()


    def test_int_return(self):
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









if __name__ == "__main__":
    unittest.main()
