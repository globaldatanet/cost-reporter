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
light_green = "#3ecc54"
dark_green = "#2db2a1"
COLORS = [purple, dark_green, pink, yellow, light_green, magenta, cyan]


def draw_bars(all_bars, dates, title):
    first_key = list(all_bars.keys())[0]
    days = len(all_bars[first_key])
    # The position of the bars on the x-axis
    r = range(days)
    # Names of group and bar width (assuming the data starts at the first of the month)
    barWidth = 0.5

    # Draw bars
    bottom = [0 for x in r]
    edgecolor = "white"
    x = 0
    for label in all_bars.keys():
        # There is nothing below the first bar, skip it for the first iteration
        if x > 0:
            print(previous_bar)  # noqa: F821
            bottom = np.add(bottom, previous_bar).tolist()  # noqa: F821

        plt.bar(r, all_bars[label], bottom=bottom, color=COLORS[x], edgecolor=edgecolor, width=barWidth, label=label)
        x += 1
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
    plt.savefig('/tmp/image.png', bbox_inches='tight')
