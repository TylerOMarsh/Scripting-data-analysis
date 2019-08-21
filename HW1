# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 17:25:03 2019


"""

import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt




df =  pd.read_csv("YouthRisk2009.csv")

df.head(60) # loook at a good chunk of data
df.shape
df.info() # structure of our data

# extract strings in our Sleep column
df['Sleep'] = df['Sleep'].str.extract("(\d+)", expand=False)

df = df.rename(columns = lambda col: col.replace(" ", ""))
#this will work 

cols = ["SmokeLife", "SmokeDaily"]


df[cols] = df[cols].replace({'Yes': 1, "No": 0})


no_na_df = df.dropna()

#story shallow copy so we can preserve original amount of data
df1 = no_na_df.copy()
#replace nas with zero
df.isnull().values.any() # checks for null values


df[pd.isnull(df).any(axis=1)]

df1.head(60)

df1.isnull().values.any()

check_string = df1['Sleep'].str.isnumeric()

#drop unnamed column
df1 = df1.drop(df.columns[0], axis=1)

#analyze data

df1.info()


#for each age group, does their marijuaEver go up?

print("Percents of each age group that has tried marijuana\n\n" + str(df1.groupby(['Age'])['MarijuaEver'].sum() / df1['Age'].value_counts()))

#it appears that the percentage goes up by age

# does less sleep equal more smoking or does more smoking equal less sleep?


# MarijuEver  is higher in those that sleep longer which seems stereotypical
#shows us the percents of each category by sleep7
print("Percent of teens with less than 7 hours of sleep or >= 7 by category\n\n" + str(df1.groupby(['Sleep7'])["SmokeLife","MarijuaEver","SmokeDaily"].sum()/df1['Sleep7'].sum()))

df1['Sleep7'].value_counts() # much more sleep  7 or more.

#look at the percentages of those who sleep 7 or 

#mean age of all tried marijuana

print("The mean age of teens that tried Marijuana and admitted it in a survey \n\n" + str(df1.groupby("MarijuaEver")["Age"].mean()))

calc =df1.groupby(['Age'])['MarijuaEver'].sum() / df1['Age'].value_counts()


calc.plot( kind = "bar")
print("Percent of each age that has atleast tried Marijuana")
