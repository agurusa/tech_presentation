import pytest
from simulation import HydroGen
import datetime
from time import sleep
import statistics
from threading import Thread

RPM = 200  # standard RPM acquired by shop drill
TEST_TIME = 10  # seconds to run the drill
POW_SUCCESS = 20  # must generate at least 30 W to be acceptable


@pytest.fixture
def hydrogen():
    return HydroGen()


def test_on(hydrogen):
    pass


def test_LED_board(hydrogen):
    pass


def test_LED_converter(hydrogen):
    pass


def test_LEDs_match(hydrogen):
    pass


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
