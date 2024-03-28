from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_bcrypt import Bcrypt
import qrcode
from io import BytesIO
import base64
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '7a3c6f28205c6b78d29fa93f'

bcrypt = Bcrypt(app)

# links to work on
# https://flask.palletsprojects.com/en/2.1.x/quickstart/#
# https://github.com/jimdevops19/codesnippets
from Website.retrievedata import firestore_db, database, dataframe_to_import, CartItem, wallet_data, status_data, generate_request_data
from Website.forms import registrationform, loginform, marketform, fodderform, trainingform, workshopform, \
    instituteform, ethnoform, cartform

##scripting different pages.>
@app.route('/')
#@app.route('/home')
def home_page():
    return render_template('home.html')  # render templates handle request and request them in htl file


@app.route('/About')
def about_page():
    return render_template('home.html', section= "about.section4")  # render templates handle request and request them in htl file


@app.route('/Services')
def services_page():
    return render_template('home.html', section ="services.section3")


@app.route('/Technology')
def technology_page():
    return render_template('technology.html')


@app.route('/Healthcare')
def healthcare_page():
    return render_template('fodder.html')


@app.route('/HeathcareServices')
def healthcareservices_page():
    return render_template('fodder.html', section ="services.section3")


@app.route('/Education')
def study_page():
    return render_template('study.html')


@app.route('/Education/Case Study')
def case_page():
    return render_template('case.html')


@app.route('/marketsearch/<machine>/<automation>/<capacity>')
def marketsearch_page(machine, automation, capacity):
    if machine == 'Cream Separator':
        table = database.get_table('Recommendation_table1')
        a = int(capacity)
        docs = table.where('AutomationGrade', '==', automation).where('capacity', '>=', a).get()
        items = list(map(lambda x: x.to_dict(), docs))
        if items:
            return render_template('markettable.html', items=items)
        else:
            return render_template('notfound.html')
    
    else:
        return render_template('notfound.html')

@app.route('/marketdetail/<product>')
def marketdetail_page(product):
        table = database.get_table('Recommendation_table1')
        docs = table.where('product', '==', product).get()
        items = list(map(lambda x: x.to_dict(), docs))
        return render_template('marketdetail.html', items=items)


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
        table = database.get_table('Fodder')
        docs = table.where('state', '==', state).get()
        items = list(map(lambda x: x.to_dict(), docs))
        if items:
            return render_template('fodder_table.html', items=items)
        else: 
            return render_template('notfound.html')

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
    table = database.get_table('Vetsinfo')
    docs = table.where('animals', 'in', [animal, "All"]).get()
    items = list(map(lambda x: x.to_dict(), docs))
    return render_template('vets_table.html', items=items)


@app.route('/vetsinfo', methods=['GET', 'POST'])
def vetsinfo_page():
    return render_template('vetsinfo.html')


@app.route('/vetsdetail/<name>', methods=['GET', 'POST'])
def vetsdetail_page(name):
    table = database.get_table('Vetsinfo')
    docs = table.where('name', '==', name).get()
    items = list(map(lambda x: x.to_dict(), docs))
    return render_template('vetsdetails.html', items=items)


@app.route('/ethnosearch/<animal>')
def ethnosearch_page(animal):
    if animal == "Cow":
        table = database.get_table('Ethno_Disease_Imgs').get()
        items = list(map(lambda x: x.to_dict(), table))
        return render_template('ethno_table.html', items=items)
    else:
        return render_template('notfound.html') 


@app.route('/ethnoinfo', methods=['GET', 'POST'])
def ethnoinfo_page():
    return render_template('ethnoinfo.html')


@app.route('/ethnodetail/<id>', methods=['GET', 'POST'])
def ethnodetail_page(id):
    table = database.get_table('Ethnodetail')
    docs = table.where('id', '==', int(id)).get()
    items = list(map(lambda x: x.to_dict(), docs))
    return render_template('ethnodetail.html', items=items)


@app.route('/trainingssearch')
def trainingssearch_page():
    table = database.get_table('training').get()
    items = list(map(lambda x: x.to_dict(), table))
    if items:
        return render_template('training_table.html', items=items)
    else:
        return render_template('notfound.html')


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
    table = database.get_table('WorkDetail_List')
    docs = table.where('instituteName', '==', institute).get()
    items = list(map(lambda x: x.to_dict(), docs))
    if items:
        return render_template('workshop_table.html', items=items)
    else:
        return render_template('notfound.html')
    


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
    table = database.get_table('Institutes')
    docs = table.where('institute', '==', institute).where('courseType', '==', type).get()
    items = list(map(lambda x: x.to_dict(), docs))
    if items:
        return render_template('institute_table.html', items=items)
    else:
        return render_template('notfound.html')
    
    


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
    table = database.get_table('Mktdb').get()
    items = list(map(lambda x: x.to_dict(), table))
    return render_template('buy.html', items=items)


@app.route('/cart')
def view_cart():
    cart_items = CartItem.get_cart_items()
    return render_template('cart.html', cart_items=cart_items)


@app.route('/add_to_cart/<product_id>', methods=['GET', 'POST'])
def add_to_cart(product_id):
    quantity = int(1)
    cart_item = CartItem(product_id, quantity)
    cart_item.add_to_cart()
    return redirect(url_for('view_cart'))


@app.route('/remove_from_cart/<product_id>', methods=['GET', 'POST'])
def remove_from_cart(product_id):
    cart_item = CartItem(product_id)
    cart_item.remove_from_cart()
    return redirect(url_for('view_cart'))


@app.route('/cgrequest/', methods=['GET'])
def cgrequest():
    cart_items = CartItem.get_cart_items()
    return render_template('cgrequest.html', cart_items = cart_items)

@app.route('/confirm_request')
def confirm_request():
    customer_id = 1
    request_call = generate_request_data(customer_id)
    success = request_call.confirm_request_generate()
    return render_template('confirm_request.html', success = success)

@app.route('/status', methods=['GET', 'POST'])
def status():
    # add customner id variable here for each unique session
    customer_id = 1
    status_call = status_data(customer_id)
    status_d = status_call.get_status_detail()
    now = datetime.now()
    return render_template('status.html', status_d=status_d, now = now)


@app.route('/wallet/', methods=['GET', 'POST'])
def wallet():
    paytm_url = "https://p.paytm.me/xCTH/j17d7pzj"

    # Generate QR code for Paytm URL
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(paytm_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buffered = BytesIO()
    img.save(buffered)
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    # add customner id variable here for each unique session
    customer_id = 1
    wallet_call = wallet_data(customer_id)
    wallet_d = wallet_call.get_wallet_detail()

    return render_template('wallet.html', wallet_d=wallet_d, qr_image=img_str)


@app.route('/add_money_to_wallet/<customer_id>', methods=['POST'])
def add_money_to_wallet(customer_id):
    # You can implement the logic to generate a unique payment token here
    amount = float(request.form.get('amount', 0))
    wallet_call = wallet_data(customer_id)
    wallet_call.add_to_wallet(amount)
    # add to wallet function give amount parameter
    return redirect(url_for('wallet'))


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


if __name__ == '__main__':
    app.run(debug=True)
