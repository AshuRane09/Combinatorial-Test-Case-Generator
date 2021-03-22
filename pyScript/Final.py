#!/usr/bin/env python
# coding: utf-8

# In[92]:


import pandas as pd
import numpy as np


# In[93]:

def Final():
    df=pd.read_csv("result.csv",index_col=0)
    #df.head()


    # In[54]:


    #concession = ['95','100','85','90','70','80']
    #df['concession']=np.NAN
    # def Concession():
    #     df['concession'] = np.where((df['Disabled Passenger'] != 'NA') | (df['Patient'] != 'NA') | (df['Widow'] != 'NA') | (df['Awardees'] != 'NA') | (df['Student'] != 'NA') | (df['youth'] != 'NA') | (df['Kisan'] != 'NA') | (df['Artists and sportsmen'] !='NA') | (df['Medical Professionals'] !='NA'), 70, np.nan)
    #     df['concession'] = np.where((df['Disabled Passenger'] != 'NA') & (df['Patient'] != 'NA') & (df['Student'] != 'NA'),80, np.nan)
    #     df['concession'] = np.where((df['Patient'] != 'NA'), 85, np.nan)
    #     df['concession'] = np.where((df['Disabled Passenger'] != 'NA') & (df['Patient'] != 'NA') & (df['Widow'] != 'NA'), 95, np.nan)
    #     df['concession'] = np.where((df['Disabled Passenger'] != 'NA') & (df['Passenger Type'] == 'Senior Citizen') & (df['Widow'] != 'NA') &(df['Patient'] != 'NA'), 100, np.nan)


    # In[55]:


    #Concession()


    # In[57]:



    # In[71]:


    # if(df.loc[df.loc['Patient'] != 'NA']):
    #     df['concession'] = '85'
    #df['concession'] = df[df['Patient'] != 'NA'] 
    # if(df['Patient'] != 'NA'):
    #     df['concession'] = '85'

    #df.loc[df.loc['A'] > 2, 'A']


    # In[94]:


    df.loc[(df['Disabled Passenger'] != 'NA') | (df['Patient'] != 'NA') | (df['Widow'] != 'NA') | (df['Awardees'] != 'NA') | (df['Student'] != 'NA') | (df['youth'] != 'NA') | (df['Kisan'] != 'NA') | (df['Artists and sportsmen'] !='NA') | (df['Medical Professionals'] !='NA'),'concession'] = '70'
    df.loc[(df['Disabled Passenger'] != 'NA') & (df['Patient'] != 'NA') & (df['Student'] != 'NA'),'concession'] = '80'
    df.loc[df['Patient'] != 'NA','concession'] = '85'
    df.loc[(df['Disabled Passenger'] != 'NA') & (df['Patient'] != 'NA') & (df['Widow'] != 'NA'),'concession'] = '95'
    df.loc[(df['Disabled Passenger'] != 'NA') & (df['Passenger Type'] == 'Senior Citizen') & (df['Widow'] != 'NA') &(df['Patient'] != 'NA'),'concession'] = '100'


    # In[96]:


    #df


    # In[97]:


    df.to_csv('Final.csv')


    # In[ ]:




