# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 11:27:38 2018

@author: Mikkel
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import csv
import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.sandbox.stats.multicomp import multipletests

subjects = 4

def read_csv(fname):
   prefix = ""
   with open(prefix+fname, 'rt') as f:
       reader = csv.reader(f, delimiter = ",")
       data = []
       for row in reader:
           row2 = []
           for a in row:
               if(a.isdigit()):
                   row2.append(float(a))
               else:
                   row2.append(a)
           data.append(row2)
       return (data)

col = ['Participant','Trial','Condition','Time','TargetDistance','Duration','Mis-Clicks','TargetLocation','OrderLabel']
data = read_csv("exper1c.csv")

data = (pd.DataFrame(data, columns = col))
#
#data = data.melt(data, id_vars=['Condition'], var_name=['Condition'], value_vars=['Duration'])
##
#
data2 = data.groupby(['Condition','Participant'])['Duration'].mean().reset_index()

sns.barplot(x='Condition', y='Duration', data=data)
plt.show()
#
#sns.barplot(x='TargetLocation', y='Duration', data=data)
#plt.show()


#sns.barplot(x='Condition', y='Mis-Clicks', data=data, hue='TargetLocation')

#print(data2)

normal = data2[data2['Condition'] == 'normal']['Duration']
bubble = data2[data2['Condition'] == 'bubble']['Duration']
fixBubble = data2[data2['Condition'] == 'fixBubble']['Duration']
halo = data2[data2['Condition'] == 'halo']['Duration']
fixHalo = data2[data2['Condition'] == 'fixHalo']['Duration']

ttestBubble = stats.ttest_rel(normal, bubble)
ttestFixBubble = stats.ttest_rel(normal, fixBubble)
ttestHalo = stats.ttest_rel(normal, halo)
ttestFixHalo = stats.ttest_rel(normal, fixHalo)
    
print("T-test for Condition, Bubble")  
print(ttestBubble)
print()
print("T-test for OrderLabel")
one = data[data['OrderLabel'] == 1.0 ]['Duration']
two = data[data['OrderLabel'] == 4.0 ]['Duration']
print(stats.ttest_rel(one, two))

print()

model = ols('Duration ~ C(Condition)', data=data2).fit()
table = sm.stats.anova_lm(model, typ=2)
print(table)


newresult = (multipletests([ttestBubble.pvalue, ttestFixBubble.pvalue, ttestHalo.pvalue, ttestFixHalo.pvalue], 0.05, 'bonferroni'))
print(newresult)

# 
##We want 4, 5*60 arrays of durations
#def get_ind(data, dInd):
#    proc_data = np.ndarray(shape = (subjects,5,60), dtype = 'float')
#    indCount = np.zeros((subjects,5), dtype = "int")
#    for r in data:
#        if(not(r[0].isalpha())):
#            i1 = int(float(r[0]))-1
#        else:
#            continue
#        if(r[2] == "bubble"):
#            i2 = 0
#        if(r[2] == "fixBubble"):
#            i2 = 1
#        if(r[2] == "halo"):
#            i2 = 2
#        if(r[2] == "fixHalo"):
#            i2 = 3
#        if(r[2] == "normal"):
#            i2 = 4
#        cInd = indCount[i1][i2]
#        proc_data[i1][i2][cInd] = r[dInd]
#        indCount[i1][i2] += 1
#    return proc_data
#
#dur_data = get_ind(data,5)
#err_data = get_ind(data,6)
#dist_data = get_ind(data,4)
#
#def get_avs(data):
#    x,y,z = data.shape
#    avs = np.zeros((x,y))
#    for i in range(subjects):
#        for j in range(5):
#            avs[i][j] = np.average(data[i][j])
#    return avs
#
#def get_tots(data):
#    x,y,z = data.shape
#    avs = np.zeros((x,y))
#    for i in range(subjects):
#        for j in range(5):
#            avs[i][j] = np.sum(data[i][j])
#    return avs
#
#dur_avg = get_avs(dur_data)
#err_tot = get_tots(err_data)
#dist_avg = get_avs(dist_data)
#
#def find_minmax_2d(data):
#    mins = []
#    maxs = []
#    for i in data:
#        mins.append(min(i))
#        maxs.append(max(i))
#    return (min(mins), max(maxs))
#
#dist_minmax = find_minmax_2d(dist_avg)
#
#dur_avg_t = dur_avg.T
#err_tot_t = err_tot.T
#
#def show_data_per_participant(data, name):
#    fig = plt.figure()
#    x = ["Bubble", "Fix Bubble", "Halo", "Fix Halo", "Normal"]
#    x_pos = np.arange(len(x))
#    f, axs = plt.subplots(2,2, sharey = True)
#    for i in range(2):
#        for j in range(2):
#            axs[i][j].bar(x_pos, data[i+j], align='center', alpha=0.75)
#            axs[i][j].set_xticks(x_pos)
#            axs[i][j].set_xticklabels(x)
#    f.suptitle(name)
#
#    f.savefig(name+".png", bbox_inches='tight')
#    
#show_data_per_participant(dur_avg, "Average Duration for each Participant")
#show_data_per_participant(err_tot, "Total Error for each Participant")
#
#def show_data_overall(data, name):
#    fig = plt.figure()
#    x = ["Bubble", "Fix Bubble", "Halo", "Fix Halo", "Normal"]
#    x_pos = np.arange(len(x))
#    plt.bar(x_pos,data, align='center', alpha=0.75)
#    plt.xticks(x_pos,x)
#    plt.suptitle(name)
#    plt.savefig(name+".png", bbox_inches='tight')
#
#def get_overall(data):
#    overalls = []
#    for r in data:
#        overalls.append(np.average(r))
#    return overalls
#
#overall_dur_data = get_overall(dur_avg_t)
#overall_err_data = get_overall(err_tot_t)
#
#show_data_overall(overall_dur_data, "Average Duration over all Participants")
#show_data_overall(overall_err_data, "Average Errors over all Participants")
#print("done")
#            
#
#
#
