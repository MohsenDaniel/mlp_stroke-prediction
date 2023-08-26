import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import plotly.express as px
import seaborn as sns

mako = sns.color_palette('mako_r')


def pieChart(df):

    data = df.value_counts().values
    lables = df.value_counts().index
    
    fig, ax = plt.subplots(figsize=(2,2))
    ax.pie(data, labels=lables, colors=mako, autopct='%.0f%%', startangle=90)
    plt.show()

    
def percentLine(percents: list, labels: list, title: str, rows: bool, lower_limit: float, upper_limit: float):

    length = len(percents)
    ratios = percents/100
        
    fig, ax = plt.subplots(figsize=(15, 0.5))
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(xmax=1,decimals=1))
    ax.yaxis.set_visible(False)
    
    mako = sns.color_palette('mako_r')
    color = [(0, 0, 0)]
    colors = color + mako[0:length-1]
    
    if rows == False:
        
        ax.scatter(x=ratios, y=[0]*length, color=colors)
        
        for i in range(length):
            ax.text(ratios[i]+(0.02*upper_limit), -0.012, labels[i])
            
    else:
        
        for i in range(length):
            ax.scatter(x=ratios[i], y=[0], label=labels[i], color=colors[i])
        
        ax.legend(loc='lower right', ncol=6, handletextpad=0, columnspacing=0.2, bbox_to_anchor=(1, 1.2), borderaxespad=0)
        
    plt.xlim(lower_limit, upper_limit)
    plt.title(title, loc='left', pad=10)
    plt.show()
    
    
def histogram(df, column: str, title: str, figsize: tuple):
    
    hist_df = df.copy()
    hist_df[column] = pd.Categorical(hist_df[column], df[column].value_counts().index)
    hist_df = hist_df.sort_values(column)
    
    fig, ax = plt.subplots(figsize=figsize)
    sns.histplot(data=hist_df, x=column, hue=column, palette='mako_r', legend=False, ax=ax)

    length = len(hist_df[column].value_counts())
    height = hist_df[column].value_counts().values
    percent = (height/len(hist_df[column])) * 100

    for i in range(length):
        ax.text(x=i-0.2, y=height[i]+50, s='{}%'.format(round(percent[i],1)))

    ax.set(xlabel=None)
    ax.tick_params(bottom=False)

    plt.title(title, pad=10)
    plt.ylim(0, max(height)+250)
    plt.show()
    
    
def barChartByStroke(df, bins, labels, column: str, title: str):
    
    bar_df = df[[column,'stroke']].copy()
    bar_df[column] = pd.cut(x=df[column], bins=bins, labels=labels)
    bar_df = bar_df.value_counts().to_frame().sort_index().reset_index()
    nostroke_count = [bar_df['count'][x] if bar_df.stroke[x] == 0 else 0 for x in bar_df.index]
    stroke_count = [bar_df['count'][x] if bar_df.stroke[x] == 1 else 0 for x in bar_df.index]
    bar_df['nostroke_count'] = nostroke_count
    bar_df['stroke_count'] = stroke_count
    bar_df = bar_df.drop(['count', 'stroke'], axis=1).groupby([column]).sum().reset_index()
    
    fig, ax = plt.subplots(figsize=(8,4))
    ax.bar(x=bar_df[column], height=bar_df.nostroke_count, width=1, color=mako[2], bottom=bar_df.stroke_count, edgecolor='black', alpha=0.8)
    ax.bar(x=bar_df[column], height=bar_df.stroke_count, width=1, color=mako[4], edgecolor='black', alpha=0.8)
    ax.legend(['No Stroke', 'Stroke'])
    ax.tick_params(bottom=False)
    plt.title(title)
    plt.show()
    
    
def pScatterPlot(df, control_var, title: str):

    length = len(df.index)
    significance_level = 0.05

    fig, ax = plt.subplots(figsize=(15,3))
    sns.scatterplot(x=df[control_var], y=df.p_value, hue=df.index, palette='mako_r', legend=False, ax=ax)
    ax.axhline(y=significance_level, color=mako[0], linewidth=0.8)
    ax.axhspan(-0.05, significance_level, color=mako[0], alpha=0.05)
    ax.text(0.1, 0.125, 'significance level = 0.05', color=mako[0], bbox=dict(facecolor=mako[0], alpha=0.05))
    ax.set(xlabel=None)
    plt.title(title)
    plt.xlim(0,10)
    plt.ylim(-0.05,1.05)
    plt.show()