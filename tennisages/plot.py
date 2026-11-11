"""Scatter plot of a player's age vs. the age gap to each opponent."""
import matplotlib.pyplot as plt

COLORS = {"Win": "#2a9d8f", "Loss": "#e76f51"}


def plot_age_scatter(matches):
    """Plot player age (x) vs. opponent age minus player age (y), colored by result.

    `matches` is the DataFrame from get_player_matches(). Returns the matplotlib Axes.
    """
    _, ax = plt.subplots(figsize=(9, 6))
    for result, color in COLORS.items():
        d = matches[matches["result"] == result]
        ax.scatter(d["player_age"], d["opponent_age"] - d["player_age"], s=14, alpha=0.7,
                   color=color, edgecolors="none", label=f"{result} ({len(d)})")
    ax.axhline(0, color="gray", ls="--", lw=1)
    ax.set(xlabel="Player's age", ylabel="Opponent's age minus player's age (years)")
    ax.legend(frameon=False)
    ax.grid(alpha=0.3)
    return ax
