import pytest
from simulation import HydroGen, RED, GREEN, BOARD, CONVERTER, CAN_ADDRESS, FIRMWARE_VERSION, POWER_CONSUMED
import datetime
from time import sleep
import statistics
from threading import Thread

RPM = 200  # standard RPM acquired by shop drill
TEST_TIME = 10  # seconds to run the drill
POW_SUCCESS = 20  # must generate at least 30 W to be acceptable

COLOR_DICT = {'R': RED, 'G': GREEN}


@pytest.fixture(scope="module")
def hydrogen():
    DUT = HydroGen()  # device under test
    DUT.flash()
    DUT.turn_on()
    return DUT


def test_on(hydrogen):
    assert hydrogen.pow_con == POWER_CONSUMED


def test_flashed(hydrogen):
    assert hydrogen.can_address == CAN_ADDRESS
    assert hydrogen.firmware_version == FIRMWARE_VERSION


def test_LEDs(hydrogen):
    # color_board = solicit_LED(hydrogen, BOARD)
    # color_converter = solicit_LED(hydrogen, CONVERTER)
    LEDs = hydrogen.get_LEDs()
    assert LEDs[BOARD] == GREEN
    assert LEDs[CONVERTER] == GREEN


def test_pow_generated(hydrogen):
    now = datetime.datetime.now()
    end = now + datetime.timedelta(0, TEST_TIME)
    thread = start_drill(hydrogen)
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
    thread = Thread(target=run_drill, args=(_hydrogen,))
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


def stop_drill(hg):
    pass


def test_off(hydrogen):
    pass
