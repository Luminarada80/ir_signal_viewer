import pandas as pd
from bokeh.plotting import figure, show
from bokeh.io import output_notebook, output_file
from bokeh.models import ColumnDataSource, WheelZoomTool, \
  Range1d, HoverTool

output_notebook()

df = pd.read_csv("pulses.csv", header=0, index_col=None)

# Time > 0 between some rows, should be 0
def fill_missing_signals_with_spaces(df: pd.DataFrame) -> pd.DataFrame:
  """
  Adds rows with SPACES for times when signals were not received.

  The dataset contains gaps in time where signals were not received 
  between MARKs. These should have a value of 0 in the step function,
  but will instead have a value of 1 if the missing time values are not
  filled in with SPACE. This causes the bokeh plot to show signals of 1
  for missing signals. The follwoing code finds lines where the End of
  a signal row does not match the Start of the next row, and fills in the 
  missing information with a SPACE value.
  """
  for i, row in df.iterrows():
    if i < df.shape[0] - 1:
      if df.loc[i, "End"] != df.loc[i+1, "Start"]:
        missing_row_start = df.loc[i, "End"]
        missing_row_duration = df.loc[i+1, "Start"] - df.loc[i, "End"]
        missing_row_end = df.loc[i+1, "Start"]
        missing_row_type = "SPACE"

        # Fill in the missing row information as a space
        df.loc[i+1] = [
          missing_row_start, 
          missing_row_duration,
          missing_row_end, 
          missing_row_type
          ]
      
        df.index = df.index + 1
        df = df.sort_index()

        return df

df = fill_missing_signals_with_spaces(df)

x_coords = df["Start"]
y_coords = [1 if i == "MARK" else 0 for i in df["Type"]]

data = dict(
  signal_start=x_coords,
  signal_value=y_coords,
  duration=df["Duration"]
  )

source = ColumnDataSource(data)

p = figure(
  title="IR Signal", width=600, height=300,
  x_axis_label="Time (us)", y_axis_label="Signal Received",
  y_range=Range1d(-0.5, 1.5, bounds=(-0.5, 1.5)),
  tools=["reset, pan, xbox_select"]
)

p.add_tools(WheelZoomTool(dimensions="width"))

step_plot = p.step(
  x="signal_start", 
  y="signal_value",
  source=source,
  line_width=2,
  mode="center"
  )

circle_renderer = p.circle(
  x="signal_start",
  y="signal_value",
  source=source,
  size=8,
  alpha=0,  # fully transparent
  hover_alpha=0.6,  # fade in on hover
  color="orange"
)

tooltips = [
  ("Duration", "@duration")
]

dur_hover_tool = HoverTool(
  renderers=[circle_renderer],
  tooltips=[*tooltips]
  )

p.add_tools(dur_hover_tool)

show(p)