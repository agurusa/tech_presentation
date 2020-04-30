from numpy.polynomial import polynomial as poly
import datetime as dt

# conversion constants
KNOT = 0.5144  # meters/second  # 80 W at 5.7 Knots
PI = 3.14
MAX = 60  # store a max of 60 seconds of power readings

# LED info
RED = 'red'
GREEN = 'green'
BOARD = 'board'
CONVERTER = 'converter'

# exception strings
EXCEPT_MAXTIME = 'Simulation does not record more than 60 seconds worth of data.'
EXCEPT_OFF = 'Simulation is not "Powered on."'
EXCEPT_COLOR = f'Simulation does not support colors other than {RED} OR {GREEN}'
EXCEPT_LOC = f'Simulation does not support LED locations other than {BOARD} or {CONVERTER}'

# Manufacturer specs
X = [6.4, 5.5, 4.9, 4.4]  # knots
Y = [113.2, 71.7, 47.7, 33.9]  # W generated
COEFFS = poly.polyfit(X, Y, 2)  # fit quadratic to W&S chart
PROPELLER = 200  # mm diameter


class Reading:  # defines the structure used to record power generated
    def __init__(self, power, timestamp):
        self.power = power  # W
        self.timestamp = timestamp


class HydroGen:  # CRUISING300, 200 MM
    def __init__(self):
        self.pow_gen = []  # holds the last 1 minute of Readings
        self.LEDS = {BOARD: GREEN, CONVERTER: GREEN}  # assume LEDs indicate proper setup

    def turn_on(self):
        pass

    def generate(self, RPM):  # calculates generated power based on RPM
        if not RPM:
            reading = Reading(0, dt.datetime.now())
        else:
            knots = self.rpm_to_knots(RPM)
            ffit = poly.polyval(knots, COEFFS)
            reading = Reading(ffit, dt.datetime.now())

        self.record_pow(reading)
        return reading

    def record_pow(self, reading):  # records the last 1 min of generated power
        if self.pow_gen:
            if reading.timestamp - self.pow_gen[0].timestamp < dt.timedelta(0, MAX):
                self.pow_gen.append(reading)
            else:
                while self.pow_gen and (reading.timestamp - self.pow_gen[0].timestamp >= dt.timedelta(0, MAX)):
                    del self.pow_gen[0]
                self.pow_gen.append(reading)
        else:
            self.pow_gen.append(reading)

    def get_pow(self, seconds):  # gets the recorded Readings for the last however many seconds
        if seconds > MAX:
            raise Exception(EXCEPT_MAXTIME)
        if self.pow_gen:
            first = dt.datetime.now() - dt.timedelta(0, seconds)
            return [r for r in self.pow_gen if r.timestamp >= first]
        else:
            raise Exception(EXCEPT_OFF)

    def set_LED(self, color, loc):  # sets LED colors on board and converter
        if color is not RED and color is not GREEN:
            raise Exception(EXCEPT_COLOR)
        if loc is not BOARD and loc is not CONVERTER:
            raise Exception(EXCEPT_LOC)
        self.LEDS[loc] = color

    def get_LED(self, loc):
        if loc is not BOARD and loc is not CONVERTER:
            raise Exception(EXCEPT_LOC)
        return self.LEDS[loc]

    def rpm_to_knots(self, RPM):
        meters_per_rotation = (PROPELLER / 1000) * PI
        rotations_per_second = RPM / 60
        knots = 1 / KNOT * (meters_per_rotation * rotations_per_second)
        return knots

    def knots_to_rpm(self, knots):
        meters_per_rotation = (PROPELLER / 1000) * PI
        rpm = knots * KNOT / meters_per_rotation * 60
        return rpm
