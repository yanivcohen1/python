# https://plotly.com/javascript/
# bebbug run: Python: Flask plotly
# python debugger: debug python file
# in terminal run: python -m flask run
import json
from flask import Flask, request, render_template
import plotly
import plotly.graph_objs as go
import webbrowser

app = Flask(__name__ )# , template_folder='yaniv/plotly_web/templates'

@app.route('/')
def index():
    # Render the main page with the form to submit data
    return render_template('index.html')

@app.route('/plot', methods=['POST'])
def plot():
    # Get parameters from the web page
    data = request.data.decode()
    data_json = json.loads(data)
    x_values = data_json["x_values"] #.getlist('x_values', type=float)
    y_values = data_json["y_values"]# .getlist('y_values', type=float)
    # Create a plot using Plotly
    fig = go.Figure() # data=[go.Scatter(x=x_values, y=y_values, mode='lines+markers')])
    fig.add_trace(go.Scatter(
        x=x_values,
        y=y_values,
        name="Name of Trace 1"       # this sets its legend entry
    ))
    y_valuesX2 = [x * 2 for x in y_values]
    fig.add_trace(go.Scatter(
    x=x_values,
    y=y_valuesX2,
    name="Name of Trace 2"
))
    # leyout = go.Layout() # for all Layout options
    fig.update_layout(
    title="Plot Title",
    xaxis_title="X Axis Title",
    yaxis_title="Y Axis Title",
    legend_title="Legend Title",
    font=dict(
        family="Courier New, monospace",
        size=14,
        color="RebeccaPurple"
        ),
    # border size optional
    # width=800,  # specify the width
    height=320,  # specify the height
    margin=dict(l=50, r=50, b=50, t=50, pad=4),
    # paper_bgcolor="LightSteelBlue",
    )
    plot_json = fig.to_json() # json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # Return the plot to the web page
    return plot_json

if __name__ == '__main__':
    # url = "http://127.0.0.1:5000/"
    # optional Open the default web browser to the specified URL
    # webbrowser.open(url)
    app.run(debug=True)
