from pydantic import BaseModel
from typing import Optional


class SignUpModel(BaseModel):
    id:Optional[int]
    username:str
    email:str
    password:str
    is_staff:Optional[bool]
    is_active:Optional[bool]
    
    
    class Config:
        orm_mode=True
        schema_extra={
            'example':{
                'username':'johndoe',
                'email':'johndoe@gmail.com',
                'password':'password',
                'is_staff':False,
                'is_active':True,
            }
        }


class Settings(BaseModel):
    authjwt_secret_key:str='73e9d2643bf74dab13db4cf4e779200051eeb823c222e9912da0736684b2dcf9'
    
    
class LoginModel(BaseModel):
    username:str
    password:str
    
    
class OrderModel(BaseModel):
    id:Optional[int]
    quantity:int
    order_status:Optional[str]='PENDING'
    pizza_size:Optional[str]='SMALL'
    user_id:Optional[int]
    
    
    class Config:
        orm_mode=True
        schema_extra={
            'example':{
                'quantity':2,
                'pizza_size':'LARGE',
            }
        }


class OrderStatusModel(BaseModel):
    order_status:Optional[str]='PENDING'
    
    class Config:
        orm_mode=True
        schema_extra={
            'example':{
                'order_status':'PENDING',
            }
        }