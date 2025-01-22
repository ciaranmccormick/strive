from math import exp
import typer
from rich import print

from strive.models.duration import Duration

app = typer.Typer()


@app.command()
def distance(pace: str, duration: str):
    """Calculate the total distance covered for a particular pace
    and duration.

    Pace and duration can be specified in a standard H:M:S or M:S format
    or using the PTH1M23S5 ISO 8601 format.
    """
    duration_obj = Duration.from_string(duration=duration)
    pace_obj = Duration.from_string(duration=pace)
    distance = round(duration_obj.to_seconds() / pace_obj.to_seconds(), 2)
    print(f"{distance}")


@app.command()
def pace(distance: float, duration: str):
    """Calculate a pace from a distance and a duration.

    Duration can be specified in a standard H:M:S or M:S format
    or using the PTH1M23S5 ISO 8601 format.
    """
    total_seconds = Duration.from_string(duration=duration).to_seconds()
    seconds_per_distance = int(total_seconds / distance)
    pace = Duration.from_seconds(total_seconds=seconds_per_distance)
    print(str(pace))


@app.command()
def time(distance: float, pace: str) -> None:
    """Calculate a time from a distance and a pace.

    Pace can be specified in a standard H:M:S or M:S format
    or using the PTH1M23S5 ISO 8601 format.
    """
    pace_in_seconds = Duration.from_string(duration=pace).to_seconds()
    total_time = int(pace_in_seconds * distance)
    duration = Duration.from_seconds(total_seconds=total_time)
    print(str(duration))


@app.command()
def tanda(distance: float, pace: str) -> None:
    """Calculates a predicted marathon pace using the Tanda formula."""
    P = Duration.from_string(pace).to_seconds()
    pace_sec_per_km = round(17.1 + 140.0 * exp(-0.0053 * distance) + 0.55 * P)
    predicted_pace = Duration.from_seconds(pace_sec_per_km)
    print(str(predicted_pace))
