"""
Starting the math, looking for correlation in currencies
Basically test and break. Iterative testing too
"""
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
plt.style.use('seaborn-darkgrid')


data = yf.download(['EURUSD=X', 'GBPUSD=X'], start='2020-01-01', end='2021-01-01', group_by='ticker')
data.index = pd.to_datetime(data.index)

# Plot both forex pairs
ax = data['EURUSD=X']['Close'].plot(label='EUR/USD')
ax2 = data['GBPUSD=X']['Close'].plot(secondary_y=True, color='g',  ax=ax, label='GBP/USD')

# Set the title and axis labels
plt.title('EUR/USD and GBP/USD Data')
ax.set_xlabel('Year-Month')
ax.set_ylabel('Close Prices')
ax2.set_ylabel('Close Prices')
ax.tick_params(axis='both')
h1, l1 = ax.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1+h2, l1+l2, loc=2, prop={'size': 15})

# Save the figure

# Show the plot
plt.show()
