from typing import List, Optional
from app.repositories.product_repo import ProductRepository, product_repo
from app.schemas import ProductCreate, ProductUpdate, ProductResponse

class ProductService:
    def __init__(self, repo: ProductRepository = product_repo):
        self.repo = repo

    def create_product(self, product: ProductCreate) -> ProductResponse:
        return self.repo.create(product)

    def get_product(self, product_id: int) -> Optional[ProductResponse]:
        return self.repo.get_by_id(product_id)

    def get_all_products(
        self,
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
    ) -> List[ProductResponse]:
        return self.repo.get_all(category, min_price, max_price)

    def update_product(self, product_id: int, product: ProductUpdate) -> Optional[ProductResponse]:
        return self.repo.update(product_id, product)

    def delete_product(self, product_id: int) -> bool:
        return self.repo.delete(product_id)

    def calculate_discount(self, product_id: int, discount_pct: float) -> Optional[dict]:
        product = self.repo.get_by_id(product_id)
        if not product:
            return None
        discount_amount = round(product.price * (discount_pct / 100), 2)
        final_price = round(product.price - discount_amount, 2)
        return {
            "product_id": product.id,
            "original_price": product.price,
            "discount_pct": discount_pct,
            "discount_amount": discount_amount,
            "final_price": final_price,
        }

product_service = ProductService()