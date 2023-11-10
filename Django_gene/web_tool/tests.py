import pandas as pd

data = {'column_name': ['Hellooooo564564564oooooo', 'Hellooooo564564564oooooo', 'Hellooooo564564564oooooo', 'Hellooooo564564564oooooo']}
df = pd.DataFrame(data)

# Insert '|' at positions 14 and 21 in the 'column_name' column
df['column_name'] = df['column_name'].str.slice_replace(14, 14, '|').str.slice_replace(21, 21, '|')

print(df)