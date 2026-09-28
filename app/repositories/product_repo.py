from typing import Dict, List, Optional
from app.schemas import ProductCreate, ProductUpdate, ProductResponse

class ProductRepository:
    def __init__(self):
        self._db: Dict[int, dict] = {}
        self._counter: int = 0

    def create(self, product: ProductCreate) -> ProductResponse:
        self._counter += 1
        data = product.model_dump()
        data["id"] = self._counter
        self._db[self._counter] = data
        return ProductResponse(**data)

    def get_by_id(self, product_id: int) -> Optional[ProductResponse]:
        data = self._db.get(product_id)
        if data:
            return ProductResponse(**data)
        return None

    def get_all(
        self,
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
    ) -> List[ProductResponse]:
        results = list(self._db.values())
        if category:
            results = [p for p in results if p["category"].lower() == category.lower()]
        if min_price is not None:
            results = [p for p in results if p["price"] >= min_price]
        if max_price is not None:
            results = [p for p in results if p["price"] <= max_price]
        return [ProductResponse(**p) for p in results]

    def update(self, product_id: int, product: ProductUpdate) -> Optional[ProductResponse]:
        if product_id not in self._db:
            return None
        current = self._db[product_id]
        update_data = product.model_dump(exclude_unset=True)
        current.update(update_data)
        self._db[product_id] = current
        return ProductResponse(**current)

    def delete(self, product_id: int) -> bool:
        if product_id in self._db:
            del self._db[product_id]
            return True
        return False

    def clear(self):
        self._db.clear()
        self._counter = 0

product_repo = ProductRepository()