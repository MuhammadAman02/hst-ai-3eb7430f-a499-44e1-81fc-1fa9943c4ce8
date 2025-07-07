"""
Main FastAPI application with routes and templates
"""
from fastapi import FastAPI, Request, Depends, HTTPException, Form, File, UploadFile, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional, List
import os
from pathlib import Path

from core.database import get_db, init_db
from models.schemas import Product, User, CartItem, Order
from services.auth import AuthService
from services.product import ProductService
from services.cart import CartService
from services.order import OrderService
from app.config import settings

# Initialize FastAPI app
app = FastAPI(
    title="LuxeCloth - Luxury Fashion",
    description="Premium luxury clothing e-commerce platform",
    version="1.0.0"
)

# Security
security = HTTPBearer(auto_error=False)

# Static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize database
init_db()

# Services
auth_service = AuthService()
product_service = ProductService()
cart_service = CartService()
order_service = OrderService()

# Dependency to get current user
async def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[dict]:
    """Get current user from session or token"""
    # Check session first
    user_id = request.session.get("user_id")
    if user_id:
        return {"user_id": user_id, "email": request.session.get("email")}
    
    # Check token if provided
    if credentials:
        try:
            payload = auth_service.verify_token(credentials.credentials)
            return payload
        except:
            pass
    
    return None

# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint for deployment"""
    return {"status": "healthy", "service": "LuxeCloth E-commerce"}

# Home page
@app.get("/", response_class=HTMLResponse)
async def home(
    request: Request,
    db: Session = Depends(get_db),
    current_user: Optional[dict] = Depends(get_current_user)
):
    """Home page with featured products"""
    try:
        featured_products = product_service.get_featured_products(db, limit=8)
        categories = product_service.get_categories(db)
        
        return templates.TemplateResponse("home.html", {
            "request": request,
            "products": featured_products,
            "categories": categories,
            "current_user": current_user,
            "page_title": "LuxeCloth - Luxury Fashion"
        })
    except Exception as e:
        print(f"Error loading home page: {e}")
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": "Unable to load products",
            "error_details": str(e)
        })

# Products page
@app.get("/products", response_class=HTMLResponse)
async def products(
    request: Request,
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Optional[dict] = Depends(get_current_user)
):
    """Products listing page with filtering"""
    try:
        products_list = product_service.get_products(
            db, category=category, search=search
        )
        categories = product_service.get_categories(db)
        
        return templates.TemplateResponse("products.html", {
            "request": request,
            "products": products_list,
            "categories": categories,
            "current_category": category,
            "search_query": search,
            "current_user": current_user,
            "page_title": f"Products - {category or 'All'}"
        })
    except Exception as e:
        print(f"Error loading products: {e}")
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": "Unable to load products",
            "error_details": str(e)
        })

# Product detail page
@app.get("/product/{product_id}", response_class=HTMLResponse)
async def product_detail(
    request: Request,
    product_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[dict] = Depends(get_current_user)
):
    """Individual product detail page"""
    try:
        product = product_service.get_product(db, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        related_products = product_service.get_related_products(
            db, product.category, exclude_id=product_id, limit=4
        )
        
        return templates.TemplateResponse("product_detail.html", {
            "request": request,
            "product": product,
            "related_products": related_products,
            "current_user": current_user,
            "page_title": product.name
        })
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error loading product detail: {e}")
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": "Unable to load product",
            "error_details": str(e)
        })

# Authentication pages
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page"""
    return templates.TemplateResponse("auth/login.html", {
        "request": request,
        "page_title": "Login"
    })

@app.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Process login"""
    try:
        user = auth_service.authenticate_user(db, email, password)
        if not user:
            return templates.TemplateResponse("auth/login.html", {
                "request": request,
                "error": "Invalid email or password",
                "page_title": "Login"
            })
        
        # Set session
        request.session["user_id"] = user.id
        request.session["email"] = user.email
        
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    except Exception as e:
        print(f"Login error: {e}")
        return templates.TemplateResponse("auth/login.html", {
            "request": request,
            "error": "Login failed",
            "error_details": str(e),
            "page_title": "Login"
        })

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Registration page"""
    return templates.TemplateResponse("auth/register.html", {
        "request": request,
        "page_title": "Register"
    })

@app.post("/register")
async def register(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    full_name: str = Form(...),
    db: Session = Depends(get_db)
):
    """Process registration"""
    try:
        # Check if user exists
        if auth_service.get_user_by_email(db, email):
            return templates.TemplateResponse("auth/register.html", {
                "request": request,
                "error": "Email already registered",
                "page_title": "Register"
            })
        
        # Create user
        user = auth_service.create_user(db, email, password, full_name)
        
        # Set session
        request.session["user_id"] = user.id
        request.session["email"] = user.email
        
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    except Exception as e:
        print(f"Registration error: {e}")
        return templates.TemplateResponse("auth/register.html", {
            "request": request,
            "error": "Registration failed",
            "error_details": str(e),
            "page_title": "Register"
        })

@app.get("/logout")
async def logout(request: Request):
    """Logout user"""
    request.session.clear()
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

# Shopping cart
@app.get("/cart", response_class=HTMLResponse)
async def cart_page(
    request: Request,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Shopping cart page"""
    if not current_user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    try:
        cart_items = cart_service.get_cart_items(db, current_user["user_id"])
        total = cart_service.calculate_total(cart_items)
        
        return templates.TemplateResponse("cart.html", {
            "request": request,
            "cart_items": cart_items,
            "total": total,
            "current_user": current_user,
            "page_title": "Shopping Cart"
        })
    except Exception as e:
        print(f"Cart error: {e}")
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": "Unable to load cart",
            "error_details": str(e)
        })

# Add middleware for sessions
from starlette.middleware.sessions import SessionMiddleware
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

# CORS middleware for API calls
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)