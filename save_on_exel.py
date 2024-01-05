import re

import pandas as pd
from ast import literal_eval

df = pd.read_csv('result_output/electronic_store_outputs.csv', converters={'outputs': literal_eval})

result_df = pd.DataFrame(columns=['name', 'website', 'phones', 'social', 'count'])

for index, row in df.iterrows():
    name = row['outputs']['name']
    website = row['outputs']['website']
    phones = ','.join(map(str, row['outputs']['phone'])).replace("'", "").replace("[", "").replace("]", "").replace("Показать телефон", "")

    social = ' /// '.join(map(str, row['outputs']['social']))

    count = df[df['outputs'].apply(lambda x: x['name'] == name)].shape[0]

    result_df = pd.concat([result_df, pd.DataFrame(
        {'name': [name], 'website': [website], 'phones': [phones], 'social': [social], 'count': [count]})])

result_df = result_df.drop_duplicates(subset='name')

result_df.to_excel('результат.xlsx', index=False, engine='openpyxl')