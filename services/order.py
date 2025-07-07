"""
Order management service
"""
from sqlalchemy.orm import Session
from typing import List

from core.database import Order, OrderItem, CartItem
from services.cart import CartService

class OrderService:
    """Service for order management"""
    
    def __init__(self):
        self.cart_service = CartService()
    
    def create_order_from_cart(
        self, 
        db: Session, 
        user_id: int, 
        shipping_address: str
    ) -> Order:
        """Create order from user's cart"""
        # Get cart items
        cart_items = self.cart_service.get_cart_items(db, user_id)
        if not cart_items:
            raise ValueError("Cart is empty")
        
        # Calculate total
        total_amount = self.cart_service.calculate_total(cart_items)
        
        # Create order
        order = Order(
            user_id=user_id,
            total_amount=total_amount,
            shipping_address=shipping_address,
            status="pending"
        )
        db.add(order)
        db.commit()
        db.refresh(order)
        
        # Create order items
        for cart_item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            db.add(order_item)
        
        # Clear cart
        self.cart_service.clear_cart(db, user_id)
        
        db.commit()
        return order
    
    def get_user_orders(self, db: Session, user_id: int) -> List[Order]:
        """Get all orders for user"""
        return db.query(Order).filter(Order.user_id == user_id).all()
    
    def get_order(self, db: Session, order_id: int) -> Order:
        """Get single order by ID"""
        return db.query(Order).filter(Order.id == order_id).first()
    
    def update_order_status(self, db: Session, order_id: int, status: str) -> Order:
        """Update order status"""
        order = self.get_order(db, order_id)
        if order:
            order.status = status
            db.commit()
            db.refresh(order)
        return order