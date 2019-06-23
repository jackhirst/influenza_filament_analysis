# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 14:59:32 2019

@author: 2263524H
"""
import pandas as pd
import os
import numpy as np
import FilamentAnalysisFunctions as faf

titre_data = [ # raw normalised data for plaque assays for the cryopreservants
        [1,1,1,1,1],
        [0.95, 0.71, 0.83, 0.57, 0.69],
        [0.66, 1.14, 0.55, 0.78],
        [2.2, 1.03, 0.97, 0.36, 0.98],
        [1, 0.33, 1.05],
        ]

#raw mean values for each well, drawn from the same population (n = 3)
val_medians = [3.430500, 3.425833, 3.722500, 3.392167, 3.686833, 3.448833, 3.538667,
           3.541333, 3.768833, 3.604667, 3.285167, 3.839333, 3.608333, 3.706500,
           3.174167, 3.683667, 3.430667, 3.634667, 3.324000, 3.609167, 3.563333,
           3.569000, 3.246167, 3.673000]

val_counts = [244.00,252.00,270.67,	278.67,	283.00,	298.67,	277.00,	275.33,	291.50,	
          283.33, 258.00,270.50,271.67,329.00,259.33,229.00,220.00,268.67,288.00,
          227.33,325.33,309.00,266.50,242.00]

val_counts = val_counts/np.mean(val_counts)
val_medians = val_medians/np.mean(val_medians)

#not absolutely necessary, but presets let you change between conditions faster
presets = {
        #key :[file_list, x_label, xlabels, continuous x axis?], examples below
        "dil": [["validation 1.1", "validation 4.1", "validation 5.1"], "Expected concentration\n(relative to untreated)", ["1", "0.5", "0.25"], True],
        "if16": [["if16.6", "if16.8", "if16.5", "if16.4", "if16.3", "if16.1"], "Freezing condition", ["Unfrozen", "Standard", "Snap", "DMSO", "Snap + DMSO"], False],
        }
'''csv files should be formatted as a column of filament lengths for each 
condition, with the title of the condition as the very first value in the 
column'''
condition = "if16"
preset = presets[condition]
files = preset[0] 
x_title = preset[1]
conditions = preset[2]
continuous_x = preset[3] 

#aesthetics for the graphs
dpi = 600
axis_fontsize = 20
tick_fontsize = 18
plot_height = 5
bar_y_lim = 1.6
axis_weight = 1.5
extra_x = 1

#import the data and calculate parameters to plot (e.g. mean and stdev)
mf = pd.DataFrame()
mf["conditions"] = conditions
mf["values"] = faf.normalised_counts_from_file_names(files)
mf = faf.calculate_parameters(mf)


faf.plot_violins(files, x_lim = 0.9, y_lim = 30, x_title = x_title, 
                 y_title = "Length of filament (μm)", x_labs = mf["conditions"], 
                 ast_height = 0.75, dpi = dpi, axis_fontsize= axis_fontsize,
                 tick_fontsize= tick_fontsize, figheight = plot_height, axis_weight = axis_weight)

if continuous_x:
    faf.plot_scatter(mf, x_title=x_title, dpi = dpi, axis_fontsize= axis_fontsize,
                 tick_fontsize= tick_fontsize, figheight = plot_height, y_lim=bar_y_lim,
                 extra_x_space=extra_x)
else:       
    faf.plot_bar(mf, x_title=x_title, y_title = "Filament concentration\n(normalised to untreated)",
                 dpi = dpi, axis_fontsize= axis_fontsize,
                 tick_fontsize= tick_fontsize, figheight = plot_height, y_lim=bar_y_lim,
                 axis_weight = axis_weight)

#titre analysis
mf = pd.DataFrame()
mf["conditions"] = conditions
mf["values"] = titre_data
mf = faf.calculate_parameters(mf)
faf.plot_bar(mf,x_title=x_title, dpi = dpi, axis_fontsize= axis_fontsize,
                 tick_fontsize= tick_fontsize, figheight = plot_height, y_lim=2.5,
                 y_title = "Infectious titre (pfu)\n(normalised to untreated)")

#validation histograms
faf.plot_hist(val_medians, 0.75, 1.4, 0.05, y_lim = 12, 
              xlab = "Median filament length\n(normalised to plate mean)",
              ylab = "Frequency", figheight = plot_height, axis_fontsize = axis_fontsize,
              tick_fontsize = tick_fontsize)

faf.plot_hist(val_counts, 0.75, 1.4, 0.05, y_lim = 12,
              xlab = "Filament concentration\n(normalised to plate mean)",
              ylab = "Frequency", figheight = plot_height, axis_fontsize = axis_fontsize,
              tick_fontsize = tick_fontsize)