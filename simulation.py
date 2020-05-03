from numpy.polynomial import polynomial as poly
import datetime as dt
from random import choice
import specs

# conversion constants
KNOT = 0.5144  # meters/second  # 80 W at 5.7 Knots
PI = 3.14

# exception strings
EXCEPT_MAXTIME = 'Simulation does not record more than 60 seconds worth of data.'
EXCEPT_OFF = 'Simulation is not "Powered on."'
EXCEPT_COLOR = f'Simulation does not support colors other than {specs.RED} OR {specs.GREEN}'
EXCEPT_LOC = f'Simulation does not support LED locations other than {specs.BOARD} or {specs.CONVERTER}'
EXCEPT_POW = 'Power reading cannot be parsed'
EXCEPT_GEN = 'No readings have yet been generated.'


# Conversions
def rpm_to_knots(RPM):
    meters_per_rotation = (specs.PROPELLER / 1000) * PI
    rotations_per_second = RPM / 60
    knots = 1 / KNOT * (meters_per_rotation * rotations_per_second)
    return knots


def knots_to_rpm(knots):
    meters_per_rotation = (specs.PROPELLER / 1000) * PI
    rpm = knots * KNOT / meters_per_rotation * 60
    return rpm


# defines the structure used to record power generated
class Reading:
    def __init__(self, power, timestamp):
        self.power = power  # W
        self.timestamp = timestamp


# CRUISING300, 200 MM
class HydroGen:
    def __init__(self):
        self.pow_gen = []  # holds the last 1 minute of Readings
        self.pow_con = 0  # W, represents power consumed
        self.LEDS = {specs.BOARD: specs.RED, specs.CONVERTER: specs.RED}  # must be flashed
        self.can_address = 0  # must be flashed
        self.firmware_version = 0  # must be flashed
        self.voltage_spike = choice([True, False])
        self.voltage_oscillation = choice([True, False])

    def flash(self):
        self.can_address = specs.CAN_ADDRESS
        self.firmware_version = specs.FIRMWARE_VERSION

    def turn_on(self):
        self.pow_con = specs.POWER_CONSUMED
        self.LEDS[specs.CONVERTER] = specs.RED if self.voltage_spike else specs.GREEN
        self.LEDS[specs.BOARD] = specs.RED if self.voltage_oscillation else specs.GREEN

    def turn_off(self):
        self.pow_con = 0

    def generate(self, RPM):  # calculates generated power based on RPM
        if not self.pow_con:
            raise Exception(EXCEPT_OFF)

        if specs.RED in self.LEDS.values():
            reading = Reading(-1, dt.datetime.now())
        elif not RPM:
            reading = Reading(0, dt.datetime.now())
        else:
            knots = rpm_to_knots(RPM)
            ffit = poly.polyval(knots, specs.COEFFS)
            reading = Reading(ffit, dt.datetime.now())

        self.record_pow(reading)
        return reading

    def record_pow(self, reading):  # records the last 1 min of generated power
        if self.pow_gen:
            if reading.timestamp - self.pow_gen[0].timestamp < dt.timedelta(0, specs.MAX):
                self.pow_gen.append(reading)
            else:
                while self.pow_gen and (reading.timestamp - self.pow_gen[0].timestamp >= dt.timedelta(0, specs.MAX)):
                    del self.pow_gen[0]
                self.pow_gen.append(reading)
        else:
            self.pow_gen.append(reading)

    def get_pow(self, seconds):  # gets the recorded Readings for the last however many seconds
        if seconds > specs.MAX:
            raise Exception(EXCEPT_MAXTIME)

        first = dt.datetime.now() - dt.timedelta(0, seconds)
        power = [r for r in self.pow_gen if r.timestamp >= first]
        if -1 in power:
            raise Exception(EXCEPT_POW)

    def set_LED(self, color, loc):  # sets LED colors on board and converter
        if color is not specs.RED and color is not specs.GREEN:
            raise Exception(EXCEPT_COLOR)
        if loc is not specs.BOARD and loc is not specs.CONVERTER:
            raise Exception(EXCEPT_LOC)
        self.LEDS[loc] = color

    def get_LEDs(self):
        return self.LEDS
