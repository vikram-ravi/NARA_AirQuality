# -*- coding: utf-8 -*-
"""
Created on Fri Oct 09 12:45:26 2015

@author: vik
# description - plots stacked bar plots of PM emissions based on NEI 2011
"""

# import important libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
#%%
start_time = time.time()

# directory where all NEI files are placed
indir = "C:/Users/vik/Documents/2011NEIv1_fires/"

# define months, statecodes, FIPS and statenames
months     = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
stateCode  = ['04', '06', '08', '16', '30', '32', '35', '38', '41', '46', '49', '53', '56']
#stateName  = {'04':'AZ', '06':'CA', '08':'CO', '16':'ID', '30':'MT', '32':'NV', '35':'NM', '38':'ND', '41':'OR', '46':'SD', '49':'UT', '53':'WA', '56':'WY'}
stateName  = {'04':'Arizona', '06':'California', '08':'Colorado', '16':'Idaho', '30':'Montana', '32':'Nevada', '35':'New Mexico', '38':'North Dacota', '41':'Oregon', '46':'South Dacota', '49':'Utah', '53':'Washington', '56':'Wyoming'}
fireType   = {2811015000:'Prescribed Fire', 2810001000:'WildFire'}
#store the file names
infiles = []
for mt in months:
    data_file = indir + "ptday_ptfire_" + mt + "_2011_FLA_Adj_txt_13aug2013_v0_orl.txt"
    infiles.append(data_file)
    
# names for indexing the Dataframe and datatype for each column
col_names = ['FIPS', 'FIREID', 'LOCID', 'SCC', 'DATA', 'DATE', 'DATAVALUE', 'BEGHOUR', 'ENDHOUR']

# now read the data
tmp_data = [] # an empty list where the data will be stored
for infile in infiles:
    tmp_df = pd.read_csv(infile, comment = '#', names = col_names, converters={'FIPS': lambda x : str(x)})
    tmp_df['DATE'] = pd.to_datetime(pd.Series(tmp_df['DATE']), format = '%m/%d/%y')
    tmp_data.append(tmp_df)
    
# concatenate all the dataframes
data = pd.concat([tmp_data[i] for i in np.arange(len(tmp_data))], join='outer') # do a union i.e. keep all the values from all the tmp DFs

# create a dataframe with only PM2.5 data and also create an empty dataframe for plotting later
data2 = data.loc[(data.DATA == 'PM2_5'), col_names]
pm_df = pd.DataFrame(index=np.arange(1,13), columns=stateName.values())

#%%
# below, all the calculation and plotting is done 
for scc in [2811015000, 2810001000]: #set(data2.SCC):
    data3 = data2.loc[(data2.SCC == scc), col_names]
    data3['State'] = data3['FIPS'].str[:2]
#    new_cols = col_names.append('State')
    data4 = data3.set_index('DATE')
    new_cols = data4.columns
    for m in np.arange(1,13):
        data5 = data4.loc[data4.index.month==m, new_cols]
        for fips in stateCode:
            data6 = data5.loc[data5.State==fips, 'DATAVALUE']
            pm_df.ix[m, stateName[fips]] = data6.sum()
    # plotting begins
    fig, ax = plt.subplots(figsize=(15,10))
    pm_df.plot(ax=ax, kind='bar', stacked=True, colormap="Set1", legend='reverse', grid=True, fontsize=20)
    ax.set_xticklabels(pm_df.index, rotation=0)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1], loc='best', fontsize=15)
    plt.title('PM$_{2.5}$ Emissions from '+ fireType[scc], fontsize=20, weight='bold')
    plt.xlabel('Month of 2011', fontsize=20, weight='bold')
    plt.ylabel('Tons', fontsize=20, weight='bold')
    plt.savefig(indir+"/plots/"+ fireType[scc] + '.png',  pad_inches=0)   # save the figure to file

