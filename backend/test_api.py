import sys
sys.path.insert(0, r"C:\Users\Aaron\Desktop\AAProject\backend")

from app.main import create_app
app = create_app()

from app.interface.api.v1.router import router as api_router_v1
app.include_router(api_router_v1, prefix="/api/v1")

from fastapi.testclient import TestClient
client = TestClient(app)

print("Test /api/v1/health:")
resp = client.get('/api/v1/health')
print(f"  Status: {resp.status_code}")
print(f"  Body: {resp.json()}")

print("\nTest /api/v1/categories:")
resp = client.get('/api/v1/categories')
print(f"  Status: {resp.status_code}")
print(f"  Body: {resp.json()}")