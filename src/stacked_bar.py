# libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc

# Thanks to Olivier Gaudard for this example! https://python-graph-gallery.com/12-stacked-barplot-with-matplotlib/


# nice colors
yellow = "#fed919"
cyan = "#2db2a1"
pink = "#ff6f61"
magenta = "#a41d53"
purple = "#6a45ce"
green = "#3ecc54"
COLORS = [purple, green, pink, yellow, magenta, cyan]


def draw_bars(all_bars):
    first_key = list(all_bars.keys())[0]
    days = len(all_bars[first_key])
    # The position of the bars on the x-axis
    r = range(days)
    # Names of group and bar width (assuming the data starts at the first of the month)
    names = [str(x + 1) for x in r]
    barWidth = 0.5

    # Draw bars
    bottom = [0 for x in r]
    edgecolor = "white"
    x = 0
    for label in all_bars.keys():
        # There is nothing below the first bar, skip it for the first iteration
        if x > 0:
            print(previous_bar)
            bottom = np.add(bottom, previous_bar).tolist()

        plt.bar(r, all_bars[label], bottom=bottom, color=COLORS[x], edgecolor=edgecolor, width=barWidth, label=label)
        x += 1
        previous_bar = all_bars[label]

    # Custom X axis
    plt.xticks(r, names, fontweight='bold')
    plt.xlabel("Days")
    plt.ylabel("Cost")

    plt.legend()

    # y-axis in bold
    rc('font', weight='bold')

    # Show graphic
    plt.show()


if __name__ == "__main__":
    # Values of each group
    all_bars = {
        "Lambda": [12, 28, 1, 8, 22, 21, 12],
        "EC2": [28, 7, 16, 4, 10, 11, 14],
        "Salt": [25, 3, 23, 25, 17, 2, 2],
        "Pepper": [25, 3, 23, 25, 17, 2, 2]
    }

    draw_bars(all_bars)
