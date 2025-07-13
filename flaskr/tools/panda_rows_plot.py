import pandas as pd
import matplotlib.pyplot as plt

# Sample DataFrame
data = {
    'Column1': [1, 2, 3, 4],
    'Column2': [10, 20, 30, 40],
    'Column3': [100, 200, 300, 400]
}
row_names = ['Row1', 'Row2', 'Row3', 'Row4']
df = pd.DataFrame(data, index=row_names) # columns=headers

# Select specific rows and columns
selected_data = df.loc[['Row1', 'Row3'], ['Column1', 'Column2']]

# Display the DataFrame
print(df)
print('Column2 is',df['Column2'][0:2].values)
element = df.loc['Row2', 'Column2']
print('row2 column2 is:', element)

print('selected df:\n', selected_data)
# Plot the selected data
selected_data.plot(kind='bar')

# Customize the plot
plt.title("Selected Rows and Columns")
plt.xlabel("Rows")
plt.ylabel("Values")
plt.legend(title="Columns")
plt.show()
