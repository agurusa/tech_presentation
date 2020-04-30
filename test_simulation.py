import pytest
from simulation import HydroGen


@pytest.fixture
def hydrogen():
    return HydroGen()


def test_conversion(hydrogen):
    av_speed = 5.7  # knots
    rpm = hydrogen.knots_to_rpm(av_speed)
    knots = hydrogen.rpm_to_knots(rpm)
    assert (av_speed == knots)


def test_generate(hydrogen):
    av_speed = 5.7  # knots
    av_pow = 80  # W
    rpm = hydrogen.knots_to_rpm(av_speed)
    hydrogen.generate(rpm)
    assert (hydrogen.pow_gen[-1].power == pytest.approx(av_pow, rel=0.5))