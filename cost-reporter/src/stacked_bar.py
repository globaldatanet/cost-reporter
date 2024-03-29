import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rc

# Thanks to Olivier Gaudard for this example! https://python-graph-gallery.com/12-stacked-barplot-with-matplotlib/


# nice colors
YELLOW = "#fed919"
CYAN = "#2db2a1"
PINK = "#ff6f61"
MAGENTA = "#a41d53"
PURPLE = "#6a45ce"
LIGHT_GREEN = "#3ecc54"
DARK_GREEN = "#2db2a1"
COLORS = [PURPLE, DARK_GREEN, PINK, YELLOW, LIGHT_GREEN, MAGENTA, CYAN]


def generate_dates() -> List[str]:
    """ Create a short-format of dates which lends itself for labeling the X axis.
    """
    days = int(os.environ["DAYS"])

    dates = [(datetime.today() - timedelta(days=i)).strftime("%d") for i in range(0, days)]
    dates.reverse()

    return dates


def draw_bars(all_bars: Dict[str, List[float]], title: str) -> None:
    dates = generate_dates()
    days = len(dates)
    # The position of the bars on the x-axis
    r = range(days)
    # Names of group and bar width (assuming the data starts at the first of the month)
    bar_width = 0.5

    # Draw bars
    bottom = [0] * days
    edgecolor = "white"
    for idx, label in enumerate(all_bars.keys()):
        # There is nothing below the first bar, skip it for the first iteration
        if idx > 0:
            bottom = np.add(bottom, previous_bar).tolist()  # noqa: F821

        plt.bar(r, all_bars[label], bottom=bottom, color=COLORS[idx], edgecolor=edgecolor, width=bar_width, label=label)
        previous_bar = all_bars[label]  # noqa: F841

    # Custom X axis
    plt.xticks(r, dates, fontweight='bold')
    plt.xlabel("Days")
    plt.ylabel("Cost")

    plt.legend()
    plt.title(title)

    # y-axis in bold
    rc('font', weight='bold')

    # Show graphic
    plt.savefig(Path('/tmp/image.png'), bbox_inches='tight')
