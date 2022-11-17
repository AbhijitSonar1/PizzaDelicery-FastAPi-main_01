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
                "username":"abc",
                "email":"abc@gmail.com",
                "password":"abhijit@1287",
                "is_staff":True,
                "is_active":True
            }
        }

class Setting(BaseModel):
    authjwt_secret_key:str='59a868c03a8a13f75fe19c6dba403c2d2528f206988edc68e4963efaa45be61e'
    

class LoginModel(BaseModel):
    username:str
    password:str
    

class OrderModel(BaseModel):
    id:Optional[int]
    quantity:int
    order_status:Optional[str]="PENDING"
    pizza_size:Optional[str]="SMALL"
    user_id:Optional[int]
    class Config:
        orm_mode=True
        schema_extra={
            "example":{
                "quantity":2,
                "pizza_size":"LARGE",
            }
        }
        
class OrderstatusModel(BaseModel):
    order_status:Optional[str]="PENDING"
    
    class Config:
        orm_mode=True
        schema_extra={
            "example":{
                "order_status":"PENDING"
            }
        }