import pandas as pd
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, HoverTool, WheelZoomTool, Range1d
from bokeh.io import output_notebook

# Load CSV data
df = pd.read_csv("pulses.csv")
df["Signal"] = df["Type"].map({"MARK": 1, "SPACE": 0})

# Build step plot data
time = []
signal = []

for i, row in df.iterrows():
    time.append(row["Start"])
    signal.append(row["Signal"])
    time.append(row["End"])
    signal.append(row["Signal"])

# Build Bokeh data source
source = ColumnDataSource(data=dict(
    time=time,
    signal=signal,
    label=["MARK" if s == 1 else "SPACE" for s in signal]
))

# Create interactive plot
p = figure(
    width=1000,
    height=300,
    title="IR Signal Viewer",
    tools="pan,box_zoom,reset",
    active_scroll=None,  # disable default scroll behavior
    x_axis_label="Time (µs)",
    y_axis_label="Signal",
    y_range=Range1d(-0.5, 1.5, bounds=(-0.5, 1.5)),  # fixed y-range
)

# Fix the y-axis range to disable vertical zooming
p.y_range.start = -0.5
p.y_range.end = 1.5

# Add horizontal-only zoom tool
wheel_zoom_x = WheelZoomTool(dimensions='width')
p.add_tools(wheel_zoom_x)
p.toolbar.active_scroll = wheel_zoom_x

# Step-like plot
p.step(x='time', y='signal', line_width=2, mode='after', source=source, legend_label="IR Signal")

# Add hover tool
hover = HoverTool(
    tooltips=[
        ("Time", "@time"),
        ("Signal", "@label"),
    ],
    mode="vline"
)
p.add_tools(hover)

# Display
output_notebook()  # or 
output_file("ir_viewer.html")
show(p)
