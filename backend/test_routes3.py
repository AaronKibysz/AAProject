import sys
sys.path.insert(0, r"C:\Users\Aaron\Desktop\AAProject\backend")

from app.main import create_app
app = create_app()

from app.interface.api.v1.router import router as router_v1
app.include_router(router_v1, prefix="/api/v1")

print("Total routes:", len(app.routes))
print("\nAll routes (filtering /api/v1):")
for route in app.routes:
    path = getattr(route, "path", None)
    if path and ("/api/v1" in str(path) or "/health" in str(path)):
        print(f"  PATH: {path} - METHODS: {getattr(route, 'methods', '?')}")

print("\nAll routes (ALL):")
for route in app.routes:
    path = getattr(route, "path", None)
    print(f"  PATH: {path}")