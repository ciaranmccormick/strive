from pydantic import BaseModel, field_validator
from typing_extensions import Self, override

from strive.constants import (
    KM_IN_A_MILE,
    MILES_IN_A_KM,
    SECONDS_IN_HOURS,
    SECONDS_IN_MINUTES,
)
from strive.utils import parse_duration, to_int


class Duration(BaseModel):
    hours: int = 0
    minutes: int = 0
    seconds: int = 0

    @override
    def __str__(self) -> str:
        if self.hours > 0:
            return f"{self.hours:02}:{self.minutes:02}:{self.seconds:02}"
        else:
            return f"{self.minutes:02}:{self.seconds:02}"

    @field_validator("*", mode="before")
    def validate_ints(cls, v: str) -> int:
        return to_int(v)

    def to_seconds(self) -> int:
        """Return the total seconds of the Duration."""
        return (
            self.hours * SECONDS_IN_HOURS
            + self.minutes * SECONDS_IN_MINUTES
            + self.seconds
        )

    @classmethod
    def from_string(cls, duration: str) -> Self:
        """Parse a duration string and return a Duration."""
        return cls.model_validate(parse_duration(duration=duration))

    @classmethod
    def from_seconds(cls, total_seconds: int) -> Self:
        """Create a duration from number of seconds."""
        hours = int(total_seconds // SECONDS_IN_HOURS)
        remainder_seconds = total_seconds - (hours * SECONDS_IN_HOURS)
        minutes = int(remainder_seconds // SECONDS_IN_MINUTES)
        seconds = int(remainder_seconds % SECONDS_IN_MINUTES)
        return cls(hours=hours, minutes=minutes, seconds=seconds)

    def adjust(self, percent: int) -> Self:
        """Adjust the duration by `percent`."""
        total_seconds = self.to_seconds()
        divisor = percent / 100.0
        new_total_seconds = round(total_seconds / divisor)
        return self.from_seconds(new_total_seconds)


def miles_to_km(pace: str) -> int:
    return round(Duration.from_string(duration=pace).to_seconds() * MILES_IN_A_KM)


def km_to_miles(pace: str) -> int:
    return round(Duration.from_string(duration=pace).to_seconds() * KM_IN_A_MILE)
