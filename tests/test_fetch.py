from pathlib import Path
from urllib.error import HTTPError

import pytest

from tennisages import fetch

MOCK = Path(__file__).parent / "data"


@pytest.mark.parametrize("name", ["serena williams", "Serena Williams", "SerenaWilliams", "  serena  williams "])
def test_normalize_name(name):
    assert fetch._normalize_name(name) == "SerenaWilliams"


def fake_site(player_page="var dob = 19810926;", missing=()):
    """Stand-in for _download: serves the mock JS and a player page, never the network."""
    def download(url):
        if any(m in url for m in missing):
            raise HTTPError(url, 404, "Not Found", None, None)
        return (MOCK / "FemalePlayerCareer.js").read_text() if "jsmatches" in url else player_page
    return download


def test_get_player_matches(monkeypatch):
    monkeypatch.setattr(fetch, "_download", fake_site())
    df = fetch.get_player_matches("serena williams")
    assert len(df) == 3
    assert {"player_age", "opponent_age", "result"} <= set(df.columns)


def test_unknown_player_gives_meaningful_error(monkeypatch):
    monkeypatch.setattr(fetch, "_download", fake_site(missing=["jsmatches"]))
    with pytest.raises(ValueError, match="not found on Tennis Abstract"):
        fetch.get_player_matches("Gaston Sanchez")


def test_missing_birth_date_is_an_error(monkeypatch):
    monkeypatch.setattr(fetch, "_download", fake_site(player_page="<html></html>"))
    with pytest.raises(ValueError, match="No birth date"):
        fetch.get_player_matches("Serena Williams")
