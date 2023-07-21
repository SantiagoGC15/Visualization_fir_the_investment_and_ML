"""
Author: Santiago Cruz
Date: September 09, 2022
Description: Graph spend behavior for a certain period compared to the last two previous years. 
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from adjustText import adjust_text
from matplotlib.ticker import FuncFormatter
import matplotlib as mpl

plt.rcParams['figure.figsize']=(16,9)
plt.rcParams["legend.loc"] = 'best'
plt.style.use('ggplot')
mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=["#E24A33", "#348ABD", "#8EBA42"]) 

def Number_format(num, pos):
  num = float('{:.3g}'.format(num))
  magnitude = 0
  while abs(num) >= 1000:
    magnitude += 1
    num /= 1000.0
  decimalnumber = str(round(num, 1))
  return '{}{}'.format(decimalnumber, ['', 'K', 'M', 'B', 'T'][magnitude])

def transform_data(chartdata, country_name):
  chart_df=chartdata.copy()
  list_of_years=chart_df.harmonized_year.drop_duplicates().tolist()

  texts = []
  fig, ax = plt.subplots()
  for x in list_of_years:
    Year_data = chart_df.loc[chart_df['harmonized_year'] == x][['Spend','harmonized_month']]
    Year_data = Year_data.set_index('harmonized_month')
    plt.plot(Year_data,'-o',label=str(x))
    plt.xticks(range(1,13,1))
    ax.set_xticklabels(['January', 'February', 'March', 'April', 'May', 'June', 'July','August', 'September', 'October', 'November', 'December'])
    for i,j in Year_data.Spend.items():
      texts.append(plt.annotate(str(Number_format(j,1)), xy=(i, j)))
  
  adjust_text(texts, only_move={'points':'y', 'texts':'y'})
  plt.gca().yaxis.set_major_formatter(FuncFormatter(Number_format))
  plt.legend(title='Year')
  plt.title('Spend of {} for Months'.format(country_name))
  plt.xlabel('Downloaded Months')
  plt.ylabel('Spend ($)')
  plt.tight_layout()
  return plt