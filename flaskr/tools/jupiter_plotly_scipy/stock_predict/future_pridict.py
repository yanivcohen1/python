# https://www.youtube.com/watch?v=CbTU92pbDKw
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, LSTM
from sklearn.preprocessing import MinMaxScaler
import yfinance as yf

# Load the dataset
# data = pd.read_csv('your_stock_data.csv')
stocks= ['INTC']#['AAPL', 'GOOGL', 'INTC, 'MSFT]
data_yh = yf.download(stocks,  start='2018-01-01', end='2024-09-01')
data = data_yh['Close'].values.reshape(-1, 1)

# Normalize the data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data)

# Prepare the training data
train_size = int(len(scaled_data) * 0.8)
train_data = scaled_data[:train_size]
test_data = scaled_data[train_size:]

def create_dataset(data, time_step=1):
    X, Y = [], []
    for i in range(len(data) - time_step - 1):
        X.append(data[i:(i + time_step), 0])
        Y.append(data[i + time_step, 0])
    return np.array(X), np.array(Y)

time_step = 60
X_train, Y_train = create_dataset(train_data, time_step)
X_test, Y_test = create_dataset(test_data, time_step)

# Reshape input to be [samples, time steps, features]
X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

# Build the LSTM model
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(time_step, 1)))
model.add(LSTM(50, return_sequences=False))
model.add(Dense(25))
model.add(Dense(1))

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(X_train, Y_train, batch_size=1, epochs=1)

# Make predictions
train_predict = model.predict(X_train)
test_predict = model.predict(X_test)

# Inverse transform to get actual prices
train_predict = scaler.inverse_transform(train_predict)
test_predict = scaler.inverse_transform(test_predict)

# Predict future stock prices
future_steps = 30  # Number of days to predict into the future
last_data = scaled_data[-time_step:]
future_predictions = []

for _ in range(future_steps):
    last_data = last_data.reshape(1, time_step, 1)
    next_pred = model.predict(last_data)
    future_predictions.append(next_pred[0, 0])
    last_data = np.append(last_data[:, 1:, :], next_pred).reshape(time_step, 1)

future_predictions = scaler.inverse_transform(np.array(future_predictions).reshape(-1, 1))

# Create future dates
dates = data_yh['Close'].index
last_date = dates[-1]
future_dates = pd.date_range(last_date, periods=future_steps + 1).tolist()[1:]

# Plot the results
plt.figure(figsize=(14, 5))
plt.plot(dates, data, label='Actual Stock Price')
plt.plot(dates[time_step:len(train_predict) + time_step], train_predict, label='Train Predict')
plt.plot(dates[len(train_predict) + (time_step * 2) + 1:len(data) - 1], test_predict, label='Test Predict')
plt.plot(future_dates, future_predictions, label='Future Predictions')
plt.xlabel('Date')
plt.ylabel('Stock Price')
plt.title(stocks[0])
plt.legend()
plt.show()
