#!/usr/bin/env python
# coding: utf-8

# In[1]:


# An Ecommerce company based in New York City that sells clothing online but they also have in-store style and-
# clothing advice sessions.

# Customers come in to the store, have sessions/meetings with a personal stylist, then they can go home and-
# order either on a mobile app or website for the clothes they want.

# The company is trying to decide whether to focus their efforts on their mobile app experience or their website. 


# In[ ]:


# I will Analyse their "customer data" and help them in the decision making


# In[2]:


import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[28]:


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics


# In[4]:


# Reading in the Ecommerce Customers csv file as a DataFrame called customers

customers = pd.read_csv('Ecommerce Customers')


# In[5]:


# Getting an Overview of the "customer" data

customers.head()


# In[6]:


customers.info()


# In[7]:


customers.describe()


# In[8]:


customers.columns


# In[9]:


# Using seaborn to create a jointplot to compare the "Time on Website" and "Yearly Amount Spent" columns 

sns.jointplot(data = customers, x = 'Time on Website', y = 'Yearly Amount Spent')


# In[10]:


# Here the distribution is uneven and there is no trend


# In[11]:


# Now comparing "Time on App" and "Yearly Amount Spent"

sns.jointplot(data = customers, x = 'Time on App', y = 'Yearly Amount Spent')


# In[12]:


# Here we can see a slight trend of Increase in "Yearly Amount Spent" as "Time on App" increases
# But this is not enough to help with decision making


# In[13]:


# Using jointplot to create a 2D hex bin plot comparing Time on App and Length of Membership

sns.jointplot(data=customers, x = 'Time on App', y = 'Length of Membership', hue=None, kind='hex')


# In[14]:


customers.columns


# In[15]:


# Creating pairplot to see relationships across the entire data set
# Only Numerical data can be used for plotting, so selecting columns with numerical data

sns.pairplot(customers[['Avg. Session Length', 'Time on App',
       'Time on Website', 'Length of Membership', 'Yearly Amount Spent']])


# In[16]:


# 'length of Membership' and 'Yearly Amount Spent' are showing a relationship/trend as expected


# In[17]:


# Creating a linear model plot using seaborn's lmplot for Yearly Amount Spent vs. Length of Membership. 
# To see if Linear regression model will be a good fit or not

sns.lmplot(data = customers, x = 'Length of Membership', y = 'Yearly Amount Spent')


# In[18]:


# light blue shade shows line of error
# In this case it is not very thick, so Linear Regression model seems to be a good fit


# In[19]:


# Now i will be creating a Linear regression model to predict 'Yearly Amount Spent'

# Creating dataframes of X and y, y is supposed to be 'Yearly Amount Spent' and X is supposed to be rest of the column

X = customers[['Avg. Session Length', 'Time on App',
       'Time on Website', 'Length of Membership']]

y = customers['Yearly Amount Spent']


# In[20]:


# Creating train and test sets which will be used for model building

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)


# In[21]:


# Creating an instance of a LinearRegression() model named lm

lm = LinearRegression()


# In[22]:


# Training/Fitting the model on Training data i.e 'X_train' and 'y_train'

lm.fit(X_train, y_train)


# In[24]:


# Our model as seen "X_train" values
# So we will now use values which our model has not seen(i.e. "X_test") to predict values
# We have the actual values of prices for each values in "X_test"
# We will predict values and compare it to the values which we already have in "y_test"

predictions = lm.predict(X_test)


# In[25]:


# Comparing actual values(y_test) vs Predictions

plt.scatter(y_test, predictions)


# In[26]:


# The distribution of scatter plot is linear, so our model did a good job


# In[29]:


# Calculating the Mean Absolute Error, Mean Squared Error, and the Root Mean Squared Error

MAE = metrics.mean_absolute_error(y_test, predictions)
MSE = metrics.mean_squared_error(y_test, predictions)
RMSE = np.sqrt(MSE)

print(f"MAE:  {MAE}")
print(f"MSE:  {MSE}")
print(f"RMSE:  {RMSE}")


# In[ ]:


# The errors are minimal Compared to the "Yearly Amount Spent" so the model did a good job


# In[30]:


# Plotting a histogram of the residuals and make sure it looks normally distributed.

sns.displot((y_test - predictions))


# In[ ]:


# Residuals in a statistical or machine learning model are-
# the differences between observed and predicted values of data

# Residuals are evenly distributed here, the model was a success


# In[23]:


# Printing the coefficients of the model

cdf = pd.DataFrame(lm.coef_, X.columns, columns=['Coefficients'])
cdf


# In[ ]:


# The coeicients suggests "a unit change in 'Time on App' effects 'Yearly Amount Spent' majorly (i.e. 38.59 units)"
# Whereas "a unit change in 'Time on Website' effects 'Yearly Amount Spent' minorly (i.e. 0.19 units)"


# In[ ]:


# Conclusion "The company should focus their efforts on their mobile app experience"

