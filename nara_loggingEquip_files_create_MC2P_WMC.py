# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 14:17:31 2016

@author: vik
"""

import pandas as pd
import matplotlib.pyplot as plt
from fortranformat import FortranRecordWriter
#%%
inFile = "C:/Users/vik/Desktop/County Input Files/nr_logging_WMC_Spokane_EFperVehicleByEquipment_data.xlsx"

df = pd.read_excel(inFile)
df_shredder = df[df['description'] == u'Shredders > 6 HP']
df_skidder  = df[df['description'] == u'Forest Eqp - Feller/Bunch/Skidder']

df_shredder_mean = df_shredder.groupby(by='pollutantID').mean()
df_skidder_mean  = df_skidder.groupby(by='pollutantID').mean()
df_shredder_mean['pollutantID'] = df_shredder_mean.index
df_skidder_mean['pollutantID']  = df_skidder_mean.index
#%%

spokaneFIA = "C:/Users/vik/Documents/Projects/NARA/NARA_files_4_loggingEquip/Spokane_FIA_distribution.csv"
cosmoFIA   = "C:/Users/vik/Documents/Projects/NARA/NARA_files_4_loggingEquip/FIA_pts_Cosmo_marginal.csv"
df_spokane = pd.read_csv(spokaneFIA)
df_cosmo   = pd.read_csv(cosmoFIA)
df_spokane.rename(columns={'Long':'Longitude', 'Lat':'Latitude'}, inplace=True)
df_cosmo.rename(columns={'Lon':'Longitude', 'Lat':'Latitude'}, inplace=True)
df_loggingSites = pd.concat([df_spokane, df_cosmo], join='inner', ignore_index=True) 
df_emissions = df_loggingSites.loc[:,['Latitude', 'Longitude', 'NAME', 'FIA_pt']]
#%%
grams_to_tons = 1.1023113e-06

df_emissions.ix[:, 'acetaldehyde']   = (df_shredder_mean.ix[26, 'emissionRate'] + df_skidder_mean.ix[26, 'emissionRate'])*365*grams_to_tons
df_emissions.ix[:, 'acrolein']       = (df_shredder_mean.ix[27, 'emissionRate'] + df_skidder_mean.ix[27, 'emissionRate'])*365*grams_to_tons
df_emissions.ix[:, 'arsenic']        = (df_shredder_mean.ix[63, 'emissionRate'] + df_skidder_mean.ix[63, 'emissionRate'])*365*grams_to_tons
df_emissions.ix[:, 'benzene']        = (df_shredder_mean.ix[20, 'emissionRate'] + df_skidder_mean.ix[20, 'emissionRate'])*365*grams_to_tons
df_emissions.ix[:, 'butadiene']      = (df_shredder_mean.ix[24, 'emissionRate'] + df_skidder_mean.ix[24, 'emissionRate'])*365*grams_to_tons
df_emissions.ix[:, 'chromium']       = (df_shredder_mean.ix[65, 'emissionRate'] + df_skidder_mean.ix[65, 'emissionRate'])*365*grams_to_tons
df_emissions.ix[:, 'carbonMonoxide'] = (df_shredder_mean.ix[2, 'emissionRate']  + df_skidder_mean.ix[2, 'emissionRate'])*365*grams_to_tons
df_emissions.ix[:, 'ethylBenzene']   = (df_shredder_mean.ix[41, 'emissionRate'] + df_skidder_mean.ix[41, 'emissionRate'])*365*grams_to_tons
df_emissions.ix[:, 'formaldehyde']   = (df_shredder_mean.ix[25, 'emissionRate'] + df_skidder_mean.ix[25, 'emissionRate'])*365*grams_to_tons
df_emissions.ix[:, 'manganese']      = (df_shredder_mean.ix[66, 'emissionRate'] + df_skidder_mean.ix[66, 'emissionRate'])*365*grams_to_tons
df_emissions.ix[:, 'mercury']        = (df_shredder_mean.ix[60, 'emissionRate'] + df_skidder_mean.ix[60, 'emissionRate'] + df_shredder_mean.ix[61, 'emissionRate'] + df_skidder_mean.ix[61, 'emissionRate'])*365*grams_to_tons
df_emissions.ix[:, 'napthalene']     = (df_shredder_mean.ix[185, 'emissionRate']+ df_skidder_mean.ix[185, 'emissionRate'])*365*grams_to_tons
df_emissions.ix[:, 'ammonia']        = (df_shredder_mean.ix[30, 'emissionRate'] + df_skidder_mean.ix[30, 'emissionRate'])*365*grams_to_tons
df_emissions.ix[:, 'nitrogenOxides'] = (df_shredder_mean.ix[3, 'emissionRate']  + df_skidder_mean.ix[3, 'emissionRate'])*365*grams_to_tons
df_emissions.ix[:, 'PM10']           = (df_shredder_mean.ix[100, 'emissionRate']+ df_skidder_mean.ix[100, 'emissionRate'])*365*grams_to_tons
df_emissions.ix[:, 'PM2.5']          = (df_shredder_mean.ix[110, 'emissionRate']+ df_skidder_mean.ix[110, 'emissionRate'])*365*grams_to_tons
df_emissions.ix[:, 'sulfurDioxide']  = (df_shredder_mean.ix[31, 'emissionRate'] + df_skidder_mean.ix[31, 'emissionRate'])*365*grams_to_tons
df_emissions.ix[:, 'toluene']        = (df_shredder_mean.ix[45, 'emissionRate'] + df_skidder_mean.ix[45, 'emissionRate'])*365*grams_to_tons
df_emissions.ix[:, 'volatileOC']     = (df_shredder_mean.ix[87, 'emissionRate'] + df_skidder_mean.ix[87, 'emissionRate'])*365*grams_to_tons
df_emissions.ix[:, 'xylene']         = (df_shredder_mean.ix[46, 'emissionRate'] + df_skidder_mean.ix[46, 'emissionRate'])*365*grams_to_tons
df_emissions.ix[:, 'polyAroHydro']   = (df_shredder_mean.ix[68, 'emissionRate'] + df_shredder_mean.ix[168, 'emissionRate'] + df_skidder_mean.ix[68, 'emissionRate'] + df_skidder_mean.ix[168, 'emissionRate'] + \
                                        df_shredder_mean.ix[69, 'emissionRate'] + df_shredder_mean.ix[169, 'emissionRate'] + df_skidder_mean.ix[69, 'emissionRate'] + df_skidder_mean.ix[169, 'emissionRate'] + \
                                        df_shredder_mean.ix[70, 'emissionRate'] + df_shredder_mean.ix[170, 'emissionRate'] + df_skidder_mean.ix[70, 'emissionRate'] + df_skidder_mean.ix[170, 'emissionRate'] + \
                                        df_shredder_mean.ix[71, 'emissionRate'] + df_shredder_mean.ix[171, 'emissionRate'] + df_skidder_mean.ix[71, 'emissionRate'] + df_skidder_mean.ix[171, 'emissionRate'] + \
                                        df_shredder_mean.ix[72, 'emissionRate'] + df_shredder_mean.ix[172, 'emissionRate'] + df_skidder_mean.ix[72, 'emissionRate'] + df_skidder_mean.ix[172, 'emissionRate'] + \
                                        df_shredder_mean.ix[73, 'emissionRate'] + df_shredder_mean.ix[173, 'emissionRate'] + df_skidder_mean.ix[73, 'emissionRate'] + df_skidder_mean.ix[173, 'emissionRate'] + \
                                        df_shredder_mean.ix[74, 'emissionRate'] + df_shredder_mean.ix[174, 'emissionRate'] + df_skidder_mean.ix[74, 'emissionRate'] + df_skidder_mean.ix[174, 'emissionRate'] + \
                                        df_shredder_mean.ix[75, 'emissionRate'] + df_shredder_mean.ix[175, 'emissionRate'] + df_skidder_mean.ix[75, 'emissionRate'] + df_skidder_mean.ix[175, 'emissionRate'] + \
                                        df_shredder_mean.ix[76, 'emissionRate'] + df_shredder_mean.ix[176, 'emissionRate'] + df_skidder_mean.ix[76, 'emissionRate'] + df_skidder_mean.ix[176, 'emissionRate'] + \
                                        df_shredder_mean.ix[77, 'emissionRate'] + df_shredder_mean.ix[177, 'emissionRate'] + df_skidder_mean.ix[77, 'emissionRate'] + df_skidder_mean.ix[177, 'emissionRate'] + \
                                        df_shredder_mean.ix[78, 'emissionRate'] + df_shredder_mean.ix[178, 'emissionRate'] + df_skidder_mean.ix[78, 'emissionRate'] + df_skidder_mean.ix[178, 'emissionRate'] + \
                                        df_shredder_mean.ix[81, 'emissionRate'] + df_shredder_mean.ix[181, 'emissionRate'] + df_skidder_mean.ix[81, 'emissionRate'] + df_skidder_mean.ix[181, 'emissionRate'] + \
                                        df_shredder_mean.ix[82, 'emissionRate'] + df_shredder_mean.ix[182, 'emissionRate'] + df_skidder_mean.ix[82, 'emissionRate'] + df_skidder_mean.ix[182, 'emissionRate'] + \
                                        df_shredder_mean.ix[83, 'emissionRate'] + df_shredder_mean.ix[183, 'emissionRate'] + df_skidder_mean.ix[83, 'emissionRate'] + df_skidder_mean.ix[183, 'emissionRate'] + \
                                        df_shredder_mean.ix[84, 'emissionRate'] + df_shredder_mean.ix[184, 'emissionRate'] + df_skidder_mean.ix[84, 'emissionRate'] + df_skidder_mean.ix[184, 'emissionRate'] + \
                                        df_shredder_mean.ix[23, 'emissionRate'] + df_skidder_mean.ix[23, 'emissionRate'] )*365*grams_to_tons
#%%
def get_state_countyid(county):
    named_cyst_info = {'ASOTIN'   :{'STATE':53, 'COUNTYID':3} ,     'BENEWAH'     :{'STATE':16, 'COUNTYID':9} ,       'BONNER'      :{'STATE':16, 'COUNTYID':17},
                       'BOUNDARY' :{'STATE':16, 'COUNTYID':21},     'CLEARWATER'  :{'STATE':16, 'COUNTYID':35},       'Clallam'     :{'STATE':53, 'COUNTYID':9} ,
                       'Clatsop'  :{'STATE':41, 'COUNTYID':7} ,     'Columbia'    :{'STATE':41, 'COUNTYID':9} ,       'Cowlitz'     :{'STATE':53, 'COUNTYID':15},
                       'FERRY'    :{'STATE':53, 'COUNTYID':19},     'Grays Harbor':{'STATE':53, 'COUNTYID':27},       'IDAHO'       :{'STATE':16, 'COUNTYID':49},
                       'Jefferson':{'STATE':53, 'COUNTYID':31},     'KOOTENAI'    :{'STATE':16, 'COUNTYID':55},       'King'        :{'STATE':53, 'COUNTYID':33},
                       'Kitsap'   :{'STATE':53, 'COUNTYID':35},     'LATAH'       :{'STATE':16, 'COUNTYID':57},       'LEWIS'       :{'STATE':16, 'COUNTYID':61},
                       'LINCOLN'  :{'STATE':30, 'COUNTYID':53},     'Lewis'       :{'STATE':53, 'COUNTYID':41},       'Mason'       :{'STATE':53, 'COUNTYID':45},
                       'NEZ PERCE':{'STATE':16, 'COUNTYID':69},     'OKANOGAN'    :{'STATE':53, 'COUNTYID':47},       'PEND OREILLE':{'STATE':53, 'COUNTYID':51},
                       'Pacific'  :{'STATE':53, 'COUNTYID':49},     'Pierce'      :{'STATE':53, 'COUNTYID':53},       'SANDERS'     :{'STATE':30, 'COUNTYID':89},
                       'SHOSHONE' :{'STATE':16, 'COUNTYID':79},     'SPOKANE'     :{'STATE':53, 'COUNTYID':63},       'STEVENS'     :{'STATE':53, 'COUNTYID':65},
                       'Thurston' :{'STATE':53, 'COUNTYID':67},     'Tillamook'   :{'STATE':41, 'COUNTYID':57},       'WHITMAN'     :{'STATE':53, 'COUNTYID':75},
                       'Wahkiakum':{'STATE':53, 'COUNTYID':69}}
    sid = named_cyst_info[county]['STATE']
    cid = named_cyst_info[county]['COUNTYID']
    return sid, cid
#%%    
outputFile = "C:/Users/vik/Documents/Projects/NARA/NARA_files_4_loggingEquip/pt_NARA_logging_tpy.txt"
outFile = open(outputFile, 'w')
lineOut = '%s\n'*6%("#IDA",
                    "#TYPE      Point Source Inventory",
                    "#COUNTRY   US",
                    "#YEAR      2011",
                    "#DESC      NARA Logging Point Source Inventory",
                    "#DATA      ACETALDEHYD ACROLEIN ARSENIC BENZENE CHROMIUM CO DICHLOROMET ETHYLBENZEN FORMALDEHYD LEAD MANGANESE NAPHTHALENE NH3 NOX PAH PM10 PM2_5 SO2 TOLUENE VOC XYLENE")
outFile.write(lineOut)
to_3_digit_cid = lambda x: ('0'*(3-len(x))+str(x) if len(x)<3 else x)
for idx in df_emissions.index:
    county_nm= df_emissions.ix[idx, 'NAME']
    sid, cid = get_state_countyid(county_nm)
    state_id = sid
    raw_CYID = cid
    county_id= to_3_digit_cid(str(raw_CYID))
    plant_id = str(int(df_emissions.ix[idx, 'FIA_pt']))
    plant_nm = county_nm+' County, FIA point No.-'+str(int(df_emissions.ix[idx, 'FIA_pt'])) + '  '
    scc_code = '2270007000'
    stkHeight= 0
    stkDia   = 0
    stkGasTmp= 0
    stkFlowRt= 0
    stkGasVel= 0
    sic_code = 0
    latitude = df_emissions.ix[idx, 'Latitude']
    longitude= -1*df_emissions.ix[idx, 'Longitude']
    emis1    = df_emissions.ix[idx, 'acetaldehyde']
    emis2    = df_emissions.ix[idx, 'acrolein']
    emis3    = df_emissions.ix[idx, 'arsenic']
    emis4    = df_emissions.ix[idx, 'benzene']
    emis5    = df_emissions.ix[idx, 'chromium']
    emis6    = df_emissions.ix[idx, 'carbonMonoxide']
    emis7    = 0
    emis8    = df_emissions.ix[idx, 'ethylBenzene']
    emis9    = df_emissions.ix[idx, 'formaldehyde']
    emis10   = 0
    emis11   = df_emissions.ix[idx, 'manganese']
    emis12   = df_emissions.ix[idx, 'napthalene']
    emis13   = df_emissions.ix[idx, 'ammonia']
    emis14   = df_emissions.ix[idx, 'nitrogenOxides']
    emis15   = df_emissions.ix[idx, 'polyAroHydro']
    emis16   = df_emissions.ix[idx, 'PM10']
    emis17   = df_emissions.ix[idx, 'PM2.5']
    emis18   = df_emissions.ix[idx, 'sulfurDioxide']
    emis19   = df_emissions.ix[idx, 'toluene']
    emis20   = df_emissions.ix[idx, 'volatileOC']    
    emis21   = df_emissions.ix[idx, 'xylene']    
    line     = FortranRecordWriter('(I2, A3, A15, 41X, A40, A10, 8X, I4, F6.2, I4, 10X, F9.2, 74X, I4, F9.5, F9.5, 1X, 20(E13.7, 39X), E13.7, 39X)')
#    line     = FortranRecordWriter('(I2, A3, A15, 81X, A10, 8X, I4, F6.2, I4, 10X, F9.2, 74X, I4, F9.5, F9.5, 1X, E13.7, 39X, E13.7, 39X,E13.7, 39X, E13.7, 39X, E13.7, 39X,E13.7, 39X, E13.7, 39X,E13.7, 39X,E13.7, 39X, E13.7, 39X,E13.7, 39X,E13.7, 39X, E13.7, 39X,E13.7, 39X,E13.7, 39X, E13.7, 39X,E13.7, 39X,E13.7, 39X, E13.7, 39X,E13.7, 39X,E13.7, 39X, E13.7, 39X,E13.7, 39X,E13.7, 39X, E13.7, 39X,E13.7, 39X,E13.7, 39X, E13.7, 39X,E13.7, 39X,E13.7, 39X, E13.7, 39X,E13.7, 39X)\n')
    lineOut  = line.write([state_id, county_id, plant_id, plant_nm, scc_code, stkHeight, stkDia, stkGasTmp, stkGasVel, sic_code,\
                                latitude, longitude, emis1, emis2, emis3, emis4, emis5, emis6, emis7, emis8, emis9, emis10, emis11, \
                                emis12, emis13, emis14, emis15, emis16, emis17, emis18, emis19, emis20, emis21])
    lineOut = lineOut + ' '*39 + '\n'
    outFile.write(lineOut)
outFile.close()
#%% 
# get total annual emissions   
for idx in df_emissions.index:
    lon = df_emissions.ix[idx, 'Longitude']
    if lon > -120:
        df_emissions.ix[idx, 'Region']= 'WMC'
    else:
        df_emissions.ix[idx, 'Region']= 'MC2P'
df_emis_WMC  = df_emissions.loc[df_emissions['Region']=="WMC"]    
df_emis_MC2P = df_emissions.loc[df_emissions['Region']=="MC2P"]    

regionName = {0:'MC2P', 1:'WMC'}
for i, dfs in enumerate((df_emis_MC2P, df_emis_WMC)):
    print '\n%10s %s %10s'%('-'*10, regionName[i], '-'*10)
    for poll in ['carbonMonoxide', 'nitrogenOxides', 'ammonia', 'volatileOC', 'sulfurDioxide', 'PM2.5']:
        print '%-15s %s' %(poll, dfs[poll].sum())