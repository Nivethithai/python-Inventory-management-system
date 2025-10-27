from fastapi import HTTPException, status
from backend.repository.product_repository import ProductRepository
from backend.schemas import ProductCreate, ProductUpdate

class ProductService:
    def __init__(self, db):
        self.repo = ProductRepository(db)

    async def create_product(self, payload: ProductCreate):
        if await self.repo.get_by_sku(payload.sku):
            raise HTTPException(status_code=400, detail="SKU already exists")
        return await self.repo.create(payload)

    async def list_products(self):
        return await self.repo.list()

    async def get_product(self, product_id: int):
        product = await self.repo.get(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

    async def update_product(self, product_id: int, payload: ProductUpdate):
        product = await self.repo.get(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return await self.repo.update(product, payload)

    async def delete_product(self, product_id: int):
        product = await self.repo.get(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        await self.repo.delete(product)
