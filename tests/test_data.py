from pathlib import Path

import pytest

from tennisages.data import _parse_rows, clean_matches

MOCK = Path(__file__).parent / "data"
FEMALE = (MOCK / "FemalePlayerCareer.js").read_text()
MALE = (MOCK / "MalePlayerCareer.js").read_text()


def test_parse_rows_ignores_comment_and_wrapper():
    assert len(_parse_rows(FEMALE)) == 3
    assert _parse_rows(MALE)[0][11] == "Guillermo Platel"


def test_female_opponent_age_comes_from_birth_date():
    df = clean_matches(FEMALE, "1981-09-26")
    assert len(df) == 3
    assert df.loc[0, "opponent_age"] == pytest.approx(18.78, abs=0.01)  # born 1977-01-19, match 1995-10-30
    assert df.loc[0, "player_age"] == pytest.approx(14.1, abs=0.01)
    assert set(df["result"]) == {"Loss"}


def test_male_opponent_age_is_used_as_is():
    df = clean_matches(MALE, "1986-06-03")
    assert df["opponent_age"].tolist() == [22.264, 24.29, 18.76]
    assert df.loc[0, "player_age"] == pytest.approx(15.27, abs=0.01)
    assert df["result"].tolist() == ["Loss", "Loss", "Win"]


def test_rows_without_opponent_age_are_dropped():
    js = 'var morematchmx = [["20010910","T","Hard","S","W","","","","","","","A","","","","","","","","0"]];'
    assert clean_matches(js, "1986-06-03").empty
