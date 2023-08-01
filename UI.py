#!/usr/bin/env python
# coding: utf-8

# In[25]:


import pandas as pd
import tkinter as tk
from tkinter import simpledialog,messagebox
import sys


# In[26]:


def default_function():
    df_final=pd.read_csv('final_dataset.csv')
    zipcodelst=[int(i) for i in df_final['Zipcode'].values.tolist()]

    ROOT = tk.Tk()
    ROOT.withdraw()
    use_input = simpledialog.askinteger(title='Zipcode',prompt='Enter a zip code (LA city only, e.g. 90007):')

    for i in range(0,len(df_final['Zipcode'])):

        if use_input==int(df_final['Zipcode'].values[i]):
            price=int(df_final['Median Price'][i])
            acre=df_final['Acre of Parks'][i].round(2)
            sqft=df_final['Park space per person(sq ft)'][i].round(2)

            messagebox.showinfo("Result",f'Median House Price:${price}\n Parks:{acre} acres\n Park space per person:{sqft} sq.ft')
    if use_input not in zipcodelst:
        messagebox.showwarning('Warning', 'No information! Try another one!')

if __name__=='__main__': 
    
    if len(sys.argv)==1: 
        default_function()

