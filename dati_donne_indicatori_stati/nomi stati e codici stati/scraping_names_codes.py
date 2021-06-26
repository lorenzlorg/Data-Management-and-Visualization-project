import pandas as pd

url = "https://www.iban.com/country-codes"
dfs = pd.read_html(url)
table = dfs[0]
table
final = pd.DataFrame(data=table)
final.drop(['Alpha-2 code', 'Numeric'], axis=1, inplace=True)
final
exporting_to_csv = final.to_csv("alpha3code_states.csv", index=False)