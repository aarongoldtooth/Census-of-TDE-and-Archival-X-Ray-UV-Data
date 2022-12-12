"""PriorityTDEFilter.py"""

"""
This module takes in:

1) 'TDE_List.tsv' file with columns: ['TDE Name','TDE Discovery Date','TDE Host Galaxy Name']

2) 'TDE_Output_Data.csv' file with observational information for each TDE.

The output returns list of indecies for priority TDE objects
"""

import pandas as pd
import os 

# # Define Early and Late epochs
early_epoch = 100 # days
late_epoch = 3000 # days

tde_file_name = 'TDE_List.tsv'

### Read in tde list file and convert to pandas dataframe
tde_list = pd.read_csv(tde_file_name, sep='\t')
tde_list = tde_list[tde_list['Name'].notnull()]  # remove empty rows

tde_dates = tde_list['Disc Date']

# Add discovery dates to information previously created csv file. For determining dt's
# NOTE: this is not saved back to csv file.
xamin_files = pd.read_csv('TDE_Output_Data.csv')
xamin_files = pd.concat( (xamin_files, tde_dates), axis='columns')


### Filtering Data

### XMM
xmm = pd.DataFrame(xamin_files['XMM Data (#obs: ObsIDs, exp date [yyyy-mm-dd], exp dur [sec])'])
xmm = pd.concat( (xmm, xamin_files['Disc Date'], xamin_files['TDE']), axis='columns')
xmm[f'xmm_within_{late_epoch}_days'] = None
xmm[f'xmm_within_{early_epoch}_days'] = None
xmm['xmm_neg_delta_days?'] = None
xmm['xmm_min_dt'] = None
xmm[f'xmm_num_dt_within_{late_epoch}'] = None
xmm[f'xmm_num_dt_within_{early_epoch}'] = None

for index, row in xmm.iterrows():
    print("Database index: ",index + 2)
    df_row = pd.DataFrame(row)
#     print(df_row)
    tde = xmm['TDE'][index]
    df_row_disc_date = df_row.to_string().split('\n')[2].split()[1]
#     print(df_row_disc_date, type(df_row_disc_date))
    df_row = df_row.to_string().split(')')[1:]
    # print(df_row)

    xmm_within_late_epoch = False
    xmm_within_early_epoch = False
    xmm_neg_delta_days = False
    xmm_diff_time_list = []
    xmm_diff_supedd_time_list = []

    for i, line in enumerate(df_row):
#         if i == 0:
#             print("Num of Obs Ids: ",line.split(':')[0])
#             print('-'*20)
        if i < len(df_row) - 1:
            if i == 0:
                line = line.split(':')[1].split(' ')[1:]
                # print(line)
                # print("exp time = ", line[2])
                exp_time = float(line[2])
            if i > 0:
                line = line.split(':')[0].split(' ')[1:]
                # print(line)
                # print("exp time = ", line[2])
                exp_time = float(line[2])
            for j, element in enumerate(line):
                element = element.strip('(').strip(',')
                # print(element)

                if j==1 and exp_time>1e3:  # getting the obervation date for all >1 ksec exposures
                    element = pd.to_datetime(element)
#                     print("obs date",element)
#                     print(type(element))
#                     print(element.year)
#                     disc_date = pd.to_datetime('1950-12-01')
#                     disc_date = pd.to_datetime(xmm['Disc Date'][index].split('?')[0])
                    disc_date = pd.to_datetime(xmm['Disc Date'][index])
#                     print("disc date",disc_date)
                    diff_time = element - disc_date
                    diff_time = diff_time.days
                    print(diff_time)
        
                    if 0 <= diff_time <= late_epoch:
                        print(f"YES, Obs within {late_epoch} days: ", diff_time)
                        print(tde)
                        xmm_within_late_epoch = True
#                         xmm_within_late_epoch = diff_time
                        xmm_diff_time_list.append(diff_time)
    
                        if 0 <= diff_time <= early_epoch:
                            print(f"YES, Obs within {early_epoch} days: ", diff_time)
                            print(tde)
                            xmm_within_early_epoch = True
    #                         xmm_within_early_epoch = diff_time
                            xmm_diff_supedd_time_list.append(diff_time)
                        
                    if diff_time < 0:
                        print("ERROR negative delta days. CHECK DISC DATE!!!", diff_time)
                        print(tde)
                        xmm_neg_delta_days = True
    
    if xmm_within_late_epoch == True:
        xmm[f'xmm_within_{late_epoch}_days'][index] = True
        xmm['xmm_min_dt'][index] = min(xmm_diff_time_list)
        xmm[f'xmm_num_dt_within_{late_epoch}'][index] = len(xmm_diff_time_list)
        if xmm_within_early_epoch == True:
            xmm[f'xmm_within_{early_epoch}_days'][index] = True
            xmm['xmm_min_dt'][index] = min(xmm_diff_supedd_time_list)
            xmm[f'xmm_num_dt_within_{early_epoch}'][index] = len(xmm_diff_supedd_time_list)
        else:
            xmm[f'xmm_within_{early_epoch}_days'][index] = False
    else:
        xmm[f'xmm_within_{late_epoch}_days'][index] = False


    if xmm_neg_delta_days == True:
        xmm['xmm_neg_delta_days?'][index] = True
    else:
        xmm['xmm_neg_delta_days?'][index] = False
                    
#             print('\n')
# #         print('.'*40)
    print('='*40)

# Filter Late Epoch observations
xmm_late_list = list(xmm.TDE.loc[ (xmm[f'xmm_within_{late_epoch}_days'] == True) 
            & (xmm["xmm_neg_delta_days?"] == False)
           ])

# Filter Early Epoch Observations
xmm_early_list = list(xmm.TDE.loc[ (xmm[f'xmm_within_{early_epoch}_days'] == True) 
            & (xmm["xmm_neg_delta_days?"] == False)
           ])


### Chandra
chan = pd.DataFrame(xamin_files['Chandra Data (#obs: ObsIDs, exp date [yyyy-mm-dd], exp dur [sec], detector)'])
chan = pd.concat( (chan, xamin_files['Disc Date'], xamin_files['TDE']), axis='columns')
chan[f'chan_within_{late_epoch}_days'] = None
chan[f'chan_within_{early_epoch}_days'] = None
chan['chan_neg_delta_days?'] = None
chan['chan_min_dt'] = None
chan[f'chan_num_dt_within_{late_epoch}'] = None
chan[f'chan_num_dt_within_{early_epoch}'] = None

for index, row in chan.iterrows():
    print("Database index: ",index + 2)
    df_row = pd.DataFrame(row)
#     print(df_row)
    tde = chan['TDE'][index]
    df_row_disc_date = df_row.to_string().split('\n')[2].split()[1]
#     print(df_row_disc_date, type(df_row_disc_date))
    df_row = df_row.to_string().split(')')[1:]
#     print(df_row)

    chan_within_late_epoch = False
    chan_within_early_epoch = False
    chan_neg_delta_days = False
    chan_diff_time_list = []
    chan_diff_supedd_time_list = []

    for i, line in enumerate(df_row):
#         print(line)
#         if i == 0:
#             print("Num of Obs Ids: ",line.split(':')[0])
#             print('-'*20)
        if i < len(df_row) - 1:
            if i == 0:
                line = line.split(':')[1].replace('   ', ' ').replace('  ', ' ').split(' ')[1:]
#                 print(line)
            if i > 0:
                line = line.split(':')[0].replace('   ', ' ').replace('  ', ' ').strip().split(' ')[1:]
#                 print(line)
            for j, element in enumerate(line):
#                 print(element, j)
                element = element.strip('(').strip(',')
#                 print(element, j)

                if j==1 and exp_time>1e3:  # getting the obervation date for all >1 ksec exposures:
                    if element == 'null':
                        break
#                     print(element)
                    element = pd.to_datetime(element)
#                     print(type(element))
#                     print(element.year)
#                     disc_date = pd.to_datetime('1950-12-01')
#                     disc_date = pd.to_datetime(chan['Disc Date'][index].split('?')[0])
                    disc_date = pd.to_datetime(chan['Disc Date'][index])
#                     print(disc_date)
                    diff_time = element - disc_date
                    diff_time = diff_time.days
#                     print(diff_time)

                    if 0 <= diff_time <= late_epoch:
                        print(f"YES, Obs within {late_epoch} days: ", diff_time)
                        print(tde)
                        chan_within_late_epoch = True
                        chan_diff_time_list.append(diff_time)

                        if 0 <= diff_time <= early_epoch:
                            print(f"YES, Obs within {early_epoch} days: ", diff_time)
                            print(tde)
                            chan_within_early_epoch = True
                            chan_diff_supedd_time_list.append(diff_time)

                    if diff_time < 0:
                        print("ERROR negative delta days. CHECK DISC DATE!!!", diff_time)
                        print(tde)
                        chan_neg_delta_days = True

    if chan_within_late_epoch == True:
        chan[f'chan_within_{late_epoch}_days'][index] = True
        chan['chan_min_dt'][index] = min(chan_diff_time_list)
        chan[f'chan_num_dt_within_{late_epoch}'][index] = len(chan_diff_time_list)
        if chan_within_early_epoch == True:
            chan[f'chan_within_{early_epoch}_days'][index] = True
            chan['chan_min_dt'][index] = min(chan_diff_supedd_time_list)
            chan[f'chan_num_dt_within_{early_epoch}'][index] = len(chan_diff_supedd_time_list)
        else:
            chan[f'chan_within_{early_epoch}_days'][index] = False
    else:
        chan[f'chan_within_{late_epoch}_days'][index] = False

    if chan_neg_delta_days == True:
        chan['chan_neg_delta_days?'][index] = True
    else:
        chan['chan_neg_delta_days?'][index] = False

#             print('\n')
# #         print('.'*40)
    print('='*40)

# Filter Late Epoch observations
chan_late_list = list(chan.TDE.loc[ (chan[f'chan_within_{late_epoch}_days'] == True) 
            & (chan["chan_neg_delta_days?"] == False)
           ])

# Filter Early Epoch observations
chan_early_list = list(chan.TDE.loc[ (chan[f'chan_within_{early_epoch}_days'] == True) 
            & (chan["chan_neg_delta_days?"] == False)
           ])


### Swift
swift = pd.DataFrame(xamin_files['Swift Data (#obs: ObsIDs, exp date [yyyy-mm-dd], XRT exp dur [sec])'])
swift = pd.concat( (swift, xamin_files['Disc Date'], xamin_files['TDE']), axis='columns')
swift[f'swift_within_{late_epoch}_days'] = None
swift[f'swift_within_{early_epoch}_days'] = None
swift['swift_neg_delta_days?'] = None
swift['swift_min_dt'] = None
swift[f'swift_num_dt_within_{late_epoch}'] = None
swift[f'swift_num_dt_within_{early_epoch}'] = None
swift

for index, row in swift.iterrows():
    print("Database index: ",index + 2)
    df_row = pd.DataFrame(row)
#     print(df_row)
    tde = swift['TDE'][index]
    df_row_disc_date = df_row.to_string().split('\n')[2].split()[1]
#     print(df_row_disc_date, type(df_row_disc_date))
    df_row = df_row.to_string().split(')')[1:]
#     print(df_row)

    swift_within_late_epoch = False
    swift_within_early_epoch = False
    swift_neg_delta_days = False
    swift_diff_time_list = []
    swift_diff_supedd_time_list = []

    for i, line in enumerate(df_row):
#         if i == 0:
#             print("Num of Obs Ids: ",line.split(':')[0])
#             print('-'*20)
        if i < len(df_row) - 1:
            if i == 0:
                line = line.split(':')[1].split(' ')[1:]
#                 print(line)
            if i > 0:
                line = line.split(':')[0].split(' ')[1:]
#                 print(line)
            for j, element in enumerate(line):
                element = element.strip('(').strip(',')
#                 print(element)

                if j==1 and exp_time>1e3:  # getting the obervation date for all >1 ksec exposures
                    element = pd.to_datetime(element)
#                     print(type(element))
#                     print(element.year)
#                     disc_date = pd.to_datetime('1950-12-01')
#                     disc_date = pd.to_datetime(swift['Disc Date'][index].split('?')[0])
                    disc_date = pd.to_datetime(swift['Disc Date'][index])
#                     print(disc_date)
                    diff_time = element - disc_date
                    diff_time = diff_time.days
#                     print(diff_time)

                    if 0 <= diff_time <= late_epoch:
                        print(f"YES, Obs within {late_epoch} days: ", diff_time)
                        print(tde)
                        swift_within_late_epoch = True
                        swift_diff_time_list.append(diff_time)

                        if 0 <= diff_time <= early_epoch:
                            print(f"YES, Obs within {early_epoch} days: ", diff_time)
                            print(tde)
                            swift_within_early_epoch = True
                            swift_diff_supedd_time_list.append(diff_time)

                    if diff_time < 0:
                        print("ERROR negative delta days. CHECK DISC DATE!!!", diff_time)
                        print(tde)
                        swift_neg_delta_days = True

    if swift_within_late_epoch == True:
        swift[f'swift_within_{late_epoch}_days'][index] = True
        swift['swift_min_dt'][index] = min(swift_diff_time_list)
        swift[f'swift_num_dt_within_{late_epoch}'][index] = len(swift_diff_time_list)
        if swift_within_early_epoch == True:
            swift[f'swift_within_{early_epoch}_days'][index] = True
            swift['swift_min_dt'][index] = min(swift_diff_time_list)
            swift[f'swift_num_dt_within_{early_epoch}'][index] = len(swift_diff_time_list)
        else:
            swift[f'swift_within_{early_epoch}_days'][index] = False
    else:
        swift[f'swift_within_{late_epoch}_days'][index] = False

    if swift_neg_delta_days == True:
        swift['swift_neg_delta_days?'][index] = True
    else:
        swift['swift_neg_delta_days?'][index] = False

#             print('\n')
# #         print('.'*40)
    print('='*40)

# Filter Late Epoch observations
swift_late_list = list(swift.TDE.loc[ (swift[f'swift_within_{late_epoch}_days'] == True) 
            & (swift["swift_neg_delta_days?"] == False)
           ])

# Filter Early Epoch observations
swift_early_list = list(swift.TDE.loc[ (swift[f'swift_within_{early_epoch}_days'] == True) 
            & (swift["swift_neg_delta_days?"] == False)
           ])


### All Data Together
full_df = pd.concat( (xmm, chan, swift), axis='columns')

### Abridged Data
abr_df = full_df[['TDE'
         ,'xmm_min_dt',f'xmm_num_dt_within_{late_epoch}',f'xmm_num_dt_within_{early_epoch}'
         ,'chan_min_dt',f'chan_num_dt_within_{late_epoch}',f'chan_num_dt_within_{early_epoch}'
         ,'swift_min_dt',f'swift_num_dt_within_{late_epoch}',f'swift_num_dt_within_{early_epoch}'
        ]]

### Prioritization

## Tier 1 (Best Data): 
# 1. XMM and/or Chandra data with more than one >1 ksec (based on exp time-->counts, but z and object’s brightness important too) spectrum within 100 days (based on trying to sample the super-Edd or ~Edd regime) 
# 2. and more than one >3 ksec spectra (based on Wen et al. 2020’s result showing that more epochs can provide better constraints) at later times.

best_df = abr_df.loc[((abr_df[f'xmm_num_dt_within_{early_epoch}'] > 1)
                      | (abr_df[f'chan_num_dt_within_{early_epoch}'] > 1)
                      | ((abr_df[f'xmm_num_dt_within_{early_epoch}'] >= 1)
                          & (abr_df[f'chan_num_dt_within_{early_epoch}'] >= 1))
                     ) 
                     & ((abr_df[f'xmm_num_dt_within_{late_epoch}'] > 1)
                          | (abr_df[f'chan_num_dt_within_{late_epoch}'] > 1)
                          | ((abr_df[f'xmm_num_dt_within_{late_epoch}'] >= 1)
                              & (abr_df[f'chan_num_dt_within_{late_epoch}'] >= 1))
                         ) 
                    ]

best_index = list(best_df.index)

# Remaining TDEs
rem_df = abr_df.drop(best_index)


## Tier 2 (Very Good Data)
# 1. XMM and/or Chandra data with one >1 ksec (based on exp time-->counts, but z and object’s brightness important too) spectrum within 100 days (based on trying to sample the super-Edd or ~Edd regime) 
# 2. and more than one >3 ksec spectra (based on Wen et al. 2020’s result showing that more epochs can provide better constraints) at later times.

very_good_df = rem_df.loc[((abr_df[f'xmm_num_dt_within_{early_epoch}'] > 0)
                      | (abr_df[f'chan_num_dt_within_{early_epoch}'] > 0)
                     ) 
                     & ((abr_df[f'xmm_num_dt_within_{late_epoch}'] > 1)
                          | (abr_df[f'chan_num_dt_within_{late_epoch}'] > 1)
                          | ((abr_df[f'xmm_num_dt_within_{late_epoch}'] >= 1)
                              & (abr_df[f'chan_num_dt_within_{late_epoch}'] >= 1))
                         ) 
                    ]

very_good_index = list(very_good_df.index)

# Remaining TDEs
rem_df = rem_df.drop(very_good_index)


## Tier 3 (Good Data)
# 1. XMM and/or Chandra data with one >1 ksec (based on exp time-->counts, but z and object’s brightness important too) spectrum within 100 days (based on trying to sample the super-Edd or ~Edd regime)

good_df = rem_df.loc[((abr_df[f'xmm_num_dt_within_{early_epoch}'] > 0)
                      | (abr_df[f'chan_num_dt_within_{early_epoch}'] > 0)
                     )
                    ]

good_index = list(good_df.index)

# Remaining TDEs
rem_df = rem_df.drop(good_index)


## Tier 4 (Fair Data)
# 1. XMM and/or Chandra data with more than one >3 ksec spectra (based on Wen et al. 2020’s result showing that more epochs can provide better constraints) at later times.

fair_df = rem_df.loc[((abr_df[f'xmm_num_dt_within_{late_epoch}'] > 1)
                      | (abr_df[f'chan_num_dt_within_{late_epoch}'] > 1)
                      | ((abr_df[f'xmm_num_dt_within_{late_epoch}'] >= 1)
                          & (abr_df[f'chan_num_dt_within_{late_epoch}'] >= 1))
                     ) 
                    ]

fair_index = list(fair_df.index)

all_priority_indices = best_index + very_good_index + good_index + fair_index

print(all_priority_indices)

    # if __name__ == "__main__":
    #     return all_priority_indices

# save indicies for use in other code.

# save_bool = True
save_bool = False

if save_bool == True:
    save_file = 'priority_tde_indicies.txt'
    with open('priority_tde_indicies.txt', 'w') as savf:
        savf.write(str(all_priority_indices))
    