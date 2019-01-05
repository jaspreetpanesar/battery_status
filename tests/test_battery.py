# -*- coding: utf-8 -*-

import unittest
import sys
import os

from battery_status import *

# ----- LOGGING SETUP -----
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# file logging
try:
    fh = logging.FileHandler("logs/test.log")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    log.addHandler(fh)
except IOError:
    pass

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


class getFancyFormatAttr_test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """runs before each test class"""
        cls.b = Battery()
        cls.b.read()


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


class getCapacityIcon_test(unittest.TestCase):

    def test_icon_case1(self):
        b = Battery()
        b.read()
        icon = b.getCapacityIcon("discharging", 80)
        log.debug(icon)
        self.assertEqual(icon, "[xxx]•")

    def test_icon_case2(self):
        b = Battery()
        b.read()
        icon = b.getCapacityIcon("discharging", 55)
        log.debug(icon)
        self.assertEqual(icon, "[xx ]•")

    def test_icon_case3(self):
        b = Battery()
        b.read()
        icon = b.getCapacityIcon("discharging", 33)
        log.debug(icon)
        self.assertEqual(icon, "[x  ]•")

    def test_icon_case4(self):
        b = Battery()
        b.read()
        icon = b.getCapacityIcon("discharging", 10)
        log.debug(icon)
        self.assertEqual(icon, "[ x ]•")

    def test_icon_case5(self):
        b = Battery()
        b.read()
        icon = b.getCapacityIcon("charging", 90)
        log.debug(icon)
        self.assertEqual(icon, "[+++]•")

    def test_icon_case6(self):
        b = Battery()
        b.read()
        icon = b.getCapacityIcon("charging", 5)
        log.debug(icon)
        self.assertEqual(icon, "[ + ]•")

    def test_icon_status_none(self):
        b = Battery()
        try:
            icon = b.getCapacityIcon()
            log.info("icon with no info: %s" %icon)
        except Exception as e:
            log.error("icon status none test fail: %s" %e)
            self.fail()




if __name__ == "__main__":
    unittest.main()
