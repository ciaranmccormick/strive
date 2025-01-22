import re


class ParsingError(Exception):
    """Exception when unable to parse a duration string."""

    pass


def to_int(value: str) -> int:
    """Convert a str to an int, an empty string will return 0."""
    if value == "":
        return 0
    return int(value)


def parse_duration(duration: str) -> dict[str, str]:
    """Parsing a duration string into a dictionary containing the hours,
    minutes and seconds.

    Three formats are accepted H:M:S, M:S or the ISO 8601 standard
    for durations (i.e. PTH1M12S).
    """
    if duration.count(":") == 1:
        pattern = r"(?P<minutes>\d*):?(?P<seconds>\d*)"
    elif duration.count(":") == 2:
        pattern = r"(?P<hours>\d*):?(?P<minutes>\d*):?(?P<seconds>\d*)"
    else:
        pattern = r"PTH?(?P<hours>\d*)M?(?P<minutes>\d*)S?(?P<seconds>\d*)"

    if matches := re.search(pattern, duration):
        return matches.groupdict()
    raise ParsingError("Unable to parse duration string.")
