import os
import random
import time
import math

import numpy as np
import pandas as pd

# for plotting
import matplotlib.pyplot as plt

# Plotting two indicators for one country or region plus SI index
def plot_cases_and_index_data(data, 
                              countries=None,
                              continents=None,
                              plot_columns=None,
                              use_continents=False):
    
    # define subplot grid
    fig, axs = plt.subplots(2, 1, figsize=(12,10))
    ax1, ax2 = axs.flatten()
    
    # plot adjustments
    plt.subplots_adjust(hspace=0.3)
    
    # setting title
    if use_continents:
        plt.suptitle("Visualizing registered cases and SI index for " + continents[0],
                     size=16, y=1.04)
    else:
        plt.suptitle("Visualizing registered cases and SI index for " + countries[0],
                     size=16, y=1.04)
    
    # define axes data
    timestamps   = np.unique(data["Timestamps"])
    
    if use_continents:
        if isinstance(plot_columns, list):
            cases_plot_1 = data.loc[data["Continent"]==continents[0],
                                    plot_columns[0]].values
            cases_plot_2 = data.loc[data["Continent"]==continents[0],
                                    plot_columns[1]].values
        else:
            cases_plot_1 = data.loc[data["Continent"]==continents[0],
                                     plot_columns].values           
        si_index     = data.loc[data["Continent"]==continents[0],
                                "SI Index"].values        
    else:
        if isinstance(plot_columns, list):
            cases_plot_1 = data.loc[data["Country"]==countries[0],
                                    plot_columns[0]].values
            cases_plot_2 = data.loc[data["Country"]==countries[0],
                                    plot_columns[1]].values
        else:
             cases_plot_1 = data.loc[data["Country"]==countries[0],
                                     plot_columns].values        
        si_index     = data.loc[data["Country"]==countries[0],
                                "SI Index"].values
    
    # cases plot
    if isinstance(plot_columns, list):
        ax1.plot(timestamps, cases_plot_1, color="red", label=plot_columns[0])
        ax1.plot(timestamps, cases_plot_2, color="green", label=plot_columns[1])
    else:
        ax1.plot(timestamps, cases_plot_1, color="red", label=plot_columns)
    ax1.set_xticklabels(timestamps, rotation=45, ha="right")
    
    # reducing number of displayed labels for better plot visibility
    for n, label in enumerate(ax1.xaxis.get_ticklabels()[:-1]):
        if n % math.ceil((len(timestamps) * 0.1)) != 0:
            label.set_visible(False)
    
    ax1.set_ylabel("Registered Cases")
    ax1.legend()
    
    # SI index plot
    ax2.plot(timestamps, si_index, color="brown", label="Stringency Index")
    ax2.set_xticklabels(timestamps, rotation=45, ha="right")
    
    # reducing number of displayed labels for better plot visibility
    for n, label in enumerate(ax2.xaxis.get_ticklabels()[:-1]):
        if n % math.ceil((len(timestamps) * 0.1)) != 0:
            label.set_visible(False)
    
    ax2.set_ylabel("Index Value")
    ax2.legend()

    fig.tight_layout()
    plt.show();

# Plotting two countries indicators plus SI Index
def plot_cases_and_index_data_comparison(data, 
                                         countries=None,
                                         continents=None,
                                         plot_columns=None,
                                         use_continents=False):
    
    # define subplot grid
    fig, axs = plt.subplots(2, 2, figsize=(12,10))
    ax1, ax2, ax3, ax4 = axs.flatten()
    
    # setting title
    if use_continents:
        plt.suptitle("Visualizing registered cases and SI index for " + " & ".join(continents),
                     size=16, y=1.04)
    else:
        plt.suptitle("Visualizing registered cases and SI index for " + " & ".join(countries),
                     size=16, y=1.04)
        
    # setting column titles per country or continent
    if use_continents:
        column_titles = continents
    else:
        column_titles = countries
        
    for ax, col in zip(axs[0], column_titles):
        ax.set_title(col, fontsize=16, y=1.02)
    
    # plot adjustments
    plt.subplots_adjust(hspace=0.3)
    
    # define axes data
    timestamps   = np.unique(data["Timestamps"])
    
    if use_continents:
        cases_plot_1 = data.loc[data["Continent"]==continents[0],
                                plot_columns].values
        cases_plot_2 = data.loc[data["Continent"]==continents[1],
                                plot_columns].values
       
        si_index_1   = data.loc[data["Continent"]==continents[0],
                                "SI Index"].values
        si_index_2   = data.loc[data["Continent"]==continents[1],
                                "SI Index"].values       
    else:
        cases_plot_1 = data.loc[data["Country"]==countries[0],
                                plot_columns].values
        cases_plot_2 = data.loc[data["Country"]==countries[1],
                                plot_columns].values
       
        si_index_1   = data.loc[data["Country"]==countries[0],
                                "SI Index"].values
        si_index_2   = data.loc[data["Country"]==countries[1],
                                "SI Index"].values
    
    # Cases Plot
    ax1.plot(timestamps, cases_plot_1, color="red", label=plot_columns)
    ax1.set_xticklabels(timestamps, rotation=45, ha="right")
    
    for n, label in enumerate(ax1.xaxis.get_ticklabels()[:-1]):
        if n % math.ceil((len(timestamps) * 0.1)) != 0:
            label.set_visible(False)
    
    ax1.set_ylabel("Registered Cases")
    ax1.legend()
    
    ax2.plot(timestamps, cases_plot_2, color="orange", label=plot_columns)
    ax2.set_xticklabels(timestamps, rotation=45, ha="right")
    
    for n, label in enumerate(ax2.xaxis.get_ticklabels()[:-1]):
        if n % math.ceil((len(timestamps) * 0.1)) != 0:
            label.set_visible(False)
            
    ax2.legend()
    
    # SI Index plot
    ax3.plot(timestamps, si_index_1, color="brown", label="Stringency Index")
    ax3.set_xticklabels(timestamps, rotation=45, ha="right")
    
    for n, label in enumerate(ax3.xaxis.get_ticklabels()[:-1]):
        if n % math.ceil((len(timestamps) * 0.1)) != 0:
            label.set_visible(False)
    
    ax3.set_ylabel("Index Value")
    ax3.legend()

    ax4.plot(timestamps, si_index_2, color="navy", label="Stringency Index")
    ax4.set_xticklabels(timestamps, rotation=45, ha="right")

    for n, label in enumerate(ax4.xaxis.get_ticklabels()[:-1]):
        if n % math.ceil((len(timestamps) * 0.1)) != 0:
            label.set_visible(False)
            
    ax4.legend()
                            
    fig.tight_layout()
    plt.show();