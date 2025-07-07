"""
Luxury Clothing E-commerce Platform
Entry point for the FastAPI application
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from app.main import app

if __name__ == "__main__":
    import uvicorn
    
    # Dependency check
    def check_dependencies():
        """Verify all required dependencies are available."""
        required_packages = ['fastapi', 'uvicorn', 'jinja2', 'sqlalchemy', 'python_dotenv']
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package.replace('-', '_'))
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            print(f"❌ Missing packages: {', '.join(missing_packages)}")
            print(f"📦 Install with: pip install {' '.join(missing_packages)}")
            return False
        
        print("✅ All dependencies available")
        return True
    
    if check_dependencies():
        port = int(os.getenv("PORT", 8000))
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=port,
            reload=True
        )
    else:
        exit(1)