# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 14:59:32 2019

@author: Jack Hirst
"""
import pandas as pd
import os
import numpy as np
import FilamentAnalysisFunctions as iff
import scipy.stats as st

#os.chdir("")

'''1: plot concentration of filaments and violin plots of their length distribution'''

#not absolutely necessary, but presets let you change between conditions faster
presets = {
        #key :[file_list, x_label, xlabels, continuous x axis?]
        #egs here, these will need to be altered
        "pip": [["pipette1", "pipette2", "pipette3"], "Pipette actions", ["0", "5", "10", "30"], True],
        "cla": [["clarification1", "clarification2", "clarification3"], " ", ["Unclarified", "Clarified"], False]
        }

'''csv files should be formatted as a column of filament lengths for each 
condition, with the title of the condition as the very first value in the 
column'''

#select the conditions f
condition = "pip"
preset = presets[condition]
files = preset[0] 
x_title = preset[1]
conditions = preset[2]
continuous_x = preset[3] 

#set the plot aesthetics
dpi = 600
axis_fontsize = 20
tick_fontsize = 18
plot_height = 5
bar_y_lim = 1
axis_weight = 1.5
extra_bar_x = 0.5
extra_scatter_x = 0.1

mf = pd.DataFrame()
mf["conditions"] = conditions
mf["values"] = iff.normalised_counts_from_file_names(files)
mf = iff.calculate_parameters(mf, multiple_values=True)

#plot the graphs
iff.plot_violins(files, x_lim = 1.1, y_lim = 40, x_title = x_title, make_stats=True,
                 y_title = "Length of filament (μm)", x_labs = mf["conditions"], 
                 ast_height = 0.9, dpi = dpi, axis_fontsize= axis_fontsize,
                 tick_fontsize= tick_fontsize, figheight = plot_height, axis_weight = axis_weight)

if continuous_x:
    iff.plot_scatter(mf, x_title=x_title, y_title = "Observed filament concentration\n(normalised to untreated)", dpi = dpi, axis_fontsize= axis_fontsize,
                 tick_fontsize= tick_fontsize, figheight = plot_height, y_lim=bar_y_lim,
                 extra_x_space=extra_scatter_x, line_type="linear")
else:       
    iff.plot_bar(mf, x_title=x_title, y_title = "Observed filament concentration\n(normalised to untreated)",
                 dpi = dpi, axis_fontsize= axis_fontsize, make_stats=True,
                 tick_fontsize= tick_fontsize, figheight = plot_height, y_lim=bar_y_lim,
                 axis_weight = axis_weight)

'''2: plot infectious titres'''

titre_data = [ #normalised data for plaque assays
        [1,1,1,1,1],
        [0.95, 0.71, 0.83, 0.57, 0.69],
        [0.66, 1.14, 0.55, 0.78],
        [2.2, 1.03, 0.97, 0.36, 0.98],
        [1, 0.33, 1.05],
        ]

mf = pd.DataFrame()
mf["conditions"] = conditions
mf["values"] = titre_data
mf = iff.calculate_parameters(mf)

iff.plot_bar(mf,x_title=x_title, dpi = dpi, axis_fontsize= axis_fontsize,
                 tick_fontsize= tick_fontsize, figheight = plot_height, y_lim=2,
                 y_title = "Infectious titre (pfu)\n(normalised to untreated)"
                 )

print(mf["p_values"])


'''3: Plot the eccentricities of fitted ellipse to the filaments. These 
require csv files with columns "Condition", "Major", "Minor" which can be
partially generated using the imageJ macro "Eccentricity Analysis" (also in
the Github repository)'''

os.chdir("")
#using freezing as an example, takes repeats from each repeat and pools the same
#conditions from each
frozen_files = ["frozen1", "frozen2", "frozen3"]
unfrozen_files = ["unfrozen1", "unfrozen2", "unfrozen3"]
conditions = ["Unfrozen", "Frozen"]
frozen_frames = iff.get_data_frames(frozen_files)
unfrozen_frames = iff.get_data_frames(unfrozen_files)

def get_all_eccentricities(frames):
    eccs = []
    for frame in frames:
        eccentricities = [iff.calculate_eccentricity(major,minor) for major,minor
                      in zip(frame["Major"], frame["Minor"])]
        eccs += eccentricities
    return(eccs)

frozen_eccs = get_all_eccentricities(frozen_frames)
unfrozen_eccs = get_all_eccentricities(unfrozen_frames)        

kinky_data = [unfrozen_eccs, frozen_eccs]

kinky_data = [[iff.mean_eccentricity_of_frame(x) for x in unfrozen_frames],
              [iff.mean_eccentricity_of_frame(x) for x in frozen_frames]]

mf = pd.DataFrame()
mf["conditions"] = conditions
mf["values"] = kinky_data
mf = iff.calculate_parameters(mf)

iff.plot_bar(mf,x_title=x_title, dpi = dpi, axis_fontsize= axis_fontsize,
                 tick_fontsize= tick_fontsize, figheight = plot_height, y_lim=1,
                 y_min = 0.75, y_title = "Mean eccentricity of fitted ellipses",
                 edgecolor = "none")

p_values = []
for i in range(1, len(mf["values"])):
    p_values += [st.ttest_ind(mf["values"][0], mf["values"][i])]
print(p_values)
print("")


''' 4: Plot histograms of how length and concentrations vary across several
samples'''
#raw mean values for each condition, drawn from the same population (n = 3)
val_medians = [3.430500, 3.425833, 3.722500, 3.392167, 3.686833, 3.448833, 3.538667,
           3.541333, 3.768833, 3.604667, 3.285167, 3.839333, 3.608333, 3.706500,
           3.174167, 3.683667, 3.430667, 3.634667, 3.324000, 3.609167, 3.563333,
           3.569000, 3.246167, 3.673000]

val_counts = [244.00,252.00,270.67,	278.67,	283.00,	298.67,	277.00,	275.33,	291.50,	
          283.33, 258.00,270.50,271.67,329.00,259.33,229.00,220.00,268.67,288.00,
          227.33,325.33,309.00,266.50,242.00]

#normalise the values to the plate mean
val_counts = val_counts/np.mean(val_counts)
val_medians = val_medians/np.mean(val_medians)


iff.plot_hist(val_medians, 0.75, 1.4, 0.05, y_lim = 12, 
              xlab = "Median filament length\n(normalised to plate mean)",
              ylab = "Frequency", figheight = plot_height, axis_fontsize = axis_fontsize,
              tick_fontsize = tick_fontsize)

iff.plot_hist(val_counts, 0.75, 1.4, 0.05, y_lim = 12,
              xlab = "Filament concentration\n(normalised to plate mean)",
              ylab = "Frequency", figheight = plot_height, axis_fontsize = axis_fontsize,
              tick_fontsize = tick_fontsize)
