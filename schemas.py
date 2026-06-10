from typing import List, Optional
from pydantic import BaseModel, EmailStr, field_validator, ConfigDict  # data validation = pydantic = class
import re
from datetime import datetime
from enums import OrderStatus

#Article inside UserDisplay
class Post(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    content: str

class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[^\w\s]', v):
            raise ValueError('Password must contain at least one special character')
        return v

class ImageInUser (BaseModel):
    model_config = ConfigDict(from_attributes=True)
    file_path: str
    id: int

class UserDisplay(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str
    email: str
    id: int
    images: List[ImageInUser] = []
    posts: List[Post] = []  #tpye of data which we want return

class UserImage (BaseModel):
    id: int
    file_path: str
    user_id: int


class FriendshipBase(BaseModel):
    user_id: int
    friend_id: int
    sender_username: str

class FriendshipCreate(FriendshipBase):
    pass

class Friendship(FriendshipBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

class FriendRequests(BaseModel):
    friend_requests: List[Friendship]
        

#user inside article display and ProductDisplay
class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:int
    username: str

class PostBase(BaseModel): #what we recieve from the user when we are creating post
    content: str
    user_id : int
    username: str
    timestamp: datetime

class ImageInPost (BaseModel):
    model_config = ConfigDict(from_attributes=True)
    file_path: str
    id: int

class  PostDisplay(BaseModel): #a data structure to send to the user when we are creating post
    model_config = ConfigDict(from_attributes=True)
    id: int
    content: str
    user: User
    user_id : int
    images: List[ImageInPost] = []
    timestamp: datetime

class PostUpdate(BaseModel):
    content: str
    image_url: str = None

class PostImage (BaseModel):
    id: int
    file_path: str
    post_id: int

class UserAuth(BaseModel):
    id: int
    username: str
    email: str


#For Post Display
class CommentDisplay(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    txt: str
    user_id: int
    username: str
    timestamp: datetime

class CommentBase(BaseModel):
    txt: str
    username: str
    post_id: int
    user_id: int


#Group
        
class GroupBase(BaseModel):
    name: str
    description: str
    created_at: datetime = datetime.now()
    creator_id: int  # ID of the user who created the group
    members: List[int] = []  # List of user IDs representing members of the group
    is_public: bool = True  # Indicates whether the group is public or private
    visibility: str = "public"  # Visibility settings of the group

class GroupDisplay(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    description: str
    created_at: datetime
    creator_id: int
    members: List[int]
    visibility: str

class GroupMembershipRequest(BaseModel):
    user_id: int

class GroupMembershipResponse(BaseModel):
    message: str

class GroupMembers(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username:str

class GroupPostBase(BaseModel):
    content: str
    group_id: int
    author_id: int
    created_at: datetime = datetime.now()

class GroupPostCreate(GroupPostBase):
    pass

class GroupPostDisplay(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    content: str
    group_id: int
    author_id: int
    created_at: datetime = datetime.now()

class GroupPostUpdate(BaseModel):
    content: str

class ProductBase (BaseModel):
    product_name: str
    description: str
    price: float
    quantity: int 
    published: bool

class TestProductBase (BaseModel):
    product_name: str
    description: str
    price: float
    quantity: int 
    published: bool
    seller_id: int

#PRoductReview inside ReviewDisplay
class ProductReview (BaseModel):
    model_config = ConfigDict(from_attributes=True)
    product_name: str
    seller_id: int

#ImageInProduct inside ProductDisplay
class ImageInProduct (BaseModel):
    model_config = ConfigDict(from_attributes=True)
    file_path: str
    id: int

class ProductDisplay (BaseModel):
    model_config = ConfigDict(from_attributes=True)
    product_name: str
    id: int
    description: str
    price: float
    quantity: float
    images: List[ImageInProduct] = []
    published: bool
    user: User

class ProductImage (BaseModel):
    id: int
    file_path: str
    product_id: int

class MinOrderLine(BaseModel):
    product_id: int
    quantity: int

class OrderLine(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    order_id: Optional[int]
    id: int
    product_id: int
    quantity: int
    total: Optional[float]

#Inside Order
class OrderLines(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    product_id: int
    quantity: int
    total: Optional[float]

class Order(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    order_status: OrderStatus
    user_id: int
    total: float = 0
    order_lines: List[OrderLines] = []

class Review(BaseModel):
    score: int
    comment: str

#Username inside ReviewDisplay
class Username(BaseModel):
    username: str

class ReviewDisplay(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    creator_id: int
    creator_username: Username
    product_id: int
    score: int
    comment: str
    product: ProductReview

#Product inside UserProductDisplay
class Product(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    product_name: str
    id: int
    description: str
    price: float
    published: bool

class UserProductDisplay(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str
    email: str
    id: int
    products: List[Product] = []
