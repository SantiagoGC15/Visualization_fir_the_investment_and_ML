"""
Author: Santiago Cruz
Date: September 14, 2022
Description: Graph of a histogram to display the amount of mapping that was done manually against the one that made the Machine Learning.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize']=(20,9)
plt.style.use('ggplot')

def transform_data(df, country_name="Null"): 
    df1=df.assign(x=pd.to_datetime(df['download_period']).dt.strftime('%B %d, %Y')).pivot(index='x', columns='Mapped_type', values='number_of_mapped').sort_values(by='x',key=pd.to_datetime)
    df1['Machine Learning'] = df1['Machine Learning'].replace(np.nan, 0)
    df1['Manual Mapping'] = df1['Manual Mapping'].replace(np.nan, 0)

    pro = df1.div(df1.sum(axis=1), axis=0)
    ax=pro.plot(kind='bar',stacked=True, rot=0, xlabel='Download Period', ylabel='Number of Mapping',title='Amount of Mapping for {} \n \n'.format(country_name))
    ax.get_yaxis().set_ticks([])
    plt.grid()
    ax.legend(loc='right',bbox_to_anchor=(1, 1.085),fancybox=True, shadow=True, ncol=2,title='Mapped type')

    cols = pro.columns

    for c, col in zip(ax.containers, cols):
        vals = df1[col]
        labels = [f'{val:0.0f}' if (w := v.get_height()) != 0 else '' for v, val in zip(c, vals)]
        ax.bar_label(c, labels=labels, label_type='center', fontweight='bold')

    df1['tot'] = df1.astype(int).sum(axis=1)

    for i in range(10):
        x = ax.patches[i].get_x()
        ax.annotate('{:.0f}'.format(df1['tot'][i]), xy=(x+0.25,1.003),fontweight='bold',ha='center')
    plt.tight_layout()
    return plt 

