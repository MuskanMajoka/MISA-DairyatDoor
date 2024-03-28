##evaluating the machine and ranking it

# Importing the libraries
import pandas as pd
from Website.adddata import new_machine

new_machine_dataframe = pd.DataFrame.from_dict(new_machine)

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


sumxij = 0
for k in new_machine_dataframe[['Safety Efficiency', 'Sludge removal efficiency', 'Type', 'Reliability']]:
    temp = new_machine_dataframe.iloc[0][k]
    temp_val = val(temp)
    sumxij += temp_val

count = 0
for m in new_machine_dataframe[['Safety Efficiency', 'Sludge removal efficiency', 'Type', 'Reliability']]:
    temp = new_machine_dataframe.iloc[0][m]
    temp_val = val(temp)
    rij = temp_val / sumxij
    weight = wval(m)
    count += (rij * weight)
com_val = {'Product': new_machine_dataframe.iloc[0]['product'], 'Count': count}


#### more dataset needed
#### detailed datasets formation and their linking and brochures
#### store data in the mysql or any platform
#### interface with frontend
