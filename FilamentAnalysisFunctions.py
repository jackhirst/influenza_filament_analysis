# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 14:37:40 2019

@author: 2263524H
"""

import pandas as pd
import numpy as np
from scipy import stats
import scipy.stats as st
import math
import itertools
import matplotlib.pyplot as plt

def strip_nans(a_list):
    ''' takes a list and returns all values that aren't na'''
    return([x for x in a_list if str(x) != "nan"])

def get_data_frames(list_of_file_names):
    '''takes a list of csv file names and imports the files as data frames'''
    frames = []
    for name in list_of_file_names:
        frames += [pd.read_csv(name + ".csv", delimiter = ",")]
    return(frames)

def get_counts(some_frames):
    ''' takes a list of data frames and returns a list of the counts for
    each column'''
    counts_list = []
    for frame in some_frames:
        counts_list += [frame.count()]
    return(counts_list)

def normalise_to_first(counts_list):
    '''normalises each value relative to the first column'''
    normalised_count = [x/counts_list[0] for x in counts_list]
    return(normalised_count)

def get_param_for_column(list_of_counts_lists, col_index, param_function):
    '''if a list of lists of values were arranged as a dataframe, this
    returns the outcome of a function applied to a given column in that frame'''
    targets = []
    try:
        for counts_list in list_of_counts_lists:
            targets += [counts_list[col_index]]
    except IndexError:
        print("")
    return(param_function(targets))

def get_all_params(list_of_counts, param_function):
    '''if a list of lists of values were arranged as a dataframe, this
    returns the outcome of a function applied to every column in that frame'''
    stdevs = []
    for i in range(0, len(list_of_counts[0])):
        stdevs += [get_param_for_column(list_of_counts, i, param_function)]
    return(stdevs)

def ss_ttests(list_of_counts_by_column):
    '''returns single sample two-tailed ttest for each list in a list of lists,
    with a comparison mean of 1'''
    return([stats.ttest_1samp(x,1)[1] for x in list_of_counts_by_column])

def p_to_asterisks(p_values, normalised_to_first = True):
    ''' takes a list of p_values and returns a list of strings containing
    asterisks corresponding with those values'''
    output = []
    if normalise_to_first:
        p_values = p_values[1:len(p_values)]
    for p in p_values:
        if p >= 0.05:
            output += ["n.s"]
        elif 0.01 <= p <= 0.05:
            output += ["*"]
        else:
            magnitude = math.floor(math.log10(p))
            output += ["*" * (abs(magnitude)-1)]
    if normalised_to_first:
        output = [""] + output
    return(output)

def get_centre_x(rectangle):
    '''returns the x position of the centre of a bar on the bar chart'''
    return(rectangle.get_x() + rectangle.get_width()/2)

def combine_lists(list_of_lists):
    '''takes a list of list and returns one combined list of all the values'''
    return(list(itertools.chain.from_iterable(list_of_lists)))

def transpose_list_of_lists(list_of_lists):
    '''if the list of lists were a dataframe, this returns a transposed data
    frame in the form of list of lists'''
    transposed_frame = pd.DataFrame(list_of_lists).transpose()
    transposed_list = pd.Series.tolist(transposed_frame)
    return([strip_nans(x) for x in transposed_list])

def get_lengths(list_of_lists):
    '''returns the length of each list in a list of lists'''
    return([len(x) for x in list_of_lists])

def get_maxes(list_of_lists):
    '''returns the maximum value for each list in a list of lists'''
    return([max(x) for x in list_of_lists])

def duplicate_x_labs(xlabs, list_of_lengths):
    '''duplicates each value in a list to allow it to be plotted as a scatter
    plot'''
    final_xlabs = []
    for index, value in enumerate(list_of_lengths):
        final_xlabs += [list(itertools.repeat(xlabs[index], value))]
    return(final_xlabs)

def get_max(list_of_frames, col_index):
    ''' returns the maximum value from a given column in multiple data frames'''
    subframes = [frame for frame in list_of_frames if
                 len(frame.iloc[0]) >= col_index+1]
    # subframes accounts for unequal n numbers
    columns = [strip_nans(frame.iloc[:,col_index]) for frame in subframes]
    each_max = [max(column) for column in columns]
    return(max(each_max))

def make_intervals(start, stop, step):
    ''' basically just makes a range, but I think it will be easier to
    read the code this way'''
    return(np.arange(start, stop, step))

def get_kde(a_list):
    ''' takes a list and returns the kernel density estimation'''
    stripped_list = strip_nans(a_list)
    return(st.gaussian_kde(stripped_list))

def get_kdes_from_frames(list_of_frames, col_index):
    ''' takes a list of frames and column index and returns the density
    estimation for each'''
    output = []
    subframes = [frame for frame in list_of_frames if
                 len(frame.iloc[0]) >= col_index+1]  
    # subframes accounts for unequal n numbers
    for frame in subframes:
        column = frame.iloc[:,col_index]
        output += [get_kde(column)]
    return(output)

def kde_to_values(kde, intervals):
    ''' takes a density estimation and a list of intervals and returns
    the value for each interval'''
    return([float(kde(interval)) for interval in intervals])

def get_estimations_for_column(list_of_frames, col_index):
    ''' takes a list of frames, a column index and a list of intervals,
    and returns the estimated value of each interval in a data frame
    based on the kde of the inputs'''
    intervals = make_intervals(0, get_max(list_of_frames, col_index), 0.1)
    kdes = get_kdes_from_frames(list_of_frames, col_index)
    values = [kde_to_values(kde, intervals) for kde in kdes]
    return(pd.DataFrame(values).transpose())

def get_y_values(means):
    '''returns the y_values to plot the curve, going from 0 to the maximum
        in increments of 0.1'''
    return(np.arange(0, len(means)/10, 0.1))        

def get_95CI(a_list):
    '''Takes a list of values and returns the 95% confidence interval for 
    the mean'''
    return(st.t.interval(0.95, len(a_list)-1, loc=np.mean(a_list), 
                         scale=st.sem(a_list)))

def get_CIs(estimates_list):
    ''' Takes a list of lists and returns the 95% confidence interval for the
        mean in each'''
    return([get_95CI(estimate) for estimate in estimates_list])

def get_CI_curves(estimates):
    '''takes the curve for the mean distribution and returns the curves for 
    either end of the 95% confidence interval at each point along the mean
    curve'''
    CIs = estimates.apply(get_95CI, 1)
    lower = [CI[0] for CI in CIs]
    upper = [CI[1] for CI in CIs]
    return(lower, upper)

def get_curves_for_column(frames_list, col_index):
    ''' returns a dictionary containing the mean curve, upper CI curve, 
    lower CI curve and y_values for a given column in a set of frames'''
    estimates = get_estimations_for_column(frames_list, col_index)
    means = np.mean(estimates, 1)
    lengths = get_y_values(means)
    CI_curves = get_CI_curves(estimates)
    lower_curves = CI_curves[0]
    upper_curves = CI_curves[1]
    return{"lengths":lengths, "means":means, "lowers":lower_curves,
           "uppers":upper_curves}

def get_all_curves(frames_list):
    ''' returns a dictionary containing the mean curve, upper CI curve, 
    lower CI curve and y_values for every column in a set of frames'''
    all_curves = []
    for index, value in enumerate(frames_list[0]):
        all_curves += [get_curves_for_column(frames_list, index)]
    return(all_curves)
    
def flip_set(curveset, x_lim):
    ''' takes a curveset (upper, lower CIs and means) and returns the same
    set but reflected in the vertical axis'''
    new_curveset = {}
    new_curveset["lengths"] = curveset["lengths"]
    for name, values in curveset.items():
        if name != "lengths":
            new_curveset[name] = [x_lim - x for x in values]
    return(new_curveset)

def get_reflected_curves(list_of_curves, x_lim):
    ''' takes curvesets (upper, lower CIs and means) and returns the same
    sets but reflected in the vertical axis'''
    newcurves = []
    for curve_set in list_of_curves:
        newcurves += [flip_set(curve_set, x_lim)]
        newcurves += [curve_set]
    return(newcurves)

def get_medians_and_stdevs(frames):
    ''' returns the median and standard deviation for every column in every
    frame in a list of data frames'''
    medians = []
    medians += [list(frame.median()) for frame in frames]
    median_frame = pd.DataFrame(medians)
    mean_medians = median_frame.mean()
    stdevs = median_frame.std()
    return(mean_medians, stdevs)

def length_ttests(frames):
    ''' performs a one sample, two-tailed t test comparing the median value
    of every column in a data frame with the first column, and does this over
    every frame in the input list'''
    medians = []
    medians += [list(frame.median()) for frame in frames]
    median_frame = pd.DataFrame(medians)
    p_values = []
    for i in range(1, len(median_frame.iloc[0])):
        column = median_frame.iloc[:,i]
        column = strip_nans(column)
        p_values += [st.ttest_ind(median_frame.iloc[:,0], column)[1]]
    return(p_values)
    
def duplicate_values(values, list_of_lengths):
    '''duplicates each value in a list to allow it to be plotted as a scatter
    plot'''
    final_values = []
    for index, value in enumerate(list_of_lengths):
        final_values += [list(itertools.repeat(values[index], value))]
    return(final_values)

def get_asterisk_positions(subplots, frames, y_lim):
    '''Returns the x and y positions above the centre of each violin so the
    asterisks can be plotted.'''
    xs = []
    ys = []
    for value, subplot in enumerate(subplots):
        if value %2 != 0:
            continue
        else:
            xs += [subplot.get_position().get_points()[1,0]]
            ys += [subplot.get_position().get_points()[1,1]]
            #ys will be the same across the entire plot,so this isn't
            #necessarily that helpful...
    return(xs, ys)

def set_violin_params():
    '''aesthetics for the violin plot'''
    rc = {"axes.spines.left" : False,
          "axes.spines.right" : False,
          "axes.spines.bottom" : True,
          "axes.spines.top" : False,
          "xtick.bottom" : False,
          "xtick.labelbottom" : False,
          "ytick.labelleft" : True,
          "ytick.left" : False}
    plt.rc('ytick', labelsize=14)
    plt.rcParams.update(rc)

def set_bar_params():
    '''aesthetics for the bar and scatter plots and histograms'''
    rc = {"axes.spines.left" : True,
      "axes.spines.right" : False,
      "axes.spines.bottom" : True,
      "axes.spines.top" : False,
      "xtick.bottom" : False,
      "xtick.labelbottom" : True,
      "ytick.labelleft" : True,
      "ytick.left" : True}
    plt.rc('ytick', labelsize=14)
    plt.rcParams.update(rc)
    

def plot_violins(files, x_lim, y_lim, x_title, y_title, x_labs, ast_height,
                figheight = 5, axis_fontsize = 16, tick_fontsize = 14,
                axis_weight = 2, dpi = 300):
    frames = get_data_frames(files)
    curves = get_all_curves(frames)
    newcurves = get_reflected_curves(curves, x_lim)
    medians, stdevs  = get_medians_and_stdevs(frames)
    p_values = [1] + length_ttests(frames)
    asterisks = p_to_asterisks(p_values)
    set_violin_params() #Hide all the boxes around the plots
    
    fig, axs = plt.subplots(1, len(newcurves), sharex=True, sharey=True, dpi = dpi)
    fig.set_figheight(figheight)
    fig.set_figwidth(len(x_labs)*2) # keeps the widths of the violins consistent between plots
    plt.ylim(0, y_lim)
    plt.xlim(0, x_lim)
    #plot all the curves
    for index, curve_set in enumerate(newcurves):    
        axs[index].plot(curve_set["means"], curve_set["lengths"], color = "black",
           linewidth = 0.8)
        axs[index].fill_betweenx(curve_set["lengths"], curve_set["lowers"], 
                             curve_set["uppers"], alpha = 0.2, color = "gray")
        axs[index].spines['bottom'].set_linewidth(axis_weight)
        axs[index].tick_params(axis='both', which='major', labelsize=tick_fontsize)
        #each violin plot is 2 plots back-to-back. Therefore only the even numbered
        #plots need the labels
        if index % 2 == 0:
            axs[index].errorbar(x_lim, medians[index//2], yerr = stdevs[index//2], 
               capsize = 6, color = "black", marker = '_')
            axs[index].set_xlabel(x_labs[index//2], fontsize = tick_fontsize)
            axs[index].xaxis.set_label_coords(1, -0.025)
        else:
            axs[index].errorbar(0, medians[index//2], yerr = stdevs[index//2], 
               capsize = 6, color = "black", marker = '_')
    #label the x axis
    fig.text(0.5, -0.05, x_title, ha='center', fontsize = axis_fontsize) 
    #label up the y axis on the first plot   
    axs[0].spines['left'].set_visible(True)
    axs[0].spines['left'].set_linewidth(axis_weight)
    axs[0].set_ylabel(y_title, fontsize = axis_fontsize)
    fig.subplots_adjust(hspace=0, wspace=0) #remove gaps between subplots
    asterisk_coords = get_asterisk_positions(axs, frames, y_lim)
    for i, asterisk in enumerate(asterisks):
        fig.text(asterisk_coords[0][i], ast_height,  asterisk, ha = "center", 
                 fontsize = 12)

def calculate_parameters(df):
    df["means"] = [np.mean(x) for x in df["values"]]
    df["stdevs"] = [np.std(x) for x in df["values"]]
    df["max"] = [max(x) for x in df["values"]]
    df["p_values"] = [st.ttest_1samp(x,1)[1] for x in df["values"]]
    df["asterisks"] = p_to_asterisks(df["p_values"])
    lengths = [len(x) for x in df["values"]]
    df["scatter_values"] = duplicate_values(df["conditions"], lengths)
    df["medians"] = [np.median(x) for x in df["values"]]
    return(df)

def transpose_nested_list(nested_list):
    '''if the nested+list were a dataframe, this returns a transposed data
    frame in the form of a nested_list'''
    transposed_frame = pd.DataFrame(nested_list).transpose()
    transposed_list = pd.Series.tolist(transposed_frame)
    return([strip_nans(x) for x in transposed_list])

def normalised_counts_from_file_names(file_names):
    '''import files of length data, return a nested list of the number of 
    filaments in each condition normalised to the first column'''
    frames = get_data_frames(file_names)
    counts = get_counts(frames)
    normalised_counts = [normalise_to_first(x) for x in counts]
    transposed_counts = transpose_nested_list(normalised_counts)
    return(transposed_counts)

def plot_bar(df, show_points = True, y_lim = 1.2,
             dpi = 600, figheight =5, figwidth = 12,
             x_title = "X", y_title = "Y", axis_fontsize = 12,
             tick_fontsize = 10, axis_weight = 2):
    set_bar_params()
    fig, ax = plt.subplots(nrows = 1, dpi = dpi)
    fig.set_figheight(figheight) 
    ax.set_ylabel(y_title, 
                 fontsize = axis_fontsize)
    #ax.set_xlabel(x_title, fontsize = axis_fontsize)
    fig.text(0.5, -0.05, x_title, ha='center', fontsize = axis_fontsize)
    plt.setp(ax.spines.values(), linewidth=axis_weight)
    plt.tick_params(axis='both', which='major', labelsize=tick_fontsize)    
    plt.ylim(0, y_lim)   
    fig.set_figwidth(len(df["means"])*2)
    plt.xlim(-0.5, len(df["means"]) - 0.5)
    ax.bar(df["conditions"], df["means"], yerr = df["stdevs"], capsize = 10,
                  color = "none", edgecolor = "black", linewidth = 2)
    asterisk_xs = range(0, len(df["conditions"]))
    #plot individual points
    if show_points:
       ax.scatter(combine_lists(df["scatter_values"]), 
                  combine_lists(df["values"]), color = "none", edgecolor='black')
    #plot significance asterisks
    for i, asterisk in enumerate(df["asterisks"]):
        ax.text(asterisk_xs[i], max(df["max"][1:len(df["max"])]) + 0.1, 
                asterisk, ha = "center", fontsize = 12)

def plot_scatter(df, show_points = True, y_lim = 1.2,
             dpi = 600, figheight =5, figwidth = 12,
             x_title = "X", y_title = "Y", axis_fontsize = 12,
             tick_fontsize = 10, axis_weight = 2, extra_x_space = 1):
    set_bar_params()
    df["conditions"] = [float(x) for x in df["conditions"]]
    df["scatter_values"] = [[float(x) for x in z] for z in df["scatter_values"]]
    fig, ax = plt.subplots(nrows = 1, dpi = dpi)
    fig.set_figheight(figheight) 
    ax.set_ylabel("Filament concentration\n(normalised to untreated)", 
                  fontsize = axis_fontsize)
    #ax.set_xlabel(x_title, fontsize = axis_fontsize)
    fig.text(0.5, -0.05, x_title, ha='center', fontsize = axis_fontsize)
    plt.setp(ax.spines.values(), linewidth=axis_weight)
    plt.tick_params(axis='both', which='major', labelsize=tick_fontsize)
    plt.tick_params(axis = "x", length = 1)    
    plt.ylim(0, y_lim)   
    #plot scatter plots if x axis is continuous, and bar plots if not
    fig.set_figwidth(figwidth)
    plt.xlim(0, max(df["conditions"]) + extra_x_space)
    ax.errorbar(df["conditions"], df["means"], yerr = df["stdevs"], marker = "_", 
                           markersize='15', capsize = 10, linewidth = 2, 
                           color = "black", linestyle='None')
    z = np.polyfit(df["conditions"], df["means"], 1)
    p = np.poly1d(z)
    plt.plot(df["conditions"], p(df["conditions"]),"--", color = "black")
    asterisk_xs = df["conditions"]
    for i, asterisk in enumerate(df["asterisks"]):
       ax.text(asterisk_xs[i], max(df["max"][1:len(df["max"])]) + 0.1, 
            asterisk, ha = "center", fontsize = 12)
       
def plot_hist(counts, minimum, maximum, interval, xlab, ylab,
              dpi = 600, axis_fontsize = 12, tick_fontsize = 10,
              figheight = 8, figwidth = 10, y_lim = 12):
    set_bar_params()
    fig, ax = plt.subplots(nrows = 1, dpi = dpi)
    fig.set_figheight(figheight)
    fig.set_figwidth(figwidth)
    ax.hist(counts, bins = np.arange(minimum, maximum, interval), #arange to align xticks with bins
         edgecolor = "black", color = "white",
         linewidth = 2)
    ax.set_xlabel(xlab, fontsize = axis_fontsize)
    ax.set_ylabel(ylab, fontsize = axis_fontsize)
    ax.tick_params(axis='both', which='major', labelsize=tick_fontsize)
    plt.setp(ax.spines.values(), linewidth=2)
    plt.ylim(0, y_lim)
    ax.spines["top"].set_color("none")
    ax.spines["right"].set_color("none")