import specs
from simulation import HydroGen

NUM_SAMPLES = 100
sample_pop = [HydroGen() for i in range(NUM_SAMPLES)]


def setup(DUT, version, weekday):
    v = int(version)

    if v > 0:
        DUT.fix_board()

    if v > 1:
        DUT.battery.turn_on(specs.MAX_BATT_LEVEL)
    else:
        DUT.battery.turn_on(weekday)

    if v > 2:
        DUT.flash(firmware_change=True)
    else:
        DUT.flash()

    DUT.turn_on()
    return DUT


def devices(testver, testround):
    weekday = specs.FRIDAY if testround == '1' else specs.MONDAY
    return [setup(d, testver, weekday) for d in sample_pop]


def pytest_addoption(parser):
    parser.addoption(
        "--testver",
        choices=['0', '1', '2', '3'],
        help='The version of the test you want to check'
    )
    parser.addoption(
        "--testround",
        choices=['1', '2'],
        help='The round of testing you are on'
    )


def pytest_generate_tests(metafunc):
    if 'hydrogen' in metafunc.fixturenames:
        metafunc.parametrize('hydrogen', devices(metafunc.config.getoption('testver'),
                                                 metafunc.config.getoption('testround')), scope='module')
