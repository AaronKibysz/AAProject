"""Script para inicializar la base de datos y cargar datos de muestra."""
import sys
import os
import json

# Add backend to path - trabajar desde el directorio backend
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

from app.infrastructure.database import Base, engine
from app.domain.entities.category import Category
from app.domain.entities.pilot import Pilot
from app.domain.entities.circuit import Circuit
from app.domain.entities.season import Season
from app.domain.entities.result import Result
from app.domain.entities.session import Session


# Rutas a los archivos de datos de muestra (fuera de /app para que funcionen tanto local como en container)
SAMPLES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'samples')

# Rutas absolutas para compatibilidad con container Docker
ABS_SAMPLES_DIR = r'C:\Users\Aaron\Desktop\AAProject\data\samples'


def parse_json_file(filepath):
    """Parsear un archivo que puede contener múltiples objetos JSON concatenados (formato JSONL)."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Intentar parsear como array JSON primero
    try:
        data = json.loads(content)
        if isinstance(data, list):
            return data
        # Si es un solo objeto, envolverlo en lista
        return [data]
    except json.JSONDecodeError:
        # Formato JSONL: múltiples objetos JSON concatenados
        objects = []
        # Split by '}{' with proper handling
        # Asegurar que empiece y termine con {}
        if not content.startswith('['):
            content = '[' + content + ']'
        try:
            data = json.loads(content)
            if isinstance(data, list):
                return data
        except:
            pass
        
        # Intentar extraer objetos individuales por línea o patrón
        import re
        # Buscar patrones {...} en el texto
        start = 0
        while start < len(content):
            start = content.find('{', start)
            if start == -1:
                break
            # Encontrar el cierre correspondiente
            depth = 0
            end = start
            for i in range(start, len(content)):
                if content[i] == '{':
                    depth += 1
                elif content[i] == '}':
                    depth -= 1
                    if depth == 0:
                        end = i + 1
                        break
            try:
                obj_str = content[start:end]
                obj = json.loads(obj_str)
                objects.append(obj)
            except json.JSONDecodeError:
                pass
            start = end
        
        return objects


def init_database():
    """Crear todas las tablas en la base de datos."""
    # Crear todas las tablas definidas en los modelos
    Base.metadata.create_all(bind=engine)
    print("[OK] Tablas creadas exitosamente en automovilismo_db")
    
    # Verificar que se crearon
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"Tablas en la BD: {tables}")
    return tables


def load_sample_data():
    """Cargar datos de muestra desde los archivos JSON."""
    from app.infrastructure.database import SessionLocal
    
    db = SessionLocal()
    
    try:
        # Cargar categorías
        print("\n--- Cargando categorías ---")
        categorias_path = os.path.join(SAMPLES_DIR, 'categories_sample.json')
        # Fallback a ruta absoluta si la relativa no existe (ej. en container)
        if not os.path.exists(categorias_path):
            categorias_path = os.path.join(ABS_SAMPLES_DIR, 'categories_sample.json')
        
        if os.path.exists(categorias_path):
            categorias = parse_json_file(categorias_path)
            print(f"Archivo encontrado: {len(categorias)} categorías en JSON")
            
            for sample in categorias:
                # Asegurar que tiene las claves necesarias
                name = sample.get("name", "")
                if not name:
                    continue
                existente = db.query(Category).filter_by(name=name).first()
                if not existente:
                    db.add(Category(
                        name=sample.get("name", ""),
                        description=sample.get("description", ""),
                        is_ficticio=sample.get("is_ficticio", False)
                    ))
                    print(f"  [OK] {name} (oficial={not sample.get('is_ficticio', False)}, ficticio={sample.get('is_ficticio', False)})")
                else:
                    print(f"  - {name} ya existe")
            db.commit()
            print("[OK] Categorías cargadas")
        else:
            print(f"[X] Archivo no encontrado: {categorias_path}")
        
        # Cargar pilotos
        print("\n--- Cargando pilotos ---")
        pilots_path = os.path.join(SAMPLES_DIR, 'pilots_sample.json')
        # Fallback a ruta absoluta si la relativa no existe (ej. en container)
        if not os.path.exists(pilots_path):
            pilots_path = os.path.join(ABS_SAMPLES_DIR, 'pilots_sample.json')
        
        if os.path.exists(pilots_path):
            pilotos = parse_json_file(pilots_path)
            print(f"Archivo encontrado: {len(pilotos)} pilotos en JSON")
            
            for sample in pilotos:
                name = sample.get("name", "")
                if not name:
                    continue
                existente = db.query(Pilot).filter_by(name=name).first()
                if not existente:
                    # El archivo JSON tiene campos extra (number, category_id) que no mapeamos directamente
                    # pero el modelo Pilot solo tiene name, team, is_ficticio
                    db.add(Pilot(
                        name=sample.get("name", ""),
                        team=sample.get("team", ""),
                        is_ficticio=sample.get("is_ficticio", False)
                    ))
                    print(f"  [OK] {name} (oficial={not sample.get('is_ficticio', False)}, ficticio={sample.get('is_ficticio', False)})")
                else:
                    print(f"  - {name} ya existe")
            db.commit()
            print("[OK] Pilotos cargados")
        else:
            print(f"[X] Archivo no encontrado: {pilots_path}")
        
        # Cargar circuitos
        print("\n--- Cargando circuitos ---")
        circuits_path = os.path.join(SAMPLES_DIR, 'circuits_sample.json')
        # Fallback a ruta absoluta si la relativa no existe (ej. en container)
        if not os.path.exists(circuits_path):
            circuits_path = os.path.join(ABS_SAMPLES_DIR, 'circuits_sample.json')
        
        if os.path.exists(circuits_path):
            circuits = parse_json_file(circuits_path)
            print(f"Archivo encontrado: {len(circuits)} circuitos en JSON")
            
            for sample in circuits:
                name = sample.get("name", "")
                if not name:
                    continue
                existente = db.query(Circuit).filter_by(name=name).first()
                if not existente:
                    db.add(Circuit(
                        name=sample.get("name", ""),
                        location=sample.get("location", ""),
                        is_ficticio=sample.get("is_ficticio", False)
                    ))
                    print(f"  [OK] {name} (oficial={not sample.get('is_ficticio', False)}, ficticio={sample.get('is_ficticio', False)})")
                else:
                    print(f"  - {name} ya existe")
            db.commit()
            print("[OK] Circuitos cargados")
        else:
            print(f"[X] Archivo no encontrado: {circuits_path}")
        
        print("\n[OK] Datos de muestra cargados exitosamente")
        
    except Exception as e:
        db.rollback()
        print(f"[X] Error al cargar datos: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 60)
    print("INICIALIZANDO BASE DE DATOS - automovilismo-app")
    print("=" * 60)
    
    # Paso 1: Crear tablas
    tables = init_database()
    
    # Verificar que las tablas necesarias existen
    required_tables = ['categories', 'pilots', 'circuits']
    missing = [t for t in required_tables if t not in tables]
    if missing:
        print(f"[X] Tablas faltantes después de create_all: {missing}")
        sys.exit(1)
    
    # Paso 2: Cargar datos de muestra
    load_sample_data()
    
    print("\n" + "=" * 60)
    print("INICIALIZACIÓN COMPLETADA")
    print("=" * 60)