# Importing essential modules
import pymysql
from pandas.core.frame import DataFrame
import requests
import pandas as pd
from requests.api import get
from sqlalchemy.dialects.mysql import LONGTEXT

import os
import schedule
import time
import asyncio

# Importing the connection string from connection.py
from connection import engine

# Defining request parameters.
headers = {
'accept':'application/json',
'authorization':'Bearer *Your-bearer-code if the authentication is Bearer*'
}
baseurl = 'https://*your base url*'
endpoint  = 'your endpoint' 

# Wrap the code with an async function to make it asynchronous.
async def get_invoices():
	print("Going through the invoices")
def main_request(baseurl,endpoint,x,headers):
    # Using request's get method to pull data using defined parameters.
    # Using f string to iterate pages when the function is called.
	r = requests.get(baseurl + endpoint + f'?page={x}',headers=headers)
        return r.json()

def get_pages(response):
	return response['meta']['total_pages']

def parse_json(response):
	charlist =[]
	for item in response['invoices']:
	    charlist.append(item)
        return charlist

# Calling the main function with pre-defined parameters.
data = main_request(baseurl=baseurl,endpoint=endpoint,x=1,headers=headers)

main_invoices = []
# Iterating/paginating through API data. 
# Your API provider might be using a different
# Method for paginating.
for x in range(1,get_pages(data)+1):
	print(x)
	main_invoices.extend(parse_json(main_request(baseurl,endpoint,x,headers)))
	df_invoices = pd.DataFrame(main_invoices)
	
	# Write new data to sql database.
	# Note: Ensure the database's table name matches the table name provided here.
	df_invoices.to_sql('invoices',con=engine,if_exists='replace',index=False)
	
# This function awaits the get_invoices function,
# runs the get_invoices() function when called,
# and will be called by an external file to envoke your API call.
async def call_invoices():
	await get_invoices()