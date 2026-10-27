"""Script simple para verificar la estructura del backend."""
import os
import sys

backend_dir = r"C:\Users\Aaron\Desktop\AAProject\backend"
python_files = []

for root, dirs, files in os.walk(backend_dir):
    for f in files:
        if f.endswith('.py'):
            python_files.append(os.path.join(root, f))

print(f"Total archivos Python: {len(python_files)}")
print("\nEstructura de directorios:")
for root, dirs, files in os.walk(backend_dir):
    level = root.replace(backend_dir, "").count(os.sep)
    indent = " " * 2 * level
    print(f"{indent}{os.path.basename(root)}/")
    subindent = " " * 2 * (level + 1)
    for file in files:
        if file.endswith('.py'):
            print(f"{subindent}{file}")

print("\n--- Archivos Python ---")
for f in sorted(python_files):
    rel = os.path.relpath(f, backend_dir)
    print(f"  {rel}")