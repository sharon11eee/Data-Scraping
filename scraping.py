#!/usr/bin/env python
# coding: utf-8

# In[13]:


import sys
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import re
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import gmaps
from ipywidgets.embed import embed_minimal_html


# In[16]:


def default_function():
    
    print('Default mode--\n\n')
    print('---Data scraping---\n')
    #Dataset1
    url='https://data.lacity.org/resource/rwq7-yhp5.json'
    r=requests.get(url)
    park=r.json()
    
    df_park=pd.DataFrame(park)
    df_park.to_csv('park.csv',index=False)
    pd.set_option('display.max_columns',None)
    print('Dataset 1: Recreation and Parks Information\n',df_park,'\n')
    
    acre=df_park['area_acres']

    park_zipcode=[]
    zipcode_acre_lst=[]
    for i in range(0,len(df_park['address'])):
        re_zipcode='\s([9][0-9]+[0-9])'
        zipcode=re.findall(re_zipcode,df_park['address'][i])
        if re.search(re_zipcode,df_park['address'][i])==None:
            continue
        else:
            park_zipcode.append(zipcode[0])
            zipcode_acre_lst.append((zipcode[0],acre[i]))
    
    counts={}
    for i in park_zipcode:
        counts[i]=counts.get(i,0)+1

    zipcode_lst=[]
    for k in counts.keys():
        zipcode_lst.append(k)
    
    zip_acre={}
    for i in range(0,len(zipcode_lst)):
        lst=[]
        for k,v in zipcode_acre_lst:
            if k==zipcode_lst[i]: 
                lst.append(float(v))
        zip_acre[zipcode_lst[i]]=sum(lst)
    

    #Dataset2
    url=requests.get('https://www.california-demographics.com/zip_codes_by_population')
    soup=BeautifulSoup(url.content, 'html.parser')
    info=soup.find_all('td')

    rank_lst=[]
    zip_lst=[]
    pop_lst=[]
    for i in range(0,len(info)-1):

        if i%3==0:
            rank_lst.append(info[i].text.strip(' \nTIE'))
        if i%3==1:
            zip_lst.append(info[i].text.strip('\n'))
        if i%3==2:
            pop_lst.append(info[i].text.strip())
    
    df_population=pd.DataFrame({'Rank':rank_lst,'Zipcode':zip_lst,'Population':pop_lst})
    df_population.to_csv('pop.csv',index=False)
    
    print('Dataset 2: California Zip Codes by Population\n',df_population,'\n')
    
    ave_dic={}
    for k,v in zip_acre.items():
        for i in range(0,len(df_population)):
            if df_population['Zipcode'][i]==k:
                ave=v*43560/int(df_population['Population'][i].replace(',',''))
        ave_dic[k]=ave      
    
    df_ave=pd.DataFrame([ave_dic]).T
    df_ave.reset_index(inplace=True)
    df_ave=df_ave.rename(columns={'index':'Zipcode',0:'Park space per person(sq ft)'})
    
    print('Waiting for dataset to load...\n') 
    #Dataset3

    header={'User-Agent': 'Mozilla/5.0'}
    
    url_lst=[]
    zip_redfin=[]
    for k in ave_dic.keys():
        zipcode=k
        url='https://www.redfin.com/zipcode/'+zipcode
        url_lst.append(url)
        zip_redfin.append(k)
    
    median_lst=[]
    zip_redfin_lst=[]
    for i in range(0,len(url_lst)):
        r=requests.get(url_lst[i],headers=header)
        soup=BeautifulSoup(r.content, 'html.parser')

        pattern=re.compile(r'"res".*?"metrics.*?"value.*?\$(.*?)\\",', re.MULTILINE | re.DOTALL)
        script = soup.find("script", text=pattern)

        try:
            median = pattern.search(script.text).group(1)

            if 'K' in median:
                median=median.replace('K','000')
                zip_redfin_lst.append(zipcode_lst[i])
                median_lst.append(median)
            else:
                median=int(median.replace(',',''))
                zip_redfin_lst.append(zipcode_lst[i])
                median_lst.append(median)
        except:
            print('Waiting for dataset to load...\n') 
            continue
            
        
    df_price=pd.DataFrame({'Zipcode':zip_redfin_lst,'Median Price':median_lst})

    df_price.to_csv('price.csv',index=False)
    
    print('Dataset 3: House Median Price on Redfin\n',df_price,'\n')
    
    #Final Dataset
    
    #average park space
    final_ave=[]
    for i in range(0,len(zipcode_lst)):
        if zipcode_lst[i] in zip_redfin_lst:
            final_ave.append(df_ave.iloc[i,1])       
    
    #acre of parks        
    sum_acre=[]
    for k,v in zip_acre.items():
        for i in range(0,len(zip_acre)):
            if list(zip_acre.keys())[i]==k:
                acre=list(zip_acre.values())[i]
        sum_acre.append(acre)      
    acre_final_lst=[]
    for i in range(0,len(zipcode_lst)):
        if zipcode_lst[i] in zip_redfin_lst:
            acre_final_lst.append(sum_acre[i])
            
    df_final=df_price
    df_final['Park space per person(sq ft)']=final_ave
    
    df_final['Acre of Parks']=acre_final_lst
    print('Final Dataset:\n',df_final)

    df_final.to_csv('final_dataset.csv',index=False)
    
    
    #Analysis
    print('---Analysis---\n')
    
    
    #Scatter Plots
    print('[Scatter Plots]')
    print('Creating Scatter Plots...\n')
    
    ##Drop outliers
    df_final_afterdrop=pd.DataFrame()
    df_final_afterdrop=df_final
    for i in range(0,len(df_final)):
        if df_final['Acre of Parks'][i]>750:
            df_final_afterdrop=df_final_afterdrop.drop(i)
    
    df_final_afterdrop=df_final_afterdrop.astype(float)
    
    #plot1
    X=df_final_afterdrop['Park space per person(sq ft)'].values.reshape(-1, 1)  
    y=df_final_afterdrop['Median Price'].values.reshape(-1, 1)

    linear_regressor = LinearRegression()
    linear_regressor.fit(X, y)
    y_pred=linear_regressor.predict(X)

    plt.scatter(X, y)
    plt.plot(X, y_pred, color='red')
    plt.title(label='Scatter Plot- Price / Park space per person')
    plt.xlabel('Park space per person(sq ft)')
    plt.ylabel('Median Price (million)')
    plt.savefig('plt1.png')
    plt.show()
    
    #plot2
    X=df_final_afterdrop['Acre of Parks'].values.reshape(-1, 1)  
    y=df_final_afterdrop['Median Price'].values.reshape(-1, 1)

    linear_regressor = LinearRegression()
    linear_regressor.fit(X, y)
    y_pred=linear_regressor.predict(X)

    plt.scatter(X, y)
    plt.plot(X, y_pred, color='red')
    plt.title(label='Scatter Plot- Price / Acre of Parks')
    plt.xlabel('Acre of Parks')
    plt.ylabel('Median Price (million)')
    plt.savefig('plt2.png')
    plt.show()
    
    print('2 scatter plots are saved!\n')

    
    #Google Maps
    print('[Heatmap on Google Maps API]')
    
    API_KEY='*********'
    
    zipcode_map_lst=[]
    lat_lst=[]
    lon_lst=[]
    for i in df_final['Zipcode']:
        address=str(int(i))
        url='https://maps.googleapis.com/maps/api/geocode/json?address='+address+'&key='+API_KEY
        r=requests.get(url)
        results = r.json()['results']
        try:
            location = results[0]['geometry']['location']
            #print(address,location)
            lat=location['lat']
            lon=location['lng']

            zipcode_map_lst.append(address)
            lat_lst.append(lat)
            lon_lst.append(lon)

        except:
            continue

    df_cor=pd.DataFrame()
    df_cor['Zipcode']=zipcode_map_lst
    df_cor['Latitude']=lat_lst
    df_cor['Longitude']=lon_lst

    price_map_lst=[]
    for i in range(0,len(df_final)):
        if str(int(df_final['Zipcode'].values[i])) in zipcode_map_lst:
            price_map_lst.append(int(df_final['Median Price'].values[i])/200**2)

    df_cor['Weights']=price_map_lst
    
    print('Creating a map...\n')
    
    address='The Getty'
    url='https://maps.googleapis.com/maps/api/geocode/json?address='+address+'&key='+API_KEY
    r=requests.get(url)
    results = r.json()['results']
    location = results[0]['geometry']['location']

    lat=location['lat']
    lon=location['lng']

    coordinates=(lat,lon)

    gmaps.configure(api_key=API_KEY)
    figure_layout={'width':'100%','height':'75vh'}

    locations=df_cor[['Latitude', 'Longitude']]
    weights=df_cor['Weights']
    fig=gmaps.figure(center=coordinates, zoom_level=11, map_type='HYBRID', layout=figure_layout)
    fig.add_layer(gmaps.heatmap_layer(locations, weights=weights, point_radius=23, max_intensity=40))
    embed_minimal_html('export.html', views=[fig],title='google map export')
    print('The "export.html" file is created! Please double click on the file to see the map.')
    
    
def scrape_function():
    park_data=pd.read_csv('park.csv')
    pop_data=pd.read_csv('pop.csv')
    price_data=pd.read_csv('price.csv')
    final_data=pd.read_csv('final_dataset.csv')                
    
    print('Scrape mode-- \n')
    print('Dataset 1: Recreation and Parks Information (park.csv)\n',park_data.head(),'\n')
    print('Dataset 2: California Zip Codes by Population (pop.csv)\n',pop_data.head(),'\n')
    print('Dataset 3: House Median Price on Redfin (price.csv)\n',price_data.head(),'\n')
    print('Final Dataset\n',final_data.head(),'\n')

def static_function(path_to_static_data):
    static_data=pd.read_csv(path_to_static_data)
    
    print('Static mode-- \n')
    print('Final Dataset:\n',static_data)



if __name__=='__main__': 
    
    if len(sys.argv)==1: 
        default_function()

    elif sys.argv[1]=='--scrape': 
        scrape_function()

    elif sys.argv[1]=='--static': 
        path_to_static_data=sys.argv[2]
        static_function(path_to_static_data)

