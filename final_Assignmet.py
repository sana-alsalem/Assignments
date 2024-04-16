#!/usr/bin/env python
# coding: utf-8

# <p style="text-align:center">
#     <a href="https://skills.network/?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkPY0220ENSkillsNetwork900-2022-01-01" target="_blank">
#     <img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/assets/logos/SN_web_lightmode.png" width="200" alt="Skills Network Logo">
#     </a>
# </p>
# 

# <h1>Extracting and Visualizing Stock Data</h1>
# <h2>Description</h2>
# 

# Extracting essential data from a dataset and displaying it is a necessary part of data science; therefore individuals can make correct decisions based on the data. In this assignment, you will extract some stock data, you will then display this data in a graph.
# 

# <h2>Table of Contents</h2>
# <div class="alert alert-block alert-info" style="margin-top: 20px">
#     <ul>
#         <li>Define a Function that Makes a Graph</li>
#         <li>Question 1: Use yfinance to Extract Stock Data</li>
#         <li>Question 2: Use Webscraping to Extract Tesla Revenue Data</li>
#         <li>Question 3: Use yfinance to Extract Stock Data</li>
#         <li>Question 4: Use Webscraping to Extract GME Revenue Data</li>
#         <li>Question 5: Plot Tesla Stock Graph</li>
#         <li>Question 6: Plot GameStop Stock Graph</li>
#     </ul>
# <p>
#     Estimated Time Needed: <strong>30 min</strong></p>
# </div>
# 
# <hr>
# 

# ***Note***:- If you are working in IBM Cloud Watson Studio, please replace the command for installing nbformat from `!pip install nbformat==4.2.0` to simply `!pip install nbformat`
# 

# In[127]:


get_ipython().system('pip install yfinance')
get_ipython().system('pip install pandas beautifulsoup4')
get_ipython().system('pip install matplotlib')
get_ipython().system('pip install plotly')
get_ipython().system('pip3 install plotly')
get_ipython().system('pip list | grep plotly')
get_ipython().system('pip install pandas==1.3.3')
from io import StringIO
import yfinance as yf
import pandas as pd
import datetime
from urllib.request import Request, urlopen
import requests
import plotly.graph_objs as go
from bs4 import BeautifulSoup
from IPython.display import display
from datetime import datetime
from plotly.subplots import make_subplots
get_ipython().system('pip install pandas')
get_ipython().system('pip install html5lib')
get_ipython().system('pip install lxml')
get_ipython().system('pip install pandas lxml html5lib beautifulsoup4')


# In Python, you can ignore warnings using the warnings module. You can use the filterwarnings function to filter or ignore specific warning messages or categories.
# 

# In[128]:


import warnings
# Ignore all warnings
warnings.filterwarnings("ignore", category=FutureWarning)


# ## Define Graphing Function
# 

# In this section, we define the function `make_graph`. You don't have to know how the function works, you should only care about the inputs. It takes a dataframe with stock data (dataframe must contain Date and Close columns), a dataframe with revenue data (dataframe must contain Date and Revenue columns), and the name of the stock.
# 

# In[153]:


import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing=0.3)
    
    stock_data_specific = stock_data[pd.to_datetime(stock_data['Date']) <= '2021-06-14']
    
    # Handle parsing dates and potential errors
    try:
        revenue_data_specific = revenue_data[pd.to_datetime(revenue_data['Date'], format='%Y-%m-%d', errors='coerce') <= '2021-04-30']
    except ValueError:
        print("Error parsing dates in revenue data. Check date format.")
        return
    
    # Remove dollar signs and commas from Revenue column
    revenue_data_specific['Revenue'] = revenue_data_specific['Revenue'].str.replace('$', '').str.replace(',', '')
    
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific['Date'], infer_datetime_format=True), y=stock_data_specific['Close'].astype(float), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific['Date'], infer_datetime_format=True), y=revenue_data_specific['Revenue'].astype(float), name="Revenue"), row=2, col=1)
    
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    
    fig.update_layout(
        showlegend=False,
        height=900,
        title=stock,
        xaxis_rangeslider_visible=True
    )
    
    fig.show()


# ## Question 1: Use yfinance to Extract Stock Data
# 

# Using the `Ticker` function enter the ticker symbol of the stock we want to extract data on to create a ticker object. The stock is Tesla and its ticker symbol is `TSLA`.
# 

# In[131]:


Tesla = yf.Ticker("TSLA")


# Using the ticker object and the function `history` extract stock information and save it in a dataframe named `tesla_data`. Set the `period` parameter to `max` so we get information for the maximum amount of time.
# 

# In[132]:


tesla_hist = Tesla.history(period="max")
tesla_data = pd.DataFrame(tesla_hist)
print(tesla_data)


# =
# **Reset the index** using the `reset_index(inplace=True)` function on the tesla_data DataFrame and display the first five rows of the `tesla_data` dataframe using the `head` function. Take a screenshot of the results and code from the beginning of Question 1 to the results below.
# 

# In[133]:


stock_data = yf.download("TSLA", start="2020-01-01", end="2021-09-30", progress=False)
revenue_data = yf.download("TSLA", start="2020-01-01", end="2021-09-30", progress=False)
stock_data.reset_index(inplace=True)
tesla_data.reset_index(inplace=True)
print(tesla_data.head())


# ## Question 2: Use Webscraping to Extract Tesla Revenue Data
# 

# Use the `requests` library to download the webpage https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm Save the text of the response as a variable named `html_data`.
# 

# In[134]:


url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm'
html_data = requests.get(url).text
#print(html_data)


# Parse the html data using `beautiful_soup`.
# 

# In[135]:


soup = BeautifulSoup(html_data, 'html.parser')


# Using `BeautifulSoup` or the `read_html` function extract the table with `Tesla Revenue` and store it into a dataframe named `tesla_revenue`. The dataframe should have columns `Date` and `Revenue`.
# 

# <details><summary>Click here if you need help locating the table</summary>
# 
# ```
#     
# Below is the code to isolate the table, you will now need to loop through the rows and columns like in the previous lab
#     
# soup.find_all("tbody")[1]
#     
# If you want to use the read_html function the table is located at index 1
# 
# We are focusing on quarterly revenue in the lab.
# ```
# 
# </details>
# 

# In[136]:


tesla_revenue = pd.DataFrame(columns=['Date', 'Revenue'])
tables = soup.find_all('table')
dates = []
revenues = []

for table in tables:
    thead = table.find('thead')
    if 'Tesla' in thead.text and 'Revenue' in thead.text:
        for row in table.find_all('tr'):
            cells = row.find_all('td')
            if len(cells) >= 2: 
                date = cells[0].text.strip()
                revenue = cells[1].text.strip()
                dates.append(date)
                revenues.append(revenue)

tesla_revenue = pd.DataFrame({'Date': dates, 'Revenue': revenues})
print(tesla_revenue)


# Execute the following line to remove the comma and dollar sign from the `Revenue` column. 
# 

# In[137]:


tesla_revenue["Revenue"] = tesla_revenue["Revenue"].str.replace(r",|\$","")


# Execute the following lines to remove an null or empty strings in the Revenue column.
# 

# In[156]:


tesla_revenue.dropna(inplace=True)

tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]


# Display the last 5 row of the `tesla_revenue` dataframe using the `tail` function. Take a screenshot of the results.
# 

# In[157]:


last_5_rows = tesla_revenue.tail(5)
print(last_5_rows)


# ## Question 3: Use yfinance to Extract Stock Data
# 

# Using the `Ticker` function enter the ticker symbol of the stock we want to extract data on to create a ticker object. The stock is GameStop and its ticker symbol is `GME`.
# 

# In[140]:


GameStop = yf.Ticker("GME")


# Using the ticker object and the function `history` extract stock information and save it in a dataframe named `gme_data`. Set the `period` parameter to `max` so we get information for the maximum amount of time.
# 

# In[141]:


gme_hist = GameStop.history(period="max")
gme_data = pd.DataFrame(gme_hist)
print(gme_data)


# **Reset the index** using the `reset_index(inplace=True)` function on the gme_data DataFrame and display the first five rows of the `gme_data` dataframe using the `head` function. Take a screenshot of the results and code from the beginning of Question 3 to the results below.
# 

# In[142]:


stock_data = yf.download("GME", start="2020-01-01", end="2021-09-30", progress=False)
revenue_data = yf.download("GME", start="2020-01-01", end="2021-09-30", progress=False)
stock_data.reset_index(inplace=True)
gme_data.reset_index(inplace=True)
print(gme_data.head())


# ## Question 4: Use Webscraping to Extract GME Revenue Data
# 

# Use the `requests` library to download the webpage https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html. Save the text of the response as a variable named `html_data`.
# 

# In[143]:


url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html'
html_data = requests.get(url).text
#print(html_data)


# Parse the html data using `beautiful_soup`.
# 

# In[144]:


soup = BeautifulSoup(html_data, 'html.parser')


# Using `BeautifulSoup` or the `read_html` function extract the table with `GameStop Revenue` and store it into a dataframe named `gme_revenue`. The dataframe should have columns `Date` and `Revenue`. Make sure the comma and dollar sign is removed from the `Revenue` column using a method similar to what you did in Question 2.
# 

# <details><summary>Click here if you need help locating the table</summary>
# 
# ```
#     
# Below is the code to isolate the table, you will now need to loop through the rows and columns like in the previous lab
#     
# soup.find_all("tbody")[1]
#     
# If you want to use the read_html function the table is located at index 1
# 
# 
# ```
# 
# </details>
# 

# In[145]:


gme_revenue = pd.DataFrame(columns=['Date', 'Revenue'])
tables = soup.find_all('table')
dates = []
revenues = []

for table in tables:
    thead = table.find('thead')
    if 'GameStop' in thead.text and 'Revenue' in thead.text:
        for row in table.find_all('tr'):
            cells = row.find_all('td')
            if len(cells) >= 2:  
                date = cells[0].text.strip()
                revenue = cells[1].text.strip()
                dates.append(date)
                revenues.append(revenue)

gme_revenue = pd.DataFrame({'Date': dates, 'Revenue': revenues})
print(gme_revenue)


# Display the last five rows of the `gme_revenue` dataframe using the `tail` function. Take a screenshot of the results.
# 

# In[146]:


last_5_rows = gme_revenue.tail(5)
print(last_5_rows)


# ## Question 5: Plot Tesla Stock Graph
# 

# Use the `make_graph` function to graph the Tesla Stock Data, also provide a title for the graph. The structure to call the `make_graph` function is `make_graph(tesla_data, tesla_revenue, 'Tesla')`. Note the graph will only show data upto June 2021.
# 

# In[154]:


make_graph(tesla_data, tesla_revenue, 'Tesla')


# ## Question 6: Plot GameStop Stock Graph
# 

# Use the `make_graph` function to graph the GameStop Stock Data, also provide a title for the graph. The structure to call the `make_graph` function is `make_graph(gme_data, gme_revenue, 'GameStop')`. Note the graph will only show data upto June 2021.
# 

# In[158]:


make_graph(gme_data, gme_revenue, 'GameStop')


# <h2>About the Authors:</h2> 
# 
# <a href="https://www.linkedin.com/in/joseph-s-50398b136/">Joseph Santarcangelo</a> has a PhD in Electrical Engineering, his research focused on using machine learning, signal processing, and computer vision to determine how videos impact human cognition. Joseph has been working for IBM since he completed his PhD.
# 
# Azim Hirjani
# 

# ## Change Log
# 
# | Date (YYYY-MM-DD) | Version | Changed By    | Change Description        |
# | ----------------- | ------- | ------------- | ------------------------- |
# | 2022-02-28        | 1.2     | Lakshmi Holla | Changed the URL of GameStop |
# | 2020-11-10        | 1.1     | Malika Singla | Deleted the Optional part |
# | 2020-08-27        | 1.0     | Malika Singla | Added lab to GitLab       |
# 
# <hr>
# 
# ## <h3 align="center"> © IBM Corporation 2020. All rights reserved. <h3/>
# 
# <p>
# 
