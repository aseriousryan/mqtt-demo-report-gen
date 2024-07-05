import os
import time

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def read_csv(file_path):
    df = pd.read_csv(file_path,sep=';', header=None, names=['GID','Datetime','Ch1','Ch2','Ch3','Ch4','Ch5','Ch6','Ch7']).iloc[1:]
    df['Datetime'] = pd.to_datetime(df['Datetime'])# Convert 'Datetime' to datetime type
    df_A = df[df['GID'] == 'SM365POM240001']
    return df_A

# Function to create plots
def create_plots(df, list_channel, report_detail):
    
    first_page_num_channels = 4  # Number of channels to plot on the first page
    subsequent_page_num_channels = 3  # Number of channels to plot on subsequent pages

    total_channels = len(list_channel)
    total_pages = 1 + (total_channels - first_page_num_channels + subsequent_page_num_channels - 1) // subsequent_page_num_channels  # Calculate number of pages needed

    # Create subplots
    fig, axes = plt.subplots(nrows=len(list_channel), ncols=1, figsize=(11.69, 8.27), sharex=True)

    for page in range(total_pages):

        if page == 0:
            fig = plt.figure(figsize=(11.69, 8.27)) # A4 size in inches (landscape)

             # Add report details on the first page
            fig.text(0.1, 0.95, f'Company Name: {report_detail[list(report_detail.keys())[3]]}', fontsize=12, ha='left')
            fig.text(0.1, 0.92, f'Machine ID: {report_detail[list(report_detail.keys())[3]]}', fontsize=12, ha='left')
            fig.text(0.1, 0.89, f'Report Date: {report_detail[list(report_detail.keys())[3]]}', fontsize=12, ha='left')
            fig.text(0.1, 0.86, f'Data Date: {date_taken}', fontsize=12, ha='left')
    for i, channel in enumerate(list_channel):

        #Put title in Graph
        if i == 0:
            axes[i].set_title(f'Time Series of Selected Channels for {report_detail[list(report_detail.keys())[3]].strftime("%Y-%m-%d")}')

        axes[i].plot(df['Datetime'], df[channel], linestyle='-', label=channel)
        axes[i].set_ylabel(channel)
        axes[i].grid(axis='x')  # Enable only vertical grid lines

        # x-ticks configurations
        hourly_ticks = pd.date_range(start=report_detail[list(report_detail.keys())[3]], end=report_detail[list(report_detail.keys())[4]], freq='H')
        axes[i].set_xticks(hourly_ticks)
        axes[i].set_xticklabels(hourly_ticks.strftime('%H:%M'), rotation=45)

        # y-ticks configurations
        y_min = df[channel].min()
        y_max = df[channel].max()
        y_median = df[channel].median()
        axes[i].set_yticks([float(y_min), float(y_median), float(y_max)])

    plt.tight_layout()
    return fig