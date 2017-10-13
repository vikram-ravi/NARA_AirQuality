# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 14:17:31 2016
This program writes file in a format required for SMOKE v2 IDA format for point source
from a spreadsheet
@author: vik
"""

import pandas as pd
from fortranformat import FortranRecordWriter
#%%
inFile = "C:/Users/vik/Documents/Projects/NARA/NARA_files_4_Biorefinery/NARA_Bioref_Emissions_SMOKE.xlsx"

df_emissions = pd.read_excel(inFile)
#%%    
outputFile = "C:/Users/vik/Documents/Projects/NARA/NARA_files_4_Biorefinery/pt_NARA_biorefinery_tpy.txt"
outFile = open(outputFile, 'w')
lineOut = '%s\n'*6%("#IDA",
                    "#TYPE      Point Source Inventory",
                    "#COUNTRY   US",
                    "#YEAR      2011",
                    "#DESC      NARA Biorefinery Point Source Inventory",
                    "#DATA      ACETALDEHYD ACROLEIN ARSENIC BENZENE CHROMIUM CO DICHLOROMET ETHYLBENZEN FORMALDEHYD LEAD MANGANESE NAPHTHALENE NH3 NOX PAH PM10 PM2_5 SO2 TOLUENE VOC XYLENE")
outFile.write(lineOut)
for idx in df_emissions.index:
    st_cty_id= df_emissions.ix[idx, 'FIPS_county_code'].astype(str)
    state_id = st_cty_id[0:2]
    county_id= st_cty_id[2:]
    plant_id = df_emissions.ix[idx, 'source_number']
    plant_nm = df_emissions.ix[idx, 'facility_name']
    scc_code = df_emissions.ix[idx, 'SCC_code']
    stkHeight= df_emissions.ix[idx, 'stk_height']
    stkDia   = df_emissions.ix[idx, 'stk_diameter']
    stkGasTmp= df_emissions.ix[idx, 'stk_temperature']
    stkFlowRt= df_emissions.ix[idx, 'stk_ACFS']
    stkGasVel= df_emissions.ix[idx, 'stk_FPS']
    sic_code = df_emissions.ix[idx, 'SIC']
    latitude = df_emissions.ix[idx, 'rp_lat']
    longitude= df_emissions.ix[idx, 'rp_lon']
    emis1    = df_emissions.ix[idx, 'ACETALDEHYD']
    emis2    = df_emissions.ix[idx, ' ACROLEIN']
    emis3    = df_emissions.ix[idx, ' ARSENIC ']
    emis4    = df_emissions.ix[idx, 'BENZENE ']
    emis5    = df_emissions.ix[idx, 'CHROMIUM']
    emis6    = df_emissions.ix[idx, ' CO ']
    emis7    = 0
    emis8    = df_emissions.ix[idx, 'ETHYLBENZEN ']
    emis9    = df_emissions.ix[idx, 'FORMALDEHYD ']
    emis10   = df_emissions.ix[idx, 'LEAD ']
    emis11   = df_emissions.ix[idx, 'MANGANESE']
    emis12   = df_emissions.ix[idx, 'NAPHTHALENE']
    emis13   = df_emissions.ix[idx, ' NH3 ']
    emis14   = df_emissions.ix[idx, 'NOX ']
    emis15   = df_emissions.ix[idx, 'PAH']
    emis16   = df_emissions.ix[idx, ' PM10']
    emis17   = df_emissions.ix[idx, ' PM2_5 ']
    emis18   = df_emissions.ix[idx, 'SO2']
    emis19   = df_emissions.ix[idx, ' TOLUENE ']
    emis20   = df_emissions.ix[idx, 'VOC']    
    emis21   = df_emissions.ix[idx, ' XYLENE']    
    line     = FortranRecordWriter('(I2, A3, A15, 41X, A40, A10, 8X, I4, F6.2, I4, 10X, F9.2, 74X, I4, F9.5, F9.5, 1X, 20(E13.7, 39X), E13.7, 39X)')
#    line     = FortranRecordWriter('(I2, A3, A15, 81X, A10, 8X, I4, F6.2, I4, 10X, F9.2, 74X, I4, F9.5, F9.5, 1X, E13.7, 39X, E13.7, 39X,E13.7, 39X, E13.7, 39X, E13.7, 39X,E13.7, 39X, E13.7, 39X,E13.7, 39X,E13.7, 39X, E13.7, 39X,E13.7, 39X,E13.7, 39X, E13.7, 39X,E13.7, 39X,E13.7, 39X, E13.7, 39X,E13.7, 39X,E13.7, 39X, E13.7, 39X,E13.7, 39X,E13.7, 39X, E13.7, 39X,E13.7, 39X,E13.7, 39X, E13.7, 39X,E13.7, 39X,E13.7, 39X, E13.7, 39X,E13.7, 39X,E13.7, 39X, E13.7, 39X,E13.7, 39X)\n')
    lineOut  = line.write([int(state_id), county_id, plant_id, plant_nm, scc_code, stkHeight, stkDia, stkGasTmp, stkGasVel, sic_code,\
                                latitude, longitude, emis1, emis2, emis3, emis4, emis5, emis6, emis7, emis8, emis9, emis10, emis11, \
                                emis12, emis13, emis14, emis15, emis16, emis17, emis18, emis19, emis20, emis21])
    lineOut = lineOut + ' '*39 + '\n'
    outFile.write(lineOut)
outFile.close()
#%%    
outputFile = "C:/Users/vik/Documents/Projects/NARA/NARA_files_4_Biorefinery/pt_NARA_biorefinery_2xEmis_tpy.txt"
outFile = open(outputFile, 'w')
lineOut = '%s\n'*6%("#IDA",
                    "#TYPE      Point Source Inventory",
                    "#COUNTRY   US",
                    "#YEAR      2011",
                    "#DESC      NARA Biorefinery Point Source Inventory with twice original emissions",
                    "#DATA      ACETALDEHYD ACROLEIN ARSENIC BENZENE CHROMIUM CO DICHLOROMET ETHYLBENZEN FORMALDEHYD LEAD MANGANESE NAPHTHALENE NH3 NOX PAH PM10 PM2_5 SO2 TOLUENE VOC XYLENE")
outFile.write(lineOut)
for idx in df_emissions.index:
    st_cty_id= df_emissions.ix[idx, 'FIPS_county_code'].astype(str)
    state_id = st_cty_id[0:2]
    county_id= st_cty_id[2:]
    plant_id = df_emissions.ix[idx, 'source_number']
    plant_nm = df_emissions.ix[idx, 'facility_name']
    scc_code = df_emissions.ix[idx, 'SCC_code']
    stkHeight= df_emissions.ix[idx, 'stk_height']
    stkDia   = df_emissions.ix[idx, 'stk_diameter']
    stkGasTmp= df_emissions.ix[idx, 'stk_temperature']
    stkFlowRt= df_emissions.ix[idx, 'stk_ACFS']
    stkGasVel= df_emissions.ix[idx, 'stk_FPS']
    sic_code = df_emissions.ix[idx, 'SIC']
    latitude = df_emissions.ix[idx, 'rp_lat']
    longitude= df_emissions.ix[idx, 'rp_lon']
    emis1    = 2.0*df_emissions.ix[idx, 'ACETALDEHYD']
    emis2    = 2.0*df_emissions.ix[idx, ' ACROLEIN']
    emis3    = 2.0*df_emissions.ix[idx, ' ARSENIC ']
    emis4    = 2.0*df_emissions.ix[idx, 'BENZENE ']
    emis5    = 2.0*df_emissions.ix[idx, 'CHROMIUM']
    emis6    = 2.0*df_emissions.ix[idx, ' CO ']
    emis7    = 0
    emis8    = 2.0*df_emissions.ix[idx, 'ETHYLBENZEN ']
    emis9    = 2.0*df_emissions.ix[idx, 'FORMALDEHYD ']
    emis10   = 2.0*df_emissions.ix[idx, 'LEAD ']
    emis11   = 2.0*df_emissions.ix[idx, 'MANGANESE']
    emis12   = 2.0*df_emissions.ix[idx, 'NAPHTHALENE']
    emis13   = 2.0*df_emissions.ix[idx, ' NH3 ']
    emis14   = 2.0*df_emissions.ix[idx, 'NOX ']
    emis15   = 2.0*df_emissions.ix[idx, 'PAH']
    emis16   = 2.0*df_emissions.ix[idx, ' PM10']
    emis17   = 2.0*df_emissions.ix[idx, ' PM2_5 ']
    emis18   = 2.0*df_emissions.ix[idx, 'SO2']
    emis19   = 2.0*df_emissions.ix[idx, ' TOLUENE ']
    emis20   = 2.0*df_emissions.ix[idx, 'VOC']    
    emis21   = 2.0*df_emissions.ix[idx, ' XYLENE']    
    line     = FortranRecordWriter('(I2, A3, A15, 41X, A40, A10, 8X, I4, F6.2, I4, 10X, F9.2, 74X, I4, F9.5, F9.5, 1X, 20(E13.7, 39X), E13.7, 39X)')
#    line     = FortranRecordWriter('(I2, A3, A15, 81X, A10, 8X, I4, F6.2, I4, 10X, F9.2, 74X, I4, F9.5, F9.5, 1X, E13.7, 39X, E13.7, 39X,E13.7, 39X, E13.7, 39X, E13.7, 39X,E13.7, 39X, E13.7, 39X,E13.7, 39X,E13.7, 39X, E13.7, 39X,E13.7, 39X,E13.7, 39X, E13.7, 39X,E13.7, 39X,E13.7, 39X, E13.7, 39X,E13.7, 39X,E13.7, 39X, E13.7, 39X,E13.7, 39X,E13.7, 39X, E13.7, 39X,E13.7, 39X,E13.7, 39X, E13.7, 39X,E13.7, 39X,E13.7, 39X, E13.7, 39X,E13.7, 39X,E13.7, 39X, E13.7, 39X,E13.7, 39X)\n')
    lineOut  = line.write([int(state_id), county_id, plant_id, plant_nm, scc_code, stkHeight, stkDia, stkGasTmp, stkGasVel, sic_code,\
                                latitude, longitude, emis1, emis2, emis3, emis4, emis5, emis6, emis7, emis8, emis9, emis10, emis11, \
                                emis12, emis13, emis14, emis15, emis16, emis17, emis18, emis19, emis20, emis21])
    lineOut = lineOut + ' '*39 + '\n'
    outFile.write(lineOut)
outFile.close()
#%%
    