from threading import Thread
import pytest
import specs

RPM = 200  # standard RPM acquired by shop drill
TEST_TIME = 1  # seconds to run the drill
POW_SUCCESS = 20  # must generate at least this much power to be acceptable


def test_on(hydrogen):
    assert hydrogen.pow_con == specs.POWER_CONSUMED


def test_flashed(hydrogen):
    assert hydrogen.can_address == specs.CAN_ADDRESS
    assert hydrogen.firmware_version != 0
    # assert hydrogen.firmware_version == specs.VERSION_PROP[hydrogen.manufacture_version]  # third major change


def test_board_LED(hydrogen):
    LEDs = hydrogen.get_LEDs()
    assert LEDs[specs.BOARD] == specs.GREEN


def test_converter_LED(hydrogen):
    LEDs = hydrogen.get_LEDs()
    assert LEDs[specs.CONVERTER] == specs.GREEN


def test_LEDS_match(hydrogen):
    LEDs = hydrogen.get_LEDs()
    assert LEDs[specs.BOARD] == LEDs[specs.CONVERTER]


def test_pow_generated(hydrogen):
    thread = start_drill(hydrogen)  # user begins spinning the generator
    thread.join()
    av_pow = hydrogen.get_pow(-1)[0].power
    if isinstance(av_pow, str):
        pytest.fail(av_pow)
    else:
        assert av_pow >= POW_SUCCESS


def start_drill(_hydrogen):
    thread = Thread(target=run_drill, args=(_hydrogen,))
    thread.start()
    return thread


def run_drill(_hydrogen):
    _hydrogen.generate(RPM)


def test_off(hydrogen):
    hydrogen.turn_off()
    assert hydrogen.pow_con == 0
