# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 19:21:15 2023

@author: erinp
"""

import pandas as pd
import numpy as np

# Import files
wage_by_occupation = pd.read_excel('C:/Users/erinp/Documents/Grad School/Term 5 2023 Spring/470.708 Unleashing Open Data with Python/Final Project/Project Proposal/Data Source Ideas/Wage by Occupation state_M2021_dl.xlsx')
# note summary stats are for all raw data, but wage by occupation was used in analysis based on Texas values only for comparability with ibc data

ibc = pd.read_excel('C:/Users/erinp/Documents/Grad School/Term 5 2023 Spring/470.708 Unleashing Open Data with Python/Final Project/Project Proposal/Data Source Ideas/industry-based-certifications-earned-by-graduates-from-2017-thru-2021.xlsx', skiprows=2)
ibc.drop(ibc.tail(3).index,inplace=True) # drop last 3 rows

soc_cluster_crosswalk = pd.read_excel('C:/Users/erinp/Documents/Grad School/Term 5 2023 Spring/470.708 Unleashing Open Data with Python/Final Project/Project Proposal/Data Source Ideas/Perkins_IV_Crosswalk_Table_5_SOC-ONET-Nontrad-Cluster-Pathway.xlsx')

# get number of observations
len(wage_by_occupation)
len(ibc)
len(soc_cluster_crosswalk)

# get number of variables
len(wage_by_occupation.columns)
len(ibc)
len(soc_cluster_crosswalk)

# get summary statistics

# coerce variables to numeric for summary stats since there are some non-numeric values
wage_by_occupation['TOT_EMP'] = pd.to_numeric(wage_by_occupation['TOT_EMP'],errors='coerce')
wage_by_occupation['JOBS_1000'] =  pd.to_numeric(wage_by_occupation['JOBS_1000'],errors='coerce')
wage_by_occupation['H_MEAN'] = pd.to_numeric(wage_by_occupation['H_MEAN'],errors='coerce')
wage_by_occupation['A_MEAN'] =  pd.to_numeric(wage_by_occupation['A_MEAN'],errors='coerce')
wage_by_occupation['H_MEDIAN'] = pd.to_numeric(wage_by_occupation['H_MEDIAN'],errors='coerce')
wage_by_occupation['A_MEDIAN'] =  pd.to_numeric(wage_by_occupation['A_MEDIAN'],errors='coerce')

wage_by_occupation[['TOT_EMP','JOBS_1000','H_MEAN','A_MEAN','H_MEDIAN','A_MEDIAN']].mean()
wage_by_occupation[['TOT_EMP','JOBS_1000','H_MEAN','A_MEAN','H_MEDIAN','A_MEDIAN']].median()
wage_by_occupation[['TOT_EMP','JOBS_1000','H_MEAN','A_MEAN','H_MEDIAN','A_MEDIAN']].std()

ibc['Graduates 2017'] = pd.to_numeric(ibc['Graduates 2017'],errors='coerce')
ibc['Graduates 2018'] = pd.to_numeric(ibc['Graduates 2018'],errors='coerce')
ibc['Graduates 2019'] = pd.to_numeric(ibc['Graduates 2019'],errors='coerce')
ibc['Graduates 2020'] = pd.to_numeric(ibc['Graduates 2020'],errors='coerce')
ibc['Graduates 2021'] = pd.to_numeric(ibc['Graduates 2021'],errors='coerce')


ibc[['Graduates 2017', 'Graduates 2018', 'Graduates 2019', 'Graduates 2020', 'Graduates 2021']].mean()
ibc[['Graduates 2017', 'Graduates 2018', 'Graduates 2019', 'Graduates 2020', 'Graduates 2021']].median()
ibc[['Graduates 2017', 'Graduates 2018', 'Graduates 2019', 'Graduates 2020', 'Graduates 2021']].std()



# which industry-based credentials are gaining popularity (by number of graduates earning IBCs) in Texas?

# rearrange columns so Graduates are at the end
ibc_cols = list(ibc.columns)
ibc_cols = ibc_cols[0:3] + ibc_cols[8:11] + ibc_cols[3:8]
ibc = ibc[ibc_cols]

# replace <5 values with null
ibc = ibc.replace('<5', np.NaN)

# find rightmost grads column as most recent
ibc['Most Recent Graduates'] = ibc.ffill(axis=1).iloc[:, -1]

# find leftmost grads column as least recent
ibc['Least Recent Graduates'] = ibc.iloc[:,6:11].fillna(method='bfill', axis=1).iloc[:, 0]

# calculate growth
ibc['IBC Growth'] = ibc['Most Recent Graduates'] - ibc['Least Recent Graduates']
ibc = ibc.sort_values('IBC Growth', ascending = False)

# graph dotplot to show growth for top IBCs
import plotly.express as px
import plotly.io as pio
#pio.renderers.default = 'svg'
pio.renderers.default = 'browser' # show in browser

# get only rows for top 20
ibc_top20 = ibc[0:20]

# convert to long data
ibc_names = ibc_top20['Industry-Based Certification (IBC) Name'].tolist()
ibc_most_recent = ibc_top20['Most Recent Graduates'].tolist()
ibc_least_recent = ibc_top20['Least Recent Graduates'].tolist()
n_ibcs = len(ibc_top20['Industry-Based Certification (IBC) Name'])

ibc_long = pd.DataFrame(dict(ibc_name=ibc_names*2,
                             graduates = ibc_most_recent + ibc_least_recent,
                              timing = ["Most Recent Graduates"]*n_ibcs
                             + ["Least Recent Graduates"]*n_ibcs))

# Use column names of df for the different parameters x, y, color
top_ibc_growth = px.scatter(ibc_long, x="graduates", y="ibc_name", color="timing",
                 title="Top 20 IBCs by Change in Number of Graduates",
                 labels={"graduates":"Number of Graduates",
                         "ibc_name":"Industry-Based Certification Name",
                         "timing":"Timing"} # customize axis label
                )


top_ibc_growth.update_traces(marker=dict(size=15))
top_ibc_growth.update_layout(
    font=dict(size=24))

top_ibc_growth.show()

# which IBCs are losing popularity (by number of graduates earning IBCs) in Texas?
# get row number of last available growth number, - 496 after resetting index
ibc = ibc.reset_index(drop=True)
ibc[ibc['IBC Growth'] == -496].index # index is 161 for the IBC losing the most number of graduates

# get row number of first available negative growth, -1
ibc[ibc['IBC Growth'] == -1].index # first index is 122

# if we just want to look at the bottom 20, the index would be 142

# get only bottom 20 rows with negative growth
ibc_bottom20 = ibc[142:162]

# convert to long data
ibc_names_bottom = ibc_bottom20['Industry-Based Certification (IBC) Name'].tolist()
ibc_most_recent_bottom = ibc_bottom20['Most Recent Graduates'].tolist()
ibc_least_recent_bottom = ibc_bottom20['Least Recent Graduates'].tolist()
n_ibcs_bottom = len(ibc_bottom20['Industry-Based Certification (IBC) Name'])

ibc_long_bottom = pd.DataFrame(dict(ibc_name=ibc_names_bottom*2,
                             graduates = ibc_most_recent_bottom + ibc_least_recent_bottom,
                              timing = ["Most Recent Graduates"]*n_ibcs_bottom
                             + ["Least Recent Graduates"]*n_ibcs_bottom))

# Use column names of df for the different parameters x, y, color
top_ibc_loss = px.scatter(ibc_long_bottom, x="graduates", y="ibc_name", color="timing",
                 title="Bottom 20 IBCs by Change in Number of Graduates",
                 labels={"graduates":"Number of Graduates",
                         "ibc_name":"Industry-Based Certification Name",
                         "timing":"Timing"} # customize axis label
                )


top_ibc_loss.update_traces(marker=dict(size=15))
top_ibc_loss.update_layout(
    font=dict(size=24))

top_ibc_loss.show()


# What career clusters (i.e. groups of occupations) are associated with the most popular industry-based credentials?

ibc_top20_grouped = ibc_top20.groupby(['Primary State Career Cluster']).agg({'Status':'count',
                                                                 'Industry-Based Certification (IBC) Name':'count',
                                                                 'Graduates 2017':'sum','Graduates 2018':'sum', 
                                                                 'Graduates 2019':'sum', 'Graduates 2020':'sum',
                                                                 'Graduates 2021':'sum', 'Most Recent Graduates': 'sum',
                                                                 'Least Recent Graduates': 'sum',
                                                                 'IBC Growth':'sum'})
# rename column status to indicate retired/sunsetting
ibc_top20_grouped = ibc_top20_grouped.rename(columns={'Status':'Retired or Sunsetting'})

# add column with count of active IBCs by subtracting retired or sunsetting from count of IBC names
ibc_top20_grouped['Active'] = ibc_top20_grouped['Industry-Based Certification (IBC) Name'] - ibc_top20_grouped['Retired or Sunsetting']

# sort values by Growth
ibc_top20_grouped = ibc_top20_grouped.sort_values('IBC Growth', ascending = False)

# reset index so Primary State Career Cluster is its own column
ibc_top20_grouped = ibc_top20_grouped.reset_index()

# create stacked bar chart by cluster
top20_ibc_cluster_by_status = px.bar(ibc_top20_grouped, x ="Primary State Career Cluster", 
                                     y =["Retired or Sunsetting", "Active"],
                                     title = "Number of IBCs by Career Cluster within Largest-Growth IBCs",
                                     labels = {"value":"Number of Industry-Based Credentials",
                                               "variable":"IBC Status"})

top20_ibc_cluster_by_status.update_layout(
    yaxis={'tickvals':[*range(0,5)]},
    xaxis={'categoryorder':'total descending'},
    font=dict(size=24))

top20_ibc_cluster_by_status.show()


# group the full data on Primary State Career Cluster for merging with wages/employment

# remove nas before grouping
# get row numbers of nan values for IBC growth
np.where(ibc['IBC Growth'].isnull())[0] #162

ibc_notnull = ibc[0:162]

ibc_cluster = ibc_notnull.groupby(['Primary State Career Cluster']).agg({'Status':'count',
                                                                 'Industry-Based Certification (IBC) Name':'count',
                                                                 'Graduates 2017':'sum','Graduates 2018':'sum', 
                                                                 'Graduates 2019':'sum', 'Graduates 2020':'sum',
                                                                 'Graduates 2021':'sum','Most Recent Graduates': 'sum',
                                                                 'Least Recent Graduates': 'sum',
                                                                 'IBC Growth':'sum'})

# rename column status to indicate retired/sunsetting
ibc_cluster = ibc_cluster.rename(columns={'Status':'Retired or Sunsetting'})

# add column with count of active IBCs by subtracting retired or sunsetting from count of IBC names
ibc_cluster['Active'] = ibc_cluster['Industry-Based Certification (IBC) Name'] - ibc_cluster['Retired or Sunsetting']

# sort values by Growth
ibc_cluster = ibc_cluster.sort_values('IBC Growth', ascending = False)

# reset index so Primary State Career Cluster is its own column
ibc_cluster = ibc_cluster.reset_index()

# create stacked bar chart by cluster
all_ibc_cluster_by_status = px.bar(ibc_cluster, x ="Primary State Career Cluster", 
                                     y =["Retired or Sunsetting", "Active"],
                                     title = "Overall Number of IBCs by Career Cluster",
                                     labels = {"value":"Number of Industry-Based Credentials",
                                               "variable":"IBC Status"})

all_ibc_cluster_by_status.update_layout(
    xaxis={'categoryorder':'total descending'},
    yaxis={'dtick':5, 'tickmode':'array',
           'tickvals':[5, 10, 15, 20, 25, 30, 35, 40],},
    yaxis_range=[0,45],
    font=dict(size=20))

all_ibc_cluster_by_status.update_yaxes(nticks=20)

all_ibc_cluster_by_status.show()


# top 5 clusters by growth overall are 1) Business, Marketing and Finance, 
# 2) Manufacturing, 3) Health Science, 4) Agriculture, Food and Natural Resources, and
# 5) Information Technology

# Human services is the only cluster that experienced a decrease in graduates over the same timeframe

# merge cluster information with wage information
# change name of OCC_CODE to match crosswalk table
wage_by_occupation = wage_by_occupation.rename(columns={'OCC_CODE':'SOC CODE'})

wage_merged = pd.merge(wage_by_occupation, soc_cluster_crosswalk[['SOC CODE', 
                                                                  'SOC Career Clstr No', 
                                                                  'SOC_Career Clusters', 
                                                                  'SOC PTHWY NO', 'SOC_PTHWYTITL']], 
                       on='SOC CODE', how='left')

# subset to Texas only for comparability with ibc data
wage_merged_tx = wage_merged[wage_merged['PRIM_STATE']=='TX']

# note that energy and information technology are in TX IBC data but not Federal wage data
# Government & Public Admin is in Federal wage but not TX IBC data

# replace Business Management & Administration, Finance & Marketing into one Business, Marketing and Finance category
# update other names as necessary

clusters_to_replace =  { 
    'Agriculture, Food & Natural Resources' : 'Agriculture, Food and Natural Resources',
    'Architecture & Construction' : 'Architecture and Construction',
    'Arts, Audio/Video Technology & Communications' : 'Arts, Audio Visual Technology and Communication',
    'Business Management & Administration' : 'Business, Marketing and Finance', 
    'Finance' : 'Business, Marketing and Finance', 
    'Marketing' : 'Business, Marketing and Finance',
    'Education & Training': 'Education and Training',
    'Health Science': 'Health Science',
    'Hospitality & Tourism' : 'Hospitality and Tourism',
    'Human Services': 'Human Services',
    'Law, Public Safety, Corrections & Security' : 'Law and Public Service',
    'Manufacturing': 'Manufacturing',
    'Science, Technology, Engineering & Mathematics': 'Science, Technology, Engineering and Mathematics',
    'Transportation, Distribution & Logistics': 'Transportation, Distribution and Logistics'
}

wage_merged_tx = wage_merged_tx.replace({'SOC_Career Clusters': clusters_to_replace})

# replace * and # values with null
wage_merged_tx = wage_merged_tx.replace('*', np.NaN)
wage_merged_tx = wage_merged_tx.replace('#', np.NaN)

# group by cluster like ibc
wage_cluster = wage_merged_tx.groupby(['SOC_Career Clusters']).agg({'TOT_EMP':'sum', 'H_MEDIAN':'median',
                                                                    'H_PCT25':'median',
                                                                    'H_PCT75':'median',
                                                                    'A_MEDIAN':'median',
                                                                    'A_PCT25':'median',
                                                                    'A_PCT75':'median'
                                                                    })

# reset index so clusters becomes its own column
wage_cluster = wage_cluster.reset_index()

# change name of column for merging
wage_cluster = wage_cluster.rename(columns={'SOC_Career Clusters':'Primary State Career Cluster'})


# merge popularity information
ibc_wage_cluster = pd.merge(ibc_cluster, wage_cluster, 
                       on='Primary State Career Cluster', how='left')
# look at growth as a rate instead of absolute numbers to account for industry size
ibc_wage_cluster['IBC Growth Rate'] = ibc_wage_cluster['IBC Growth']/ibc_wage_cluster['Least Recent Graduates'] * 100

# make all cols numeric
ibc_wage_cluster_cols = [i for i in ibc_wage_cluster.columns if i not in ['Primary State Career Cluster']]

for col in ibc_wage_cluster_cols:
    ibc_wage_cluster[col]=pd.to_numeric(ibc_wage_cluster[col])

import statsmodels.formula.api as smf

popularity_lin_model =smf.ols('Q("IBC Growth Rate") ~ A_MEDIAN + TOT_EMP', data=ibc_wage_cluster)

popularity_results = popularity_lin_model.fit()

popularity_results.summary()

# run model for likelihood of IBC being retired

# first create column with proportion of retired IBCs
ibc_wage_cluster['Proportion Retired or Sunsetting'] = ibc_wage_cluster['Retired or Sunsetting'] / ibc_wage_cluster['Industry-Based Certification (IBC) Name']*100

retired_lin_model =smf.ols('Q("Proportion Retired or Sunsetting") ~ A_MEDIAN + TOT_EMP', data=ibc_wage_cluster)

retired_results = retired_lin_model.fit()

retired_results.summary()

# both models have data limitations and don't yield much information
# the code is included for transparency on the analytical process

# scatterplots can visualize the relationship (or lack thereof)
popularity_wage = px.scatter(ibc_wage_cluster, x="A_MEDIAN", y="IBC Growth Rate", 
                             text="Primary State Career Cluster", size_max=60,
                             labels={"A_MEDIAN": "Median Annual Salary",
                                     "IBC Growth Rate":"IBC Growth Rate (%)"})

popularity_wage.update_traces(textposition='top center',
                              marker = dict(size=14)
                              )

popularity_wage.update_layout(
    autosize=True,
    title_text='IBC Growth Rate by Median Annual Salary and Career Cluster',
    font=dict(size=20),
    xaxis_range=[20000, 100000],
    yaxis_range=[-50, 1000]
)

popularity_wage.show()

# popularity (rate in growth) by size
popularity_rate_size = px.scatter(ibc_wage_cluster, x="TOT_EMP", y="IBC Growth Rate", 
                             text="Primary State Career Cluster", size_max=60,
                             labels={"TOT_EMP": "Total Employment in Career Cluster",
                                     "IBC Growth Rate":"IBC Growth Rate (%)"})

# fix label positioning
def set_text_position(cluster):
    if cluster in ['Transportation, Distribution and Logistics']:
        return 'middle right'
    else:
        return 'top center'

popularity_rate_size.update_traces(textposition=list(map(set_text_position,
                                                         ibc_wage_cluster['Primary State Career Cluster'])),
                              marker = dict(size=14)
                              )

popularity_rate_size.update_layout(
    autosize=True,
    title_text='IBC Growth Rate by Total Employment in Career Cluster',
    font=dict(size=18),
    xaxis_range=[-600000, 4200000],
    yaxis_range=[-50, 910]
)

popularity_rate_size.show()




# sunset by earnings

sunset_wage = px.scatter(ibc_wage_cluster, x="A_MEDIAN", y="Proportion Retired or Sunsetting", 
                             text="Primary State Career Cluster", size_max=60,
                             labels={"A_MEDIAN": "Median Annual Salary",
                                     "Proportion Retired or Sunsetting":"Proportion of IBCs Retired or Sunsetting (%)"})

# fix label positioning
def set_text_position(cluster):
    if cluster in ['Agriculture, Food and Natural Resources']:
        return 'middle right'
    else:
        return 'top center'

sunset_wage.update_traces(textposition=list(map(set_text_position,
                                                ibc_wage_cluster['Primary State Career Cluster'])),
                              marker = dict(size=14)
                              )

sunset_wage.update_layout(
    autosize=True,
    title_text='Proportion of IBCs Retired or Sunsetting by Median Annual Salary and Career Cluster',
    font=dict(size=18),
    xaxis_range=[20000, 100000],
    yaxis_range=[-10, 100]
)

sunset_wage.show()

# sunset by size
sunset_size = px.scatter(ibc_wage_cluster, x="TOT_EMP", y="Proportion Retired or Sunsetting", 
                             text="Primary State Career Cluster", size_max=60,
                             labels={"TOT_EMP": "Total Employment in Career Cluster",
                                     "Proportion Retired or Sunsetting":"Proportion of IBCs Retired or Sunsetting (%)"})

# fix label positioning
def set_text_position(cluster):
    if cluster in ['Agriculture, Food and Natural Resources']:
        return 'bottom center'
    elif cluster in ['Education and Training']:
        return 'bottom right'
    elif cluster in ['Arts, Audio Visual Technology and Communication', 'Manufacturing', 'Health Science', 
                     'Hospitality and Tourism']:
        return 'middle right'
    else:
        return 'top center'

sunset_size.update_traces(textposition=list(map(set_text_position,
                                                ibc_wage_cluster['Primary State Career Cluster'])),
                              marker = dict(size=14)
                              )

sunset_size.update_layout(
    autosize=True,
    title_text='Proportion of IBCs Retired or Sunsetting by Total Employment in Career Cluster',
    font=dict(size=18),
    xaxis_range=[-500000, 4200000],
    yaxis_range=[-10, 100]
)

sunset_size.show()
