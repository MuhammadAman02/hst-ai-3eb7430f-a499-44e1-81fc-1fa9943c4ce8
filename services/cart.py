"""
Shopping cart service
"""
from sqlalchemy.orm import Session
from typing import List

from core.database import CartItem, Product

class CartService:
    """Service for shopping cart management"""
    
    def get_cart_items(self, db: Session, user_id: int) -> List[CartItem]:
        """Get all cart items for user"""
        return db.query(CartItem).filter(CartItem.user_id == user_id).all()
    
    def add_to_cart(self, db: Session, user_id: int, product_id: int, quantity: int = 1) -> CartItem:
        """Add item to cart or update quantity if exists"""
        # Check if item already in cart
        existing_item = db.query(CartItem).filter(
            CartItem.user_id == user_id,
            CartItem.product_id == product_id
        ).first()
        
        if existing_item:
            existing_item.quantity += quantity
            db.commit()
            db.refresh(existing_item)
            return existing_item
        else:
            cart_item = CartItem(
                user_id=user_id,
                product_id=product_id,
                quantity=quantity
            )
            db.add(cart_item)
            db.commit()
            db.refresh(cart_item)
            return cart_item
    
    def update_cart_item(self, db: Session, cart_item_id: int, quantity: int) -> CartItem:
        """Update cart item quantity"""
        cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()
        if cart_item:
            if quantity <= 0:
                db.delete(cart_item)
            else:
                cart_item.quantity = quantity
            db.commit()
            if quantity > 0:
                db.refresh(cart_item)
        return cart_item
    
    def remove_from_cart(self, db: Session, cart_item_id: int):
        """Remove item from cart"""
        cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()
        if cart_item:
            db.delete(cart_item)
            db.commit()
    
    def clear_cart(self, db: Session, user_id: int):
        """Clear all items from user's cart"""
        db.query(CartItem).filter(CartItem.user_id == user_id).delete()
        db.commit()
    
    def calculate_total(self, cart_items: List[CartItem]) -> float:
        """Calculate total price for cart items"""
        total = 0.0
        for item in cart_items:
            total += item.product.price * item.quantity
        return total