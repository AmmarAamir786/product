from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.models import Product, ProductCreate, ProductUpdate

# Add a New Product to the Database
def add_new_product(product_data: ProductCreate, session: Session):
    new_product = Product(**product_data.dict())  # Convert ProductCreate to Product
    session.add(new_product)
    session.commit()
    session.refresh(new_product)
    return new_product

# Get All Products from the Database
def get_all_products(session: Session):
    all_products = session.exec(select(Product)).all()
    return all_products

# Get a Product by ID
def get_product_by_id(product_id: int, session: Session):
    product = session.exec(select(Product).where(Product.id == product_id)).one_or_none()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Delete Product by ID
def delete_product_by_id(product_id: int, session: Session):
    product = session.exec(select(Product).where(Product.id == product_id)).one_or_none()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    session.delete(product)
    session.commit()

    return {"message": "Product deleted successfully", "deleted_product": product.dict()}  # Return product info

# Update Product by ID
def update_product_by_id(product_id: int, to_update_product_data: ProductUpdate, session: Session):
    product = session.exec(select(Product).where(Product.id == product_id)).one_or_none()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    # Update product details
    update_data = to_update_product_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)

    session.add(product)
    session.commit()
    session.refresh(product)
    
    return product  # Return the updated product

# Validate Product by ID
def validate_product_by_id(product_id: int, session: Session) -> Product | None:
    product = session.exec(select(Product).where(Product.id == product_id)).one_or_none()
    return product
