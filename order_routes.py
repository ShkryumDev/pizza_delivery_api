from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from models import User, Order
from schemas import OrderModel, OrderStatusModel
from database import Session, engine
from fastapi.encoders import jsonable_encoder

session=Session(bind=engine)

order_router=APIRouter(
    prefix='/orders',
    tags=['orders'],
)

@order_router.get('/')
async def hello(Authorize:AuthJWT=Depends()):
    
    """
        ## A sample hello world route
        This returns Hello world
    """
    
    try:
        Authorize.jwt_required()
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')
    
    return {'message':'Hello World'}


@order_router.post('/order', status_code=status.HTTP_401_UNAUTHORIZED)
async def place_an_order(order:OrderModel, Authorize:AuthJWT=Depends()):
    
    """
        ## Placing an Order
        This requires the following
        - quantity : integer
        - pizza_size : string
    """
    
    try:
        Authorize.jwt_required()
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')
    
    current_user=Authorize.get_jwt_subject()
    
    user=session.query(User).filter(User.username==current_user).first()
    
    new_order=Order(
        pizza_size=order.pizza_size,
        quantity=order.quantity
    )
    
    new_order.user=user
    
    session.add(new_order)
    
    session.commit()
    
    
    response={
        'pizza_size':new_order.pizza_size,
        'quantity':new_order.quantity,
        'id':new_order.id,
        'order_status':new_order.order_status,
    }
    
    return jsonable_encoder(response)


@order_router.get('/orders')
async def list_all_orders(Authorize:AuthJWT=Depends()):
    
    """
        ## List all Order
        This lists all orders made. It can be accessed by superusers
    """
    
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')
    
    current_user=Authorize.get_jwt_subject()
    
    user=session.query(User).filter(User.username==current_user).first()
    
    if user.is_staff:
        orders=session.query(Order).all()
        
        return jsonable_encoder(orders)
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='You Are Not Superuser')


@order_router.get('/orders/{id}')
async def get_order_by_id(id:int, Authorize:AuthJWT=Depends()):
    
    """
        ## Get an Order by its ID
        This gets an Order by its ID and is only accessed by a superuser
    """
    
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status. HTTP_401_UNAUTHORIZED, detail='Invalid Token')
    
    user=Authorize.get_jwt_subject()
    
    current_user=session.query(User).filter(User.username==user).first()
    
    if current_user.is_staff:
        order=session.query(Order).filter(Order.id==id).first()
        
        return jsonable_encoder(order)
    
    raise HTTPException(status_code=status. HTTP_401_UNAUTHORIZED, detail='User Not Alowed To Carry Out Request')


@order_router.get('/user/orders')
async def get_user_orders(Authorize:AuthJWT=Depends()):
    
    """
        ## Get a current user's Orders
        This lists the Orders made by the currently logged in user
    """
    
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status. HTTP_401_UNAUTHORIZED, detail='Invalid Token')
    
    user=Authorize.get_jwt_subject()
    
    current_user=session.query(User).filter(User.username==user).first()
    
    return jsonable_encoder(current_user.orders)
    

@order_router.get('/user/order/{id}/')
async def get_specific_order(id:int, Authorize:AuthJWT=Depends()):
    
    """
        ## Get a specific Order by the currently logged in user
        This returns an Order by ID for the currently logged in user
    """
    
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')
    
    subject=Authorize.get_jwt_subject()
    
    current_user=session.query(User).filter(User.username==subject).first()
    
    orders=current_user.orders
    
    for o in orders:
        if o.id == id:
            return jsonable_encoder(o)
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='No Order With Such id')


@order_router.put('/order/update/{id}/')
async def update_order(id:int, order:OrderModel, Authorize:AuthJWT=Depends()):
    
    """
        ## Updating an Order
        This updates an Order and requires the following fields
        - quantity : integer
        - pizza_size : string
    """
    
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')

    order_to_update=session.query(Order).filter(Order.id==id).first()
    
    order_to_update.quantity=order.quantity
    order_to_update.pizza_size=order.pizza_size
    
    session.commit()
    
    response={
            'id':order_to_update.id,
            'quantity':order_to_update.quantity,
            'pizza_size':order_to_update.pizza_size,
            'order_status':order_to_update.order_status,
        }
    
    return jsonable_encoder(response)


@order_router.patch('/order/update/{id}/')
async def update_order_status(id:int, order:OrderStatusModel, Authorize:AuthJWT=Depends()):
    
    """
        ## Update an Order's status
        This is for updating an Order's status and requires 'order_status' in string format
    """
    
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')
    
    username=Authorize.get_jwt_subject()
    
    current_user=session.query(User).filter(User.username==username).first()
    
    if current_user.is_staff:
        order_to_update=session.query(Order).filter(Order.id==id).first()
        
        order_to_update.order_status=order.order_status
        
        session.commit()
        
        response={
            'id':order_to_update.id,
            'quantity':order_to_update.quantity,
            'pizza_size':order_to_update.pizza_size,
            'order_status':order_to_update.order_status,
        }
        
        return jsonable_encoder(response)


@order_router.delete('/order/delete/{id}/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_an_order(id:int, Authorize:AuthJWT=Depends()):
    
    """
        ## Delete an Order
        This deletes an Order by its ID
    """
    
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')
    
    order_to_delete=session.query(Order).filter(Order.id==id).first()
    
    session.delete(order_to_delete)
    
    session.commit()
    
    return order_to_delete
