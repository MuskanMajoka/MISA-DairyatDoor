###display data for customer
from retrievedata import dataframe_to_import
from forms import marketform

df1 = dataframe_to_import.recommendation_table1
req_dict = {'Capacity': [], 'Automation': [], 'Cost': []}

a = input("\nEnter the Capacity required: ")
req_dict['Automation'] = input("Enter the Automation required: ")
req_dict['Capacity'] = int(a)

df1 = df1[df1['capacity'] >= req_dict['Capacity']]
df1 = df1[df1['Automation Grade'] == req_dict['Automation']]
"""
a = int(marketform.capacity.data)

df1 = df1[df1['capacity' >= a]]
df1 = df1[df1['Automation Grade' == marketform.automation.data]]

df1.sort_values(by='count', ascending=False)
df1_dict = df1.to_dict('records')
"""
print(df1[['count', 'product']])

"""
#### more dataset needed
#### detailed datasets formation and their linking and brochures
#### weight product model
#### store data in the mysql or any platform
#### interface with frontend
"""
