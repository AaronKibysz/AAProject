import sys
sys.path.insert(0, r"C:\Users\Aaron\Desktop\AAProject\backend")

from app.main import create_app
app = create_app()

# Include the router like the app does
from app.interface.api.v1.router import router as api_router_v1
app.include_router(api_router_v1, prefix="/api/v1")

print("Total routes:", len(app.routes))
print("\nAll routes:")
for route in app.routes:
    path = getattr(route, "path", None)
    methods = getattr(route, "methods", None)
    if path and "/api/v1" in str(path):
        print(f"  {methods} {path}")
    elif path:
        print(f"  {methods} {path}")