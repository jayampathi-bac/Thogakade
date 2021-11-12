**Login method**

###### mehod name : login_user(\*params)

This method checks if the user has already login or not. If the user didn't login it prints a message to log in. After the login, a user.db file will be created inside the db folder with customer id.

------------


**Create customer Account method**

###### method name : create_customer(\*params)

We can use this method to create a customer account . It creates inside customer's file with user details with user id in the db folder.

------------


**Order place method**

###### method name : place_order(\*params)

When we use this method, the following methods also work.

**1. check_qty(item_id,qty)**
_First, it checks how much from this itemId is present. Order will not be accepted if there is not enough material for the order. If there is enough quantity, the following methods will execute:_

**2. save_order()**
_Save a file from order id._

**3. place_order_details(order.last_id,order.customer_id,itemId,qty,is_qty_available[1])**

_Following methods are executed using this method :_

1. update_qty(items,qty)

   The quantity is updated when the user places an order.

2. save_order_details()
   After changing the quantity, the order details are described by the order ID in the order in the file.

The customer place order is displayed as pending. Once the owner completes the order, it changes the as done.

------------

**Order view method**

Orders can be viewed in two main ways.

1. Customer view orders
Customer can view only their orders. (from order id or all orders)

2. Admin view orders
Admin can view all customers orders.

------------


**Order delete method**
Customers can delete their orders. After deleting the customer's orders quantity will be updated in the item file.
