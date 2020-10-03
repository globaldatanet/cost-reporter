# libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import pandas as pd

# Thanks to Olivier Gaudard for this example! https://python-graph-gallery.com/12-stacked-barplot-with-matplotlib/


# nice colors
yellow = "#fed919"
cyan = "#2db2a1"
pink = "#ff6f61"
magenta = "#a41d53"
purple = "#6a45ce"
green = "#3ecc54"
colors = [purple, green, pink, yellow, magenta, cyan]


def draw_bars(all_bars):
    # The position of the bars on the x-axis
    r = range(len(all_bars[0]))
    # Names of group and bar width (assuming the data starts at the first of the month)
    names = [str(x + 1) for x in r]
    barWidth = 0.5

    # Draw bars
    bottom = [0 for x in all_bars[0]]
    edgecolor = "white"
    for x in range(len(all_bars)):
        # There is nothing below the first bar, skip it for the first iteration
        if x > 0:
            bottom = np.add(bottom, all_bars[x - 1]).tolist()

        plt.bar(r, all_bars[x], bottom=bottom, color=colors[x], edgecolor=edgecolor, width=barWidth)

    # Custom X axis
    plt.xticks(r, names, fontweight='bold')
    plt.xlabel("Days")
    plt.ylabel("Cost")

    # y-axis in bold
    rc('font', weight='bold')

    # Show graphic
    plt.show()


# Values of each group
all_bars = [
    [12, 28, 1, 8, 22, 21, 12],
    [28, 7, 16, 4, 10, 11, 14],
    [25, 3, 23, 25, 17, 2, 2],
    [25, 3, 23, 25, 17, 2, 2]
]

draw_bars(all_bars)