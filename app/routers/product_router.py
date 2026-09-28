from fastapi import APIRouter, HTTPException, Query, status
from typing import List, Optional
from app.schemas import ProductCreate, ProductUpdate, ProductResponse
from app.services.product_service import product_service

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate):
    return product_service.create_product(product)

@router.get("/", response_model=List[ProductResponse])
def get_products(
    category: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
):
    return product_service.get_all_products(category, min_price, max_price)

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int):
    prod = product_service.get_product(product_id)
    if not prod:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found",
        )
    return prod

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductUpdate):
    updated = product_service.update_product(product_id, product)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found",
        )
    return updated

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int):
    success = product_service.delete_product(product_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found",
        )

@router.get("/{product_id}/discount")
def get_discount(
    product_id: int,
    pct: float = Query(..., gt=0, le=100, description="Discount percentage (1-100)"),
):
    result = product_service.calculate_discount(product_id, pct)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found",
        )
    return result