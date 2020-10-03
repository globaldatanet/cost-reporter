# libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import pandas as pd


# nice colors
yellow = "#fed919"
cyan = "#2db2a1"
pink = "#ff6f61"
purple = "#a41d53"
green = "#3ecc54"
colors = [purple, green, pink, yellow, cyan]

# y-axis in bold
rc('font', weight='bold')
 
# Values of each group
bars1 = [12, 28, 1, 8, 22]
bars2 = [28, 7, 16, 4, 10]
bars3 = [25, 3, 23, 25, 17]
 
# Heights of bars1 + bars2
bars = np.add(bars1, bars2).tolist()
 
# The position of the bars on the x-axis
r = [0,1,2,3,4]
 
# Names of group and bar width
names = ['1','2','3','4','5']
barWidth = 0.5
 
# Create brown bars
plt.bar(r, bars1, color=colors[0], edgecolor='white', width=barWidth)
# Create green bars (middle), on top of the firs ones
plt.bar(r, bars2, bottom=bars1, color=colors[1], edgecolor='white', width=barWidth)
# Create green bars (top)
plt.bar(r, bars3, bottom=bars, color=colors[2], edgecolor='white', width=barWidth)
 
# Custom X axis
plt.xticks(r, names, fontweight='bold')
plt.xlabel("Days")
plt.ylabel("Cost")
 
# Show graphic
plt.show()
