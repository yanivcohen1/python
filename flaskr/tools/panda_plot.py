import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from numpy.fft import fft, ifft
import numbers

# tack only columns ['Timestamp (Hour Ending)', 'Demand (MWh)']
df = pd.read_csv('flaskr/tools/numpyPandasPlotly/930-data-export.csv',
        delimiter=',', parse_dates=[0], usecols=['Timestamp (Hour Ending)', 'Demand (MWh)'],
        date_format=lambda x: pd.to_datetime(x.replace("EDT", ""), format='%m/%d/%Y %I %p'))
# Step 2: Localize the datetime column to the correct timezone
df.rename(columns={'Timestamp (Hour Ending)':'hour',
                    'Demand (MWh)':'demand'},
          inplace=True)

# remove NaN
df = df[df['demand'].notna()]

# Step 1: Convert 'hour' column to datetime, removing "EDT"
df['hour'] = pd.to_datetime(df['hour'].str.replace(" EDT", ""), errors='coerce')

# df[["hour"]] = df[["hour"]].apply(pd.to_datetime)
# df[["demand"]] = df[["demand"]].apply(pd.to_numeric)

# filter dates
start_date = '2024-04-06'
end_date = '2024-04-13'
df = df.loc[(df['hour'] >= start_date) & (df['hour'] <= end_date)]

# plot
plt.figure(figsize = (10, 5))
plt.plot(df['hour'], df['demand'])
plt.xlabel('Datetime')
plt.ylabel('California electricity demand (MWh)')
plt.xticks(rotation=25) # tilte the x label in 25 dgree
plt.show()

X = fft(df['demand'])
N = len(X)
n = np.arange(N)
# get the sampling rate
sr = 1 / (60*60)
T = N/sr
freq = n/T

# Get the one-sided specturm
n_oneside = N//2
# get the one side frequency
f_oneside = freq[:n_oneside]

plt.figure(figsize = (10, 5))
plt.plot(f_oneside, np.abs(X[:n_oneside]), 'b')
plt.xlabel('Freq (Hz)')
plt.ylabel('FFT Amplitude |X(freq)|')
plt.show()

# convert frequency to hour
t_h = 1/f_oneside / (60 * 60)

plt.figure(figsize=(10,5))
plt.plot(t_h, np.abs(X[:n_oneside])/n_oneside)
plt.xticks([12, 24, 48, 84, 168])
plt.xlim(0, 200)
plt.xlabel('Period ($hour$)')
plt.show()
