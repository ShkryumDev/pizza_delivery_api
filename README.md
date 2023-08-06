PIZZA DELIVERY API
This is a REST API for a Pizza delivery service built for learning with FastAPI, SQLAlchemy and PostgreSQL.

ROUTES TO IMPLEMENT

METHOD      ROUTE                               FUNCTIONALITY               ACCESS
post        /api/signup/                        register new user           all users
post        /api/login/                         login user                  all users
post        /api/order/                         place an order              all users
put         /api/order/update/{order_id}/       update an order             all users
put         /api/order/status/{order_id}/       update order status         all users
delete      /api/order/delete/{order_id}/       delete/remove an order      all users
get         /api/user/orders/                   get users orders            all users
get         /api/orders/                        list all orders made        superuser
get         /api/orders/{order_id}/             retrieve an order           superuser
get         /api/user/order/{order_id}          get users specific order    
get         /docs/                              view api documentation      all users