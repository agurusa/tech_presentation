import pytest
import specs
from simulation import HydroGen

NUM_SAMPLES = 100


def setup():
    DUT = HydroGen()  # device under test
    DUT.flash()
    DUT.turn_on()
    DUT.battery.set_power(specs.MAX_BATT_LEVEL - 1)
    return DUT


sample_population = [setup() for i in range(NUM_SAMPLES)]


@pytest.fixture(scope="module", params=sample_population)
def hydrogen(request):
    return request.param
