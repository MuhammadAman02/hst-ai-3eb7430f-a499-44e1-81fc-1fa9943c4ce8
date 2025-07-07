# LuxeCloth - Luxury Fashion E-commerce Platform

A sophisticated e-commerce platform for luxury clothing and accessories, built with FastAPI, SQLAlchemy, and modern web technologies.

## ✨ Features

### 🛍️ E-commerce Functionality
- **Product Catalog**: Browse luxury clothing and accessories
- **Category Filtering**: Shop by Men's Suits, Women's Dresses, Accessories, and Shoes
- **Search Functionality**: Find products by name or description
- **Shopping Cart**: Add, update, and remove items
- **User Authentication**: Secure registration and login system
- **Order Management**: Track orders and purchase history

### 🎨 Luxury Design
- **Premium UI/UX**: Elegant, modern interface with luxury aesthetics
- **Responsive Design**: Optimized for desktop, tablet, and mobile
- **High-Quality Images**: Professional product photography
- **Smooth Animations**: Subtle hover effects and transitions
- **Typography**: Premium fonts (Playfair Display, Inter)

### 🔧 Technical Excellence
- **FastAPI Backend**: High-performance async web framework
- **SQLAlchemy ORM**: Robust database management
- **Jinja2 Templates**: Server-side rendering for SEO
- **Bootstrap 5**: Modern, responsive CSS framework
- **Security**: Password hashing, session management, CORS protection
- **Error Handling**: Comprehensive error management with user feedback

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

4. **Open your browser** and navigate to:
   ```
   http://localhost:8000
   ```

The application will automatically:
- Create the SQLite database
- Set up sample products and categories
- Start the web server

## 📁 Project Structure

```
LuxeCloth/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── .env                   # Environment configuration
├── app/
│   ├── main.py            # FastAPI routes and pages
│   └── config.py          # Application settings
├── core/
│   └── database.py        # Database models and setup
├── models/
│   └── schemas.py         # Pydantic validation models
├── services/              # Business logic
│   ├── auth.py           # Authentication service
│   ├── product.py        # Product management
│   ├── cart.py           # Shopping cart logic
│   └── order.py          # Order processing
├── templates/             # HTML templates
│   ├── base.html         # Base template
│   ├── home.html         # Homepage
│   ├── products.html     # Product listing
│   ├── product_detail.html # Product details
│   ├── cart.html         # Shopping cart
│   └── auth/             # Authentication pages
├── static/               # Static assets
│   ├── css/
│   └── js/
└── tests/               # Test suite
```

## 🛠️ Configuration

### Environment Variables

Copy `.env` file and customize:

```bash
# Database
DATABASE_URL=sqlite:///./luxecloth.db

# Security
SECRET_KEY=your-secret-key-here

# Application
DEBUG=True
PORT=8000
```

### Database Setup

The application uses SQLite by default. For production, you can configure PostgreSQL or MySQL:

```bash
# PostgreSQL
DATABASE_URL=postgresql://username:password@localhost/luxecloth

# MySQL
DATABASE_URL=mysql://username:password@localhost/luxecloth
```

## 🎯 Usage

### Customer Features

1. **Browse Products**:
   - Visit the homepage to see featured items
   - Use the Products page to browse all items
   - Filter by category or search by name

2. **Shopping Cart**:
   - Add items to cart (requires login)
   - Update quantities or remove items
   - View order summary with tax calculation

3. **User Account**:
   - Register for a new account
   - Login to access cart and orders
   - Secure password hashing

### Sample Data

The application includes sample products:
- **Men's Suits**: Classic Navy Suit, Charcoal Grey Suit
- **Women's Dresses**: Elegant Black Dress, Silk Evening Gown
- **Accessories**: Luxury Leather Handbag, Gold Watch
- **Shoes**: Designer Oxford Shoes, Leather Loafers

## 🔒 Security Features

- **Password Hashing**: Bcrypt for secure password storage
- **Session Management**: Secure user sessions
- **Input Validation**: Pydantic models for data validation
- **CORS Protection**: Configured for secure API access
- **SQL Injection Prevention**: Parameterized queries
- **XSS Protection**: Proper output encoding

## 🚀 Deployment

### Docker Deployment

```bash
# Build the image
docker build -t luxecloth .

# Run the container
docker run -p 8000:8000 luxecloth
```

### Fly.io Deployment

```bash
# Install Fly CLI and login
fly auth login

# Deploy the application
fly deploy
```

## 🧪 Testing

Run the test suite:

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest
```

## 📊 Performance

- **Response Time**: < 200ms for most pages
- **Database**: Optimized queries with proper indexing
- **Caching**: Static asset caching
- **Async**: Non-blocking I/O operations
- **Memory**: Efficient resource usage

## 🔧 Development

### Adding New Products

Products are managed through the database. You can:

1. **Add via Database**: Insert directly into the `products` table
2. **Admin Interface**: Extend with admin functionality
3. **API Endpoints**: Create management endpoints

### Customizing Design

- **Colors**: Modify CSS variables in `templates/base.html`
- **Fonts**: Update Google Fonts imports
- **Layout**: Customize Bootstrap components
- **Images**: Replace product images with your own

### Extending Functionality

- **Payment Processing**: Integrate Stripe or PayPal
- **Email Notifications**: Add order confirmation emails
- **Inventory Management**: Track stock levels
- **Reviews**: Add product reviews and ratings
- **Wishlist**: Save favorite products

## 🐛 Troubleshooting

### Common Issues

1. **Database Errors**:
   ```bash
   # Reset database
   rm luxecloth.db
   python main.py
   ```

2. **Dependency Conflicts**:
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   pip install -r requirements.txt
   ```

3. **Port Already in Use**:
   ```bash
   # Change port in .env file
   PORT=8001
   ```

### Error Handling

The application includes comprehensive error handling:
- **User-Friendly Messages**: Clear error descriptions
- **Technical Details**: Debug information for developers
- **Graceful Degradation**: Partial functionality when services fail
- **Logging**: Detailed logs for troubleshooting

## 📈 Future Enhancements

- **Payment Integration**: Stripe/PayPal checkout
- **Order Tracking**: Real-time order status
- **Admin Dashboard**: Product and order management
- **Email Notifications**: Order confirmations and updates
- **Product Reviews**: Customer feedback system
- **Wishlist**: Save favorite items
- **Inventory Management**: Stock tracking and alerts
- **Multi-language**: Internationalization support
- **Mobile App**: React Native companion app

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **FastAPI**: Modern, fast web framework
- **SQLAlchemy**: Powerful ORM
- **Bootstrap**: Responsive CSS framework
- **Unsplash**: High-quality product images
- **Font Awesome**: Beautiful icons

---

**LuxeCloth** - Where luxury meets technology. Built with ❤️ for the discerning customer.