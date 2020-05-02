from numpy.polynomial import polynomial as poly

# Config specs
MAX = 60  # store a max of 60 seconds of power readings
CAN_ADDRESS = 57

# preloaded firmware versions
OLD = 2.11
NEW = 2.12
FIRMWARE_VERSION = 4.2
VERSION_MAN = [OLD, NEW]  # manufacturer possibilities
VERSION_PROP = {OLD: 4.2, NEW: 4.3}  # proprietary firmware version association
FACTOR = 0.001  # ratio difference between old and new firmware

# Manufacturer specs
X = [6.4, 5.5, 4.9, 4.4]  # knots
Y = [113.2, 71.7, 47.7, 33.9]  # W generated
COEFFS = poly.polyfit(X, Y, 2)  # fit quadratic to W&S chart
PROPELLER = 200  # mm diameter
POWER_CONSUMED = 2.5  # W, av pow consumed when idle
MAX_BATT_LEVEL = 75  # % of full battery power. will not generate power if batts are above this amount


# LED info
RED = 'red'
GREEN = 'green'
BOARD = 'board'
CONVERTER = 'converter'
