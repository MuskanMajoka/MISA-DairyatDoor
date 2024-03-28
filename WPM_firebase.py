## model

# Importing the libraries
import pandas as pd

url = 'https://drive.google.com/file/d/1wGtSJ-wcPelglvXSD32_Aq7YIqag3Eb8/view?usp=sharing'
path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
df1 = pd.read_csv(path)

# define the weight function
def wval(temp_w):
    temp_wv = 0
    if temp_w == 'Safety Efficiency':
        temp_wv = 1.86
    elif temp_w == 'Sludge removal efficiency':
        temp_wv = 0.323
    elif temp_w == 'Type':
        temp_wv = 0.465
    elif temp_w == 'Reliability':
        temp_wv = 1.182

    return temp_wv


# define the val function
def val(temp_f):
    temp_v = 0
    x = {'High', 'Small', 'Tri-purpose', 'Stainless Steel', 'Automatic'}
    y = {'Moderate', 'Hermetic', 'Steel', 'Standard', 'Semi-Automatic'}
    z = {'Open', 'Low', 'Large', 'Aluminium', 'Manual', 'No'}
    w = {'NAN', 'Nil', 'Yes', 'NULL'}
    if temp_f in x:
        temp_v = 3
    elif temp_f in y:
        temp_v = 2
    elif temp_f in z:
        temp_v = 1
    elif temp_f in w:
        temp_v = 0
    else:
        temp_v = 0

    return temp_v


# input by the user
req_dict = {'Capacity': [], 'Automation': [], 'Cost': []}

a = input("\nEnter the Capacity required: ")
req_dict['Automation'] = input("Enter the Automation required: ")
req_dict['Capacity'] = int(a)

# Importing the dataset
com_val = {'Product': [], 'Count': []}
comp_list = []
product_list = []
cap_list = []
aut_list = []
cost_list = []
dff = pd.DataFrame()

for l in range(0, df1.count()[0]):
    if (req_dict['Capacity'] < df1.iloc[l]['Capacity'] or req_dict['Capacity'] == df1.iloc[l]['Capacity']) and req_dict[
        'Automation'] == df1.iloc[l]['Automation Grade']:
        comp_list.append(df1.iloc[l]['Company'])
        product_list.append(df1.iloc[l]['Product'])
        cap_list.append(df1.iloc[l]['Capacity'])
        aut_list.append(df1.iloc[l]['Automation Grade'])
        cost_list.append(df1.iloc[l]['Cost'])

dff['Company'] = comp_list
dff['Product'] = product_list
dff['Capacity'] = cap_list
dff['Automation'] = aut_list
dff['Cost'] = cost_list

sumxij_val = dict()

for k in df1[['Safety Efficiency', 'Sludge removal efficiency', 'Type', 'Reliability']]:
    sumxij = 0
    for j in range(0, df1.count()[0]):
        temp = df1.iloc[j][k]
        temp_val = val(temp)
        sumxij += temp_val
    sumxij_val[k] = int(sumxij)

for n in range(0, df1.count()[0]):
    count = 0
    for m in df1[['Safety Efficiency', 'Sludge removal efficiency', 'Type', 'Reliability']]:
        temp = df1.iloc[n][m]
        temp_val = val(temp)
        rij = temp_val/sumxij_val[m]
        weight = wval(m)
        count += (rij * weight)
    com_val['Product'].append(df1.iloc[n]['Product'])
    com_val['Count'].append(count)

df = pd.DataFrame.from_dict(com_val)
print(df)
mer1 = pd.merge(df1, df, how='left', on=['Product'])
mer1 = mer1.sort_values(by='Count', ascending=False)
#print(mer1)
#mer1.to_csv('C:/Users/Ajay Gupta/Desktop/research project/RECOMMENDATION MODEL/Recommendation_table1.csv')


mer = pd.merge(dff, df, how='left', on=['Product'])
print("Recommended Products are: ")
print("________________________")

print(mer[['Product', 'Capacity', 'Cost']].head(10))

#### more dataset needed
#### detailed datasets formation and their linking and brochures
#### store data in the mysql or any platform
#### interface with frontend
#feedback loop for the recommendation system