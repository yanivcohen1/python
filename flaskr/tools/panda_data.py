import pandas as pd
import yfinance as yf

# --------- print utc ---------------------------------------------------------------------
print(pd.to_datetime(['2018-10-26 12:00 -0530', '2018-10-26 12:00 -0500'],
                utc=True)[0]) # print in utc: 2018-10-26 17:30:00+00:00

# ------------ panda from csv ---------------------------------------------------------------------
csv_file_path = r"D:\pyProj\adi\third_year\proj3\clients_data.csv"
df = pd.read_csv(csv_file_path)
all_ids = df['ID'].astype(str).values
print("heads:",df.columns.tolist())
# print: heads: ['ID', 'Name', 'Phone number', 'Birth year', 'Is Employee']

# ------------ panda from dict ---------------------------------------------------------------------
dict1 = {
  "Date": ["2018-10-26", "2018-10-26", "2018-10-27", "2018-10-28", "2018-10-29", "2018-10-29"],
  "Sales": [1000, 1200, 1500, 1800, 2000, 2200],
  "Profit": [200, 300, 400, 500, 600, 700],
  'time': [1, 2, 3],
}
table = pd.DataFrame(dict1, columns=['Date', 'Sales', "Profit"])# option to fillter
table[["Date"]] = table[["Date"]].apply(pd.to_datetime)

# Panda print from colums ['Date', 'Profit'] 3 first rows
print(table[['Date', 'Profit']].head(3))
#         Date  Profit
# 0 2018-10-26     200
# 1 2018-10-26     300
# 2 2018-10-27     400

# ------------ panda fron csv ---------------------------------------------------------------------
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
end_date = '2024-04-12'
df2 = df.loc[(df['hour'] >= start_date) & (df['hour'] <= end_date)]
print(df2.head(3))

# ------------ panda from html ---------------------------------------------------------------------
url = "https://www.fdic.gov/resources/resolutions/bank-failures/failed-bank-list"
df = pd.read_html(url)[0]
print(df.iloc[0:3])
print("number of rows:" , df.shape[0])
print("number of columns:" , df.shape[1])
#                               Bank Name          City         State   Cert                Aquiring Institution      Closing Date  Fund  Sort ascending
# 0                   Pulaski Savings Bank       Chicago      Illinois  28611                     Millennium Bank  January 17, 2025                 10548
# 1     The First National Bank of Lindsay       Lindsay      Oklahoma   4134  First Bank & Trust Co., Duncan, OK  October 18, 2024                 10547
# 2  Republic First Bank dba Republic Bank  Philadelphia  Pennsylvania  27332   Fulton Bank, National Association    April 26, 2024                 10546
# number of rows: 10
# number of columns: 7


# ----- yahoo data with index ---------------------------------------------------------------------
start='2019-01-01'
end='2019-12-31'
stocks= ['AAPL', 'GOOGL']
df = yf.download(stocks,  start=start, end=end)
print(f"yahoo values of stacks: {stocks}:\n", df.head(3))
# yahoo values of stacks: ['AAPL', 'GOOGL']:
#  Price           Close                  High                   Low                  Open                Volume
# Ticker           AAPL      GOOGL       AAPL      GOOGL       AAPL      GOOGL       AAPL      GOOGL       AAPL     GOOGL
# Date
# 2019-01-02  37.667175  52.543530  37.889001  52.847926  36.787034  51.078838  36.944458  51.174492  148158800  31868000
# 2019-01-03  33.915253  51.088299  34.757230  53.120433  33.869933  50.933860  34.342203  52.343750  365248800  41960000
# 2019-01-04  35.363079  53.708801  35.432252  53.804953  34.299279  51.655743  34.473398  51.939713  234428400  46022000

# Select only the 'Close' columns for AAPL and GOOGL
# close_data = df.loc[:, [('Close', 'AAPL'), ('Close', 'GOOGL'), ('Volume', 'AAPL'), ('Volume', 'GOOGL')]]
# Automatically combine MultiIndex columns into single-level column names
df2 = df[['Close', 'Volume']]
# rename the columes
df2.columns = [f'{ticker} {metric}' for metric, ticker in df2.columns]
# Reset index to include 'Date' as a column insted of index
data = df2.reset_index() # optional
print(data.head(3))
#         Date  AAPL Close  GOOGL Close  AAPL Volume  GOOGL Volume
# 0 2019-01-02   37.667179    52.543530    148158800      31868000
# 1 2019-01-03   33.915245    51.088299    365248800      41960000
# 2 2019-01-04   35.363075    53.708801    234428400      46022000

dates = df.index
filter_by_index = df.loc['2019-01-01':'2019-02-01']
filter_by_index2 = filter_by_index.loc[filter_by_index.index > '2019-01-01']
print(filter_by_index2.head(3))


# add head to table ---------------------------------------------------------------------
# Create a DataFrame without headers
data = [
    [1, 4, 7],
    [2, 5, 8],
    [3, 6, 9]
]
df = pd.DataFrame(data)
# Add headers
df.columns = ['Column1', 'Column2', 'Column3']
print(df)
#    Column1  Column2  Column3
# 0        1        4        7
# 1        2        5        8
# 2        3        6        9
