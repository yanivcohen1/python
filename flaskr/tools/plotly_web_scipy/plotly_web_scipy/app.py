# https://plotly.com/javascript/
# bebbug run: Python: Flask plotly
# python debugger: debug python file
# in terminal run: python -m flask run

# u(t) = K_{p} * e(t) + K_{i} * integral(e(t)) dt + K_{d} * d(e(t)) / dt
# u(t)	=	PID control variable
# K_{p}	=	proportional gain
# e(t)	=	error value
# K_{i}	=	integral gain
# de(t)	=	change in error value
# dt	=	change in time
# K_{d}	=	Derivative gain

import json
from flask import Flask, request, render_template
import numpy as np
import plotly.graph_objs as go
from scipy.integrate import odeint
from plotly.subplots import make_subplots

app = Flask(__name__ )# , template_folder='yaniv/plotly_web/templates'

@app.route('/')
def index():
    # Render the main page with the form to submit data
    return render_template('index.html')

# Initial conditions
n = 100 # time points to plot
tf = 20.0 # final time
SP_start = 2.0 # time of set point change

fig = make_subplots(rows=2, cols=2) #, subplot_titles=("Plot 1", "Plot 2", "Plot 3", "Plot 4"))
# Update xaxis properties
fig.update_xaxes(title_text="time", showgrid=True, row=2, col=1)
fig.update_xaxes(title_text="time", showgrid=True, row=2, col=2)
# Update title and height
# fig.update_layout(title_text="PID Control System Simulation", height=700)

t = np.linspace(0,tf,n) # create time vector

# plot PID response
# plot 1,1
fig.add_trace(row=1, col=1, trace=go.Scatter(x=t, name="Setpoint (SP)",
            line=dict(color="black",width=2)))
fig.add_trace(row=1, col=1, trace=go.Scatter(x=t, name="Process Variable (PV)",
            line=dict(color="red",width=2,dash="dot")))
# plot 1,2
fig.add_trace(row=1, col=2, trace=go.Scatter(x=t, name=r'Proportional = $K_c \; e(t)$',
            line=dict(color="green",width=2,dash="dashdot",)))
fig.add_trace(row=1, col=2, trace=go.Scatter(x=t, name=r'Integral = $\frac{K_c}{\tau_I} \int_{i=0}^{n_t} e(t) \; dt$',
            line=dict(color="blue",width=2)))
fig.add_trace(row=1, col=2, trace=go.Scatter(x=t, name=r'Derivative = $-K_c \tau_D \frac{d(PV)}{dt}$',
            line=dict(color="red",width=2,dash="dash")))
# plot 2,1
fig.add_trace(row=2, col=1, trace=go.Scatter(x=t, name=r'Error (e=SP-PV)',
            line=dict(color="red",width=2,dash="dash")))
# plot 2,2
fig.add_trace(row=2, col=2, trace=go.Scatter(x=t, name=r'Controller Output (OP)',
            line=dict(color="black",width=2,dash="dash")))

# Convert to FigureWidget
# fig_widget = go.FigureWidget(fig)


# fig_widget.layout = go.Layout() # for all Layout options
fig.update_layout(
    margin=dict(l=50, r=50, b=50, t=50, pad=4),
    height=400
)

def process(y,t,u):
    Kp = 4.0
    taup = 3.0
    thetap = 1.0
    if t<(thetap+SP_start):
        dydt = 0.0  # time delay
    else:
        # u is controler output calculate with PID (the feedbeck)
        # dy/dt = 1/3 *(-y + 4*u)
        dydt = (1.0/taup) * (-y + Kp * u)
    return dydt

def pidPlot(Kc,tauI,tauD):
    # t = np.linspace(0,tf,n) # create time vector
    P= np.zeros(n)          # initialize proportional term
    I = np.zeros(n)         # initialize integral term
    D = np.zeros(n)         # initialize derivative term
    e = np.zeros(n)         # initialize error
    OP = np.zeros(n)        # initialize controller output
    PV = np.zeros(n)        # initialize process variable
    SP = np.zeros(n)        # initialize setpoint
    SP_step = int(SP_start/(tf/(n-1))+1) # setpoint start
    SP[0:SP_step] = 0.0     # define setpoint
    SP[SP_step:n] = 4.0     # step up
    y0 = 0.0                # initial condition
    # loop through all time steps
    for i in range(1,n):
        # simulate process for one time step
        ts = [t[i-1],t[i]]         # time interval
        y = odeint(process,y0,ts,args=(OP[i-1],))  # compute next step with prev step (i-1)
        y0 = y[1]                  # record new initial condition
        # calculate new OP (out) with PID
        PV[i] = y[1]               # record PV
        e[i] = SP[i] - PV[i]       # calculate error = SP - PV
        dt = t[i] - t[i-1]         # calculate time step
        P[i] = Kc * e[i]           # calculate proportional term
        I[i] = I[i-1] + (Kc/tauI) * e[i] * dt  # calculate integral term
        D[i] = -Kc * tauD * (PV[i]-PV[i-1])/dt # calculate derivative term
        OP[i] = P[i] + I[i] + D[i] # calculate new controller output

    fig.data[0].y = SP
    fig.data[1].y = PV
    fig.data[2].y = P
    fig.data[3].y = I
    fig.data[4].y = D
    fig.data[5].y = e
    fig.data[6].y = OP

pidPlot(0.1, 4.0, 0.0)

@app.route('/plot', methods=['POST'])
def plot():
    # Get parameters from the web page
    data = request.data.decode()
    data_json = json.loads(data)
    pk_values = float(data_json["pk"]) #.getlist('x_values', type=float)
    pd_values = float(data_json["pd"])# .getlist('y_values', type=float)
    pi_values = float(data_json["pi"])
    # Create a plot using Plotly
    pidPlot(pk_values, pi_values, pd_values)
    plot_json = fig.to_json() # json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # Return the plot to the web page
    return plot_json

if __name__ == '__main__':
    # URL = "http://127.0.0.1:5000/"
    # Open the default web browser to the specified URL
    # webbrowser.open(url)
    app.run(debug=True)
