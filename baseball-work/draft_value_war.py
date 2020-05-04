#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 17:03:08 2017

@author: dtsal
"""


from bs4 import BeautifulSoup
from urllib.request import urlopen

import pandas as pd


def ingest_year(year, rnd, df):
    
    
    soup = BeautifulSoup(
            urlopen(
                base_url+draft_url+str(year)+round_url+str(rnd)
                ), 'html.parser')
    
    table = soup.find('table')
    table_body = table.find_all('tbody')[0]
    
    rows = table_body.find_all('tr')
    for row in rows:
    
        
        rnd = (row.find("td", {"data-stat":"draft_round"})).getText()
        OvPck = (row.find("td", {"data-stat":"overall_pick"})).getText()
        RdPck = (row.find("td", {"data-stat":"round_pick"})).getText()
        Tm = (row.find("td", {"data-stat":"team_ID"})).getText()
        
        Name = (row.find("td", {"data-stat":"player"})).getText()
        Name = Name.replace('*', '')
        NameOnly, sep, tail = Name.partition('\xa0')
        
        Pos = (row.find("td", {"data-stat":"pos"})).getText()
        WAR = (row.find("td", {"data-stat":"WAR"})).getText()
        
        if WAR  == "":
            WAR = 0
            
        Type = (row.find("td", {"data-stat":"from_type"})).getText()
        
        vals = {
                columns[0]:year,
                columns[1]:rnd,
                columns[2]:OvPck,
                columns[3]:RdPck,
                columns[4]:Tm,
                columns[5]:NameOnly,
                columns[6]:Pos,
                columns[7]:WAR,
                columns[8]:Type
                }
        df2 = pd.DataFrame(vals, index=[0])
        df = pd.concat([df, df2], ignore_index=True)
    return df
        
def ingest_all(minyear, rnds, df):
    for year in range(minyear, 2001):
        for rnd in range(rnds):
            print('ingesting year', year, 'and round', rnd+1)
            df = ingest_year(year, rnd+1, df)
    return df

        
if __name__ == '__main__':
    columns = ['Year','Rnd','OvPck','RdPck','Tm','Name','Pos','WAR','Type']
    big_table = pd.DataFrame(columns=columns)

    base_url = "http://www.baseball-reference.com/"
    draft_url = 'draft/?query_type=year_round&year_ID='
    round_url = '&draft_round='

    new_big_table = ingest_all(1998, 2, big_table)
    print(new_big_table)
    