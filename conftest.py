import specs
from simulation import HydroGen
import copy
import pytest

NUM_SAMPLES = 100
sample_pop = [HydroGen() for i in range(NUM_SAMPLES)]
VERSIONS = [0, 1, 2, 3]
DAYS = [specs.MONDAY, specs.FRIDAY]
VERSION = 'testversion'
DAY = 'testday'


def setup():
    all = []
    for t in VERSIONS:
        all += [(copy.copy(device), {VERSION: t, DAY: specs.MONDAY}) for device in sample_pop]
        all += [(copy.copy(device), {VERSION: t, DAY: specs.FRIDAY}) for device in sample_pop]
    return all


def MVP(DUT, weekday):
    DUT.battery.turn_on(weekday)
    DUT.flash()
    DUT.turn_on()
    return DUT


def VERSION1(DUT, weekday):
    DUT.fix_board()
    DUT.battery.turn_on(weekday)
    DUT.flash()
    DUT.turn_on()
    return DUT


def VERSION2(DUT):
    DUT.fix_board()
    DUT.battery.turn_on(specs.MAX_BATT_LEVEL)
    DUT.flash()
    DUT.turn_on()
    return DUT


def VERSION3(DUT):
    DUT.fix_board()
    DUT.battery.turn_on(specs.MAX_BATT_LEVEL)
    DUT.flash(firmware_change=True)
    DUT.turn_on()
    return DUT


@pytest.fixture(scope="module", params=setup())
def hydrogen(request):
    DUT = request.param[0]
    info = request.param[1]

    if info[VERSION] == 0:
        MVP(DUT, info[DAY])

    elif info[VERSION] == 1:
        VERSION1(DUT, info[DAY])

    elif info[VERSION] == 2:
        VERSION2(DUT)

    else:
        VERSION3(DUT)

    return DUT
