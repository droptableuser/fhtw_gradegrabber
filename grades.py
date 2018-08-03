#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import getpass
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth
import requests
import pandas as pd

sem="SS2018"
URL="https://cis.technikum-wien.at/cis/private/lehre/notenliste.php?stsem="+sem

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
    
class HTMLTableParser:
      
  def parse_url(self, url, user, password):
    response = requests.get(url,auth=HTTPBasicAuth(user,password))
    soup = BeautifulSoup(response.text, 'lxml')
    return [(table,self.parse_html_table(table))\
      for table in soup.find_all('table')[0:1]]  
    
  def parse_html_table(self, table):
    n_columns = 0
    n_rows=0
    column_names = []
    # Find number of rows and columns
    # we also find the column titles if we can
    
    for row in table.find_all('tr'):
        td_tags = row.find_all('td')
        if len(td_tags) > 0:
          n_rows+=1
          if n_columns == 0:
            # Set the number of columns for our table
            n_columns = len(td_tags)             
        # Handle column names if we find them
        th_tags = row.find_all('th') 
        if len(th_tags) > 0 and len(column_names) == 0:
          for th in th_tags:
            column_names.append(th.get_text())
                    # Safeguard on Column Titles
    if len(column_names) > 0 and len(column_names) != n_columns:
      raise Exception("Column titles do not match the number of columns")
    
    columns = column_names if len(column_names) > 0 else range(0,n_columns)
       
    df = pd.DataFrame(columns = columns,index=range(0,n_rows))
    row_marker = 0
    for row in table.find_all('tr'):
      column_marker = 0
      columns = row.find_all('td')

      for column in columns:
        df.iat[row_marker,column_marker] = column.get_text()
        column_marker += 1
      if len(columns) > 0:
        row_marker += 1

    return df

if __name__ == "__main__":
  user=input("username: ")
  password=getpass.getpass(prompt="password: ")
  hp = HTMLTableParser()
  table = hp.parse_url(URL,user,password)[0][1]
  print(table)

