import pytest
import specs
from simulation import HydroGen

NUM_SAMPLES = 100


def setup(weekday):
    DUT = HydroGen()  # device under test
    DUT.fix_board()
    DUT.flash()
    DUT.battery.set_weekday(weekday)
    DUT.battery.turn_on()
    DUT.turn_on()
    return DUT


sample_population = [setup(specs.FRIDAY) for i in range(NUM_SAMPLES)]
# sample_population = [setup(specs.MONDAY) for i in range(NUM_SAMPLES)]


@pytest.fixture(scope="module", params=sample_population)
def hydrogen(request):
    return request.param
