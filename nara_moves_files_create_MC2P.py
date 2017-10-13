# vikram 3rd July 2016
''' using the ArcGIS processed file attribute tabels, we create the files required for the emission 
    inventory for the onroad mobile sources. 
    Since not all road data for NARA could be attributed to the HPMS obtained road types file, we 
    do some analysis where certain NARA roads are considered rural local or some type??
    uses two files
    1. Spokane_FIA_2_Spokane_VMT_Buffer_Intersect_ap4_county_info.csv - which is the file which has 
       county cell row/col as well as the road type information as required by SMOKE MOVES
    2. Spokane_FIA_2_Spokane_VMT_Intersect_ap4_county_info.csv - which is the county and cell row/col 
       attributed to each NARA road
'''
#%%    
import pandas as pd
import numpy as np
#file_noRoad = "C:/Users/vik/Documents/Projects/NARA/NARA_files_4_MOVES/Spokane_FIA_2_Spokane_VMT_Intersect_ap4_county_info.csv"    
#file_Road   = "C:/Users/vik/Documents/Projects/NARA/NARA_files_4_MOVES/Spokane_FIA_2_Spokane_VMT_Buffer_Intersect_ap4_county_info.csv"

file_noRoad_cosmo   = "C:/Users/vik/Documents/Projects/NARA/NARA_files_4_MOVES/FIA_2_Cosmo_marginal_cost_VMT_Intersect_ap4_county_info.csv"    
file_Road_cosmo     = "C:/Users/vik/Documents/Projects/NARA/NARA_files_4_MOVES/FIA_2_Cosmo_marginal_cost_VMT_5mBuffer_Intersect_ap4_county_info.csv"
file_noRoad_refTermi= "C:/Users/vik/Documents/Projects/NARA/NARA_files_4_MOVES/WY_Cosmo_2_Terminals_2_VMT_Intersect_ap4_county_info.csv"    
file_Road_refTermi  = "C:/Users/vik/Documents/Projects/NARA/NARA_files_4_MOVES/WY_Cosmo_2_Terminals_2_VMT_Buffer_Intersect_ap4_county_info.csv"


#df_noRoadInfo = pd.read_csv(file_noRoad)
#df_RoadInfo   = pd.read_csv(file_Road)

df_noRoadInfoCosmo  = pd.read_csv(file_noRoad_cosmo)
df_RoadInfoCosmo    = pd.read_csv(file_Road_cosmo)
df_noRoadInfo2Terminal= pd.read_csv(file_noRoad_refTermi)
df_RoadInfo2Terminal  = pd.read_csv(file_Road_refTermi)

df_noRoadInfoCosmo.rename(columns={'FIPS_1':'FIPS_12', 'NAME':'NAME_12'}, inplace=True)
df_RoadInfoCosmo.rename(columns={'FIPS_1':'FIPS_12', 'NAME':'NAME_12'}, inplace=True)
df_noRoadInfo2Terminal.rename(columns={'FIPS_1':'FIPS_12', 'NAME_1':'NAME_12'}, inplace=True)
df_RoadInfo2Terminal.rename(columns={'FIPS_1':'FIPS_12', 'NAME_1':'NAME_12'}, inplace=True)

df_noRoadInfo = pd.concat([df_noRoadInfoCosmo, df_noRoadInfo2Terminal], ignore_index=True)
df_RoadInfo   = pd.concat([df_RoadInfoCosmo, df_RoadInfo2Terminal], ignore_index=True)

#%%
def get_scc(fcode_in, ucode_in):
    '''SCC for on road sources is of the form 22-VVVV-X-RRR
       where 22   - Mobile source
             VVVV - vehicle code, which for heavy duty diesel vehicles is 3007
             X    - unused, and based on airpact4, we will use 4
             RRR  - road class code, calculated below    '''
    # 99999 - rural, anything else (here used as 99998) - urban
    road_class = {99999:{1:110, 2:130, 3:130, 4:150, 5:170, 6:190, 7:210, 0:210},
                  99998:{1:230, 2:250, 3:270, 4:290, 5:310, 6:310, 7:330}}
    get_urban = lambda u: (99999 if ((u == 99999) or (u == 0)) else 99998)
    ucode = get_urban(ucode_in)
    dummy_scc = road_class[ucode][fcode]
    scc = str(22) + str(3007) + str(4) + str(dummy_scc)
    return scc
#%%
# create the file SMOKE inventory    
df_noRoadInfo_sml = df_noRoadInfo[['Name', 'Total_Leng', 'FIA_pt', 'VMT_roundT', 'COL', 'ROW', 'FIPS_12', 'Len_Cel_Mi']] # get only necessary fields
df_noRoadInfo_sml['cel_frac'] = df_noRoadInfo_sml['Len_Cel_Mi']/df_noRoadInfo_sml['Total_Leng'] # get the fraction of each cell lenght wrt total length to FIA
df_noRoadInfo_sml['VMT_cel'] = df_noRoadInfo_sml['VMT_roundT']*df_noRoadInfo_sml['cel_frac'] # get VMT for each cell

# let's get the sum of VMT by county. this will go as the input to the SMOKE inventory
df_VMTbyCounty = df_noRoadInfo_sml.groupby(by=df_noRoadInfo_sml.FIPS_12).sum() # sum by FIPS code, i.e. get VMT for each county
df_VMTbyCounty.rename(columns={'VMT_cel': 'VMT_county'}, inplace=True) # rename since the 'VMT_cel' column actually represents the county total VMT now
#%%    
# assign SCCs
for i in df_RoadInfo.index:
    fcode = df_RoadInfo.at[i, 'f_system'] 
    ucode = df_RoadInfo.at[i, 'urban_code']
    df_RoadInfo.at[i, 'scc_code'] = get_scc(fcode, ucode)
    
# keep only the required dataframe columns
df_RoadInfo_sml = df_RoadInfo[['Name', 'Total_Leng', 'FIA_pt', 'VMT_roundT', 'RdTypLenMi', 'COL', 'ROW', 'NAME_12','FIPS_12', 'scc_code']] # get only necessary fields
df_RoadInfo_sml = df_RoadInfo_sml[df_RoadInfo_sml['VMT_roundT']>0]
#%%
# calculate county and scc based total VMT below
counter = 0
for fips in list(set(df_RoadInfo_sml['FIPS_12'])):
    df_county = df_RoadInfo_sml.loc[df_RoadInfo_sml.FIPS_12 == fips]
    df_county['RdTypVMT'] = (df_county['RdTypLenMi']/df_VMTbyCounty.at[fips, 'Len_Cel_Mi'])*df_VMTbyCounty.at[fips, 'VMT_county']
#    df_county.set_index(df_county.scc_code, inplace=True, drop=False)
#    VMT_difference = df_county.ix['2230074210', 'RdTypVMT'] + df_VMTbyCounty.ix[fips, 'VMT_county'] - df_county.RdTypVMT.sum()
    
    df_grouped = df_county.groupby(by=df_county.scc_code).sum()    
    df_grouped['scc_code'] = df_grouped.index
    
    # preferable assign the roads which were not given road type to scc = 2230074210 (rural local)
    list_scc_code = list(set(df_county.scc_code))
    diff_vmt = df_VMTbyCounty.ix[fips, 'VMT_county'] - df_grouped.RdTypVMT.sum()
    for len_scc in np.arange(len(list_scc_code)):
        df_grouped.ix[list_scc_code[len_scc], 'RdTypVMT'] = df_grouped.ix[list_scc_code[len_scc], 'RdTypVMT'] + diff_vmt/len(list_scc_code)
#    if ('2230074210' in list_scc_code):
#        df_grouped.ix[list_scc_code[0], 'RdTypVMT'] = df_grouped.ix[list_scc_code[0], 'RdTypVMT'] + df_VMTbyCounty.ix[fips, 'VMT_county'] - df_grouped.RdTypVMT.sum()
##        df_grouped.ix['2230074210', 'RdTypVMT'] = df_grouped.ix['2230074210', 'RdTypVMT'] + df_VMTbyCounty.ix[fips, 'VMT_county'] - df_grouped.RdTypVMT.sum()
#    else: # else write to first scc available
#        df_grouped.ix[list_scc_code[0], 'RdTypVMT'] = df_grouped.ix[list_scc_code[0], 'RdTypVMT'] + df_VMTbyCounty.ix[fips, 'VMT_county'] - df_grouped.RdTypVMT.sum()

    df_grouped['county_FIPS'] = fips
    if (counter == 0):
        df_VMTbyRoadCounty = pd.DataFrame(df_grouped)
    else:
        df_VMTbyRoadCounty = pd.concat([df_VMTbyRoadCounty, df_grouped], ignore_index=True)
    counter += 1
#%%        
#df_spokane = df_RoadInfo_sml.loc[df_RoadInfo_sml.FIPS_12 == 53063]
#df_spokane['RdTypVMT'] = (df_spokane['RdTypLenMi']/df_VMTbyCounty.at[53063, 'Len_Cel_Mi'])*df_VMTbyCounty.at[53063, 'VMT_county']
# now let's work for creating the fractions of county VMT for each cell (row, col) i.e. the AMGPRO file
dfRdInfo_byRowCol   = df_RoadInfo_sml.groupby(by=(df_RoadInfo_sml.COL, df_RoadInfo_sml.ROW, df_RoadInfo_sml.scc_code, df_RoadInfo_sml.FIPS_12), as_index=False).sum()    
dfnoRdInfo_byRowCol = df_noRoadInfo_sml.groupby(by=(df_noRoadInfo_sml.COL, df_noRoadInfo_sml.ROW, df_noRoadInfo_sml.FIPS_12), as_index=True).sum()
df_noRoadInfo_tmp   = df_noRoadInfo_sml.groupby(by=(df_noRoadInfo_sml.COL, df_noRoadInfo_sml.ROW), as_index=True).sum()
#df_noRoadInfo_tmp   = df_noRoadInfo_sml.set_index(['COL', 'ROW'], drop=False, inplace=False)
df_tmp = df_VMTbyRoadCounty.groupby(by=['county_FIPS', 'scc_code'],as_index=True).sum()
#iterate and get fraction in each cell by scc
for idx in list(set(dfRdInfo_byRowCol.index)):
    col_num = dfRdInfo_byRowCol.ix[idx, 'COL']
    row_num = dfRdInfo_byRowCol.ix[idx, 'ROW']
    fips_cd = dfRdInfo_byRowCol.ix[idx, 'FIPS_12']
    scc_cd  = dfRdInfo_byRowCol.ix[idx, 'scc_code']
    
#    # now get the fraction of this scc for this row and col
    if ((col_num, row_num) in set(df_noRoadInfo_tmp.index)):
        fraction_scc_cell          = dfRdInfo_byRowCol.ix[idx, 'RdTypLenMi'] / df_noRoadInfo_tmp.ix[(col_num, row_num), 'Len_Cel_Mi'] # scc's fraction of total road length for that cell
        dfRdInfo_byRowCol.ix[idx, 'scc_cel_frac']              = fraction_scc_cell
    
    fraction_scc_county_total  = dfRdInfo_byRowCol.ix[idx, 'RdTypLenMi'] / df_VMTbyCounty.ix[fips_cd, 'Len_Cel_Mi'] # scc as a fraction of total county independent of road type
    fraction_scc_county_rdType = dfRdInfo_byRowCol.ix[idx, 'RdTypLenMi'] / df_tmp.ix[(fips_cd, scc_cd), 'RdTypLenMi'] # scc as a fraction of total county of that scc's road type
    
    print col_num, row_num, fips_cd, scc_cd, fraction_scc_county_total
    
    dfRdInfo_byRowCol.ix[idx, 'scc_cel_frac_TotalLen']     = fraction_scc_county_total
    dfRdInfo_byRowCol.ix[idx, 'scc_cel_frac_cntyRdTypLen'] = fraction_scc_county_rdType
#    dfRdInfo_byRowCol.ix[idx, 'scc_cel_frac'] = dfRdInfo_byRowCol.ix[idx, 'RdTypLenMi'] / dfnoRdInfo_byRowCol.ix[(col_num,row_num,fips_cd), 'Len_Cel_Mi']




#%%
# get the fraction of total county for each cell
df_fraction = df_noRoadInfo_sml.copy()
df_fraction = df_fraction.groupby(by=['COL', 'ROW', 'FIPS_12'], as_index=True).sum()
df_county_length = df_noRoadInfo_sml.groupby(by='FIPS_12', as_index=True).sum()

for idx in df_fraction.index:
    col_number  = int(idx[0])
    row_number  = int(idx[1])
    county_fips = idx[2]
    df_fraction.loc[idx, 'cellLengFractionOfCountyLeng'] = df_fraction.loc[idx, 'Len_Cel_Mi']/df_county_length.loc[county_fips, 'Len_Cel_Mi']
    df_fraction.loc[idx, 'FIPS'] = str(county_fips)
    df_fraction.loc[idx, 'ROW']  = int(row_number)
    df_fraction.loc[idx, 'COL']  = int(col_number)

#%%
# now write the output to files for SMOKE-MOVES
# AMGPRO file
outputFile1 = "C:/Users/vik/Documents/Projects/NARA/NARA_files_4_MOVES/MC2P/amgpro_ap4_NARA_MC2P.txt"    
amgproFile = open(outputFile1, 'w')
lineOut = '%s\n'*3%('#GRID AIRPACT_04km -342000 -942000 4000 4000 285 258 0 LAMBERT METERS 30 60 -121 -121 49',
                    '# surrogates are same as airpact4, except row and column based fraction',
                    '# developed specially for NARA project')
amgproFile.write(lineOut)
srg_county ={'53063':2820,'53067':2840,'53033':2810,'53053':2810,'53035':2810}
for idx in df_fraction.index:
    fips_code  = df_fraction.loc[idx, 'FIPS']
    row_number = df_fraction.loc[idx, 'ROW']
    col_number = df_fraction.loc[idx, 'COL']
    frac_val_dummy   = df_fraction.loc[idx, 'cellLengFractionOfCountyLeng']
    if (np.isnan(frac_val_dummy)):
        frac_val = 0
    else:
        frac_val = frac_val_dummy
    
    if fips_code in srg_county.keys():
        srg_code = srg_county[fips_code]
    elif (fips_code[0:2] == '16'):
        srg_code = 2600
    elif (fips_code[0:2] == '30'):
        srg_code = 2100
    elif (fips_code[0:2] == '41'):
        srg_code = 2700
    elif (fips_code[0:2] == '53'):
        srg_code = 2800
        
    lineOut = '%s %s %s %s %s\n' %(srg_code, '0'+fips_code, int(col_number), int(row_number), frac_val)
    amgproFile.write(lineOut)
amgproFile.close()    
##%%
## VMT file
#outputFile2 = "C:/Users/vik/Documents/Projects/NARA/NARA_files_4_MOVES/MC2P/mbinv.airpact4.NARA_MC2P.orl.VMT.txt"    
#inventoryFile = open(outputFile2, 'w')
#lineOut = '%s\n'*7%("#FORMAT=FF10_ACTIVITY",
#                    "#COUNTRY  US",
#                    "#YEAR     2011",
#                    "#SELECTION_NAME",
#                    "#INVENTORY_VERSION",
#                    "#INVENTORY_LABEL",
#                    "#DESC COUNTRYREGION_CDTRIBAL_CODECENSUS_TRACT_CDSHAPE_IDSCCACT_PARM_TYPE_CDACT_PARM_UOFMSRVPOPANNUAL_VALUEEXTRA")
#inventoryFile.write(lineOut)
#
#for idx in df_VMTbyRoadCounty.index:
#    fips_code = df_VMTbyRoadCounty.loc[idx, 'county_FIPS']
#    scc_code  = df_VMTbyRoadCounty.loc[idx, 'scc_code']
#    scc_VMT_dummy = df_VMTbyRoadCounty.loc[idx, 'RdTypVMT']
#    if (np.isnan(scc_VMT_dummy)):
#        scc_VMT = 0
#    else:
#        scc_VMT = scc_VMT_dummy
#    lineOut = '%s,'*11%('US', fips_code,'','','',scc_code,'','','VMT',scc_VMT,','*16)
#    inventoryFile.write(lineOut)
#    lineOut = '\n'
#    inventoryFile.write(lineOut)
#inventoryFile.close()           
#
## SPEED file
#outputFile3 = "C:/Users/vik/Documents/Projects/NARA/NARA_files_4_MOVES/MC2P/mbinv.airpact4.NARA_MC2P.orl.SPEED.txt"    
#speedFile = open(outputFile3, 'w')
#lineOut = '%s\n'*7%("#FORMAT=FF10_ACTIVITY",
#                    "#COUNTRY  US",
#                    "#YEAR     2011",
#                    "#SELECTION_NAME",
#                    "#INVENTORY_VERSION",
#                    "#INVENTORY_LABEL",
#                    "#DESC COUNTRYREGION_CDTRIBAL_CODECENSUS_TRACT_CDSHAPE_IDSCCACT_PARM_TYPE_CDACT_PARM_UOFMSRVPOPANNUAL_VALUEEXTRA")
#speedFile.write(lineOut)
#
#for idx in df_VMTbyRoadCounty.index:
#    fips_code = df_VMTbyRoadCounty.loc[idx, 'county_FIPS']
#    scc_code  = df_VMTbyRoadCounty.loc[idx, 'scc_code']
#    scc_speed = 45
#    lineOut = '%s,'*11%('US', fips_code,'','','',scc_code,'','','SPEED',scc_speed,','*16)
#    speedFile.write(lineOut)
#    lineOut = '\n'
#    speedFile.write(lineOut)
#speedFile.close()           

#%%
# VMT file
outputFile2 = "C:/Users/vik/Documents/Projects/NARA/NARA_files_4_MOVES/MC2P/mbinv.airpact4.NARA_MC2P.orl.VMT.txt"    
inventoryFile = open(outputFile2, 'w')
lineOut = '%s\n'*7%("#FORMAT=FF10_ACTIVITY",
                    "#COUNTRY  US",
                    "#YEAR     2011",
                    "#SELECTION_NAME",
                    "#INVENTORY_VERSION",
                    "#INVENTORY_LABEL",
                    "#DESC COUNTRYREGION_CDTRIBAL_CODECENSUS_TRACT_CDSHAPE_IDSCCACT_PARM_TYPE_CDACT_PARM_UOFMSRVPOPANNUAL_VALUEEXTRA")
inventoryFile.write(lineOut)

for fips_code in sorted(list(set(df_VMTbyRoadCounty.county_FIPS))):
    fips_VMT_sum = 0
    oneCounty = df_VMTbyRoadCounty[df_VMTbyRoadCounty['county_FIPS'] == fips_code]
    print oneCounty
    countySCCs= list(oneCounty.scc_code)
    for scc_code in countySCCs:
        fips_VMT_sum += df_VMTbyCounty.ix[fips_code, 'VMT_county']/len(countySCCs)
        scc_VMT = df_VMTbyCounty.ix[fips_code, 'VMT_county']/len(countySCCs)
        print fips_code, scc_code, df_VMTbyCounty.ix[fips_code, 'VMT_county']/len(countySCCs)
        lineOut = '%s,'*11%('US', fips_code,'','','',scc_code,'','','VMT',scc_VMT,','*16)
        inventoryFile.write(lineOut)
        lineOut = '\n'
        inventoryFile.write(lineOut)
inventoryFile.close()  

#for idx in df_VMTbyRoadCounty.index:
#    fips_code = df_VMTbyRoadCounty.loc[idx, 'county_FIPS']
#    scc_code  = df_VMTbyRoadCounty.loc[idx, 'scc_code']
#    scc_VMT_dummy = df_VMTbyRoadCounty.loc[idx, 'RdTypVMT']
#    if (np.isnan(scc_VMT_dummy)):
#        scc_VMT = 0
#    else:
#        scc_VMT = scc_VMT_dummy
#    lineOut = '%s,'*11%('US', fips_code,'','','',scc_code,'','','VMT',scc_VMT,','*16)
#    inventoryFile.write(lineOut)
#    lineOut = '\n'
#    inventoryFile.write(lineOut)
#inventoryFile.close()           
#%%
# SPEED file
outputFile3 = "C:/Users/vik/Documents/Projects/NARA/NARA_files_4_MOVES/MC2P/mbinv.airpact4.NARA_MC2P.orl.SPEED.txt"    
speedFile = open(outputFile3, 'w')
lineOut = '%s\n'*7%("#FORMAT=FF10_ACTIVITY",
                    "#COUNTRY  US",
                    "#YEAR     2011",
                    "#SELECTION_NAME",
                    "#INVENTORY_VERSION",
                    "#INVENTORY_LABEL",
                    "#DESC COUNTRYREGION_CDTRIBAL_CODECENSUS_TRACT_CDSHAPE_IDSCCACT_PARM_TYPE_CDACT_PARM_UOFMSRVPOPANNUAL_VALUEEXTRA")
speedFile.write(lineOut)

for idx in df_VMTbyRoadCounty.index:
    fips_code = df_VMTbyRoadCounty.loc[idx, 'county_FIPS']
    scc_code  = df_VMTbyRoadCounty.loc[idx, 'scc_code']
    scc_speed = 45
    lineOut = '%s,'*11%('US', fips_code,'','','',scc_code,'','','SPEED',scc_speed,','*16)
    speedFile.write(lineOut)
    lineOut = '\n'
    speedFile.write(lineOut)
speedFile.close()          

# VPOP file
outputFile4 = "C:/Users/vik/Documents/Projects/NARA/NARA_files_4_MOVES/MC2P/mbinv.airpact4.NARA_MC2P.orl.VPOP.txt"    
vpopFile = open(outputFile4, 'w')
lineOut = '%s\n'*7%("#FORMAT=FF10_ACTIVITY",
                    "#COUNTRY  US",
                    "#YEAR     2011",
                    "#SELECTION_NAME",
                    "#INVENTORY_VERSION",
                    "#INVENTORY_LABEL",
                    "#DESC COUNTRYREGION_CDTRIBAL_CODECENSUS_TRACT_CDSHAPE_IDSCCACT_PARM_TYPE_CDACT_PARM_UOFMSRVPOPANNUAL_VALUEEXTRA")
vpopFile.write(lineOut)

for cnty_fips in set(df_VMTbyRoadCounty.county_FIPS):
    fips_code = cnty_fips
    #scc_code  = df_VMTbyRoadCounty.loc[idx, 'scc_code']
    scc_code  = 2230074000 # based on airpact4 inventory. though this scc doesnt exist in scc list, and I dont know why this is used- maybe a single category for all diesel HDDV
    if (fips_code == '53063' or fips_code == 53063):
        scc_vpop = 360
    else:
        scc_vpop = 0
    lineOut = '%s,'*11%('US', fips_code,'','','',scc_code,'','','VPOP',scc_vpop,','*16)
    vpopFile.write(lineOut)
    lineOut = '\n'
    vpopFile.write(lineOut)
vpopFile.close()  
#%%
# ???????????????????????????????????/
# ============== NOT USED ==============
# BELOW TRIIED TO DO SCC TYPE CELL FRACTION ALLOCATION    
#iterate and assign (1-fraction) above for each cell to scc =2230074210
#for idx in list(set(dfRdInfo_byRowCol.index)):
df_tmp1 = dfRdInfo_byRowCol.set_index(['COL', 'ROW'], drop=False)
counter=0
for c,r in sorted(list(set(zip(dfRdInfo_byRowCol.COL, dfRdInfo_byRowCol.ROW))))[:]:
#    print df_tmp.ix[(c,r), 'scc_cel_frac']
    cell_sccList = list(set(df_tmp1.ix[(c,r), 'scc_code']))
#    cellFrac_sum = df_tmp1.ix[(c,r), 'scc_cel_frac'].sum()
    cellFrac_sum = df_tmp1.ix[(c,r), 'scc_cel_frac'].sum()
    
#    counter += 1
#    print c,r,cellFrac_sum, counter
    if (cellFrac_sum != 1.0):
        df_tmp2 = df_tmp1.ix[(c,r),:]
#        print c,r,cellFrac_sum,cell_sccList
        df_tmp3 = df_tmp2.set_index(['COL','ROW','scc_code'],drop=False)
        print c,r,cellFrac_sum,cell_sccList
        if '2230074210' in cell_sccList:
            df_tmp3.ix[(c,r,'2230074210'), 'scc_cel_frac_new'] = df_tmp3.ix[(c,r,'2230074210'), 'scc_cel_frac'] + (1-cellFrac_sum)
        else:
            maxarg  = df_tmp3.ix[:, 'scc_cel_frac_TotalLen'].argmax()
            df_tmp3.ix[(c,r,maxarg[2]), 'scc_cel_frac_new'] = df_tmp3.ix[(c,r,maxarg[2]), 'scc_cel_frac_TotalLen'] + (1-cellFrac_sum)
#            df_tmp4 = df_tmp3
        if counter == 0:
            df_cellFrac = pd.DataFrame(df_tmp3)
        else:
            df_cellFrac = pd.concat([df_cellFrac, df_tmp3], ignore_index=True)
#            df_tmp.ix[(c,r),]
    counter += 1    



#%%
#iterate and assign (1-fraction) above for each cell to scc =2230074210
#for idx in list(set(dfRdInfo_byRowCol.index)):
df_tmp = dfRdInfo_byRowCol.set_index(['COL', 'ROW'], drop=False)
counter=0
for c,r in sorted(list(set(zip(dfRdInfo_byRowCol.COL, dfRdInfo_byRowCol.ROW)))):
#    print df_tmp.ix[(c,r), 'scc_cel_frac']
    cell_sccList = list(set(df_tmp.ix[(c,r), 'scc_code']))
    cellFrac_sum = df_tmp.ix[(c,r), 'scc_cel_frac'].sum()
    if (cellFrac_sum != 1.0):
        df_tmp2 = df_tmp.ix[(c,r),:]
#        print c,r,cellFrac_sum,cell_sccList
        df_tmp3 = df_tmp2.set_index(['COL','ROW','scc_code'],drop=False)
        print c,r,cellFrac_sum,cell_sccList
        if '2230074210' in cell_sccList:
            df_tmp3.ix[(c,r,'2230074210'), 'scc_cel_frac'] = df_tmp3.ix[(c,r,'2230074210'), 'scc_cel_frac'] + (1-cellFrac_sum)
        else:
            maxarg  = df_tmp3.ix[:, 'scc_cel_frac'].argmax()
            df_tmp3.ix[(c,r,maxarg[2]), 'scc_cel_frac'] = df_tmp3.ix[(c,r,maxarg[2]), 'scc_cel_frac'] + (1-cellFrac_sum)
#            df_tmp4 = df_tmp3
        if counter == 0:
            df_cellFrac = pd.DataFrame(df_tmp3)
        else:
            df_cellFrac = pd.concat([df_cellFrac, df_tmp3], ignore_index=True)
#            df_tmp.ix[(c,r),]
    counter += 1
    