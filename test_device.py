import pytest
from simulation import HydroGen
import datetime
from time import sleep
import statistics

RPM = 200  # standard RPM acquired by shop drill
TEST_TIME = 10  # seconds to run the drill
POW_SUCCESS = 20  # must generate at least 30 W to be acceptable

@pytest.fixture
def hydrogen():
    return HydroGen()


def test_device(hydrogen):
    now = datetime.datetime.now()
    ten_s = now + datetime.timedelta(0, TEST_TIME)
    while now < ten_s:
        hydrogen.generate(RPM)
        sleep(1)
        now = datetime.datetime.now()
    power_reading = statistics.mean((p.power for p in hydrogen.pow_gen[-TEST_TIME:]))
    assert(power_reading >= POW_SUCCESS)
