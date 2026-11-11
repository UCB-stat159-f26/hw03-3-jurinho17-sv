"""Turn a Tennis Abstract career JS file into a clean DataFrame."""
import json

import pandas as pd

DAYS_PER_YEAR = 365.25
# positions inside each `morematchmx` row
COLUMNS = {0: "date", 1: "tournament", 2: "surface", 4: "result", 11: "opponent", 16: "opponent_info"}


def _parse_rows(js_text):
    """Strip the JS wrapper of `var morematchmx = [[...], ...];` and parse the array as JSON."""
    return json.loads(js_text[js_text.index("["):js_text.rindex("]") + 1])


def _years(timedelta):
    return (timedelta.dt.days / DAYS_PER_YEAR).round(3)


def _opponent_age(date, info):
    """Women's files hold the opponent's birth date (YYYYMMDD), men's files hold the age itself."""
    is_dob = info.str.fullmatch(r"\d{8}").fillna(False).astype(bool)
    dob = pd.to_datetime(info.where(is_dob), format="%Y%m%d", errors="coerce")
    return _years(date - dob).where(is_dob, pd.to_numeric(info, errors="coerce").round(3))


def clean_matches(js_text, player_dob):
    """Return one row per match: date, tournament, surface, result, opponent, player_age, opponent_age."""
    df = pd.DataFrame(_parse_rows(js_text)).iloc[:, list(COLUMNS)]
    df.columns = list(COLUMNS.values())
    df["date"] = pd.to_datetime(df["date"], format="%Y%m%d")
    df["player_age"] = _years(df["date"] - pd.Timestamp(player_dob))
    df["opponent_age"] = _opponent_age(df["date"], df.pop("opponent_info"))
    df["result"] = df["result"].map({"W": "Win", "L": "Loss"})
    return df.dropna(subset=["result", "opponent_age"]).reset_index(drop=True)
