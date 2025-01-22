import typer

from strive.cli import calculate, coach, convert

app = typer.Typer()

app.add_typer(convert.app, name="convert")
app.add_typer(calculate.app, name="calculate")
app.add_typer(coach.app, name="coach")


def cli():
    app()
