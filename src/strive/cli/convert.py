import typer
from rich import print

from strive.constants import KM_IN_A_MILE, MILES_IN_A_KM
from strive.models.duration import Duration, km_to_miles, miles_to_km

app = typer.Typer()


@app.command()
def pace(duration: str, to_metric: bool = False):
    """Convert paces from metric to imperial and vice versa.

    If --to-metric is used pace is coverted from imperial to metric.

    """
    if not to_metric:
        units = "mi"
        pace = round(km_to_miles(duration))
    else:
        units = "km"
        pace = round(miles_to_km(duration))

    new_duration = Duration.from_seconds(pace)
    print(f"{str(new_duration)}/{units}")


@app.command()
def distance(distance: float, to_metric: bool = False):
    """Convert distances from metric to imperial and vice versa.

    If --to-metric is used distance is coverted from imperial to metric.

    """
    if not to_metric:
        units = "mi"
        new_distance = round(distance * MILES_IN_A_KM, 2)
    else:
        units = "km"
        new_distance = round(distance * KM_IN_A_MILE, 2)

    print(f"{new_distance}{units}")
