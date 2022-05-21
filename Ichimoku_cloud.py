#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')


# In[2]:


data = pd.read_csv("Crypto_Trading_Strategies_Intermediate\CTSI_Resources\data_modules\BTCUSD.csv", index_col = 'Date', parse_dates=True)


# In[3]:


data.head()


# ### Conversion line

# In[5]:


high_20 = data.high.rolling(window=20).max()
low_20 = data.low.rolling(window=20).min()
high_60 = data.high.rolling(window=60).max()
low_60 = data.low.rolling(window=60).min()
high_120 = data.high.rolling(window=120).max()
low_120 = data.low.rolling(window=120).min()


# In[6]:


conversion_line = (high_20 +low_20)/2
base_line = (high_60 +low_60)/2
data.close[-500:].plot(figsize = (10,5));
conversion_line[-500:].plot(label  = "Conversion_line");
base_line[-500:].plot(label = 'base_line');
plt.legend()
plt.ylabel("Bitcoin Price")


# In[7]:


data['conversion_line'] = conversion_line
data['base_line'] = base_line


# In[8]:


data['leading_span_A'] = (data['conversion_line']+ data['base_line'])/2


# In[ ]:


pd.options.plotting.backend = "plotly"


# In[9]:


data[["conversion_line","base_line","leading_span_A",'close']][-500:].plot()


# In[10]:


data['leading_span_B'] = (high_120+low_120)/2


# In[11]:


data[["conversion_line","base_line","leading_span_A",'close', 'leading_span_B']][-500:].plot()


# In[12]:


data['lagging_span'] = data.close.shift(-30)
data[["conversion_line","base_line","leading_span_A",'close', 'leading_span_B','lagging_span']][-500:].plot()


# In[26]:


fig, ax = plt.subplots(1, 1, sharex=True, figsize=(10, 10))
ax.fill_between(data.index[-500:],data['leading_span_A'][-500:], data['leading_span_B'][-500:], color = 'black')
data[['leading_span_A','close', 'leading_span_B']][-500:].plot(ax = ax)


# ### Entry Signal

# In[17]:


import numpy as np
data['signal'] = np.nan

# Prices are above the cloud
condition_1 = (data.close > data.leading_span_A) & (data.close > data.leading_span_B)

# leading Span A (senkou_span_A) is rising above the leading span B (senkou_span_B)
condition_2 = (data.leading_span_A > data.leading_span_B)

# Conversion Line (tenkan_sen) moves above Base Line (kijun_sen)
condition_3 = (data.conversion_line > data.base_line)

# Combine the conditions and store in the signal column 1 when all the conditions are true
data.loc[condition_1 & condition_2 & condition_3, 'signal'] = 1


# ### Exit Signal

# In[20]:


# Prices are below the cloud
condition_1 = (data.close < data.leading_span_A) & (data.close < data.leading_span_B)

# leading Span A (senkou_span_A) is falling below the leading span B (senkou_span_B)
condition_2 = (data.leading_span_A < data.leading_span_B)

# Conversion Line (tenkan_sen) moves below Base Line (kijun_sen)
condition_3 = (data.conversion_line < data.base_line)

# Combine the conditions and store in the signal column 0 when all the conditions are true
data.loc[condition_1 & condition_2 & condition_3, 'signal'] = 0
# Signal will remain same till next signal
data.signal.fillna(method='ffill', inplace=True)


# ### Strategy Returns

# In[22]:


# Calculate daily returns
daily_returns = data.close.pct_change()

# Calculate the strategy returns
strategy_returns = daily_returns * data.signal.shift(1)
strategy_returns.dropna(inplace=True)

# Plot the strategy returns
strategy_returns.cumsum().plot(figsize=(10, 5))
plt.xlabel('Date')
plt.ylabel('Strategy Returns (%)')
plt.show()


# In[ ]:




