import specs
from simulation import HydroGen
import copy
import pytest

NUM_SAMPLES = 100
sample_pop = [HydroGen() for i in range(NUM_SAMPLES)]
testversions = [0, 1, 2, 3]
testdays = [specs.MONDAY, specs.FRIDAY]
VERSION = 'testversion'
DAY='testday'

def setup():
    all = []
    for t in testversions:
        all += [(copy.deepcopy(device), {VERSION: t, DAY: specs.MONDAY}) for device in sample_pop]
        all += [(copy.deepcopy(device), {VERSION: t, DAY: specs.FRIDAY}) for device in sample_pop]
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


# def pytest_addoption(parser):
#     parser.addoption(
#         "--testver",
#         choices=['0', '1', '2', '3'],
#         help='The version of the test you want to check'
#     )
#     parser.addoption(
#         "--testround",
#         choices=['1', '2'],
#         help='The round of testing you are on'
#     )


# def pytest_generate_tests(metafunc):
#     if 'hydrogen' in metafunc.fixturenames:
#         metafunc.parametrize('hydrogen', devices(metafunc.config.getoption('testver'),
#                                                  metafunc.config.getoption('testround')), scope='module')
