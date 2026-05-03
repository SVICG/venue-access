import os
import pandas as pd

#load data folders
data_folder = '../data/raw/'
output_folder = '../data/processed'
data_file = 'MYE24_SDZ.xlsx'

data_file_path = os.path.join(data_folder, data_file)

#extract correct sheet from Excel file
pop_df = pd.read_excel(data_file_path, sheet_name='Flat')

#filter data by year, sex and age
pop_filtered = pop_df.loc[
    (pop_df['Year'] == 2024) &
    (pop_df['Sex']=='All Persons') &
    (pop_df['Age']=='All ages')]

#save file as csv
output_file = 'PopulationData.csv'
pop_filtered.to_csv(os.path.join(output_folder, output_file))