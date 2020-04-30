from numpy.polynomial import polynomial as poly
from datetime import datetime as dt

KNOT = 0.5144  # meters/second  # 80 W at 5.7 Knots
PI = 3.14
MAX = 60  # store a max of 60 seconds of power readings


class Reading:  # defines the structure used to record power generated
    def __init__(self, power, timestamp):
        self.power = power  # W
        self.timestamp = timestamp


class HydroGen:  # CRUISING 300, 200 MM
    def __init__(self):
        self.propeller = 200  # mm diameter
        self.pow_gen = []  # holds the last 1 minute of Readings
        self.x = [6.4, 5.5, 4.9, 4.4]  # knots
        self.y = [113.2, 71.7, 47.7, 33.9]  # W generated
        self.coefs = poly.polyfit(self.x, self.y, 2)  # fit quadratic to W&S chart

    def generate(self, RPM):  # calculates generated power based on RPM
        knots = self.rpm_to_knots(RPM)
        ffit = poly.polyval(knots, self.coefs)
        self.record(ffit, dt.now())

    def record(self, power, timestamp):  # records the last 1 min of generated power
        if self.pow_gen:
            if timestamp - self.pow_gen[0].timestamp < MAX:
                self.pow_gen.append(Reading(power, timestamp))
            else:
                while self.pow_gen and (timestamp - self.pow_gen[0].timestamp >= MAX):
                    del self.pow_gen[0]
                self.pow_gen.append(Reading(power, timestamp))
        else:
            self.pow_gen.append(Reading(power, timestamp))

    def rpm_to_knots(self, RPM):
        meters_per_rotation = (self.propeller / 1000) * PI
        rotations_per_second = RPM / 60
        _knots = 1 / KNOT * (meters_per_rotation * rotations_per_second)
        return _knots

    def knots_to_rpm(self, knots):
        meters_per_rotation = (self.propeller / 1000) * PI
        rpm = knots * KNOT / meters_per_rotation * 60
        return rpm
