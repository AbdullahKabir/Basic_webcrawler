#!/usr/bin/env python
# coding: utf-8

# In[261]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import json
import statistics as st#


# In[265]:


def mean(data):
    total = sum(data)
    number = len(data)
    return total/number
    
    
def splitter(base,connect,i=[0]):
    internal_links = []
    inside = []
    external_links = []
    internal_wiki = []
    dateOfModification = []
    source_code= requests.get(base+connect)
    i[0]+=1
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text,"html.parser")
    for links in soup.findAll("a"):
        href = str(links.get("href"))
        internal_links.append(href)
    for check in range(len(internal_links)):
        if not internal_links[check].find("#"):
            inside.append(internal_links[check])
        elif not internal_links[check].find("htt"):
            external_links.append(internal_links[check])
        elif not internal_links[check].find("/wiki") :
            internal_wiki.append(internal_links[check])
    for modifying in soup.findAll("script",{"type":"application/ld+json"}):
        json_object = json.loads(modifying.contents[0])
        string = json_object['dateModified']
        dateOfModification.append(string)
    return internal_wiki,inside,external_links,dateOfModification,i[0]

def build_dataframe():
    url = splitter("https://simple.wikipedia.org","/wiki/Climate_change")
    iterateURL = url [0]
    insideNumber = []
    insidePage = []
    externalLink= []
    dateOfModification = []
    pagenumber = []
    for k in range(len(iterateURL)):
        print("Base URL" +iterateURL[k])
        a = splitter("https://simple.wikipedia.org",iterateURL[k])
        second = a[0]
        for i in range(len(second)):
            print("Base URL" +second[i])
            again = splitter("https://simple.wikipedia.org",second[i])
            if again[4]<200:
                insideNumber.append(len(again[0]))
                insidePage.append(len(again[1]))
                externalLink.append(len(again[2]))
                dateOfModification.append(str(again[3]))
                pagenumber.append(again[4])
            else:
                break
    
    data = {'PageCount': pagenumber, 'INTcount': insideNumber, 'URLfragment': insidePage, 'EXTcount' : externalLink,'timestamp': dateOfModification}  
    df = pd.DataFrame(data)
    df['timestamp'].astype('string')
    df.loc[df['timestamp'] == "",'timestamp'] = 'None'
    return df
def manual_time_plot(data):
    manual_histo = []
    manual_histo2 = []
    for a in data["timestamp"]:
        if a != "[]":
            ab=a.split("T")
            manual_histo.append(ab[1])
    for b in manual_histo:
        bd = b.split(":")
        manual_histo2.append(bd[0])
    my_dict = {i:manual_histo2.count(i) for i in manual_histo2}
    Times = list(my_dict.keys())
    values = list(my_dict.values())
    histogram = pd.DataFrame(values,Times)
    histogram.plot(kind='bar')
    
    
data = build_dataframe()

print("Median of INTcount: "+str(st.median(data['INTcount'])))
print("Median of EXTcount: "+str(st.median(data['EXTcount'])))
print("Median of URLfragment: "+str(st.median(data['URLfragment'])))
print("Mean of INTcount: "+str(mean(data['INTcount'])))
print("Mean of EXTcount: "+str(mean(data['EXTcount'])))
print("Mean of URLfragment: "+str(mean(data['URLfragment'])))


manual_time_plot(data)

data.groupby('PageCount').plot(kind='bar')

    


# In[ ]:




