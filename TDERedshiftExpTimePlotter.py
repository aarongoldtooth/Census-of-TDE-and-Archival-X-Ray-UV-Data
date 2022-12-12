"""TDERedshiftExpTimePlotter.py"""

"""
This module takes in:

1) 'Full New TDE Catalog (Published).tsv'

2) 'priority_tde_indicies.txt' from the 'PriorityTDEFilter.py' module

and generates redshift vs exposure time range plots of each set of observations made on each TDE Target.

The output file is 'tde_exp_times_vs_redshift.pdf'
"""

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy import stats

# toggle saving of file
# file_save = True
file_save = False

# Read-in the TDE Catalog as a pandas dataframe
tde_file_name = 'Full New TDE Catalog (Published).tsv'
tde_cat = pd.read_table(tde_file_name)

# drop TDEs that may be other phenomena or that are not relevent

obj1 = {'name':'IGR J17361-4441', 'index':31}  # possible LMXB
obj2 = {'name':'NGC 247', 'index':53}  # possible LMXB
obj3 = {'name':'ASASSN-15oi', 'index':11} # inconclusive results
obj4 = {'name':'MAXI J1807+132', 'index':52}  # possible LMXB

# print(obj1.get('index'))

drop_dict = {0:obj1, 1:obj2, 2:obj3, 3:obj4}

# print([drop_dict[i].get('index')-2 for i in range(len(drop_dict))])

drop_indices = [drop_dict[i].get('index')-2 for i in range(len(drop_dict))]

# Get priority tde indicies from 'priority_tde_indicies.txt'
with open('priority_tde_indicies.txt', 'r') as rfile:
    for line in rfile:
        priority_tdes = [int(num) for num in line.strip('][').split(', ')]
    
# priority_tdes = [1, 2, 3, 7, 9, 12, 14, 16, 19, 21, 23, 25, 51, 80, 81, 82, 101, 102, 107, 111, 112
#                  , 4, 50, 78, 114, 117
#                  , 0, 5, 6, 8, 11, 22, 24, 52, 55, 115
#                  , 29, 30, 31, 64, 83, 110]

# Update indicies to exclude dropped data
for index in drop_indices:
    if index in priority_tdes:
        priority_tdes.remove(index)

# Bins for histogram 
bin_width = 0.05


xray_df = tde_cat[['All XMM Data (#obs: ObsIDs, exp date [yyyy-mm-dd], exp dur [sec])'
                         , 'All Chandra Data (#obs: ObsIDs, exp date [yyyy-mm-dd], exp dur [sec], detector)'
                        ]
                       ]

xray_dat = pd.DataFrame(xray_df.to_numpy().flatten()).dropna()


def get_exp_times(df):
    all_exp_times = []

    for item in df[0]:
        # print(item)

        item = item.split(':')[1]
        # print(item)

        items = item.split('),')
        # print(items)

        items = [x for x in items if x!='']
        # print(items)

        exp_times = []

        for i,element in enumerate(items):
            # print(element)
            exp_times.append( float(element.split(',')[1]) )

        # print(exp_times)

        # break

        all_exp_times += exp_times

        # print('\n')
        # print(all_exp_times)
        # print('\n')

    # print(len(all_exp_times), all_exp_times)
    # print(f'min exp time = {min(all_exp_times)}; max exp time = {max(all_exp_times)}')
    return all_exp_times

all_exp_times = get_exp_times(xray_dat)


fitted_df = tde_cat.iloc[[3,5,7]]
fitted_xray_df = fitted_df[['All XMM Data (#obs: ObsIDs, exp date [yyyy-mm-dd], exp dur [sec])'
                         , 'All Chandra Data (#obs: ObsIDs, exp date [yyyy-mm-dd], exp dur [sec], detector)'
                        ]
                       ]
fitted_xray_dat = pd.DataFrame(fitted_xray_df.to_numpy().flatten()).dropna()
fitted_exp_times = get_exp_times(fitted_xray_dat)


priority_tdes_df = tde_cat.iloc[priority_tdes]
priority_tdes_df


# Code for getting colors from matplotlib default color cycle
prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']


def plot_z_vs_exp_t(df, color=colors[0], linestyle='solid', linewidth=2):
    
    for index, row in df.iterrows():
        # print(row['z'])
        # print(row[['All XMM Data (#obs: ObsIDs, exp date [yyyy-mm-dd], exp dur [sec])'
        #                      , 'All Chandra Data (#obs: ObsIDs, exp date [yyyy-mm-dd], exp dur [sec], detector)'
        #                     ]
        #                    ])

        exp_t_df = row[['All XMM Data (#obs: ObsIDs, exp date [yyyy-mm-dd], exp dur [sec])'
                             , 'All Chandra Data (#obs: ObsIDs, exp date [yyyy-mm-dd], exp dur [sec], detector)'
                            ]
                           ]

        z = row['z']

        exp_t_df = pd.DataFrame( exp_t_df.to_numpy().flatten() ).dropna() 

        exp_times = get_exp_times(exp_t_df)
        # print(exp_times)

        zs = [z]*len(exp_times)
        # print(zs)
        
        plt.plot(zs, exp_times, c=color, linestyle=linestyle, linewidth=linewidth)
        # plt.scatter(zs, exp_times, c=color, linestyle=linestyle, linewidth=linewidth)
        
        # Plotting ticks for median values for each exp time range
        # plt.scatter(z, np.median(exp_times), marker='+'
        #             , c=color, linestyle=linestyle, linewidth=linewidth)
        
        # Plotting ticks for extrema for each exp time range
        if exp_times != []:
            # print(np.amax(exp_times), np.amin(exp_times))
            plt.scatter(z, np.amax(exp_times), marker='_'
                        , c=color, linestyle=linestyle, linewidth=linewidth
                       )
            plt.scatter(z, np.amin(exp_times), marker='_'
                        , c=color, linestyle=linestyle, linewidth=linewidth
                       )

        # print('\n')
        # break

        
### Plotting
fig, ax = plt.subplots(
                       # figsize=(12,8)
                      )


# plot_z_vs_exp_t(tde_cat
#                , linewidth=4 
#                )

# plot_z_vs_exp_t(priority_tdes_df, colors[2]
#                 # , linestyle='dotted'
#                 , linewidth=4 )
    
# plot_z_vs_exp_t(fitted_df, colors[3]
#                , linewidth=4
#                )

plot_z_vs_exp_t(tde_cat, color='grey'
               # , linewidth=4 
               )

plot_z_vs_exp_t(priority_tdes_df, colors[2]
                # , linestyle='dotted'
                # , linewidth=4 
               )
    
plot_z_vs_exp_t(fitted_df, colors[3]
               # , linewidth=4
               )

# print(fitted_df.Name.iloc[0], '\n', min(get_exp_times(pd.DataFrame(fitted_xray_df.iloc[0].to_numpy().flatten()).dropna())))

# plt.plot([0.01*i for i in range(40)], f([0.01*i for i in range(40)])
#           , ls='-.', c='k')

# plt.plot([0.01*i for i in range(40)], g([0.01*i for i in range(40)])
#           , ls='-.', c='grey')

# plt.plot([0.01*i for i in range(40)], quadratic_curve_fitted([0.01*i for i in range(40)])
#         , ls='-', c='k'
#         )

# ax.set_title('Exposure Time Range Vs Redshift')

ax.set_xlabel(f'Redshift', fontsize=12
              # , fontweight='bold'
             )
ax.set_ylabel('Exposure Time Range [sec]', fontsize=12
              # , fontweight='bold'
             )
# ax.tick_params(size=10)


# ax.grid(axis='y')
# ax.set_facecolor('#d8dcd6')
ax.set_xlim(-0.01,0.375)
# ax.set_xlim(0,0.02)
ax.set_ylim(1000,2e5)
ax.set_xticks([0.05*i for i in range(8)], fontsize=14)
ax.set_yticks([1000*(10**i) for i in range(3)], fontsize=14)

# ax.set_xscale('log')
ax.set_yscale('log')

# plt.fill_between([0.01*i for i in range(40)], quadratic_curve_fitted([0.01*i for i in range(40)])
#                 , y2=0, where=None, interpolate=False, step=None, data=None, color='pink')

# plt.text(0.4,20
#          , fr'$\mu={round(z_mean,3)},\; \sigma={round(z_std,3)},\; \sigma^2={round(z_var,3)}$'
#         )

# fitted_str = '\n'.join(str(e) for e in list(fitted_df[['Name','z']].to_numpy().flatten()))
# print(fitted_str)

# plt.text(0.2,2.5e3
#          , f'{fitted_str}'
#         )

# plt.axvline(z_mean, color='k', linestyle='dotted', linewidth=4)

# plt.axvline(z_mean+z_std, color='k', linestyle='dotted', linewidth=2)
# plt.axvline(z_mean-z_std, color='k', linestyle='dotted', linewidth=2)
# plt.axvline(z_mean+2*z_std, color='k', linestyle='dotted', linewidth=2)
# plt.axvline(z_mean+3*z_std, color='k', linestyle='dotted', linewidth=2)

# for z in tde_cat.z.iloc[[3,5,7,9]]:
#     plt.axvline(z, color='k', linestyle='dotted', linewidth=2)

# plt.show()

if file_save == True:
    plt.savefig('tde_exp_times_vs_redshift.pdf', format='pdf')