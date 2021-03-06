# !pip install selenium
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# PATH = "C:\Program Files (x86)\chromedriver.exe"
PATH = "dati_donne_indicatori_stati/global gender gap 2019/chromedriver.exe"
driver = webdriver.Chrome(PATH)

ISL = driver.get("https://reports.weforum.org/global-gender-gap-report-2020/dataexplorer/#economy=ISL")
ISL

# al posto di: alpha3_db = pd.read_csv("alpha3code_states.csv")
url = "https://www.iban.com/country-codes"
dfs = pd.read_html(url)
table = dfs[0]
table
final = pd.DataFrame(data=table)
final.drop(['Alpha-2 code', 'Numeric'], axis=1, inplace=True)
final
alpha3_db = final

alpha3_db.head()

# take only the column with the code
alpha3_code_states = alpha3_db["Alpha-3 code"].to_list()

alpha3_code_states[2]

# instantiate an empty dataframe
dfObj = pd.DataFrame()

dfObj

for code in alpha3_code_states:
    try:
        driver.get(f"https://reports.weforum.org/global-gender-gap-report-2020/dataexplorer/#economy={code}")
        
        # find the right element
        first = driver.find_element_by_css_selector('#content-final > div > div > div:nth-child(3) > div.sc-bMVAic.Unojw')
        # split the text
        country_list_item = first.text.split("\n")
        # convert to dataframe and transpose
        tmp = pd.DataFrame(data=country_list_item).transpose()
        # append to the dataframe
        dfObj = dfObj.append(tmp)
        
        print("This is: ", f"{code}")
    except:
        print("Not found.")

# store the original dataset obtained
# to avoid errors and the need to call the website again
dfObj_original = dfObj

# work over a copy of the original object
dfObj_copy = dfObj.copy()

dfObj_copy.head()

# rename columns
dfObj_copy.rename(columns = {0:'country', 7:'score'}, inplace = True)

dfObj_copy.head()

# drop uninteresting columns
dfObj_copy.drop([1, 2, 3, 4, 5, 6], axis = 1, inplace = True)

dfObj_copy.head()

exporting_to_csv = dfObj_copy.to_csv("dati_donne_indicatori_stati/global gender gap 2019/gender_gap_2019_original.csv", index=False)

# close just the tab
driver.close()
# close the entire browser
driver.quit()