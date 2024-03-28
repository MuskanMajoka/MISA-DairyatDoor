from retrievedata import firestore_db

# add data by manufacturer
new_machine = {}


new_machine['automation'] = input()
new_machine['bowlspeed'] = input()
new_machine['capacity'] = input()
new_machine['company'] = input()
new_machine['cost'] = input()
new_machine['material'] = input()
new_machine['presenceOfRubberSeals'] = input()
new_machine['product'] = input()
new_machine['Reliability'] = input()
new_machine['Safety Efficiency'] = input()
new_machine['size'] = input()
new_machine['Sludge Removal Efficiency'] = input()
new_machine['Type'] = input()
new_machine['voltageSupplyNeeded'] = input()

firestore_db.collection(u'dairy_project').add(
    {'automationGrade': new_machine['automation'],
     'bowlSpeed': new_machine['bowlspeed'],
     'capacity': new_machine['capacity'],
     'company': new_machine['company'],
     'cost': new_machine['cost'],
     'material': new_machine['material'],
     'presenceOfRubberSeals': new_machine['presenceOfRubberSeals'],
     'product': new_machine['product'],
     'reliability': new_machine['Reliability'],
     'safetyEfficiency': new_machine['Safety Efficiency'],
     'size': new_machine['size'],
     'sludgeRemovalEfficiency': new_machine['Sludge Removal Efficiency'],
     'type': new_machine['Type'],
     'voltageSupplyNeeded': new_machine['voltageSupplyNeeded']})

from modelforadddata import com_val

firestore_db.collection(u'Recommendation_table').add(
    {
        'product': com_val['Product'],
        'count': com_val['Count']
    })

firestore_db.collection(u'Recommendation_table1').add(
    {'automationGrade': new_machine['automation'],
     'bowlSpeed': new_machine['bowlspeed'],
     'capacity': new_machine['capacity'],
     'company': new_machine['company'],
     'cost': new_machine['cost'],
     'material': new_machine['material'],
     'presenceOfRubberSeals': new_machine['presenceOfRubberSeals'],
     'product': new_machine['product'],
     'reliability': new_machine['Reliability'],
     'safetyEfficiency': new_machine['Safety Efficiency'],
     'size': new_machine['size'],
     'sludgeRemovalEfficiency': new_machine['Sludge Removal Efficiency'],
     'type': new_machine['Type'],
     'voltageSupplyNeeded': new_machine['voltageSupplyNeeded'],
     'count': com_val['Count']})

# df.to_dict('records')   df.T.to_dict().values()  dataframe to list of dictionary
