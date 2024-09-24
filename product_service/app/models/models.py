from typing import Optional
from sqlmodel import SQLModel, Field

# Model for database and responses (including 'id')
class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int
    name: str
    description: str
    price: float
    category: str

# Model for creating a new product (without 'id')
class ProductCreate(SQLModel):
    product_id: int
    name: str
    description: str
    price: float
    category: str

# Model for updating a product (without 'id')
class ProductUpdate(SQLModel):
    product_id: Optional[int] = None  # Optional, since users may want to update only a few fields
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
