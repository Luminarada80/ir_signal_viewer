import pandas as pd
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, HoverTool, WheelZoomTool, Range1d
from bokeh.io import output_notebook
output_notebook()
# Load CSV data
df = pd.read_csv("pulses.csv")
from bokeh.models import HoverTool

# Prepare quad coordinates for each pulse segment
data = dict(
    left=df["Start"],
    right=df["End"],
    top=[1.1 if t == "MARK" else 0.1 for t in df["Type"]],
    bottom=[0.9 if t == "MARK" else -0.1 for t in df["Type"]],
    duration=df["Duration"],
    type=df["Type"]
)

source = ColumnDataSource(data)

p = figure(
    title="IR Signal", width=600, height=300,
    x_axis_label="Time (µs)", y_axis_label="Signal Received",
    y_range=Range1d(-0.5, 1.5, bounds=(-0.5, 1.5)),
    tools="reset, pan, wheel_zoom"
)
p.add_tools(WheelZoomTool(dimensions="width"))

# Add visible rectangular pulses
quad_renderer = p.quad(
    left="left", right="right", 
    top="top", bottom="bottom",
    source=source, 
    fill_color="navy", fill_alpha=0.4, line_color="black"
)

# Add hover tool for the full pulse spans
hover = HoverTool(
    renderers=[quad_renderer],
    tooltips=[
        ("Type", "@type"),
        ("Start", "@left"),
        ("End", "@right"),
        ("Duration", "@duration µs")
    ],
    mode='mouse'
)

p.add_tools(hover)

show(p)
