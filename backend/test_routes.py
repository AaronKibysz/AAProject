import sys
sys.path.insert(0, r"C:\Users\Aaron\Desktop\AAProject\backend")

from app.main import create_app
app = create_app()

print("Total routes:", len(app.routes))
for route in app.routes:
    path = getattr(route, "path", "?")
    methods = getattr(route, "methods", "?")
    print(f"  {methods} {path}")