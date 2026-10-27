import sys
sys.path.insert(0, r"C:\Users\Aaron\Desktop\AAProject\backend")

# Test the import chain
from app.interface.api.v1.router import router as direct_router
print("Direct import works:", direct_router)

from app.interface.api.v1 import router as router_from_package
print("Import from package works:", router_from_package)

from app.main import create_app
app = create_app()

# Check if our router is in the app's routers
for r in app.routes:
    print(f"App route: {getattr(r, 'path', '?')}")

# Try to add the router manually
from app.interface.api.v1.router import router as api_router_v1
print(f"\nRouter object: {api_router_v1}")
print(f"Router routes: {[r.path for r in api_router_v1.routes if hasattr(r, 'path')]}")

# Try including it
app.include_router(api_router_v1, prefix="/api/v1")
print(f"\nAfter include_router, total routes: {len(app.routes)}")
for route in app.routes:
    path = getattr(route, 'path', '?')
    if '/api/v1' in str(path):
        print(f"  Found: {path} - {getattr(route, 'methods', '?')}")