import pytest
import datetime
from time import sleep
import statistics
from threading import Thread

from simulation import HydroGen
import specs

RPM = 200  # standard RPM acquired by shop drill
TEST_TIME = 10  # seconds to run the drill
POW_SUCCESS = 20  # must generate at least this much power to be acceptable


@pytest.fixture(scope="module")
def hydrogen():
    DUT = HydroGen()  # device under test
    DUT.flash()
    DUT.turn_on()
    DUT.battery.set_power(specs.MAX_BATT_LEVEL)
    return DUT


def test_on(hydrogen):
    assert hydrogen.pow_con == specs.POWER_CONSUMED


def test_flashed(hydrogen):
    assert hydrogen.can_address == specs.CAN_ADDRESS
    assert hydrogen.firmware_version == specs.FIRMWARE_VERSION


def test_LEDs(hydrogen):
    LEDs = hydrogen.get_LEDs()  # solicit the user
    assert LEDs[specs.BOARD] == specs.GREEN
    assert LEDs[specs.CONVERTER] == specs.GREEN


def test_pow_generated(hydrogen):
    now = datetime.datetime.now()
    end = now + datetime.timedelta(0, TEST_TIME)
    thread = start_drill(hydrogen)  # user begins spinning the generator
    power_readings = []
    delay = 1  # seconds
    while now < end:
        sleep(delay)
        power_readings += [p.power for p in hydrogen.get_pow(delay)]
        now = datetime.datetime.now()
    thread.join()
    av_pow = statistics.mean(power_readings)
    assert (av_pow >= POW_SUCCESS)


def start_drill(_hydrogen):
    thread = Thread(target=run_drill, args=(_hydrogen,), daemon=True)
    thread.start()
    return thread


def run_drill(_hydrogen):
    now = datetime.datetime.now()
    end = now + datetime.timedelta(0, TEST_TIME)
    delay = 0.05  # hydrogen records at 20 Hz
    while now < end:
        _hydrogen.generate(RPM)
        sleep(delay)
        now = datetime.datetime.now()


def test_off(hydrogen):
    hydrogen.turn_off()
    assert hydrogen.pow_con == 0
