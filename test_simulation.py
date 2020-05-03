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
    simulation.flash()
    assert simulation.firmware_version == specs.FIRMWARE_VERSION
    assert simulation.can_address == specs.CAN_ADDRESS


def test_power_on(simulation):
    simulation.turn_on()
    assert simulation.pow_con == specs.POWER_CONSUMED

    LED_board, LED_converter = (simulation.LEDS[specs.BOARD], simulation.LEDS[specs.CONVERTER])

    assert LED_converter == specs.RED if simulation.voltage_spike else LED_converter == specs.GREEN
    assert LED_board == specs.RED if simulation.voltage_oscillation else LED_board == specs.GREEN


def test_power_off(simulation):
    simulation.turn_on()
    simulation.turn_off()
    assert simulation.pow_con == 0


def test_conversion():
    av_speed = 5.7  # knots
    rpm = sim.knots_to_rpm(av_speed)
    knots = sim.rpm_to_knots(rpm)
    assert av_speed == knots


def test_get_pow(simulation):
    with pytest.raises(Exception) as exc:
        simulation.get_pow(specs.MAX + 1)
        assert sim.EXCEPT_MAXTIME in str(exc.value)

    with pytest.raises(Exception) as exc:
        simulation.get_pow(10)
        assert sim.EXCEPT_OFF in str(exc.value)

    simulation.turn_on()
    simulation.set_LED(specs.GREEN, specs.CONVERTER)
    simulation.set_LED(specs.GREEN, specs.BOARD)

    first_reading = simulation.generate(0)
    assert simulation.get_pow(10) == [first_reading]

    rpm = sim.knots_to_rpm(AV_SPEED)
    second_reading = simulation.generate(rpm)
    assert simulation.get_pow(10) == [first_reading, second_reading]


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
    simulation.turn_on()
    rpm = sim.knots_to_rpm(AV_SPEED)
    if specs.RED in simulation.get_LEDs().values():
        with pytest.raises(Exception) as exc:
            reading = simulation.generate(rpm)
            assert sim.EXCEPT_POW in str(exc.value)
    else:
        reading = simulation.generate(rpm)
        assert reading.power == pytest.approx(AV_POW, rel=0.5)
