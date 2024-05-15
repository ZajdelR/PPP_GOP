# -*- coding: utf-8 -*-
"""
Created on Wed May 15 10:35:06 2024

@author: UPWr
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 9
# plt.rcParams['font.size'] = 9

dirs = {'inp': 'INPUT',
        'plots': 'OUTPUT_PLOTS',
        'out': 'OUTPUT_DATA'}

def load_and_prepare_data(filepath):
    data = pd.read_csv(filepath, skiprows=1, delim_whitespace=True, header=None)
    columns = [
        'Solution_AC', 'Site', 'Period', 'Conv', 'Have', 'Expt', 'Rat', 'ignore1',
        'Hpe68', 'Hpe95', 'ignore2', 'Vpe68', 'Vpe95', 'ignore3',
        'biasN', 'biasE', 'biasU', 'ignore4', 'stdN', 'stdE', 'stdU', 'ignore5',
        'rmsN', 'rmsE', 'rmsU'
    ]
    data.columns = columns
    data.drop(columns=[col for col in data.columns if 'ignore' in col], inplace=True)
    data[['AC', 'Interval', 'Systems']] = data['Solution_AC'].str.split('-', expand=True)
    data.drop(columns=['Solution_AC'], inplace=True)
    return data

def analyze_by_ac_and_site(data):
    results = {}
    for (interval, ac), group in data.groupby(['Interval', 'Systems']):
        group_stats = group.groupby('AC')[['Hpe95','Vpe95']].quantile(.95)
        results[(interval, ac)] = group_stats
        
    results = pd.concat(results).reset_index()
    columns = list(results.columns)
    columns[:3] = ['int','sys','sol']
    results.columns = columns 
    return results

def boxplot_interval_systems(data, column, period, strategy, ylim=30, scaler=1e3, unit='mm'):
    
    f, ax = plt.subplots(1, 1, figsize=(8.4/2.54, 8/2.54))  # Figure size in inches (converted from cm)

    subset_data = data[(data['Interval'] == period) & (data['Systems'] == strategy)]
    subset_data.loc[:, column] *= scaler
    
    subset_data['sort_key'] = subset_data['AC'].apply(lambda x: ('0' if x == 'REF' else '2' if x.startswith('IG') else '1') + x)
    subset_data.sort_values('sort_key', inplace=True)
    subset_data.drop(columns=['sort_key'], inplace=True)
    sorted_columns = subset_data['AC'].unique()
    
    bx = sns.boxplot(x='AC', y=column, data=subset_data,
                     whis=[0, 100], color="#aec6cf", ax=ax)
    
    iqr = subset_data.groupby('AC')[column].agg(lambda x: x.quantile(0.95))
    iqr = iqr.loc[sorted_columns].reset_index()
    best_ac = iqr[column].idxmin()
    bx.patches[best_ac].set_facecolor('lightgreen')
    worst_ac = iqr[column].idxmax()
    bx.patches[worst_ac].set_facecolor('salmon')
    
    ax.set_title(f'{period} - {strategy}')
    ax.set_ylim(0, ylim)
    
    ax.set_ylabel(f'{column.upper()} [{unit}]')

    ax.set_xlabel('AC')
    ax.tick_params(axis='x', rotation=90)  # Rotate x-tick labels by 90 degrees

    plt.tight_layout(pad=0.01)
    # Saving the plot to file
    plt.savefig(os.path.join(dirs['plots'], f'{column}_{period}_{strategy}.png'),
                dpi=600)

def heatmap_mean_rate(data, interval, systems, aggfunc='mean'):
    # Calculate mean or other aggregate function of 'Rat' for each 'Site', grouped by 'AC', 'Interval', 'Systems'
    rat_mean_per_site = data.groupby(['AC', 'Interval', 'Systems', 'Site'])['Rat'].agg(aggfunc).reset_index()
    
    # Filter data for the specified 'Interval' and 'Systems'
    filtered_data = rat_mean_per_site[(rat_mean_per_site['Interval'] == interval) & (rat_mean_per_site['Systems'] == systems)]
    
    # Sort the ACs with 'REF' first and those starting with 'IG' at the end
    filtered_data['sort_key'] = filtered_data['AC'].apply(lambda x: ('0' if x == 'REF' else '2' if x.startswith('IG') else '1') + x)
    filtered_data.sort_values('sort_key', inplace=True)
    filtered_data.drop(columns=['sort_key'], inplace=True)
    sorted_columns = filtered_data['AC'].unique()
    
    # Create a pivot table for the heatmap
    pivot_table = filtered_data.pivot(index="Site", columns="AC", values="Rat")
    
    pivot_table = pivot_table[sorted_columns]
    
    # Plot heatmap
    plt.figure(figsize=(17.4/2.54, 15/2.54))  # Size in inches
    sns.heatmap(pivot_table, annot=True, fmt=".2f", 
                cmap="RdYlGn", linewidths=.5, cbar=False)
    plt.title(f'Mean Rat by Site and AC \n Solution: {interval}-{systems}')
    plt.xlabel('AC')
    plt.ylabel('')
    
    plt.tight_layout(pad=0.01)
    # Check if directories provided and save the plot to file
    plt.savefig(os.path.join(dirs['plots'],f'HEATMAP_{interval}_{systems}.png'),dpi=600)
    return pivot_table    
    
def save_results_to_excel(analysis_results, filename):
    with pd.ExcelWriter(os.path.join(dirs['out'],filename+'.xlsx')) as writer:
        for key, df in analysis_results.items():
            interval, sys = key
            df.to_excel(writer, sheet_name=f'{interval}_{sys}')