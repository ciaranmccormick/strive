import pytest

from strive.models.duration import Duration

HMS = tuple[int, int, int]


@pytest.mark.parametrize(
    "test_value,expected",
    [
        ("PTH1M1S1", (1, 1, 1)),
        ("PTH0M20S15", (0, 20, 15)),
        ("PTM20S15", (0, 20, 15)),
        ("PTS15", (0, 0, 15)),
        ("PTH1S5", (1, 0, 5)),
        ("PTH1M0", (1, 0, 0)),
        ("PTH0M0S0", (0, 0, 0)),
        ("PT", (0, 0, 0)),
    ],
)
def test_from_string(test_value: str, expected: HMS):
    duration = Duration.from_string(test_value)
    hours, minutes, seconds = expected
    assert duration.hours == hours
    assert duration.minutes == minutes
    assert duration.seconds == seconds


@pytest.mark.parametrize(
    "test_value,expected",
    [
        ((1, 1, 1), 3661),
        ((0, 1, 1), 61),
        ((0, 0, 1), 1),
        ((5, 1, 1), 18061),
    ],
)
def test_to_seconds(test_value: HMS, expected: int):
    hours, minutes, seconds = test_value
    duration = Duration(hours=hours, minutes=minutes, seconds=seconds)
    assert duration.to_seconds() == expected


@pytest.mark.parametrize(
    "test_value,expected",
    [
        (3661, (1, 1, 1)),
        (61, (0, 1, 1)),
        (1, (0, 0, 1)),
        (18061, (5, 1, 1)),
    ],
)
def test_from_seconds(test_value: int, expected: HMS):
    hours, minutes, seconds = expected
    duration = Duration.from_seconds(test_value)
    assert duration.hours == hours
    assert duration.minutes == minutes
    assert duration.seconds == seconds


@pytest.mark.parametrize(
    "test_value,test_percent,expected",
    [
        (240, 100, 240),
        (240, 50, 480),
        (200, 110, 182),
        (200, 130, 154),
        (321, 75, 428),
        (200, 121, 165),
    ],
)
def test_adjust(test_value: int, test_percent: int, expected: int) -> None:
    duration = Duration.from_seconds(test_value)
    adjusted_duration = duration.adjust(test_percent)
    assert adjusted_duration.to_seconds() == expected
