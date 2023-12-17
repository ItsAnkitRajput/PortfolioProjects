#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import datetime as dt
import pandas_datareader as pdr
import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt
import cufflinks as cf
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


# Selecting a Time Frame from 1st Jan 2006 to 1st Jan 2016

start_date = dt.datetime(2006,1,1)
end_date = dt.datetime(2016,1,1)


# In[3]:


# Fetch data from Yahoo Finance

# Bank of America
BAC = yf.download("BAC", start_date, end_date)

# CitiGroup
C = yf.download("C", start_date, end_date)

# Goldman Sachs
GS = yf.download("GS", start_date, end_date)

# JPMorgan Chase
JPM = yf.download("JPM", start_date, end_date)

# Morgan Stanley
MS = yf.download("MS", start_date, end_date)

# Wels Fargo
WFC = yf.download("WFC", start_date, end_date)





# In[4]:


#list of the ticker symbols (as strings) in alphabetical order.
tickers = ['BAC', 'C', 'GS', 'JPM', 'MS', 'WFC']


# In[5]:


#concatenated the bank dataframes together to a single data frame called bank_stocks. 
#Setting the keys argument equal to the tickers list.
bank_stock = pd.concat([BAC,C,GS,JPM,MS,WFC], axis=1,keys=tickers)


# In[6]:


#Setting the column name levels
bank_stock.columns.names = ['Bank Ticker','Stock Info']


# In[7]:


#Checking the head of the bank_stock dataframe
bank_stock.head()


# In[8]:


#The max Close price for each bank's stock throughout the time period

#First method
for tick in tickers:
    print(tick, bank_stock[tick]['Close'].max())
    
#Second method using cross section method(.xs)
bank_stock.xs(key='Close',axis=1,level='Stock Info').max()


# In[9]:


#"returns" dataframe is created to store values of 'returns' for each bank stock

returns = pd.DataFrame()

for tick  in tickers:
    returns[tick+' Return'] = bank_stock[tick]['Close'].pct_change()

returns.head()


# In[10]:


#Creating a pairplot to compare behaviours of different stocks

sns.pairplot(returns[1:])
plt.suptitle("Comparing behaviours of different stocks", y=1.02, fontsize = 24)



# In[11]:


# Dates for the best and worst single day returns for each bank

# Dates of Worst returns

returns.idxmin()


# In[12]:


# Dates of Best returns

returns.idxmax()


# In[13]:


# Using standard deviation(std) to see stability of a stock, lowest std = most stable and vice versa
returns.loc['2015-01-01' : '2015-12-31'].std()


# In[14]:


# Creating displot using seaborn of the 2015 returns for Morgan Stanley 
sns.displot(returns.loc['2015-01-01' : '2015-12-31']['MS Return'], color='green', bins=50)
plt.title('2008 Returns for Morgan Stanley')


# In[15]:


# Creating displot using seaborn of the 2008 returns for CitiGroup 
sns.displot(returns.loc['2008-01-01' : '2008-12-31']['C Return'], color='green', bins=50)
plt.title('2008 Returns for CitiGroup')


# In[16]:


# Creating a line plot showing Close price for each bank for the entire index of time
# Using 'xs'(cross section) method

sns.lineplot(bank_stock.xs(key='Close',axis=1,level='Stock Info'))
plt.ylabel('Closing Price')
plt.gcf().set_size_inches(10, 6)
plt.title('Closing price for each bank')


# In[17]:


# Using 'for' loop

for tick in tickers:
    sns.lineplot(bank_stock[tick]['Close'],label = tick)
    plt.ylabel('Close Price')
    plt.gcf().set_size_inches(10, 6)
    
plt.title('Closing price for each bank')



# In[18]:


# Creating an interactive Line plot using Cufflinks module
# Drag-Release to view a portion of the graph, double click to zoom out

cf.set_config_file(offline=True)
cuff_data = bank_stock.xs(key = 'Close', 
                          axis = 1, 
                          level = 'Stock Info').iplot(asFigure=True, 
                                                      mode='lines',
                                                      title='Interactive graph of Closing price for each bank', 
                                                      xTitle = 'Date', 
                                                      yTitle = 'Closing Price')
cuff_data.show()


# In[19]:


# Rolling 30 day average against the Close Price for Bank Of America's stock for the year 2008

plt.figure(figsize=(12,4))
BAC['Close'].loc['2008-01-01': '2009-01-01'].rolling(window=30).mean().plot(label='30 day moving average')
BAC['Close'].loc['2008-01-01': '2009-01-01'].plot(label = "Close Price for Bank Of America's stock")

plt.legend()
plt.title('30 day moving average vs Bank of America Closing Price for the year 2008')
plt.ylabel('Closing Price')


# In[20]:


# Creating a heatmap for the correlations between the stocks Close Price
# Creating a correlation-dataframe first and then calling it into heatmap

corr_df = bank_stock.xs(key = 'Close', axis=1, level = 'Stock Info').corr()
corr_df.head()


# In[21]:


sns.heatmap(corr_df, annot = True)


# In[22]:


# Clustermap to show Correlation between Stocks

sns.clustermap(corr_df, annot = True)


# In[26]:


# Interacive andle plot of Bank of America's stock from Jan 1st 2015 to Jan 1st 2016
# Candle plot is used in financial analysis of stocks to see if a stock is increasing o decreasing on a certain time frame

bac15 = BAC[['Open','High','Low','Close']].loc['2015-01-01':'2016-01-02']
bac15.iplot(kind='candle',
            layout=dict(height=600, width=1000, title="Bank of America's stock from Jan 1st 2015 to Jan 1st 2016",
                        xaxis=dict(title='Date')))


# In[24]:


# Exploring cufflinks ta_plot()

help(MS.ta_plot)


# In[25]:


# Simple Moving Averages plot of Morgan Stanley for the year 2015
# You can click on the contents in the graph legend to enable/disable that line graph

ms_df = MS['Close'].loc['2015-01-01':'2016-01-01']
ms_df.ta_plot(study='sma', periods=[13,21,55], color = ['green', 'blue'], layout=dict(height=600, width=1000))            


# In[27]:


# Creating a Bollinger Band Plot for Bank of America for the year 2015
# Bollinger Bands are a technical analysis tool that is primarily used to- 
# gauge the volatility of a financial instrument, such as a stock, and to identify potential trend reversals or breakouts0

bac_2015 = BAC['Close'].loc['2015-01-01':'2016-01-01']
bac_2015.ta_plot(study='boll')

