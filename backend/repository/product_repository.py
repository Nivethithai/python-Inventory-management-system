from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models import Product
from backend.schemas import ProductCreate, ProductUpdate

class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, payload: ProductCreate):
        product = Product(**payload.dict())
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def get(self, product_id: int):
        result = await self.db.execute(select(Product).where(Product.id == product_id))
        return result.scalars().first()

    async def get_by_sku(self, sku: str):
        result = await self.db.execute(select(Product).where(Product.sku == sku))
        return result.scalars().first()

    async def list(self):
        result = await self.db.execute(select(Product))
        return result.scalars().all()

    async def update(self, product: Product, payload: ProductUpdate):
        for key, value in payload.dict(exclude_unset=True).items():
            setattr(product, key, value)
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def delete(self, product: Product):
        await self.db.delete(product)
        await self.db.commit()
