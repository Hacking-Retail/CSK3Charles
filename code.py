# -*- coding: utf-8 -*-
"""
Created on Mon May  2 09:51:13 2022

@author: Proprietaire
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#df = pd.read_csv(r"C:\Users\Proprietaire\Downloads\VO_annonces_2015-ALL_CR\VO_annonces_2015-ALL_CR.csv")

#Lets start by cleaning up the data :
    
print(df.shape)

#print(df.isna)

df_clean=df.dropna()

print(df_clean.shape)

#print(df_clean)

#Maybe this is a bit exagerrated to delete every row with missing data.
#Lets see how it goes anyway

#print("Only "+str((4227/3552912)*100)+"% "+"of the data has been retrieved properly by CS3K")

#After more consideration we don't have to delete the rows were it is the body type or color slug missing


df_clean2=df.dropna(subset =['maker','model','date_created','date_last_seen','price_eur'])

df_clean2.shape

print("Only "+str((2419551/3552912)*100)+"% "+"of the data has been retrieved properly by CS3K")

#This looks like a better dataset to work with
#Lets now format it

df_clean2.info()

df_clean2['date_created']=pd.to_datetime(df_clean2['date_created'],errors='coerce',format='%Y-%m-%d' )
df_clean2['date_last_seen']=pd.to_datetime(df_clean2['date_last_seen'],errors='coerce',format='%Y-%m-%d')

#lets see the sales for 2016 :
    
df_2016=df_clean2[~(df_clean2['date_last_seen'] > '2017-01-01')]
df_2016.date_last_seen.max()
#We have 2053196 cars sold without considering the ones who were just taken off the market

#Now the total value :
    
print(str(df_2016.price_eur.sum())+" €")


#Lets see wich makers we have

brand=df_clean2.maker.unique()

sums_of_sales=pd.DataFrame(brand)
sales=[]

for i in brand : 
    sale=df_2016.loc[df_2016['maker'] == i, 'price_eur'].sum()
    sales.append(sale)

sums_of_sales['Total sales in 2016']=sales

print(sums_of_sales.sum())

shares=[]

for i in range(len(brand)) :
    shares.append((sales[i]/df_2016.price_eur.sum())*100)
    
sums_of_sales['Share of the Market']=shares

#Lets create a new variable for the uptime

df_2016['nb_days'] = ((df_2016.date_last_seen - df_2016.date_created)/np.timedelta64(1, 'D'))
df_2016['nb_days'] = df_2016['nb_days'].astype(int)

#We can now calculate the mean

mean_tts=df_2016.nb_days.sum()/df_2016.shape[0]
print(mean_tts)

#The average uptime on the database is 85.0005376983006 days

mean_age=df_2016.manufacture_year.mean(skipna=True)
print(int(mean_age))

#The average car is from 2003 so the mean age is 13 years old

#Lets now try to throw away forgotten cars

df_2016.nb_days.unique()
df_2016.nb_days.mode()
uptime=df_2016['nb_days'].value_counts().nlargest(100)
uptime
figure=plt.figure(figsize=(18,12))
figure=plt.plot(uptime,'^')
plt.title("Numbers of sales per duration")
plt.xlabel("Days of uptime")
plt.ylabel("Ads taken down")


#We're gonna assume that every post the following

# =============================================================================
# Every post thats more 150,175 days old is inactive and therefore
# deleted
# Moreover, half of the post that are 60 days old are inactive.
# This is done to be in line with most number of sales for other days
# =============================================================================

df_real = df_2016.loc[(df_2016["nb_days"] != 150) | (df_2016["nb_days"] != 175) ]
df_real = df_real.drop(df_real[(df_real['nb_days'] == 60)].sample(frac=.5).index)


#Let's see if everythnig worked fine
real_uptime=df_real['nb_days'].value_counts().nlargest(100)
real_uptime
figure=plt.figure(figsize=(18,12))
figure=plt.plot(real_uptime,'o')
plt.title("Numbers of sales per duration")
plt.xlabel("Days of uptime")
plt.ylabel("Ads taken down")

#We therefore have a way to know how many have been miscalculated :
    
misc=len(df_2016)-len(df_real)
misc

mean_tts_real=df_real.nb_days.mean(skipna=True)
print(mean_tts_real)
mean_tts


models=pd.DataFrame(df_real.model.unique())

tts=[]

tts= df_real.groupby('model')['nb_days'].mean()
tts=tts.loc['nb_days']
tts['nb_days']
tts=pd.DataFrame(tts)
tts['nb_days'].nsmallest(10)

import tkinter as tk

root= tk.Tk()

canvas1 = tk.Canvas(root, width = 400, height = 300,  relief = 'raised')
canvas1.pack()
label1 = tk.Label(root, text='Get the Average Time to Sale for a Model')
label1.config(font=('helvetica', 14))
label2 = tk.Label(root, text='Type your Model:')
label2.config(font=('helvetica', 10))
canvas1.create_window(200, 100, window=label2)
canvas1.create_window(200, 25, window=label1)
entry1 = tk.Entry (root) 
canvas1.create_window(200, 140, window=entry1)
def getSaleTime ():  
    x1 = entry1.get()
    rep=tts.query(f'model==@x1')
    label1 = tk.Label(root, text=rep)
    canvas1.create_window(200, 230, window=label1)
button1 = tk.Button(text='Get Results', command=getSaleTime,bg='brown', fg='white', font=('helvetica', 9, 'bold'))
canvas1.create_window(200, 180, window=button1)

root.mainloop()


#Let's now create our algorithm 

df_real['model'].value_counts()
final=df_real['model'].value_counts().nlargest(300)
final.index
df_final= df_real[~df_real['model'].isin(final.index)]



score=[]

df_final['score'] = ( (tts['nb_days'] > 5).astype(int)
                + (df_final['Color'] == 'Red').astype(int) 
                + (df['Risk'] > 7).astype(int) )

models=pd.DataFrame(df_final.model.unique())

tts=[]

tts= df_final.groupby('model')['nb_days'].mean()
tts=pd.DataFrame(tts)
tts=tts.loc['nb_days']
tts['nb_days']

tts['nb_days'].nsmallest(10)

