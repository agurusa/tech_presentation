from numpy.polynomial import polynomial as poly
import datetime as dt
from random import choice
from numpy.random import choice as weighted
import specs

# exception strings
EXCEPT_MAXTIME = 'Simulation does not record more than 60 seconds worth of data.'
EXCEPT_OFF = 'Simulation is not "Powered on."'
EXCEPT_COLOR = f'Simulation does not support colors other than {specs.RED} OR {specs.GREEN}'
EXCEPT_LOC = f'Simulation does not support LED locations other than {specs.BOARD} or {specs.CONVERTER}'
EXCEPT_POW = 'Power reading cannot be parsed'
EXCEPT_GEN = 'No readings have yet been generated.'


class Battery:
    def __init__(self):
        self.power = 100  # percent

    def turn_on(self, pow):  # second major change
        self.power = pow


# structure used to record power generated
class Reading:
    def __init__(self, power, timestamp):
        self.power = power  # W
        self.timestamp = timestamp


# CRUISING300, 200 MM
class HydroGen:

    def __init__(self):
        self.pow_gen = []  # generated power (Readings)
        self.pow_con = 0  # power consumed (W)
        self.manufacture_version = weighted(specs.VERSION_MAN, 1, p=[0.1, .9])[0]  # probability based on order date
        self.LEDS = {specs.BOARD: specs.RED, specs.CONVERTER: specs.RED}
        self.can_address = 0
        self.firmware_version = 0
        self.battery = Battery()
        self.voltage_spike = choice([True, False])
        self.voltage_oscillation = choice([True, False])

    def fix_board(self):  # first major change
        self.voltage_spike = False
        self.voltage_oscillation = False

    def flash(self, firmware_change=False):
        self.can_address = specs.CAN_ADDRESS

        if not firmware_change:  # third major change
            self.firmware_version = specs.VERSION_PROP[specs.OLD]
        else:
            self.firmware_version = specs.VERSION_PROP[self.manufacture_version]

    def turn_on(self):
        self.pow_con = specs.POWER_CONSUMED
        self.LEDS[specs.CONVERTER] = specs.RED if self.voltage_spike else specs.GREEN
        self.LEDS[specs.BOARD] = specs.RED if self.voltage_oscillation else specs.GREEN

    def turn_off(self):
        self.pow_con = 0

    def generate(self, RPM):  # calculates generated power based on RPM
        if not self.pow_con:
            raise Exception(EXCEPT_OFF)

        now = dt.datetime.now()

        if specs.RED in self.LEDS.values():
            reading = Reading(-1, now)
        elif not RPM:
            reading = Reading(0, now)
        elif self.battery.power > specs.MAX_BATT_LEVEL:
            reading = Reading(0, now)
        else:
            knots = specs.rpm_to_knots(RPM)
            ffit = poly.polyval(knots, specs.COEFFS)
            reading = Reading(ffit, now)

        reading.power *= specs.FACTOR_DICT[self.manufacture_version]
        self.record_pow(reading)

        return reading

    def record_pow(self, reading):  # records the last 1 min of generated power
        diff = dt.timedelta(0, specs.MAX)
        while self.pow_gen and (reading.timestamp - self.pow_gen[0].timestamp >= diff):
            del self.pow_gen[0]

        self.pow_gen.append(reading)

    def get_pow(self, seconds):  # gets the recorded Readings for the last however many seconds
        if seconds > specs.MAX:
            raise Exception(EXCEPT_MAXTIME)
        if seconds == -1:
            return [self.parse_power(self.pow_gen[-1])]
        else:
            first = dt.datetime.now() - dt.timedelta(0, seconds)
            return [self.parse_power(r) for r in self.pow_gen if r.timestamp >= first]

    def parse_power(self, x):
        if x.power < 0:
            return Reading(EXCEPT_POW, x.timestamp)
        else:
            x.power /= specs.FACTOR_DICT[self.firmware_version]
            return x

    def set_LED(self, color, loc):  # sets LED colors on board and converter
        if color is not specs.RED and color is not specs.GREEN:
            raise Exception(EXCEPT_COLOR)
        if loc is not specs.BOARD and loc is not specs.CONVERTER:
            raise Exception(EXCEPT_LOC)
        self.LEDS[loc] = color

    def get_LEDs(self):
        return self.LEDS
