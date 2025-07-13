# https://plotly.com/python/
# https://www.geeksforgeeks.org/python-plotly-tutorial/
import cufflinks as cf
import plotly.express as px
import plotly.graph_objects as go

# Make Plotly work in your Jupyter Notebook
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

# init_notebook_mode(connected=True)
# Use Plotly locally
# cf.go_offline()
import pandas as pd

pd.options.plotting.backend = "plotly"

print(pd.to_datetime(['2018-10-26 12:00 -0530', '2018-10-26 12:00 -0500'],
                utc=True)[0]) # 2018-10-26 17:30:00+00:00

csv = {
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "Sales": [1000, 1200, 1500, 1800, 2000, 2200],
    "Profit": [200, 300, 400, 500, 600, 700],
    "time": [1, 2, 3],
}

table = pd.DataFrame(csv, columns=["Month", "Sales", "Profit"])  # option to fillter
# table = pd.read_csv('data.csv')

# Panda print 2 first rows
# use a list of indexes:
print(table.loc[[0, 1]])
#    Month  Sales  Profit
# 0   Jan   1000     200
# 1   Feb   1200     300


# ------------ using plotly express --------

# Make multiple line plots
fig = px.line(
    table,
    x="Month",
    y=["Sales", "Profit"],  # select two columes for two lines
    # labels={'x':'Date', 'y':'Value of Dollar'}, # not working take it from the colume name
    title="Sales Vs. Profit",
    markers=True,
)

fig.update_layout(yaxis_title="Y Axis Title", legend_title="Legend Title")

fig.show()


# -------------- using panda for plot -----------------

# plot a line plot of the Sales column with points
# fig = go.Figure()
fig: go.Figure = table.plot.line(
    x="Month", y=["Sales", "Profit"], title="plot for panda data", markers=True
)

fig.update_layout(yaxis_title="Y Axis Title", legend_title="Legend Title")

fig.show()


# -------------- using panda and numpy for multiline plot -----------------

import numpy as np
import pandas as pd

df1 = pd.DataFrame({"X":np.linspace(0,30,10), "Y":np.random.rand(10)})
df2 = pd.DataFrame({"A":np.linspace(20,40,9), "B":np.random.rand(9)})

fig1 = px.line(df1, x='X', y='Y', title="X Vs. Y", markers=True)
fig2 = px.line(df2, x='A', y='B', title="A Vs. B", markers=True)

fig = go.Figure(data = fig1.data + fig2.data)
fig['data'][0]['line']['color']='rgb(204, 104, 100)' # 0 for fig1
fig.update_layout(title='Data Titles', yaxis_title="Y Axis Title", xaxis_title="X Axis Title",
                  legend_title="Legend Title")
fig.show()
