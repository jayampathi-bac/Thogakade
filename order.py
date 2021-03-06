import json
import os
from pprint import pprint
import datetime


from order_details import OrderDetails, place_order_details

__db_location__ = "db"
__order_folder__ = f"{__db_location__}/order"
__order__last_id__ = f"{__db_location__}/order_id.db"
__user_id__ = f"{__db_location__}/user.db"
__order_detail_folder__ = f"{__db_location__}/order_detail"

class Order():
    def __init__(self) :
        if os.path.exists(__order__last_id__):
            with open(__order__last_id__, "r") as last_id_f:
                self.last_id = int(last_id_f.readline())
        else:
            self.last_id = 0

    def __repr__(self):
        return f"id:{self.id},customerId:{self.customer_id},date:{self.date},date:{self.status}"


    def __str__(self):
        return f"id:{self.id},customerId:{self.customer_id},date:{self.date},date:{self.status}"

    def save_order(self):
        id = self.last_id+1

        # Save database orders
        _data_ = {
            "id": id,
            "customer_id": self.customer_id,
            "date": self.date,
            "status":self.status
        }
        with open(f"{__order_folder__}/{id}.db", "w") as item_file:
            json.dump(_data_, item_file)

        # Save next id
        self.last_id += 1
        with open(__order__last_id__, "w") as f:
            f.write(str(self.last_id))

    def __get_order_by_path(self,order, path):
        
        with open(path, "r") as item_file:
            _data_ = json.load(item_file)
            order.id = _data_["id"]
            order.customer_id = _data_["customer_id"]
            order.date = _data_["date"]
            order.status = _data_["status"]

    def _get_user_by_path():
        if os.path.exists(__user_id__):
            with open(__user_id__, "r") as last_id_f:
                return last_id_f.readline()
            

    def all_orders(self):
        order_file_names = os.listdir(__order_folder__)
        orders = []
        for order_file_name in order_file_names:
            order = Order()
            order.__get_order_by_path(
                order, f"{__order_folder__}/{order_file_name}")
            orders.append(order)
        return orders


    def get_by_id(self,id):
        Order.__get_order_by_path(self, f"{__order_folder__}/{id}.db")

    def delete_item(self,id):
        if os.path.exists(f"{__order_folder__}/{id}.db"):
            os.remove(f"{__order_folder__}/{id}.db")
            print("**",id,"deleted","**")
        else:
            print("The order does not exist")



def place_order(itemId,qty):
    try:
        order = Order()
        order.customer_id = Order._get_user_by_path()
        order.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        order.status = "Pending"
        is_qty_available = check_qty(itemId,qty)
    
        if is_qty_available[0] :
            order.save_order()
            is_place = place_order_details(order.last_id,order.customer_id,itemId,qty,is_qty_available[1])
            if  is_place:
                print("Your order placed..!")
    except:
        print("** Could not match item id..! **")
   
   

def check_qty(itemId,qty):
   
    a = Order._get_user_by_path()
    
    if a is not None:
        with open("db/item/"f"{itemId}.db", "r") as jsonFile:
                data = json.load(jsonFile)


        have_qty = int(data["qty"])
        if int(have_qty) > int(qty):
            return True,float(data["sellingPrice"])
        else:
            print("** Sorry we have only "f"{have_qty} ..! **")
            return False,-1
    else:
        print("** Please login..! **")
        return False,-1

def order_done(id):
    if os.path.exists(f"{__order_folder__}/{id}.db"):
        with open("db/order/"f"{id}.db", "r") as jsonFile:
            data = json.load(jsonFile)

        data["status"] = "done"

        with open("db/order/"f"{id}.db", "w") as jsonFile:
            json.dump(data, jsonFile)
            print("** Order mark as done..! **")
    else:
         print("** Sorry could not find the order id "f"{id} **" )  


def get_my_orders():

    user = Order._get_user_by_path()
    if user is not None:
        print("Choose your option :")
        print("[1]. All orders")
        print("[2]. One order")
        user_input = input("Please select number : ")
        
        if user_input == "2":
            order_id = input("Please eneter your order id : ")

        if user_input == "1":
            order_id = None

        result = filter_customer_orders(order_id)
        
        if result is not None :
            print('|------------------------------------Orders------------------------------------ |')
            pprint(result)
           
            
        else:
            print("You does not place orders.. ! ")
        
    else:
        print("Please login or create account ")


def filter_customer_orders(order_id):
    order_detail = OrderDetails()
    order_details = order_detail.all_orders()
    order_cust_id = order_detail._get_user_by_path()
    orders_tuple = tuple(order_details)
    cust_orders =[]

    # check customer have an order and get their orders
    if order_id == None :
        for i in range(len(order_details)):
            if int(order_cust_id) == int(orders_tuple[i].customer_id) :
                cust_orders.append(orders_tuple[i])
    else :
        for i in range(len(order_details)):
            if int(order_id) == int(orders_tuple[i].order_id) :
                cust_orders.append(orders_tuple[i])

 
    if len(cust_orders) == 0:
        return None
    else:
           return cust_orders