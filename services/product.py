"""
Product service for managing products and categories
"""
from sqlalchemy.orm import Session
from typing import List, Optional

from core.database import Product, Category

class ProductService:
    """Service for product management"""
    
    def get_products(
        self, 
        db: Session, 
        category: Optional[str] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Product]:
        """Get products with optional filtering"""
        query = db.query(Product).filter(Product.is_active == True)
        
        if category:
            query = query.join(Category).filter(Category.name == category)
        
        if search:
            query = query.filter(Product.name.contains(search))
        
        return query.offset(skip).limit(limit).all()
    
    def get_product(self, db: Session, product_id: int) -> Optional[Product]:
        """Get single product by ID"""
        return db.query(Product).filter(
            Product.id == product_id,
            Product.is_active == True
        ).first()
    
    def get_featured_products(self, db: Session, limit: int = 8) -> List[Product]:
        """Get featured products"""
        return db.query(Product).filter(
            Product.is_featured == True,
            Product.is_active == True
        ).limit(limit).all()
    
    def get_related_products(
        self, 
        db: Session, 
        category_id: int, 
        exclude_id: int,
        limit: int = 4
    ) -> List[Product]:
        """Get related products from same category"""
        return db.query(Product).filter(
            Product.category_id == category_id,
            Product.id != exclude_id,
            Product.is_active == True
        ).limit(limit).all()
    
    def get_categories(self, db: Session) -> List[Category]:
        """Get all categories"""
        return db.query(Category).all()
    
    def update_stock(self, db: Session, product_id: int, quantity_change: int):
        """Update product stock quantity"""
        product = self.get_product(db, product_id)
        if product:
            product.stock_quantity += quantity_change
            db.commit()
            db.refresh(product)
        return product