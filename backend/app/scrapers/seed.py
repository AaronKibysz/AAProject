# Script de seed para cargar datos reales de Turismo Carretera
# Extraídos de Wikipedia y otras fuentes públicas

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from sqlalchemy import select
from app.infrastructure.database import SessionLocal, Base, engine
from app.domain.entities.season import Season
from app.domain.entities.category import Category
from app.domain.entities.pilot import Pilot
from app.domain.entities.result import Result
from app.domain.entities.session import Session
from app.domain.entities.circuit import Circuit
from app.scrapers.tc_data import (
    get_tc_categories,
    get_tc_circuits,
    get_tc_pilots,
)


def seed_categories(db: Session) -> int:
    """Cargar categorías de automovilismo argentino."""
    count = 0
    for cat_data in get_tc_categories():
        stmt = select(Category).where(Category.name == cat_data["name"])
        existing = db.execute(stmt).scalar_one_or_none()
        if not existing:
            category = Category(
                name=cat_data["name"],
                description=cat_data["description"],
                is_ficticio=cat_data["is_ficticio"],
            )
            db.add(category)
            count += 1
    db.commit()
    return count


def seed_circuits(db: Session) -> int:
    """Cargar circuitos del Turismo Carretera."""
    count = 0
    for circuit_data in get_tc_circuits():
        stmt = select(Circuit).where(Circuit.name == circuit_data["name"])
        existing = db.execute(stmt).scalar_one_or_none()
        if not existing:
            circuit = Circuit(
                name=circuit_data["name"],
                location=circuit_data["location"],
                country=circuit_data.get("country"),
                length_km=circuit_data.get("length_km"),
                turns=circuit_data.get("turns"),
                description=circuit_data.get("description"),
                photo_url=circuit_data.get("photo_url"),
                record_lap=circuit_data.get("record_lap"),
                record_holder=circuit_data.get("record_holder"),
                capacity=circuit_data.get("capacity"),
                is_ficticio=False,
            )
            db.add(circuit)
            count += 1
        else:
            existing.location = circuit_data.get("location", existing.location)
            existing.country = circuit_data.get("country", existing.country)
            existing.length_km = circuit_data.get("length_km", existing.length_km)
            existing.turns = circuit_data.get("turns", existing.turns)
            existing.description = circuit_data.get("description", existing.description)
            existing.photo_url = circuit_data.get("photo_url", existing.photo_url)
            existing.record_lap = circuit_data.get("record_lap", existing.record_lap)
            existing.record_holder = circuit_data.get("record_holder", existing.record_holder)
            existing.capacity = circuit_data.get("capacity", existing.capacity)
            count += 1
    db.commit()
    return count


def seed_pilots(db: Session) -> int:
    """Cargar pilotos históricos del Turismo Carretera."""
    count = 0
    for pilot_data in get_tc_pilots():
        stmt = select(Pilot).where(Pilot.name == pilot_data["name"])
        existing = db.execute(stmt).scalar_one_or_none()
        if not existing:
            pilot = Pilot(
                name=pilot_data["name"],
                team=pilot_data["team"],
                number=pilot_data.get("number"),
                biography=pilot_data.get("biography"),
                photo_url=pilot_data.get("photo_url"),
                birth_date=pilot_data.get("birth_date"),
                nationality=pilot_data.get("nationality"),
                championships=pilot_data.get("titles", 0),
                wins=pilot_data.get("wins", 0),
                podiums=pilot_data.get("podiums", 0),
                is_ficticio=False,
            )
            db.add(pilot)
            count += 1
        else:
            existing.team = pilot_data.get("team", existing.team)
            existing.number = pilot_data.get("number", existing.number)
            existing.biography = pilot_data.get("biography", existing.biography)
            existing.photo_url = pilot_data.get("photo_url", existing.photo_url)
            existing.birth_date = pilot_data.get("birth_date", existing.birth_date)
            existing.nationality = pilot_data.get("nationality", existing.nationality)
            existing.championships = pilot_data.get("titles", existing.championships)
            existing.wins = pilot_data.get("wins", existing.wins)
            existing.podiums = pilot_data.get("podiums", existing.podiums)
            count += 1
    db.commit()
    return count


def run_seed():
    """Ejecutar seed completo."""
    db = SessionLocal()
    try:
        print("[SEED] Iniciando seed de datos de Turismo Carretera...")

        cats = seed_categories(db)
        print(f"  [OK] Categorías: {cats} nuevas")

        circuits = seed_circuits(db)
        print(f"  [OK] Circuitos: {circuits} nuevos")

        pilots = seed_pilots(db)
        print(f"  [OK] Pilotos: {pilots} nuevos")

        print("[OK] Seed completado exitosamente!")
    except Exception as e:
        print(f"[ERROR] Error durante seed: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
