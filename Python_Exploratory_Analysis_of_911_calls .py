#!/usr/bin/env python
# coding: utf-8

# In[1]:


# For this project I will be analyzing some 911 call data from Kaggle


# In[2]:


# Importing Reqired libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[32]:


# Reading Data into python dataframe

df = pd.read_csv('911.csv')
df.head()


# In[33]:


# Column names

df.columns


# In[4]:


# top 5 zipcodes for 911 calls

df['zip'].value_counts().head(5)


# In[5]:


# top 5 townships (twp) for 911 calls

df['twp'].value_counts().head(5)


# In[6]:


# Taking a look at the 'title' column, to see how many unique title codes are there

df['title'].nunique()


# In[7]:


# In the titles column there are "Reasons/Departments" specified before the title code. These are EMS, Fire, and Traffic.
# We will create a new column called "Reason" that contains this string value.

df['reason'] = df['title'].apply(lambda title: title.split(':')[0])
df['reason'].head()


# In[8]:


#  most common Reason for a 911 call

df['reason'].value_counts()


# In[9]:


# Using seaborn to create a countplot of 911 calls by Reason

sns.countplot(x='reason',data=df,palette='viridis')


# In[10]:


# Checking the data type of the objects in the timeStamp column

type(df['timeStamp'].iloc[0])


# In[11]:


# These timestamps are still "strings". We will use "pd.to_datetime" to convert the column from "strings" to "DateTime" objects.

df['timeStamp'] = pd.to_datetime(df['timeStamp'])


# In[12]:


# Using ".apply()" to create 3 new columns called hour, month, and dayofweek
# We will create these columns based off of the timeStamp column

df['hour'] = df['timeStamp'].apply(lambda time: time.hour)
df['month'] = df['timeStamp'].apply(lambda time: time.month)
df['dayofweek'] = df['timeStamp'].apply(lambda time: time.dayofweek)

df[['hour','month','dayofweek']].head()


# In[13]:


# Day of Week is an integer 0-6.
# We will use the ".map()" method to map the actual string names to the day of the week i.e. 0 = Mon, 1 = Tue and so on

dmap = {0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'}
df['dayofweek'] = df['dayofweek'].map(dmap)

df[['hour','month','dayofweek']].head()


# In[14]:


# Creating a new dataframe with count of occurrences of each reason per month
count_df = df.groupby(['month', 'reason']).size().reset_index(name='count')
count_df

# Plot the line plot with count of occurrences of each reason per month
sns.lineplot(x='month', y='count', hue='reason', data=count_df)


# In[15]:


# Using seaborn to create a countplot of the Day of Week column with the hue based off of the Reason column
sns.countplot(x='dayofweek',data=df,hue='reason',palette='viridis')

# To relocate the legend
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)


# In[16]:


# Now do the same for Month:
sns.countplot(x='month',data=df,hue='reason',palette='viridis')

# To relocate the legend
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)


# In[17]:


# The data we fetched is missing some months, 9,10, and 11 are not there.
# We can maybe fill in this information by plotting the information in another way-
# possibly a simple line plot that fills in the missing months
# We will create a new dataframe off of original dataframe

byMonth = df.groupby('month').count()
byMonth.head()


# In[18]:


# Creating a simple plot off of the dataframe indicating the count of calls per month. 
# We can use any column to plot 

byMonth['lat'].plot() 


# In[19]:


# Using seaborn's lmplot() to create a linear fit on the number of calls per month

sns.lmplot(x='month', y='twp', data=byMonth.reset_index())


# In[20]:


# Creating a new column called 'Date' that contains the date from the timeStamp column.

df['date'] = df['timeStamp'].apply(lambda t:t.date())


# In[21]:


# Now perforing groupby on "Date" column with the count() aggregate to create a plot of counts of 911 calls.

df.groupby('date').count()['lat'].plot()
plt.tight_layout()
plt.xticks(rotation=45, ha='right')
plt.title('Counts of 911 calls')


# In[22]:


# Creating 3 separate plots with each plot representing a Reason for the 911 call

df[df['reason']=='Traffic'].groupby('date').count()['lat'].plot()
plt.title('Traffic')
plt.tight_layout()
plt.xticks(rotation=45, ha='right')


# In[23]:


df[df['reason']=='Fire'].groupby('date').count()['lat'].plot()
plt.title('Fire')
plt.tight_layout()
plt.xticks(rotation=45, ha='right')


# In[24]:


df[df['reason']=='EMS'].groupby('date').count()['lat'].plot()
plt.title('EMS')
plt.tight_layout()
plt.xticks(rotation=45, ha='right')


# In[25]:


# Restructuring the dataframe so that the columns become the Hours and the Index becomes the Day of the Week
# To create heatmaps with seaborn and our data

day_hour = df.groupby(by=['dayofweek','hour']).count()['reason'].unstack()
day_hour.head()


# In[26]:


# HeatMap using this new DataFrame

sns.heatmap(day_hour, cmap='viridis')


# In[27]:


# Clustermap using this DataFrame

sns.clustermap(day_hour,cmap='viridis', figsize=(7,5))


# In[28]:


# Repeating these same plots and operations for a DataFrame that shows the Month as the column.

day_month = df.groupby(by=['dayofweek','month']).count()['reason'].unstack()
day_month.head()


# In[29]:


# Heatmap

sns.heatmap(day_month, cmap='viridis')


# In[30]:


# ClusterMap

sns.clustermap(day_hour, cmap='coolwarm', figsize=(7,5))


# In[ ]:




