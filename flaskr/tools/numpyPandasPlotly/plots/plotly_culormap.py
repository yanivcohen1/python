import plotly.graph_objects as go
import numpy as np

data = [
['Monday', 'Morning', 1],
['Monday', 'Afternoon', 20],
['Monday', 'Evening', 30],
['Tuesday', 'Morning', None],
['Tuesday', 'Afternoon', 1],
['Tuesday', 'Evening', 60],
['Wednesday', 'Morning', 30],
['Wednesday', 'Afternoon', 60],
['Wednesday', 'Evening', 1],
['Thursday', 'Morning', 50],
['Thursday', 'Afternoon', 80],
['Thursday', 'Evening', -10],
['Friday', 'Morning', 1],
['Friday', 'Afternoon', 30],
['Friday', 'Evening', 20]
]


seq_time = {'Morning':0, 'Afternoon':1, 'Evening':2}
seq_day = {'Monday':0, 'Tuesday': 1, 'Wednesday':2, 'Thursday':3, 'Friday':4}
data.sort(key = lambda x: seq_time[x[1]])
z = np.array([i[2] for i in data]).reshape(3,5).astype(float)
x = sorted(list(set([i[0] for i in data])), key = lambda x: seq_day[x])
y = sorted(list(set([i[1] for i in data])), key = lambda x: seq_time[x])

fig = go.Figure(data=go.Heatmap(
                   z=z,
                   x=x,
                   y=y,
                   hoverongaps = False))
fig.show()
