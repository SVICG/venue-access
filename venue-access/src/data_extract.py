import os
import pandas as pd

#load data folders
data_folder = '../data/raw/'
output_folder = '../data/processed'

data_file = 'MYE24_SDZ.xlsx'
data_file_path = os.path.join(data_folder, data_file)

pop_df = pd.read_excel(data_file_path, sheet_name='Flat')

print(pop_df.head())