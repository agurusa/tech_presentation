import pytest
import simulation as sim

# watt & sea test constants
AV_SPEED = 5.7  # knots
AV_POW = 80  # W


@pytest.fixture
def simulation():
    return sim.HydroGen()


def test_flash(simulation):
    assert simulation.firmware_version == 0
    assert simulation.can_address == 0
    assert simulation.LEDS == {sim.BOARD: sim.RED, sim.CONVERTER: sim.RED}
    simulation.flash()
    assert simulation.firmware_version == sim.FIRMWARE_VERSION
    assert simulation.can_address == sim.CAN_ADDRESS
    assert simulation.LEDS == {sim.BOARD: sim.GREEN, sim.CONVERTER: sim.GREEN}


def test_power_on(simulation):
    assert simulation.pow_con == 0
    simulation.turn_on()
    assert simulation.pow_con == sim.POWER_CONSUMED


def test_conversion(simulation):
    av_speed = 5.7  # knots
    rpm = simulation.knots_to_rpm(av_speed)
    knots = simulation.rpm_to_knots(rpm)
    assert av_speed == knots


def test_get_pow(simulation):
    with pytest.raises(Exception) as exc:
        simulation.get_pow(sim.MAX + 1)
        assert sim.EXCEPT_MAXTIME in str(exc.value)

    with pytest.raises(Exception) as exc:
        simulation.get_pow(10)
        assert sim.EXCEPT_OFF in str(exc.value)

    first_reading = simulation.generate(0)
    assert simulation.get_pow(10) == [first_reading]

    rpm = simulation.knots_to_rpm(AV_SPEED)
    second_reading = simulation.generate(rpm)
    assert simulation.get_pow(10) == [first_reading, second_reading]


def test_set_LEDs(simulation):
    with pytest.raises(Exception) as exc:
        simulation.set_LED('blue', sim.CONVERTER)
        assert sim.EXCEPT_COLOR in str(exc.value)

    with pytest.raises(Exception) as exc:
        simulation.set_LED(sim.GREEN, 'hull_computer')
        assert sim.EXCEPT_LOC in str(exc.value)

    simulation.set_LED(sim.RED, sim.BOARD)
    LEDs = simulation.get_LEDs()
    assert LEDs[sim.BOARD] == sim.RED

    simulation.set_LED(sim.GREEN, sim.CONVERTER)
    LEDs = simulation.get_LEDs()
    assert LEDs[sim.CONVERTER] == sim.GREEN


def test_generate(simulation):
    rpm = simulation.knots_to_rpm(AV_SPEED)
    reading = simulation.generate(rpm)
    assert reading.power == pytest.approx(AV_POW, rel=0.5)
