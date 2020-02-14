# t99-charts
Generate Tetris 99-style graphs from game statistics.

![alt text](https://raw.githubusercontent.com/bitbybyte/t99-charts/master/example.png)

## Requirements
- Python 3.x
- matplotlib
- pandas

## Usage
- Adjust config in `generate_graphs.py`
- Run using `python generate_graphs.py stats.xls sheet_name`

## Expected Input
For a given sheet:
|  Rank   | KOs      | VIP              |
|---------|----------|------------------|
| [1, 99] |  [0, 98] | {"Y", NULL}      |

## Miscellaneous
To add titles to a graph, use `set_title()` on the main axis for each figure:

`ax3.set_title(title, fontname="FOT-Comet Std", color="white", fontsize="24", pad=10)`
