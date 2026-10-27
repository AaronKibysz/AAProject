"""
Script para sembrar datos de Fase 3 (Season, Result, Session) en PostgreSQL.
"""
import sys
sys.path.insert(0, r'C:\Users\Aaron\Desktop\AAProject\backend')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone

from app.infrastructure.database import engine
from app.domain.entities.season import Season
from app.domain.entities.result import Result
from app.domain.entities.session import Session as SessionEntity
from app.domain.entities.category import Category
from app.domain.entities.pilot import Pilot
from app.domain.entities.circuit import Circuit

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = SessionLocal()

try:
    # Verificar si ya hay datos
    existing_seasons = db.query(Season).count()
    existing_results = db.query(Result).count()
    existing_sessions = db.query(SessionEntity).count()
    
    print(f"Estado actual: {existing_seasons} temporadas, {existing_results} resultados, {existing_sessions} sesiones")
    
    if existing_seasons == 0:
        print("\n--- Sembrando temporadas ---")
        seasons_data = [
            {"year": 2024, "category_id": 1, "is_active": True, "is_ficticio": False,
             "start_date": "2024-02-15", "end_date": "2024-12-15"},
            {"year": 2023, "category_id": 1, "is_active": False, "is_ficticio": False,
             "start_date": "2023-02-12", "end_date": "2023-12-10"},
            {"year": 2022, "category_id": 1, "is_active": False, "is_ficticio": False,
             "start_date": "2022-02-20", "end_date": "2022-12-11"},
            {"year": 2025, "category_id": 1, "is_active": False, "is_ficticio": True,
             "start_date": "2025-02-10", "end_date": "2025-12-14"},
        ]
        
        for s in seasons_data:
            season = Season(
                year=s["year"],
                category_id=s["category_id"],
                is_active=s["is_active"],
                is_ficticio=s["is_ficticio"],
                start_date=datetime.fromisoformat(s["start_date"]),
                end_date=datetime.fromisoformat(s["end_date"]),
            )
            db.add(season)
            print(f"  [OK] Temporada {s['year']} (oficial={not s['is_ficticio']})")
        
        db.commit()
        print("[OK] Temporadas cargadas")
    else:
        print("- Temporadas ya existen, saltando")
    
    # Obtener IDs para resultados y sesiones
    seasons = db.query(Season).all()
    season_ids = [s.id for s in seasons]
    
    if existing_results == 0 and season_ids:
        print("\n--- Sembrando resultados ---")
        results_data = [
            {"position": 1, "points": 25.5, "time_gap": None, "session_type": "race",
             "circuit_id": 1, "pilot_id": 1, "season_id": season_ids[0], "is_ficticio": False},
            {"position": 2, "points": 20.0, "time_gap": "+3.450", "session_type": "race",
             "circuit_id": 1, "pilot_id": 2, "season_id": season_ids[0], "is_ficticio": False},
            {"position": 3, "points": 15.5, "time_gap": "+8.200", "session_type": "race",
             "circuit_id": 1, "pilot_id": 3, "season_id": season_ids[0], "is_ficticio": True},
            {"position": 1, "points": 25.5, "time_gap": None, "session_type": "race",
             "circuit_id": 2, "pilot_id": 2, "season_id": season_ids[0], "is_ficticio": False},
            {"position": 2, "points": 20.0, "time_gap": "+1.800", "session_type": "race",
             "circuit_id": 2, "pilot_id": 1, "season_id": season_ids[0], "is_ficticio": False},
        ]
        
        for r in results_data:
            result = Result(
                position=r["position"],
                points=r["points"],
                time_gap=r["time_gap"],
                session_type=r["session_type"],
                circuit_id=r["circuit_id"],
                pilot_id=r["pilot_id"],
                season_id=r["season_id"],
                is_ficticio=r["is_ficticio"],
            )
            db.add(result)
            print(f"  [OK] Resultado posición {r['position']} - temporada {r['season_id']}")
        
        db.commit()
        print("[OK] Resultados cargados")
    else:
        print("- Resultados ya existen, saltando")
    
    if existing_sessions == 0 and season_ids:
        print("\n--- Sembrando sesiones ---")
        sessions_data = [
            {"session_type": "practice", "date": "2024-04-12T09:00:00", "time": "09:00",
             "weather_conditions": "soleado", "status": "completed",
             "circuit_id": 1, "season_id": season_ids[0], "is_ficticio": False},
            {"session_type": "qualifying", "date": "2024-04-13T14:00:00", "time": "14:00",
             "weather_conditions": "nublado", "status": "completed",
             "circuit_id": 1, "season_id": season_ids[0], "is_ficticio": False},
            {"session_type": "race", "date": "2024-04-14T15:00:00", "time": "15:00",
             "weather_conditions": "soleado", "status": "completed",
             "circuit_id": 1, "season_id": season_ids[0], "is_ficticio": False},
            {"session_type": "practice", "date": "2024-04-12T09:00:00", "time": "09:00",
             "weather_conditions": "lluvia", "status": "completed",
             "circuit_id": 2, "season_id": season_ids[0], "is_ficticio": False},
            {"session_type": "qualifying", "date": "2024-04-13T14:00:00", "time": "14:00",
             "weather_conditions": "soleado", "status": "scheduled",
             "circuit_id": 2, "season_id": season_ids[0], "is_ficticio": False},
        ]
        
        for s in sessions_data:
            session = SessionEntity(
                session_type=s["session_type"],
                date=datetime.fromisoformat(s["date"]),
                time=s["time"],
                weather_conditions=s["weather_conditions"],
                status=s["status"],
                circuit_id=s["circuit_id"],
                season_id=s["season_id"],
                is_ficticio=s["is_ficticio"],
            )
            db.add(session)
            print(f"  [OK] Sesión {s['session_type']} - circuito {s['circuit_id']}")
        
        db.commit()
        print("[OK] Sesiones cargadas")
    else:
        print("- Sesiones ya existen, saltando")
    
    # Resumen final
    print("\n" + "=" * 60)
    print("RESUMEN DE DATOS FASE 3")
    print("=" * 60)
    print(f"Temporadas: {db.query(Season).count()}")
    print(f"Resultados: {db.query(Result).count()}")
    print(f"Sesiones: {db.query(SessionEntity).count()}")
    
except Exception as e:
    db.rollback()
    print(f"[X] Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
