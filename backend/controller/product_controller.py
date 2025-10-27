from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database import get_db
from backend.service.product_service import ProductService
from backend.schemas import ProductCreate, ProductUpdate, ProductOut
from typing import List

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=ProductOut)
async def create_product(payload: ProductCreate, db: AsyncSession = Depends(get_db)):
    return await ProductService(db).create_product(payload)

@router.get("/", response_model=List[ProductOut])
async def list_products(db: AsyncSession = Depends(get_db)):
    return await ProductService(db).list_products()

@router.get("/{product_id}", response_model=ProductOut)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    return await ProductService(db).get_product(product_id)

@router.put("/{product_id}", response_model=ProductOut)
async def update_product(product_id: int, payload: ProductUpdate, db: AsyncSession = Depends(get_db)):
    return await ProductService(db).update_product(product_id, payload)

@router.delete("/{product_id}")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    await ProductService(db).delete_product(product_id)
    return {"message": "Product deleted successfully"}
