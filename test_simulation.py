import pytest
import simulation as sim
import specs

# watt & sea test constants
AV_SPEED = 5.7  # knots
AV_POW = 80  # W


@pytest.fixture
def simulation():
    return sim.HydroGen()


def test_flash(simulation):
    assert simulation.firmware_version == 0
    assert simulation.can_address == 0
    assert simulation.LEDS == {specs.BOARD: specs.RED, specs.CONVERTER: specs.RED}

    simulation.manufacture_version = specs.OLD
    simulation.flash()
    assert simulation.firmware_version == specs.VERSION_PROP[specs.OLD]
    assert simulation.can_address == specs.CAN_ADDRESS
    assert simulation.LEDS == {specs.BOARD: specs.GREEN, specs.CONVERTER: specs.GREEN}

    # simulation.manufacture_version = specs.NEW
    # simulation.flash()
    # assert simulation.firmware_version == specs.VERSION_PROP[specs.NEW]


def test_power_on(simulation):
    assert simulation.pow_con == 0
    simulation.turn_on()
    assert simulation.pow_con == specs.POWER_CONSUMED


def test_power_off(simulation):
    simulation.turn_on()
    simulation.turn_off()
    assert simulation.pow_con == 0


def test_conversion(simulation):
    av_speed = 5.7  # knots
    rpm = simulation.knots_to_rpm(av_speed)
    knots = simulation.rpm_to_knots(rpm)
    assert av_speed == knots


def test_get_pow(simulation):
    with pytest.raises(Exception) as exc:
        simulation.get_pow(specs.MAX + 1)
        assert sim.EXCEPT_MAXTIME in str(exc.value)

    with pytest.raises(Exception) as exc:
        simulation.get_pow(10)
        assert sim.EXCEPT_OFF in str(exc.value)

    first_reading = simulation.generate(0)
    assert simulation.get_pow(10) == [first_reading]

    rpm = simulation.knots_to_rpm(AV_SPEED)
    second_reading = simulation.generate(rpm)
    assert simulation.get_pow(10) == [first_reading, second_reading]
    assert second_reading.power == 0

    simulation.battery.set_power(specs.MAX_BATT_LEVEL - 1)
    third_reading = simulation.generate(rpm)
    assert third_reading.power > 0


def test_set_LEDs(simulation):
    with pytest.raises(Exception) as exc:
        simulation.set_LED('blue', specs.CONVERTER)
        assert sim.EXCEPT_COLOR in str(exc.value)

    with pytest.raises(Exception) as exc:
        simulation.set_LED(specs.GREEN, 'hull_computer')
        assert sim.EXCEPT_LOC in str(exc.value)

    simulation.set_LED(specs.RED, specs.BOARD)
    LEDs = simulation.get_LEDs()
    assert LEDs[specs.BOARD] == specs.RED

    simulation.set_LED(specs.GREEN, specs.CONVERTER)
    LEDs = simulation.get_LEDs()
    assert LEDs[specs.CONVERTER] == specs.GREEN


def test_generate(simulation):
    rpm = simulation.knots_to_rpm(AV_SPEED)
    reading = simulation.generate(rpm)
    assert reading.power == 0

    simulation.battery.power = specs.MAX_BATT_LEVEL - 1
    reading = simulation.generate(rpm)
    assert reading.power == pytest.approx(AV_POW, rel=0.5)
