#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generate Tetris 99-style graphs from game statistics."""

import matplotlib.pyplot as pyplot
from matplotlib.ticker import MaxNLocator
import pandas

import sys

## Config

# VIP filter flag
# True: VIP games only
# False: Normal (T99) games only
VIP = True

# Figure size
X_IN = 15
Y_IN = 5

# Figure colors
BACKGROUND_COLOR = "#0c2359"
AXIS_COLOR = "#5c73a9"
PLACE_COLOR = "#56abfb"
KO_COLOR = "tab:red"

## Main entry

if len(sys.argv) < 3:
    sys.exit("Usage: generate_graphs.py stats.xls sheet_name")

channel = pandas.read_excel(sys.argv[1], sheet_name=sys.argv[2])
channel = channel.fillna("") # Fill empty cells to avoid attribute errors

# Filter games
if VIP:
    channel = channel.loc[channel["VIP"] == "Y"] # TODO: Any, not just "Y"
else:
    channel = channel.loc[channel["VIP"] != "Y"]

# Dumb index hack for axis numbering
channel = channel.reset_index()
channel = channel.rename(columns={"index": "Overall_Index"}) # Index for all games on sheet
channel = channel.reset_index()
channel = channel.rename(columns={"index": "Game"}) # Index for games being analyzed
channel["Game"] = channel["Game"] + 1 # Start index at 1

## Overall stats line graph
fig = pyplot.subplots()[0]
fig.set_size_inches(X_IN, Y_IN)
fig.set_facecolor(BACKGROUND_COLOR)

ax1 = pyplot.gca()
ax1.set_facecolor(BACKGROUND_COLOR)

ax1.set_xlabel("Game")
ax1.xaxis.label.set_color(AXIS_COLOR)
ax1.tick_params(axis="x", colors=AXIS_COLOR)
ax1.set_xlim([0, channel.shape[0] + 1]) # Margin on both sides
ax1.xaxis.get_major_ticks()[0].set_visible(False) # Hide 0
ax1.xaxis.tick_top()
ax1.xaxis.set_label_position("top")

ax1.yaxis.label.set_color(PLACE_COLOR)
ax1.tick_params(axis="y", colors=BACKGROUND_COLOR)
ax1.tick_params(axis="y", labelcolor=AXIS_COLOR)
ax1.set_ylabel("Place")
ax1.set_ylim([1,99])
ax1.invert_yaxis()
ax1.set_yticks([1,21,41,61,81,99])
ax1.axhline(y=1, color=AXIS_COLOR) # Axis lines
ax1.axhline(y=21, color=AXIS_COLOR)
ax1.axhline(y=41, color=AXIS_COLOR)
ax1.axhline(y=61, color=AXIS_COLOR)
ax1.axhline(y=81, color=AXIS_COLOR)

ax1.spines["top"].set_visible(False)
ax1.spines["bottom"].set_visible(False)
ax1.spines["left"].set_visible(False)
ax1.spines["right"].set_visible(False)

# Draw place line shadow
channel["Rank"] += 1
pyplot.axis("off")
channel.plot(kind="line", legend=None, x="Game", y="Rank", color="black", marker="s", markersize=7.5, linewidth=2.5, clip_on=False, ax=ax1)

# Draw main place line
pyplot.axis("on")
channel["Rank"] -= 1
channel.plot(kind="line", legend=None, x="Game", y="Rank", color=PLACE_COLOR, marker="s", markersize=7.5, linewidth=2.5, clip_on=False, ax=ax1)

# Annotate placements
for x, y in zip(channel["Game"], channel["Rank"]):
    if y < 20:
        offset = -15
    else:
        offset = 8
    pyplot.annotate(y, (x, y), textcoords="offset points", xytext=(0,offset), ha="center", color="white")

# KOs
ax2 = ax1.twinx()
ax2.tick_params(axis="y", colors=BACKGROUND_COLOR)
ax2.yaxis.label.set_color(KO_COLOR)
ax2.set_ylabel("K.O.")
ax2.set_ylim([0,25])

ax2.spines["top"].set_visible(False)
ax2.spines["bottom"].set_visible(False)
ax2.spines["left"].set_visible(False)
ax2.spines["right"].set_visible(False)

# Drawn KOs line
channel.plot(kind="line", legend=None, x="Game", y="KOs", color=KO_COLOR, marker="s", markersize=7.5, linewidth=2.5, clip_on=False, ax=ax2)

# Annotate KO numbers
for x, y in zip(channel["Game"], channel["KOs"]):
    pyplot.annotate(y, (x, y), textcoords="offset points", xytext=(0,8), ha="center", color="white")

fig.savefig("overall.png", bbox_inches="tight", facecolor=BACKGROUND_COLOR, dpi=125)

## Placements bar graph
fig.clf()
fig = pyplot.subplots()[0]
fig.set_facecolor(BACKGROUND_COLOR)
fig.set_size_inches(X_IN, Y_IN)

# Show places with no data
channel = channel.sort_values(by="Rank", ascending=True).groupby(by="Rank").size()
series = pandas.Series(channel)
channel = series.reindex([*range(1, 100, 1)] , fill_value=0)

ax3 = pyplot.gca()
ax3.set_facecolor(BACKGROUND_COLOR)

ax3.tick_params(axis="x", colors=AXIS_COLOR)
ax3.xaxis.label.set_color(AXIS_COLOR)
ax3.set_xlabel("Place")

ax3.tick_params(axis="y", colors=AXIS_COLOR)
ax3.tick_params(axis="y", labelcolor=AXIS_COLOR)
ax3.yaxis.label.set_color(AXIS_COLOR)
ax3.set_ylabel("Total")
ax3.yaxis.set_major_locator(MaxNLocator(integer=True)) # No floats

ax3.spines["top"].set_color(AXIS_COLOR)
ax3.spines["bottom"].set_color(AXIS_COLOR)
ax3.spines["left"].set_color(AXIS_COLOR)
ax3.spines["right"].set_color(AXIS_COLOR)

channel.plot(kind="bar", legend=None, color=PLACE_COLOR, x="Rank", y="Game", rot=0, ax=ax3)

ax3.set_xticks([0, 9, 24, 49, 74, 98]) # Set ticks after objects exist
ax3.set_xticklabels(["1", "10", "25", "50", "75", "99"])

fig.savefig("placements.png", bbox_inches="tight", facecolor=BACKGROUND_COLOR, dpi=125)
