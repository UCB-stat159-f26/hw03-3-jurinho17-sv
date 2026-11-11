import matplotlib

matplotlib.use("Agg")

from tennisages.data import clean_matches
from tests.test_data import MALE


def test_plot_has_one_point_per_match_and_win_loss_legend():
    from tennisages import plot_age_scatter

    matches = clean_matches(MALE, "1986-06-03")
    ax = plot_age_scatter(matches)
    assert sum(len(c.get_offsets()) for c in ax.collections) == len(matches)
    assert [t.get_text() for t in ax.get_legend().get_texts()] == ["Win (1)", "Loss (2)"]
