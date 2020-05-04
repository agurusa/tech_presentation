import pytest
import specs
from simulation import HydroGen

NUM_SAMPLES = 100


def setup(weekday):
    DUT = HydroGen()  # device under test
    DUT.fix_board()  # first major change
    DUT.flash(firmware_change=True)  # third major change
    # DUT.flash()
    # DUT.battery.turn_on(weekday)
    DUT.battery.turn_on(specs.MAX_BATT_LEVEL)  # second major change
    DUT.turn_on()
    return DUT


sample_population = [setup(specs.FRIDAY) for i in range(NUM_SAMPLES)]
# sample_population = [setup(specs.MONDAY) for i in range(NUM_SAMPLES)]


@pytest.fixture(scope="module", params=sample_population)
def hydrogen(request):
    return request.param
