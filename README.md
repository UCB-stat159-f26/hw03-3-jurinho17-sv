# tennisages

A small Python package for HW03. It downloads a player's career matches from [tennisabstract.com](https://www.tennisabstract.com) and plots the player's age against the age gap to each opponent. The plot is like the NYT graphic from HW2, minus the annotations.

## Install

```bash
pip install git+https://github.com/UCB-stat159-f26/hw03-3-jurinho17-sv.git
```

## Usage

```python
from tennisages import get_player_matches, plot_age_scatter

serena = get_player_matches("serena williams")   # also "Serena Williams" or "SerenaWilliams"
plot_age_scatter(serena)

rafa = get_player_matches("Rafael Nadal")
plot_age_scatter(rafa)

get_player_matches("GastonSanchez")              # ValueError: Player 'GastonSanchez' not found ...
```

- `get_player_matches(name)` returns a DataFrame with `date`, `tournament`, `surface`, `result`, `opponent`, `player_age` and `opponent_age`. Matches with no opponent age are dropped.
- `plot_age_scatter(matches)` draws player age on the x-axis and opponent age minus player age on the y-axis, colored by win or loss. It returns the matplotlib `Axes`.

## Tests

```bash
pip install -e ".[test]"
pytest
```

The tests use the mock career files in `tests/data/` and never contact the live site.

## Reflections

- My mock-based tests all passed, but the first run on Serena's real file crashed. The real file ends in `"]`, a newline and `];`, not `]];`. Mock data only tests what I already thought to put in it, so I now also run a real man and a real woman by hand.
- The career file has no birth date for the player. I found it on the player's page (`var dob = ...`), and the same lookup works for women and men.
- Downloading the career file first is the easiest way to catch a wrong name, because Tennis Abstract answers 404 for it.
- The 20-line limit made me split parsing, cleaning and downloading into small functions, and the small pieces were easy to test.
