# links to work on
# https://flask.palletsprojects.com/en/2.1.x/quickstart/#
# https://github.com/jimdevops19/codesnippets

import app
from flask import render_template, redirect, url_for, flash
from retrievedata import firestore_db, dataframe_to_import, CartItem
from forms import registrationform, loginform, marketform , fodderform, vetsform, trainingform, workshopform, instituteform, ethnoform
import pandas


##scripting different pages.>
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')  # render templates handle request and request them in htl file

@app.route('/About')
def about_page():
    return render_template('home.html')  # render templates handle request and request them in htl file

@app.route('/Services')
def services_page():
    return render_template('home.html')

@app.route('/Technology')
def technology_page():
    return render_template('technology.html')

@app.route('/Fodder')
def fodder_page():
    return render_template('fodder.html')

@app.route('/HealthcareServices')
def healthcareservices_page():
    return render_template('fodder.html')

@app.route('/Education')
def study_page():
    return render_template('study.html')



@app.route('/Education/Case Study')
def case_page():
    return render_template('case.html')


@app.route('/marketsearch/<machine>/<automation>/<capacity>')
def marketsearch_page(machine, automation, capacity):
    if machine == 'Cream Separator':
        df1 = dataframe_to_import.recommendation_table1
        df1 = df1[df1['Automation Grade'] == automation]
        a = int(capacity)
        df1 = df1[df1['capacity'] >= a]
        df1.sort_values(by='count', ascending=False)
        df1_dict = df1.to_dict('records')
        items = df1_dict
        return render_template('markettable.html', items=items)
    else:
        return render_template('notfound.html')


@app.route('/market', methods=['GET', 'POST'])
def market_page():
    form = marketform()
    if form.validate_on_submit():
        data = {
            'capacity': form.capacity.data,
            'automation': form.automation.data,
            'machine': form.machine.data
        }
        return redirect(url_for('marketsearch_page', machine=data['machine'], automation=data['automation'],
                                capacity=data['capacity']))

    if form.errors != {}:  # no error from validation
        for err_msg in form.errors.values():
            flash(f'There was an error in searching: {err_msg}', category='danger')
    return render_template('market.html', form=form)

@app.route('/foddersearch/<state>')
def foddersearch_page(state):
    df1 = dataframe_to_import.fod_table
    df1 = df1[df1['state'] == state]
    df1_dict = df1.to_dict('records')
    items = df1_dict
    return render_template('fodder_table.html', items=items)


@app.route('/fodderinfo', methods=['GET', 'POST'])
def fodderinfo_page():
    form = fodderform()
    if form.validate_on_submit():
        data = {
            'state': form.state.data,
            
        }
        return redirect(url_for('foddersearch_page', state=data['state']))

    if form.errors != {}:  # no error from validation
        for err_msg in form.errors.values():
            flash(f'There was an error in searching: {err_msg}', category='danger')
    return render_template('fodinfo.html', form=form)

@app.route('/vetssearch/<animal>')
def vetssearch_page(animal):
    df1 = dataframe_to_import.vetsinfo_table
    df1 = df1[(df1['animals'] == animal)|(df1['animals']=='All')]
    df1_dict = df1.to_dict('records')
    items = df1_dict
    return render_template('vets_table.html', items=items)


@app.route('/vetsinfo', methods=['GET', 'POST'])
def vetsinfo_page():
    return render_template('vetsinfo.html')

@app.route('/vetsdetail/<name>', methods=['GET', 'POST'])
def vetsdetail_page(name):
    df1 = dataframe_to_import.vetsinfo_table
    df1 = df1[(df1['name'] == name)]
    df1_dict = df1.to_dict('records')
    items = df1_dict
    return render_template('vetsdetail.html', items=items)

@app.route('/ethnosearch/<animal>')
def ethnosearch_page(animal):
        df1 = dataframe_to_import.ethno_disease
        df1_dict = df1.to_dict('records')
        items = df1_dict
        return render_template('ethno_table.html', items=items)

    
@app.route('/ethnoinfo', methods=['GET', 'POST'])
def ethnoinfo_page():
    return render_template('ethnoinfo.html')

@app.route('/ethnodetail/<id>', methods=['GET', 'POST'])
def ethnodetail_page(id):
    df1 = dataframe_to_import.ethno_table
    df1 = df1[(df1['id'] == int(id))]
    df1_dict = df1.to_dict('records')
    items = df1_dict
    return render_template('ethnodetail.html', items=items)


@app.route('/trainingssearch')
def trainingssearch_page():
        df1 = dataframe_to_import.training_table
        df1 = df1
        df1_dict = df1.to_dict('records')
        items = df1_dict
        return render_template('training_table.html', items=items)


@app.route('/training', methods=['GET', 'POST'])
def training_page():
    form = trainingform()
    if form.validate_on_submit():
        return redirect(url_for('trainingssearch_page'))

    if form.errors != {}:  # no error from validation
        for err_msg in form.errors.values():
            flash(f'There was an error in searching: {err_msg}', category='danger')
    return render_template('training.html', form=form)

@app.route('/workshopsearch/<institute>')
def workshopsearch_page(institute):
        df1 = dataframe_to_import.workshop_table
        df1 = df1[df1['instituteName'] == institute]
        df1_dict = df1.to_dict('records')
        items = df1_dict
        return render_template('workshop_table.html', items=items)


@app.route('/workshop', methods=['GET', 'POST'])
def workshop_page():
    form = workshopform()
    if form.validate_on_submit():
        data = {
            'institute': form.institute.data,
            
        }
        return redirect(url_for('workshopsearch_page', institute=data['institute']))

    if form.errors != {}:  # no error from validation
        for err_msg in form.errors.values():
            flash(f'There was an error in searching: {err_msg}', category='danger')
    return render_template('workshop.html', form=form)

@app.route('/coursesearch/<institute>/<type>')
def coursesearch_page(institute, type):
        df1 = dataframe_to_import.institute_table
        df1 = df1[df1['institute'] == institute]
        df1 = df1[df1['courseType'] == type]
        df1_dict = df1.to_dict('records')
        items = df1_dict
        return render_template('institute_table.html', items=items)


@app.route('/institutes', methods=['GET', 'POST'])
def institute_page():
    form = instituteform()
    if form.validate_on_submit():
        data = {
            'institute': form.institute.data,
            'type': form.type.data
        }
        return redirect(url_for('coursesearch_page', institute=data['institute'], type=data['type']))

    if form.errors != {}:  # no error from validation
        for err_msg in form.errors.values():
            flash(f'There was an error in searching: {err_msg}', category='danger')
    return render_template('institute.html', form=form)

@app.route('/MarketPlace')
def marketplace_page():
    # Retrieve all products from Firestore
     df1 = dataframe_to_import.mkt
     df1 = df1
     df1_dict = df1.to_dict('records')
     items = df1_dict
     return render_template('buy.html', items=items)

@app.route('/add_to_cart/<product_id>', methods=['GET', 'POST'])
def add_to_cart(product_id):
    quantity = int(1)
    cart_item = CartItem(product_id, quantity)
    cart_item.add_to_cart()
    return redirect(url_for('view_cart'))

@app.route('/cart')
def view_cart():
    cart_items = CartItem.get_cart_items()
    return render_template('cart.html', cart_items=cart_items)

@app.route('/remove_from_cart/<product_id>', methods=['GET', 'POST'])
def remove_from_cart(product_id):
    cart_item = CartItem(product_id)
    cart_item.remove_from_cart()
    return redirect(url_for('view_cart'))

##bootstrap styling option

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = registrationform()
    if form.validate_on_submit():
        user_to_create = {
            'Name': form.name.data,
            'email': form.email_address.data,
            'password': form.password1.data,
            'confirmpassword': form.password2.data,
            'typeofuser': form.usertype.data
        }
        firestore_db.collection(u'manufacturer_registration').add(user_to_create)
        return redirect(url_for('market_page'))
    if form.errors != {}:  # no error from validation
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = loginform()
    if form.validate_on_submit():
        attempted = dataframe_to_import.man_register[dataframe_to_import.man_register['email'] == form.email.data]
        attempted_user = attempted.to_dict('list')
        if attempted_user and form.password.data == attempted.iloc[0]['password']:
            name = attempted.iloc[0]['Name']
            flash(f'Success! You are logged in as: {name}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password do not match!', category='danger')

    return render_template('login.html', form=form)
