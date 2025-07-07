"""
Database configuration and connection
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from datetime import datetime
import os

from app.config import settings

# Database setup
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    cart_items = relationship("CartItem", back_populates="user")
    orders = relationship("Order", back_populates="user")

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    
    # Relationships
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    image_url = Column(String)
    stock_quantity = Column(Integer, default=0)
    is_featured = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    category = relationship("Category", back_populates="products")
    cart_items = relationship("CartItem", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")

class CartItem(Base):
    __tablename__ = "cart_items"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_amount = Column(Float, nullable=False)
    status = Column(String, default="pending")  # pending, confirmed, shipped, delivered
    shipping_address = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)  # Price at time of order
    
    # Relationships
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")

def get_db() -> Session:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database with sample data"""
    Base.metadata.create_all(bind=engine)
    
    # Add sample data
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(Category).first():
            return
        
        # Create categories
        categories = [
            Category(name="Men's Suits", description="Premium men's formal wear"),
            Category(name="Women's Dresses", description="Elegant women's dresses"),
            Category(name="Accessories", description="Luxury accessories"),
            Category(name="Shoes", description="Designer footwear"),
        ]
        
        for category in categories:
            db.add(category)
        db.commit()
        
        # Create sample products
        products = [
            Product(
                name="Classic Navy Suit",
                description="Handcrafted navy blue suit made from premium wool. Perfect for business meetings and formal events.",
                price=1299.99,
                category_id=1,
                image_url="https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=800&h=600&fit=crop",
                stock_quantity=15,
                is_featured=True
            ),
            Product(
                name="Elegant Black Dress",
                description="Sophisticated black evening dress with intricate detailing. Made from premium silk.",
                price=899.99,
                category_id=2,
                image_url="https://images.unsplash.com/photo-1566479179817-c0b0b1e3b2e5?w=800&h=600&fit=crop",
                stock_quantity=8,
                is_featured=True
            ),
            Product(
                name="Luxury Leather Handbag",
                description="Handcrafted Italian leather handbag with gold-plated hardware.",
                price=599.99,
                category_id=3,
                image_url="https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=800&h=600&fit=crop",
                stock_quantity=12,
                is_featured=True
            ),
            Product(
                name="Designer Oxford Shoes",
                description="Premium leather Oxford shoes with traditional craftsmanship.",
                price=449.99,
                category_id=4,
                image_url="https://images.unsplash.com/photo-1549298916-b41d501d3772?w=800&h=600&fit=crop",
                stock_quantity=20,
                is_featured=True
            ),
            Product(
                name="Charcoal Grey Suit",
                description="Modern fit charcoal grey suit perfect for contemporary professionals.",
                price=1199.99,
                category_id=1,
                image_url="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&h=600&fit=crop",
                stock_quantity=10
            ),
            Product(
                name="Silk Evening Gown",
                description="Luxurious silk evening gown with beaded embellishments.",
                price=1599.99,
                category_id=2,
                image_url="https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=800&h=600&fit=crop",
                stock_quantity=5
            ),
            Product(
                name="Gold Watch",
                description="Swiss-made luxury watch with 18k gold case.",
                price=2999.99,
                category_id=3,
                image_url="https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&h=600&fit=crop",
                stock_quantity=3
            ),
            Product(
                name="Leather Loafers",
                description="Comfortable leather loafers with premium construction.",
                price=329.99,
                category_id=4,
                image_url="https://images.unsplash.com/photo-1560769629-975ec94e6a86?w=800&h=600&fit=crop",
                stock_quantity=25
            ),
        ]
        
        for product in products:
            db.add(product)
        db.commit()
        
        print("✅ Database initialized with sample data")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()