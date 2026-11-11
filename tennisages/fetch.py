"""Download a player's career from Tennis Abstract."""
import re
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from tennisages.data import clean_matches

BASE = "https://www.tennisabstract.com"


def _normalize_name(name):
    """'serena williams' / 'Serena Williams' / 'SerenaWilliams' -> 'SerenaWilliams'."""
    words = name.split()
    return "".join(w.capitalize() for w in words) if len(words) > 1 else name.strip()


def _download(url):
    request = Request(url, headers={"User-Agent": "tennisages (student project)"})
    with urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def _player_dob(key):
    """The career JS has no birth date for the player, but the player page defines `var dob = YYYYMMDD;`."""
    match = re.search(r"var dob = (\d{8})", _download(f"{BASE}/cgi-bin/player.cgi?p={key}"))
    if match is None:
        raise ValueError(f"No birth date found for player {key!r}.")
    return match.group(1)


def get_player_matches(name):
    """Career matches of a player as a DataFrame (player_age, opponent_age, result, ...)."""
    key = _normalize_name(name)
    try:
        js_text = _download(f"{BASE}/jsmatches/{key}Career.js")
    except HTTPError as error:
        if error.code == 404:
            raise ValueError(f"Player {name!r} not found on Tennis Abstract. Check the spelling, e.g. 'Serena Williams'.") from None
        raise
    return clean_matches(js_text, _player_dob(key))
