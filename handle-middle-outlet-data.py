import numpy as np
import pandas as pd
import os

pd.set_option('display.max_columns', None)

# read the data
os.chdir('D:/code/python/vaxjo')
df = pd.read_excel("mitt-utlopp-data-point.xlsx")

# group the data by month
grouped = df.groupby("year_month")
# lists to store new data
new_data = []

# list of columns that should be checked for null values
columns_to_check = ['Temperatur', 'Siktdjup_m', 'Klorofyll_µg_l', 'pH', 'Alkalinitet_mekv_l',
                    'Syrgashalt_mg_l', 'Syrem', 'Nitrigen', 'fosfor']

# iterate through each group
for year_month, group in grouped:
    # get the rows where station is middle
    middle = group[group["Övervakningsstation"] == "Växjösjön mitt"]
    
    if middle.empty:
        # if no middle station data for month, use outlet data
        outlet = group[group["Övervakningsstation"] == "Växjösjön utlopp"]
        new_row = outlet.iloc[0].copy()
        new_row["Stationskoordina_N_X"] = float(56.867805)
        new_row["Stationskoordina_E_Y"] = float(14.81321)
        new_row["Övervakningsstation"] = "Växjösjön"
    #elif middle.size == 18:
    elif middle.shape[0] == 1:
        new_row = middle.iloc[0].copy()
        new_row["Övervakningsstation"] = "Växjösjön"
    elif middle.shape[0] > 1:
        new_row = middle.iloc[0].copy()  
        # if new_row['year_month'] == "2000-10":
        #     print(new_row)
        for col in columns_to_check:
            mean_array = []
            for i in range(0, middle.shape[0]):
                middle_row = middle.iloc[i]
                if middle_row[col]:
                    mean_array.append(middle_row[col])
                # if new_row['year_month'] == "2000-10":
                #     print(mean_array)
            new_row[col] = np.nanmean(mean_array)
            if new_row['year_month'] == "2000-10":
                print(new_row[col])
        new_row["Övervakningsstation"] = "Växjösjön"
        # if new_row['year_month'] == "2000-10":
        #     print(new_row)
    else:
        # otherwise use the middle station data
        new_row = middle.iloc[0].copy()
        new_row["Övervakningsstation"] = "Växjösjön"
    if new_row[columns_to_check].isnull().any().any():
        # if middle station data has null values in the specified columns, use outlet data to fill in
        outlet = group[group["Övervakningsstation"] == "Växjösjön utlopp"]
        if (outlet.empty == False):
            for col in columns_to_check:
                # print(new_row[col])
                if pd.isnull(new_row[col]):
                    new_row[col] = outlet[col].values[0]

    new_data.append(new_row)

# print(new_data)
# create new dataframe with new data
new_df = pd.DataFrame(
    new_data, columns=['PROVPUNKT_Original', 'St_Original', 'Datum', 'Temperatur', 'Siktdjup_m',
                       'Klorofyll_µg_l', 'pH', 'Alkalinitet_mekv_l', 'Syrgashalt_mg_l', 'Syrem',
                       'Nitrigen', 'fosfor', 'Övervakningsstation', 'Stationskoordina_N_X', 'Stationskoordina_E_Y',
                       'Year', 'year_month'])
# print(new_df)


# write new data to csv file
new_df.to_excel("new_data-2.xlsx", index=False)
