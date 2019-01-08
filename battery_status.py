# -*- coding: utf-8 -*-

"""
**Battery Status Display**

Displays battery information in long text form
or a minimal graphical display.
"""

import os
import sys
import argparse
import subprocess
import time
import logging
import random


__author__  = "Jaspreet Panesar"
__version__ = 1


# ----- LOGGING SETUP -----
log = logging.getLogger("battery_status_test")
log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# file logging
try:
    fh = logging.FileHandler("logs/battery_status.log")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    log.addHandler(fh)
except IOError as e:
    nh = logging.NullHandler()
    log.addHandler(nh)


def fancy_prefix(value, format):
    """return string with prefix formatted
    added at front
    
    Args:
        value (string): the string value to 
            be modified
        format (string): the prefix to add on to
            string
    
    Returns:
        string: formatted string with prefix
    """
    return "%s%s" %(format, str(value))


def fancy_suffix(value, format):
    """return string with suffix formatted
    added at end
    
    Args:
        value (string): the string value to 
            be modified
        format (string): the suffix to add on to
            string
    
    Returns:
        string: formatted string with suffix
    """
    return "%s%s" %(str(value), format)


def fancy_decimal(value, decimal):
    """returns integer value as decimal float
    value to specified decimal place
    
    Args:
        value (int): integer to conver to decimal
        decimal (string): decimal places to convert
            integer to
    
    Returns:
        float: formatted floating point number or None
            if a zero division error is raised while
            formatting.
    """
    newval = float(value)
    for i in range(decimal):
        newval = newval/10
    return "%.*f" %(decimal, newval)


def fancy_case(value, case):
    """returns string formatted to specified
    case
    
    Args:
        value (string): 
        case (string): coos from following:
                capital: Example 
                upper: EXAMPLE
                lower: example
                random: eXAmPlE
    
    Returns:
        string: string with formatted case 
    """
    # get Capital case
    if case == "capital":
        return "%s%s" %(value[0].upper(), value[1:].lower())

    # get UPPER case
    if case == "upper":
        return value.upper()

    # get lower case
    if case == "lower":
        return value.lower()

    # get RaNDomIsed case
    if case == "random":
        newval = ""
        for i in value:
            if bool(random.getrandbits(1)):
                newval += i.upper()
            else:
                newval += i.lower()
        return newval


class Colour(object):
    """Format text for printing to stdout 
    using ANSI escape sequences.
    """

    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

    @staticmethod
    def format(text, colour):
        """return text fromatted with colour prefix
        and suffix
        
        Args:
            text (string): text to be formatted with color/
                options.
            colour (Colour.Attribute): color identifier from
                Colour class to format text with.
        
        Returns:
            string: formatted string
        """
        return "%s%s%s" %(colour, text, Colour.END)


class Battery(object):
    """battery status data

    Attributes:
        capacity (int): reads the current charge  of the battery
        temp (int): reads the currrent temperature of the battery
        health (string): describes the health of the battery
        status (string): describes whether the battery is discharging or charging
        chargeCounter (int): max charge cycle count
        current_now (int): current charge cycle count
        technology (string): type of battery
        voltage (int): current voltage
    """

    ATTRIBUTES = { 
        "capacity":     {"path": "/sys/class/power_supply/battery/capacity",
                         "suffix": "%"
                         },
        "temp":         {"path": "/sys/class/power_supply/battery/temp",
                         "suffix": "°C", "decimal": 2
                         }, 
        "health":       {"path": "/sys/class/power_supply/battery/health",
                         "case": "capital"
                         }, 
        "status":       {"path": "/sys/class/power_supply/battery/status",
                         "case": "upper"

                         }, 
        "chargeCount":  {"path": "/sys/class/power_supply/battery/charge_counter"
                         }, 
        "currentNow":   {"path": "/sys/class/power_supply/battery/current_now"
                         }, 
        "technology":   {"path": "/sys/class/power_supply/battery/technology",
                         "case": "upper"
                         }, 
        "voltage":      {"path": "/sys/class/power_supply/battery/voltage_now"
                         }
    }


    FANCY_FORMATS = {
        "case":         {"function": fancy_case},
        "decimal":      {"function": fancy_decimal},
        "prefix":       {"function": fancy_prefix},
        "suffix":       {"function": fancy_suffix},
    }


    def __init__(self, *args, **kwargs):
        for i in kwargs:
            setattr(self, i, kwargs[i])
        log.info("created battery object %s" %self)
        self.read()


    def read(self):
        """read battery data from system files and save
        as class attributes"""

        log.info("battery data read started")
        for i in Battery.ATTRIBUTES:
            filepath = Battery.ATTRIBUTES[i]["path"]
            data = readData(filepath)
            if not data:
                log.info("'%s' data read unsuccessful" %i)
                continue
            else:
                setattr(self, i, data)
                log.info("'%s' data read successful" %i)

        log.info("battery data read complete")


    def getAttr(self, attr):
        """returns value stored in attribute
        
        Args:
            attr (string): attribute to read value of
        
        Returns:
            string or int or None: respective value type returned or
                None if value does not exist.
        """
        log.info("running getattr '%s' for battery" %attr)
        try:
            val = getattr(self, attr)   # AttributeError
            val = int(val)              # ValueError
        except AttributeError as e:
            log.error("Error: could not retrieve attribute - %s" %e)
            return None
        except ValueError:
            log.warning("Attribute '%s' cannot be converted to int" %val)
        log.debug("Attribute '%s' = %s" %(attr, val))
        return val


    def getFancyFormatAttr(self, attr):
        """returns fancy format of attribute
        value

        Fancy formatted is value with any required
        prefix or suffix and decimal positioning or 
        any other changes required to make value human
        readable.
        
        Args:
            attr (string): attribute to get value of
        
        Returns:
            string: fancy format of attribute value or None
                if attribute not available.
        """
        log.info("running formatattr '%s'" %attr)
        val = self.getAttr(attr)
        if val:
            log.info("attribute exists")
            for f in Battery.FANCY_FORMATS:
                log.info("searching for format '%s'" %f)
                try:
                    # grab format from attribute list
                    # exits on error
                    form = Battery.ATTRIBUTES[attr][f]      # KeyError
                    log.info("format %s found" %f)
                    
                    # grab function from format list
                    func = Battery.FANCY_FORMATS[f]["function"]

                    # convert value
                    val = func(val, form)
                    log.debug("new value = %s" %val)

                except KeyError:
                    log.warning("no '%s' format for %s" %(f, attr))

        else:
            log.warning("attribute does not exist")
        return val


    def getSmallIcon(self, status=None, charge=None, showcolour=False):
        """returns battery icon showing capcity and status

        Args:
            status (string): for debugging, specify charge status
            charge (int):  for debugging, specify charge remaining
            showcolour (bool, optional): specify if text should 
                be in colour. False by default.

        Example:
            [xxx]•  = discharging >= 80%
            [xx ]•  = discharging >= 55%
            [ x ]•  = discharging < 15%
            [++ ]•  = charging    >= 60%
            [ + ]•  = charging    > 15%

        Returns:
            string: battery icon
        """
        log.info("getSmallIcon called")

        # determine charge icon
        if not status:
            status = self.getAttr("status")
        log.debug("status = %s" %status)

        try:
            icons = { "charging":"+", "discharging":"x", "full":"#" }
            icon = icons.get(status.lower(), "?")
        except AttributeError as e:
            log.error("status could not be read: %s" %e)
            icon = "?"

        # set icon body
        if not charge:
            charge = self.getAttr("capacity")
        log.debug("charge = %s" %charge)

        # determine body icon count
        try:
            if charge >= 80:
                body = "{0}{0}{0}".format(icon)
                if showcolour:
                    body = Colour.format(body, Colour.GREEN)
            elif charge >= 35:
                body = "{0}{0} ".format(icon)
                if showcolour:
                    body = Colour.format(body, Colour.CYAN)
            elif charge >= 15:
                body = "{0}  ".format(icon)
                if showcolour:
                    body = Colour.format(body, Colour.YELLOW)
            else:
                body = " %s " %icon
                if showcolour:
                    body = Colour.format(body, Colour.RED)
        except TypeError as e:
            log.error("charge could not be read: %s" %e)
            body = " %s " %icon

        # frame body
        final = "[%s]•"%body
        log.debug("final icon = %s" %final)
        return final


    def showMinimal(self, showcolour=False):
        """return a minimal display for battery
        capacity and status
        
        Example:
            79% [xx ]•

        Args:
            showcolour (bool, optional): specify if text
                should be in colour. False by default.

        Returns:
            string: battery status (%) and graphical 
                battery icon
        """
        return "%s %s" %(self.getFancyFormatAttr("capacity"), self.getSmallIcon(showcolour=showcolour))


    def showData(self, showcolour=False):
        """print all battery information to stdout

        Args:
            showcolour (bool, optional): show colour in output.
                False by default.

        Returns:
            array of strings: all battery information lines stored in
                an array
        """
        log.info("Battery showData called")

        # content
        content = []
        for i in Battery.ATTRIBUTES:
            log.info("reading attribute %s" %i)
            attr = self.getFancyFormatAttr(i)
            if attr:
                if showcolour:
                    line = "%s: %s" %(Colour.format(fancy_case(i, "capital"), Colour.RED), attr)
                else:
                    line = "%s: %s" %(fancy_case(i, "capital"), attr)
                log.debug("showData line = %s" %line)
                content.append(line)

        return content


    def getLargeIcon(self, showcolour=False):
        # generate dynamically, instead of a static text block
        return """
    ########################################
    ##                                    ##
    ##                                    ######
    ##                                    ##   #
    ##   SOMEONE UNPLUGEGD THE BATTERY    ##   #
    ##                                    ##   #
    ##                                    ######
    ##                                    ##
    ########################################
        """


    def __repr__(self):
        return "<Battery(charge=%s)>" %getattr(self, "charge", "no available")



def readData(filepath):
    """returns the contents of file
    
    Args:
        filepath (string): full path of files to be read
        
    Returns:
        string or None: content in string form if found, or None if 
            not found.
    """
    try:
        with open(filepath) as f:
            content = f.readlines()
    except IOError as e:
        log.error("File not found: %s" %e)
        return None
    except OSError as e:
        log.error("OS error occured: %s" %e)
        return None

    log.debug("content = %s" %content)
    
    # assumption - there will only be one line of data
    # remove trailing \n character
    data = content[0].strip()
    log.debug("data = %s" %data)

    return data


def main(args):
    b = Battery()

    # has user provided any arguments when running script
    userargs = False

    if args.all:
        userargs = True
        print(b.getLargeIcon(showcolour=args.showcolour))
        for line in b.showData(showcolour=args.showcolour):
            print(line)

    if args.minimal:
        userargs = True
        print(b.showMinimal(showcolour=args.showcolour))

    if args.data:
        userargs = True
        for line in b.showData(showcolour=args.showcolour):
            print(line)

    if args.small:
        userargs = True
        print(b.getSmallIcon(showcolour=args.showcolour))

    if args.big:
        userargs = True
        print(b.getLargeIcon(showcolour=args.showcolour))

    if args.information:
        userargs = True
        print(b.getFancyFormatAttr("capacity"))


    # show minimal icon if no arguments passed (excluding colour argument)
    if not userargs:
        print(b.showMinimal(showcolour=args.showcolour))



if __name__ == "__main__":

    # setup argument parser
    parser = argparse.ArgumentParser(description="View battery status")

    parser.add_argument("-c", "--showcolour", action="store_true", 
                help="show colour on output text. False by default")

    parser.add_argument("-a", "--all", action="store_true", 
                help="View all battery information")

    parser.add_argument("-m", "--minimal", action="store_true", 
                help="view battery icon and capacity information")

    parser.add_argument("-d", "--data", action="store_true", 
                help="view all battery data")

    parser.add_argument("-s", "--small", action="store_true", 
                help="view small battery icon")

    parser.add_argument("-b", "--big", action="store_true", 
                help="view large battery icon")

    parser.add_argument("-i", "--information", action="store_true", 
                help="view battery capacity information only")


    args = parser.parse_args()
    main(args)

