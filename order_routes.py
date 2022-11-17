from   fastapi import APIRouter,Depends,status
from schemas import OrderModel,OrderstatusModel
from models import User,Order
from fastapi_jwt_auth import AuthJWT 
from fastapi.exceptions import HTTPException
from database import sessionmaker,engine
from fastapi.encoders import jsonable_encoder
order_router=APIRouter(
    prefix='/orders',
    tags=['orders']
)
Session = sessionmaker(bind=engine)
session = Session()

@order_router.get("/")
def hello(Authorize:AuthJWT=Depends()):
    """
    #Hello World
    
    This is An hello World Api
    """
    # try:
    #     Authorize.jwt_required()
    # except Exception as e:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Invalid Token "
    #     )
    return {"message":"Hello"}


@order_router.post('/order')
async def plance_an_order(order:OrderModel,Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token "
        )

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
        "id":new_order.id,
        "pizza_size":new_order.pizza_size,
        "quantity":new_order.quantity,
        "order status":new_order.order_status
    }
    return jsonable_encoder(response)

@order_router.get('/orders')
async def list_all_orders(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token ")
    current_user=Authorize.get_jwt_subject()
    user=session.query(User).filter(User.username==current_user).first()
    
    if user.is_staff:
        orders=session.query(Order).all()
        return jsonable_encoder(orders)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not a superuser")
    
    
@order_router.get('/orders/{id}')
async def get_order_by_id(id:int,Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token")
    current_user=Authorize.get_jwt_subject()
    user=session.query(User).filter(User.username==current_user).first()
    if user.is_staff:
        order=session.query(Order).filter(Order.id==id).first()
        return jsonable_encoder(order)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not allowed to access this")
    
    
@order_router.get('/user/orders')
async def get_user_orders(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token")
    current_user=Authorize.get_jwt_subject()
    
    user=session.query(User).filter(User.username==current_user).first()
    return jsonable_encoder(user.orders)
    
    
@order_router.get('/user/orders/{id}')
async def get_specific_user_orders(id:int,Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token")
        
    current_user=Authorize.get_jwt_subject()
    user=session.query(User).filter(User.username==current_user).first()
    orders=user.orders
    for order in orders:
        if order.id == id:
            return jsonable_encoder(order)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="No order Found")
    
@order_router.put('/order/update/{id}')
async def update_order(id:int,order:OrderModel,Authorize:AuthJWT=Depends()):
    print("~~~~~~~~~~~~~~~~~~~~`")
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token")
    order_to_update=session.query(Order).filter(Order.id==id).first()
    order_to_update.quantity=order.quantity
    order_to_update.pizza_size=order.pizza_size
    print(order.pizza_size,"~~~~~~~~~~~~~~~~~~~~",jsonable_encoder(order_to_update)
)
    session.commit()
    if order_to_update:
        return jsonable_encoder(order_to_update)



@order_router.patch('/order_status/update/{id}')
async def update_order_status(id:int,order:OrderstatusModel,Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token")
        
    username=Authorize.get_jwt_subject()   
    
    current_user=session.query(User).filter(User.username==username).first()
    
    if current_user.is_staff:
        order_to_update=session.query(Order).filter(Order.id==id).first()
        order_to_update.order_status=order.order_status
        session.commit()
        response={
            "id":order_to_update.id,
            "pizza_size":order_to_update.pizza_size,
            "quantity":order_to_update.quantity,
            "order status":order_to_update.order_status
        }
        return jsonable_encoder(response)
    

@order_router.delete('/order/delete/{id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(id:int,Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token")
    
    order_to_delete=session.query(Order).filter(Order.id==id).first()
    session.delete(order_to_delete)
    session.commit()
    if order_to_delete:
        return jsonable_encoder("Order Deleted ")
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="No order Found")