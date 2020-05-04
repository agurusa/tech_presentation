import pytest
import simulation as sim
import specs

# watt & sea test constants
AV_SPEED = 5.7  # knots
AV_POW = 80  # W


@pytest.fixture
def simHG():
    return sim.HydroGen()


def test_flash(simHG):

    simHG.manufacture_version = specs.OLD
    simHG.flash()
    assert simHG.firmware_version == specs.VERSION_PROP[specs.OLD]
    assert simHG.can_address == specs.CAN_ADDRESS

    simHG.manufacture_version = specs.NEW
    simHG.flash()
    assert simHG.firmware_version == specs.VERSION_PROP[specs.NEW]


def test_power_on(simHG):
    simHG.turn_on()
    assert simHG.pow_con == specs.POWER_CONSUMED

    LED_board, LED_converter = (simHG.LEDS[specs.BOARD], simHG.LEDS[specs.CONVERTER])

    assert LED_converter == specs.RED if simHG.voltage_spike else LED_converter == specs.GREEN
    assert LED_board == specs.RED if simHG.voltage_oscillation else LED_board == specs.GREEN


def test_power_off(simHG):
    simHG.turn_on()
    simHG.turn_off()
    assert simHG.pow_con == 0


def test_conversion():
    av_speed = 5.7  # knots
    rpm = specs.knots_to_rpm(av_speed)
    knots = specs.rpm_to_knots(rpm)
    assert av_speed == knots


def test_get_pow(simHG):
    with pytest.raises(Exception) as exc:
        _ = simHG.get_pow(specs.MAX + 1)
        assert sim.EXCEPT_MAXTIME in str(exc.value)

    with pytest.raises(Exception) as exc:
        _ = simHG.get_pow(10)
        assert sim.EXCEPT_OFF in str(exc.value)

    simHG.turn_on()
    simHG.set_LED(specs.GREEN, specs.CONVERTER)
    simHG.set_LED(specs.GREEN, specs.BOARD)
    _ = simHG.generate(0)

    simHG.battery.turn_on(specs.MAX_BATT_LEVEL - 1)
    rpm = specs.knots_to_rpm(AV_SPEED)
    _ = simHG.generate(rpm)

    simHG.set_LED(specs.RED, specs.CONVERTER)
    _ = simHG.generate(rpm)

    actual = [r.power for r in simHG.get_pow(10)]
    assert actual[0] == 0
    assert actual[1] == pytest.approx(AV_POW, rel=0.5)
    assert actual[2] == sim.EXCEPT_POW


def test_set_LEDs(simHG):
    with pytest.raises(Exception) as exc:
        simHG.set_LED('blue', specs.CONVERTER)
        assert sim.EXCEPT_COLOR in str(exc.value)

    with pytest.raises(Exception) as exc:
        simHG.set_LED(specs.GREEN, 'hull_computer')
        assert sim.EXCEPT_LOC in str(exc.value)

    simHG.set_LED(specs.RED, specs.BOARD)
    LEDs = simHG.get_LEDs()
    assert LEDs[specs.BOARD] == specs.RED

    simHG.set_LED(specs.GREEN, specs.CONVERTER)
    LEDs = simHG.get_LEDs()
    assert LEDs[specs.CONVERTER] == specs.GREEN

    
def test_generate_red_LED(simHG):
    simHG.turn_on()
    simHG.set_LED(specs.RED, specs.CONVERTER)
    simHG.set_LED(specs.GREEN, specs.BOARD)
    rpm = specs.knots_to_rpm(AV_SPEED)
    reading1 = simHG.generate(rpm)
    assert reading1.power < 0
    
    simHG.set_LED(specs.RED, specs.BOARD)
    rpm = specs.knots_to_rpm(AV_SPEED)
    reading2 = simHG.generate(rpm)
    assert reading2.power < 0
    
def test_generate_high_bat(simHG):
    simHG.turn_on()
    simHG.set_LED(specs.GREEN, specs.CONVERTER)
    simHG.set_LED(specs.GREEN, specs.BOARD)
    rpm = specs.knots_to_rpm(AV_SPEED)
    reading = simHG.generate(rpm)
    assert reading.power == 0
    
def test_generate_green_and_low(simHG):
    simHG.turn_on()
    simHG.set_LED(specs.GREEN, specs.CONVERTER)
    simHG.set_LED(specs.GREEN, specs.BOARD)
    simHG.battery.power = specs.MAX_BATT_LEVEL - 1
    rpm = specs.knots_to_rpm(AV_SPEED)
    reading = simHG.generate(rpm)
    scaled_pow = AV_POW * specs.FACTOR_DICT[simHG.manufacture_version]
    assert reading.power == pytest.approx(scaled_pow, rel=0.5)
