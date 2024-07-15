
# # beetle genome  blastn purging 

import pandas as pd


blastn_result = pd.read_csv('blastn_raw.txt', sep = '\t')

for i in range(len(blastn_result)):
    blastn_result.loc[i, 'sno'] = i
columns = []
columns = blastn_result.columns
print(columns[2])
log = open("log.txt", "a")


def get_unique_scaffold(in_df):
    uniq_scaffold_name = []
    uniq_scaffold_name = in_df['subject id'].unique()
    grouped_df = {}

    for value in uniq_scaffold_name:
        grouped_df[value] = in_df[in_df['subject id'] == value]
        grouped_df[value] = grouped_df[value].reset_index(drop=True)
    return grouped_df, uniq_scaffold_name

scaf_df, scaffold_name = get_unique_scaffold(blastn_result)

def reversal_finder(df_iter):
    for row_1 in range(len(df_iter)):
        if df_iter.iloc[row_1][9] > df_iter.iloc[row_1][10]:
            temp_holder = df_iter.iloc[row_1][9] 
            df_iter.iloc[row_1, 9] = df_iter.iloc[row_1, 10]
            df_iter.iloc[row_1, 10] = temp_holder 
            df_iter.loc[row_1, 'order'] = 'reversed'
            df_iter.reset_index(drop=True)
    return df_iter
                        

def duplicate_finder(scaf_df, scaffold_name):
    duplicate_df = pd.DataFrame()
    nr_nested = pd.DataFrame()
    for value in scaffold_name:
        dup_rows = {}
        dup_rows[value] = []
        duplicate_row = dup_rows[value]
        df_iter = reversal_finder(scaf_df[value])
        for row_1 in range(len(df_iter)):
            for row_2 in range(len(df_iter)):
                if row_1 == row_2:
                    continue
                else:
                    if row_1 in duplicate_row:
                        continue 
                    else:
                        if (df_iter.iloc[row_1, 9] == df_iter.iloc[row_2, 9]) \
                        & (df_iter.iloc[row_1, 10] == df_iter.iloc[row_2, 10]):
                            if row_2 not in duplicate_row:
                                duplicate_row.append(row_2)
                                df_iter.loc[[row_2,row_1], 'status'] = 'replicate'
        duplicate_temp = df_iter.iloc[duplicate_row, :]
        duplicate_df = pd.concat([duplicate_df, duplicate_temp], ignore_index=True)
        temp_nested_nr = df_iter.drop(duplicate_row)
        nr_nested = pd.concat([nr_nested, temp_nested_nr], ignore_index=True)
    duplicate_df.to_csv('duplicate.csv', index = False)
    return duplicate_df, nr_nested

duplicate_df, nested_nr_df = duplicate_finder(scaf_df, scaffold_name)

scaf_df, scaffold_name =get_unique_scaffold(nested_nr_df)
def get_nr_results(scaf_df, scaffold_name):
    #print(scaffold_name)
    nested = pd.DataFrame()
    temp_df = pd.DataFrame()
    nr_data = pd.DataFrame()
    nr_ful = pd.DataFrame()
    for value in scaffold_name:
        df_iter = reversal_finder(scaf_df[value])
        #log.write(f"{value} with number of hits {len(uniq_sub[value])} processing..")
        #nested_rows = []
        nested_rows = {}
        nested_rows[value] = []
        redunt_row = nested_rows[value] 
        nr_df = {}
        for row_1 in range(len(df_iter)):
            for row_2 in range(len(df_iter)):
                if row_1 == row_2:
                    continue
                else:
                    if row_1 in redunt_row:
                        continue 
                    else:
                        if (df_iter.iloc[row_1, 9] <= df_iter.iloc[row_2, 9]) \
                        & (df_iter.iloc[row_1, 10] >= df_iter.iloc[row_2, 10]):
                            if row_2 not in redunt_row:
                                redunt_row.append(row_2)
                                df_iter.loc[row_2, 'status'] = 'nested'
        temp_df = df_iter.iloc[redunt_row, :]
        nested = pd.concat([nested, temp_df], ignore_index=True)
        nr_data = df_iter.drop(redunt_row)
        nr_ful = pd.concat([nr_ful, nr_data], ignore_index=True)
    nested.to_csv('nested.csv', index = False)
    nr_ful.to_csv('nr.csv', index = False)
    return  nr_ful, nested

nr_df, nested = get_nr_results(scaf_df, scaffold_name)

nr_df


def get_duplicate_list(nr_df):
    nr_df['q. duplicate'] = ''
    for r in range(len(duplicate_df)):
        for l in range(len(nr_df)):
            if duplicate_df.loc[r, 'subject id'] == nr_df.loc[l, 'subject id']:
                if duplicate_df.loc[r, 's. start'] == nr_df.loc[l, 's. start']: 
                    if duplicate_df.loc[r, 's. end'] == nr_df.loc[l, 's. end']:
                        nr_df.loc[l , 'q. duplicate'] += '(' + str(duplicate_df.loc[r, 'q. start']) + "-" + str(duplicate_df.loc[r, 'q. end']) + ')'
    return nr_df

nr_df.to_csv('NUMTs_nr1.csv', index = False)

nr_df = get_duplicate_list(nr_df)

replicate_nr = nr_df[nr_df.loc[:, 'status']=='replicate']


replicate_nr

# %%
nr_df['subject id'].unique()

# %%



