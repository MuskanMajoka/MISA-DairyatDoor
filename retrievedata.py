# retrieve data
import firebase_admin
from firebase_admin import credentials, firestore
import datetime
import inflect
import pandas as pd

cred = credentials.Certificate("wsmproject.json")
firebase_admin.initialize_app(cred)

firestore_db = firestore.client()


class database:

    def get_table(table_name):
        return firestore_db.collection(table_name)

# read the data as dataframe from the firestore
request_generated_data = list(firestore_db.collection(u'Request_Generated').stream())
request_generated_data_dict = list(map(lambda x: x.to_dict(), request_generated_data))

cloud_db_rec_table = list(firestore_db.collection(u'Recommendation_table').stream())
cloud_db_rec_table_dict = list(map(lambda x: x.to_dict(), cloud_db_rec_table))

cloud_db_rec_table1 = list(firestore_db.collection(u'Recommendation_table1').stream())
cloud_db_rec_table1_dict = list(map(lambda x: x.to_dict(), cloud_db_rec_table1))

cloud_db_dairy_product = list(firestore_db.collection(u'dairy_project').stream())
cloud_db_dairy_product_dict = list(map(lambda x: x.to_dict(), cloud_db_dairy_product))

cloud_db_man = list(firestore_db.collection(u'manufacturer_registration').stream())
cloud_db_man_dict = list(map(lambda x: x.to_dict(), cloud_db_man))

cloud_db_cus = list(firestore_db.collection(u'customer_registration').stream())
cloud_db_cus_dict = list(map(lambda x: x.to_dict(), cloud_db_cus))

cloud_db_fod = list(firestore_db.collection(u'Fodder').stream())
cloud_db_fod_dict = list(map(lambda x: x.to_dict(), cloud_db_fod))

cloud_db_vets = list(firestore_db.collection(u'Vets').stream())
cloud_db_vets_dict = list(map(lambda x: x.to_dict(), cloud_db_vets))

cloud_db_vetsinfo = list(firestore_db.collection(u'Vetsinfo').stream())
cloud_db_vetsinfo_dict = list(map(lambda x: x.to_dict(), cloud_db_vetsinfo))

cloud_db_training = list(firestore_db.collection(u'training').stream())
cloud_db_training_dict = list(map(lambda x: x.to_dict(), cloud_db_training))

cloud_db_workshop = list(firestore_db.collection(u'WorkDetail_List').stream())
cloud_db_workshop_dict = list(map(lambda x: x.to_dict(), cloud_db_workshop))

cloud_db_institute = list(firestore_db.collection(u'Institutes').stream())
cloud_db_institute_dict = list(map(lambda x: x.to_dict(), cloud_db_institute))

cloud_db_disease = list(firestore_db.collection(u'Ethno_Disease_Imgs').stream())
cloud_db_disease_dict = list(map(lambda x: x.to_dict(), cloud_db_disease))

cloud_db_ethno = list(firestore_db.collection(u'Ethnodetail').stream())
cloud_db_ethno_dict = list(map(lambda x: x.to_dict(), cloud_db_ethno))

cloud_db_products = list(firestore_db.collection(u'Products').stream())
cloud_db_product_dict = list(map(lambda x: x.to_dict(), cloud_db_products))

cloud_db_cart = list(firestore_db.collection(u'Cart').stream())
cloud_db_cart_dict = list(map(lambda x: x.to_dict(), cloud_db_cart))

cloud_db_mkt = list(firestore_db.collection(u'Mktdb').stream())
cloud_db_mkt_dict = list(map(lambda x: x.to_dict(), cloud_db_mkt))

cloud_db_wallet = list(firestore_db.collection(u'wallet').stream())
cloud_db_wallet_dict = list(map(lambda x: x.to_dict(), cloud_db_wallet))

cloud_db_producer = list(firestore_db.collection(u'producer').stream())
cloud_db_producer_dict = list(map(lambda x: x.to_dict(), cloud_db_producer))

cloud_db_delivery = list(firestore_db.collection(u'delivery').stream())
cloud_db_delivery_dict = list(map(lambda x: x.to_dict(), cloud_db_delivery))


# read the data as dataframe from the firestore

# dataframe class:
class dataframe_to_import:
    recommendation_table = pd.DataFrame(cloud_db_rec_table_dict)
    recommendation_table1 = pd.DataFrame(cloud_db_rec_table1_dict)
    dairy_product = pd.DataFrame(cloud_db_dairy_product_dict)
    man_register = pd.DataFrame(cloud_db_man_dict)
    cust_register = pd.DataFrame(cloud_db_cus_dict)
    fod_table = pd.DataFrame(cloud_db_fod_dict)
    vets_table = pd.DataFrame(cloud_db_vets_dict)
    vetsinfo_table = pd.DataFrame(cloud_db_vetsinfo_dict)
    training_table = pd.DataFrame(cloud_db_training_dict)
    workshop_table = pd.DataFrame(cloud_db_workshop_dict)
    institute_table = pd.DataFrame(cloud_db_institute_dict)
    ethno_table = pd.DataFrame(cloud_db_disease_dict)
    ethno_disease = pd.DataFrame(cloud_db_ethno_dict)
    product = pd.DataFrame(cloud_db_ethno_dict)
    cart = pd.DataFrame(cloud_db_cart_dict)
    mkt = pd.DataFrame(cloud_db_mkt_dict)
    wallet = pd.DataFrame(cloud_db_wallet_dict)
    request_generated = pd.DataFrame(request_generated_data_dict)
    producer = pd.DataFrame(cloud_db_producer_dict)
    delivery = pd.DataFrame(cloud_db_delivery_dict)

class Product:
    def __init__(self, product_id, title, img_url, price, quantity):
        self.id = product_id
        self.title = title
        self.img_url = img_url
        self.price = price
        self.quantity = quantity


class CartItem:
    def __init__(self, product_id, quantity=1):
        self.product_id = product_id
        self.quantity = quantity

    def add_to_cart(self):
        cart_ref = firestore_db.collection(u'Cart').document(self.product_id)
        cart_data = cart_ref.get().to_dict()

        if cart_data:
            current_quantity = cart_data.get('quantity', 0)
            new_quantity = current_quantity + self.quantity
            cart_ref.update({'quantity': new_quantity})
        else:
            firestore_db.collection(u'Cart').document(self.product_id).set({
                'id': self.product_id,
                'quantity': self.quantity
            })

    #        firestore_db.collection(u'Cart').add(
    #            {'id': self.product_id,
    #             'quantity': self.quantity})

    def remove_from_cart(self):
        cart_ref = firestore_db.collection(u'Cart').document(self.product_id)
        cart_data = cart_ref.get().to_dict()

        if cart_data:
            current_quantity = cart_data.get('quantity', 0)
            new_quantity = max(0, current_quantity - 1)  # Ensure quantity doesn't go below 0
            cart_ref.update({'quantity': new_quantity})

    #    firestore_db.collection(u'Cart').delete(
    #        {'id': self.product_id})

    @staticmethod
    def get_cart_items():
        cloud_db_cart = list(firestore_db.collection(u'Cart').stream())
        cloud_db_cart_dict = list(map(lambda x: x.to_dict(), cloud_db_cart))
        cart = pd.DataFrame(cloud_db_cart_dict)
        cloud_db_mkt = list(firestore_db.collection(u'Mktdb').stream())
        cloud_db_mkt_dict = list(map(lambda x: x.to_dict(), cloud_db_mkt))
        df1 = pd.DataFrame(cloud_db_mkt_dict)
        df1 = df1.drop(columns=['quantity'])
        cart['quantity'] = cart['quantity'].astype(int)
        cart = cart[cart['quantity'] > 0]
        cdmerge = cart.merge(df1, how='inner', on='id')
        cdmerge['price'] = cdmerge['price'] * cdmerge['quantity']
        cart_items = cdmerge.to_dict('records')
        return cart_items


class wallet_data:
    def __init__(self, customer_id):
        self.customer_id = customer_id

    def add_to_wallet(self, amount):
        wallet_ref = firestore_db.collection(u'wallet').document(self.customer_id)
        wallet_d = wallet_ref.get().to_dict()

        if wallet_d:
            current_amount = wallet_d.get('amount', 0)
            new_amount = current_amount + amount
            wallet_ref.update({'amount': new_amount})
        else:
            firestore_db.collection(u'wallet').document(self.customer_id).set({
                'id': self.customer_id,
                'amount': amount
            })

    def get_wallet_detail(self):
        cloud_db_wallet = list(firestore_db.collection(u'wallet').stream())
        cloud_db_wallet_dict = list(map(lambda x: x.to_dict(), cloud_db_wallet))
        wallet_d = pd.DataFrame(cloud_db_wallet_dict)
        wallet_d = wallet_d[wallet_d['customer_id'] == self.customer_id]
        wallet_detail = wallet_d.to_dict('records')
        return wallet_detail


class status_data:
    def __init__(self, customer_id):
        self.customer_id = customer_id

    def get_status(self, df):
        if df['delivery_status'] == False and df['producer_status'] == False:
            val = 'Order Placed'
        elif df['delivery_status'] == False and df['producer_status'] == True:
            val = 'In Transit'
        elif df['delivery_status'] == True and df['producer_status'] == False:
            val = 'Error'
        elif df['delivery_status'] == True and df['producer_status'] == True:
            val = 'Delivered'
        return val

    def get_pr(self, df):
        df1 = dataframe_to_import.producer
        df2 = df.merge(df1, left_on='producer', right_on='id', how='left')
        df2 = df2.drop(columns=['id'])
        # Check if the producer column is 0
        df2['producer_selected'] = df2.apply(
            lambda row: 'Searching for Producer' if row['producer'] == 0 else row['name'], axis=1)
        df2.rename({'name': 'temp_producer_selected', 'contact': 'contact_producer', 'location': 'producer_location'}, axis=1, inplace=True)
        df2.rename({'temp_producer_selected': 'producer_selected'}, axis=1, inplace=True)

        return df2

    def get_dr(self, df):
        df1 = dataframe_to_import.delivery
        df2 = df.merge(df1, left_on='delivery', right_on='id', how='left')
        df2 = df2.drop(columns=['id'])
        # Check if the delivery column is 0
        df2['delivery_selected'] = df2.apply(
            lambda row: 'Searching for delivery' if row['delivery'] == 0 else row['name'], axis=1)
        df2.rename({'name': 'temp_delivery_selected', 'contact': 'contact_delivery', 'location': 'delivery_location'}, axis=1, inplace=True)
        df2.rename({'temp_delivery_selected': 'delivery_selected'}, axis=1, inplace=True)

        return df2

    def get_status_detail(self):
        request_generated_data = list(firestore_db.collection(u'Request_Generated').stream())
        request_generated_data_dict = list(map(lambda x: x.to_dict(), request_generated_data))
        status_d = pd.DataFrame(request_generated_data_dict)
        status_d = status_d[status_d['customer'] == self.customer_id]

        if not status_d.empty:
            status_d['status'] = status_d.apply(self.get_status, axis=1)
            status_d.rename({'id': 'order_id'}, axis=1, inplace=True)
            status_d = self.get_pr(status_d)
            status_d = self.get_dr(status_d)
        status_detail = status_d.to_dict('records')
        return status_detail

        # x = pd.DataFrame(request_generated_data_dict)
        # y = x['order_items'][0]
        # for i in y:
        #     print(i)
        #     a = y.get(i)
        #     print(a)
        #     print(a.get('item_id'))
        #     print(a.get('quantity'))

class generate_request_data:
    def __init__(self, customer_id):
        self.customer_id = customer_id

    def confirm_request_generate(self):
        # request_generated_data = list(firestore_db.collection(u'Request_Generated').stream())
        # request_generated_data_dict = list(map(lambda x: x.to_dict(), request_generated_data))
        # status_d = pd.DataFrame(request_generated_data_dict)
        #status_d = status_d[status_d['customer'] == self.customer_id]
        wallet = wallet_data(self.customer_id)
        wallet_detail = pd.DataFrame(wallet.get_wallet_detail())
        amount = wallet_detail['amount']

        cartitem = CartItem(self.customer_id)
        cartitems = cartitem.get_cart_items()
        df = pd.DataFrame(cartitems)
        price = df['price'].sum()

        if amount.iloc[0] < price:
            return 0
        else:
            items_no = len(df)

            p = inflect.engine()
            order_items_data = {}

            for idx, (_, row) in enumerate(df.iterrows(), start=1):
                number_word = p.number_to_words(p.ordinal(idx))

                number_data = {
                    'item_id': row['id'],
                    'name': row['title'],
                    'quantity': row['quantity']  # Convert to int if needed
                }

                order_items_data[number_word] = number_data

                #empty cart
                cart_ref = firestore_db.collection(u'Cart').document(row['id'])
                cart_data = cart_ref.get().to_dict()

                current_quantity = cart_data.get('quantity', 0)
                new_quantity = max(0, current_quantity - row['quantity'])  # Ensure quantity doesn't go below 0
                cart_ref.update({'quantity': new_quantity})

            request = firestore_db.collection(u'Request_Generated')
            order_id = len(request.get())+1
            current_timestamp = datetime.datetime.now(datetime.timezone.utc)
            document_data = {
                'customer': self.customer_id,
                'price': int(price),
                'items_no': items_no,
                'id': str(order_id),
                'delivery': 0,
                'delivery_status': False,
                'datetime': current_timestamp,
                'producer': 0,
                'producer_status': False,
                'order_items': order_items_data,
            }

            # Print keys and values in document_data for troubleshooting
            for key, value in document_data.items():
                print(f"Key: {key}, Value: {value}")

            # Attempt to set the document in Firestore
            try:
                request.document(str(order_id)).set(document_data)
                return 1
            except Exception as e:
                print(f"Error setting document in Firestore: {e}")
                return 2