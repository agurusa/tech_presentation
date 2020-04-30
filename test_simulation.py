import pytest
import simulation as sim

# watt & sea test constants
AV_SPEED = 5.7  # knots
AV_POW = 80  # W


@pytest.fixture
def hydrogen():
    return sim.HydroGen()


def test_conversion(hydrogen):
    av_speed = 5.7  # knots
    rpm = hydrogen.knots_to_rpm(av_speed)
    knots = hydrogen.rpm_to_knots(rpm)
    assert (av_speed == knots)


def test_get_pow(hydrogen):
    with pytest.raises(Exception) as exc:
        hydrogen.get_pow(sim.MAX + 1)
        assert sim.EXCEPT_MAXTIME in str(exc.value)

    with pytest.raises(Exception) as exc:
        hydrogen.get_pow(10)
        assert sim.EXCEPT_OFF in str(exc.value)

    first_reading = hydrogen.generate(0)
    assert (hydrogen.get_pow(10) == [first_reading])

    rpm = hydrogen.knots_to_rpm(AV_SPEED)
    second_reading = hydrogen.generate(rpm)
    assert (hydrogen.get_pow(10) == [first_reading, second_reading])


def test_set_LEDs(hydrogen):
    with pytest.raises(Exception) as exc:
        hydrogen.set_LED('blue', sim.CONVERTER)
        assert sim.EXCEPT_COLOR in str(exc.value)

    with pytest.raises(Exception) as exc:
        hydrogen.set_LED(sim.GREEN, 'hull_computer')
        assert sim.EXCEPT_LOC in str(exc.value)

    hydrogen.set_LED(sim.RED, sim.BOARD)
    assert (hydrogen.get_LED(sim.BOARD) == sim.RED)

    hydrogen.set_LED(sim.GREEN, sim.CONVERTER)
    assert (hydrogen.get_LED(sim.CONVERTER) == sim.GREEN)


def test_generate(hydrogen):
    rpm = hydrogen.knots_to_rpm(AV_SPEED)
    reading = hydrogen.generate(rpm)
    assert (reading.power == pytest.approx(AV_POW, rel=0.5))
