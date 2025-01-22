import typer
from rich.console import Console
from rich.table import Table
from typing_extensions import NamedTuple

from strive.models.duration import Duration, miles_to_km

app = typer.Typer()


class Limits(NamedTuple):
    lower: int
    upper: int


TRAINING_PACES = {
    "easy": Limits(lower=75, upper=83),
    "tempo": Limits(lower=90, upper=95),
    "threshold": Limits(lower=98, upper=102),
    "interval": Limits(lower=105, upper=111),
    "repetitions": Limits(lower=115, upper=119),
}

REP_DISTANCES = [500, 400, 300, 200, 100]


@app.command()
def paces(threshold_pace: str):
    threshold = Duration.from_string(threshold_pace)

    table = Table(title=f"\nPaces for {str(threshold)}")
    table.add_column("Type", justify="right", no_wrap=True)
    table.add_column("Faster pace", justify="right", no_wrap=True)
    table.add_column("Slower pace", justify="right", no_wrap=True)

    for key, value in TRAINING_PACES.items():
        lower, upper = value
        lower_duration = threshold.adjust(lower)
        upper_duration = threshold.adjust(upper)
        table.add_row(key, str(upper_duration), str(lower_duration))

    console = Console()
    console.print(table)


@app.command()
def reps(threshold_pace: str, imperial: bool = False):
    if imperial:
        units = "mi"
        threshold = Duration.from_seconds(round(miles_to_km(threshold_pace)))
    else:
        units = "km"
        threshold = Duration.from_string(threshold_pace)

    slower, faster = TRAINING_PACES["repetitions"]
    slower_duration = threshold.adjust(slower)
    faster_duration = threshold.adjust(faster)

    table = Table(title=f"\nPaces for {threshold_pace}/{units}")
    table.add_column("Distance", justify="right", no_wrap=True)
    table.add_column("Faster reps", justify="right", no_wrap=True)
    table.add_column("Slower reps", justify="right", no_wrap=True)

    for distance in REP_DISTANCES:
        slower_secs = round(slower_duration.to_seconds() * distance / 1000.0)
        faster_secs = round(faster_duration.to_seconds() * distance / 1000.0)
        table.add_row(f"{str(distance)}m", f"{faster_secs}", f"{slower_secs}")

    console = Console()
    console.print(table)
