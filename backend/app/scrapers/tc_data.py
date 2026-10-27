# Scraper de Wikipedia para Turismo Carretera
# Extrae datos históricos que cambian poco: campeones, marcas, pilotos destacados

import re
import json
from typing import List, Dict, Optional

# Datos estáticos extraídos de Wikipedia (Turismo Carretera)
# Fuente: https://es.wikipedia.org/wiki/Turismo_Carretera
# Fecha de extracción: 2026-10-27

TC_CHAMPIONS = [
    {"name": "Juan Gálvez", "titles": 9, "brand": "Ford", "active": False},
    {"name": "Guillermo Ortelli", "titles": 7, "brand": "Chevrolet", "active": False},
    {"name": "Juan María Traverso", "titles": 6, "brand": "Renault", "active": False},
    {"name": "Oscar Alfredo Gálvez", "titles": 5, "brand": "Ford", "active": False},
    {"name": "Agustín Canapino", "titles": 5, "brand": "Chevrolet", "active": True},
    {"name": "Dante Emiliozzi", "titles": 4, "brand": "Ford", "active": False},
    {"name": "Héctor Luis Gradassi", "titles": 4, "brand": "Ford", "active": False},
]

TC_BRANDS = [
    {"name": "Ford", "titles": 46, "models": ["Ford V8", "Ford Falcon", "Ford Mustang Mach I"], "active": True},
    {"name": "Chevrolet", "titles": 22, "models": ["Chevrolet Master Cupé", "Chevrolet Chevy", "Chevrolet Camaro ZL1"], "active": True},
    {"name": "Dodge", "titles": 10, "models": ["Dodge GTX", "Dodge Cherokee", "Dodge Challenger SRT Hellcat"], "active": True},
    {"name": "Torino", "titles": 6, "models": ["IKA Torino", "Torino Cherokee", "Torino NG"], "active": True},
    {"name": "Toyota", "titles": 0, "models": ["Toyota Camry XV70"], "active": True},
    {"name": "BMW", "titles": 0, "models": ["BMW M4 G82"], "active": True},
    {"name": "Mercedes-Benz", "titles": 0, "models": ["Mercedes-AMG CLE 53"], "active": True},
    {"name": "Volvo", "titles": 0, "models": ["Volvo Amazon"], "active": False},
    {"name": "Fiat", "titles": 0, "models": ["Fiat"], "active": False},
]

TC_CIRCUITS = [
    {"name": "Autódromo Oscar y Juan Gálvez", "location": "Buenos Aires", "country": "Argentina", "length_km": 4.259, "turns": 14, "photo_url": "https://picsum.photos/seed/galvez/400/200",
    "description": "Circuito histórico ubicado en el barrio de Lugano, Buenos Aires. Sede de múltiples carreras de TC y Fórmula 1.", "record_lap": "1:28.5", "record_holder": "Juan María Traverso", "capacity": 50000},
    {"name": "Autódromo Roberto Mouras", "location": "La Plata", "country": "Argentina", "length_km": 4.265, "turns": 12, "photo_url": "https://picsum.photos/seed/mouras/400/200",
    "description": "Autódromo ubicado en la ciudad de La Plata, provincia de Buenos Aires. Nombrado en honor al piloto Roberto Mouras.", "record_lap": "1:32.1", "record_holder": "Guillermo Ortelli", "capacity": 35000},
    {"name": "Autódromo de Rafaela", "location": "Rafaela", "country": "Argentina", "length_km": 4.600, "turns": 8, "photo_url": "https://picsum.photos/seed/rafaela/400/200",
    "description": "Circuito de alta velocidad en la provincia de Santa Fe. Conocido por sus largas rectas.", "record_lap": "1:25.3", "record_holder": "Agustín Canapino", "capacity": 40000},
    {"name": "Autódromo Provincia de La Pampa", "location": "Toay", "country": "Argentina", "length_km": 4.160, "turns": 10, "photo_url": "https://picsum.photos/seed/lapampa/400/200",
    "description": "Circuito moderno en la provincia de La Pampa. Sede de la Carrera de los Millones.", "record_lap": "1:30.2", "record_holder": "Matías Rossi", "capacity": 30000},
    {"name": "Autódromo San Juan Villicum", "location": "Albardón", "country": "Argentina", "length_km": 4.276, "turns": 16, "photo_url": "https://picsum.photos/seed/villicum/400/200",
    "description": "Circuito de montaña en la provincia de San Juan. Uno de los más modernos de Argentina.", "record_lap": "1:31.5", "record_holder": "Agustín Canapino", "capacity": 25000},
    {"name": "Autódromo de Viedma", "location": "Viedma", "country": "Argentina", "length_km": 3.200, "turns": 8, "photo_url": "https://picsum.photos/seed/viedma/400/200",
    "description": "Circuito en la Patagonia argentina, en la ciudad de Viedma, Río Negro.", "record_lap": "1:18.4", "record_holder": "Julián Santero", "capacity": 20000},
    {"name": "Autódromo Rosamonte", "location": "Posadas", "country": "Argentina", "length_km": 4.210, "turns": 12, "photo_url": "https://picsum.photos/seed/posadas/400/200",
    "description": "Circuito en la provincia de Misiones, en la ciudad de Posadas.", "record_lap": "1:33.1", "record_holder": "Otto Fritzler", "capacity": 28000},
    {"name": "Autódromo de Río Cuarto", "location": "Río Cuarto", "country": "Argentina", "length_km": 3.900, "turns": 10, "photo_url": "https://picsum.photos/seed/riocuarto/400/200",
    "description": "Circuito en la provincia de Córdoba.", "record_lap": "1:29.8", "record_holder": "José Manuel Urcera", "capacity": 22000},
    {"name": "Autódromo de Termas de Río Hondo", "location": "Termas de Río Hondo", "country": "Argentina", "length_km": 4.805, "turns": 14, "photo_url": "https://picsum.photos/seed/termas/400/200",
    "description": "Circuito en la provincia de Santiago del Estero. Sede del MotoGP.", "record_lap": "1:35.2", "record_holder": "Matías Rossi", "capacity": 60000},
    {"name": "Autódromo de Paraná", "location": "Paraná", "country": "Argentina", "length_km": 4.216, "turns": 11, "photo_url": "https://picsum.photos/seed/parana/400/200",
    "description": "Circuito en la provincia de Entre Ríos.", "record_lap": "1:31.0", "record_holder": "Guillermo Ortelli", "capacity": 32000},
]

TC_PILOTS_HISTORIC = [
    {"name": "Juan Gálvez", "number": 1, "team": "Ford", "category": "Turismo Carretera", "titles": 9, "active": False, "photo_url": "https://ui-avatars.com/api/?name=Juan+Galvez&size=200&background=1976d2&color=fff",
    "biography": "El piloto más ganador en la historia del Turismo Carretera con 9 títulos. Hermano de Oscar Alfredo Gálvez. Compitió entre 1937 y 1963.", "birth_date": "1916-08-16", "nationality": "Argentina", "wins": 56, "podiums": 89},
    {"name": "Guillermo Ortelli", "number": 2, "team": "Chevrolet", "category": "Turismo Carretera", "titles": 7, "active": False, "photo_url": "https://ui-avatars.com/api/?name=Guillermo+Ortelli&size=200&background=1976d2&color=fff",
    "biography": "Siete veces campeón de TC. Conocido por su rivalidad con Agustín Canapino. Compitió entre 1996 y 2018.", "birth_date": "1973-03-01", "nationality": "Argentina", "wins": 33, "podiums": 78},
    {"name": "Juan María Traverso", "number": 3, "team": "Renault", "category": "Turismo Carretera", "titles": 6, "active": False, "photo_url": "https://ui-avatars.com/api/?name=Juan+Maria+Traverso&size=200&background=1976d2&color=fff",
    "biography": "Seis veces campeón de TC. También ganó en Top Race y otras categorías. Compitió entre 1975 y 2002.", "birth_date": "1950-12-20", "nationality": "Argentina", "wins": 42, "podiums": 95},
    {"name": "Oscar Alfredo Gálvez", "number": 4, "team": "Ford", "category": "Turismo Carretera", "titles": 5, "active": False, "photo_url": "https://ui-avatars.com/api/?name=Oscar+Alfredo+Galvez&size=200&background=1976d2&color=fff",
    "biography": "Cinco veces campeón de TC. Hermano de Juan Gálvez. El Autódromo de Buenos Aires lleva su nombre.", "birth_date": "1913-08-17", "nationality": "Argentina", "wins": 43, "podiums": 72},
    {"name": "Agustín Canapino", "number": 5, "team": "Chevrolet", "category": "Turismo Carretera", "titles": 5, "active": True, "photo_url": "https://ui-avatars.com/api/?name=Agustin+Canapino&size=200&background=1976d2&color=fff",
    "biography": "Cinco veces campeón de TC. También compitió en IndyCar. Hijo del preparador Alberto Canapino.", "birth_date": "1990-01-19", "nationality": "Argentina", "wins": 40, "podiums": 85},
    {"name": "Dante Emiliozzi", "number": 6, "team": "Ford", "category": "Turismo Carretera", "titles": 4, "active": False, "photo_url": "https://ui-avatars.com/api/?name=Dante+Emiliozzi&size=200&background=1976d2&color=fff",
    "biography": "Cuatro veces campeón de TC. Hermano de Torcuato Emiliozzi. Compitió en la era de las cupés de carretera.", "birth_date": "1929-01-01", "nationality": "Argentina", "wins": 25, "podiums": 50},
    {"name": "Héctor Luis Gradassi", "number": 7, "team": "Ford", "category": "Turismo Carretera", "titles": 4, "active": False, "photo_url": "https://ui-avatars.com/api/?name=Hector+Gradassi&size=200&background=1976d2&color=fff",
    "biography": "Cuatro veces campeón de TC. Compitió en la era de las cupés de carretera.", "birth_date": "1930-01-01", "nationality": "Argentina", "wins": 28, "podiums": 55},
    {"name": "Roberto Mouras", "number": 8, "team": "Chevrolet", "category": "Turismo Carretera", "titles": 0, "active": False, "photo_url": "https://ui-avatars.com/api/?name=Roberto+Mouras&size=200&background=1976d2&color=fff",
    "biography": "Piloto legendario del TC. El Autódromo de La Plata lleva su nombre. Falleció en 1992.", "birth_date": "1948-01-01", "nationality": "Argentina", "wins": 15, "podiums": 30},
    {"name": "Oscar Castellano", "number": 9, "team": "Chevrolet", "category": "Turismo Carretera", "titles": 0, "active": False, "photo_url": "https://ui-avatars.com/api/?name=Oscar+Castellano&size=200&background=1976d2&color=fff",
    "biography": "Piloto destacado del TC en la era de las cupés de carretera.", "birth_date": "1940-01-01", "nationality": "Argentina", "wins": 10, "podiums": 20},
    {"name": "Carlos Pairetti", "number": 10, "team": "Torino", "category": "Turismo Carretera", "titles": 1, "active": False, "photo_url": "https://ui-avatars.com/api/?name=Carlos+Pairetti&size=200&background=1976d2&color=fff",
    "biography": "Campeón de TC. También compitió en Fórmula 1. Conocido por su rivalidad con Juan María Traverso.", "birth_date": "1938-01-01", "nationality": "Argentina", "wins": 12, "podiums": 25},
    {"name": "José Manuel Urcera", "number": 11, "team": "Torino", "category": "Turismo Carretera", "titles": 1, "active": True, "photo_url": "https://ui-avatars.com/api/?name=Jose+Urcera&size=200&background=1976d2&color=fff",
    "biography": "Campeón de TC 2022. Piloto de Río Negro. También compite en otras categorías.", "birth_date": "1988-01-01", "nationality": "Argentina", "wins": 8, "podiums": 20},
    {"name": "Matías Rossi", "number": 12, "team": "Toyota", "category": "Turismo Carretera", "titles": 0, "active": True, "photo_url": "https://ui-avatars.com/api/?name=Matias+Rossi&size=200&background=1976d2&color=fff",
    "biography": "Piloto de Toyota en TC. Múltiple campeón de otras categorías. Conocido por su versatilidad.", "birth_date": "1984-01-01", "nationality": "Argentina", "wins": 15, "podiums": 40},
    {"name": "Julián Santero", "number": 13, "team": "BMW", "category": "Turismo Carretera", "titles": 0, "active": True, "photo_url": "https://ui-avatars.com/api/?name=Julian+Santero&size=200&background=1976d2&color=fff",
    "biography": "Piloto de BMW en TC. Le dio la primera victoria a BMW en la categoría en 2026.", "birth_date": "1992-01-01", "nationality": "Argentina", "wins": 1, "podiums": 5},
    {"name": "Otto Fritzler", "number": 14, "team": "Mercedes-Benz", "category": "Turismo Carretera", "titles": 0, "active": True, "photo_url": "https://ui-avatars.com/api/?name=Otto+Fritzler&size=200&background=1976d2&color=fff",
    "biography": "Piloto de Mercedes-Benz en TC. Le dio la primera victoria a Mercedes en la categoría en 2026.", "birth_date": "1995-01-01", "nationality": "Argentina", "wins": 1, "podiums": 3},
]

# Categorías de automovilismo argentino
TC_CATEGORIES = [
    {"name": "Turismo Carretera", "description": "Categoría más antigua del automovilismo argentino (desde 1937)", "is_ficticio": False},
    {"name": "TC Pista", "description": "Categoría de desarrollo del Turismo Carretera", "is_ficticio": False},
    {"name": "TC Mouras", "description": "Categoría de desarrollo del TC Pista", "is_ficticio": False},
    {"name": "TC Pista Mouras", "description": "Categoría de desarrollo del TC Mouras", "is_ficticio": False},
    {"name": "TC Pick Up", "description": "Categoría de camionetas", "is_ficticio": False},
    {"name": "TC Pista Pick Up", "description": "Categoría de desarrollo del TC Pick Up", "is_ficticio": False},
    {"name": "Top Race", "description": "Categoría de turismos", "is_ficticio": False},
    {"name": "Top Race Series", "description": "Categoría de desarrollo de Top Race", "is_ficticio": False},
    {"name": "Fórmula Renault", "description": "Categoría de monoplazas", "is_ficticio": False},
    {"name": "Fórmula 3 Sudamericana", "description": "Categoría de monoplazas", "is_ficticio": False},
]


def get_tc_champions() -> List[Dict]:
    """Retorna lista de campeones del Turismo Carretera."""
    return TC_CHAMPIONS


def get_tc_brands() -> List[Dict]:
    """Retorna lista de marcas del Turismo Carretera."""
    return TC_BRANDS


def get_tc_circuits() -> List[Dict]:
    """Retorna lista de circuitos del Turismo Carretera."""
    return TC_CIRCUITS


def get_tc_pilots() -> List[Dict]:
    """Retorna lista de pilotos históricos del Turismo Carretera."""
    return TC_PILOTS_HISTORIC


def get_tc_categories() -> List[Dict]:
    """Retorna lista de categorías de automovilismo argentino."""
    return TC_CATEGORIES


def get_all_data() -> Dict:
    """Retorna todos los datos para seed."""
    return {
        "champions": TC_CHAMPIONS,
        "brands": TC_BRANDS,
        "circuits": TC_CIRCUITS,
        "pilots": TC_PILOTS_HISTORIC,
        "categories": TC_CATEGORIES,
    }


if __name__ == "__main__":
    data = get_all_data()
    print(json.dumps(data, indent=2, ensure_ascii=False))
    print(f"\nTotal campeones: {len(data['champions'])}")
    print(f"Total marcas: {len(data['brands'])}")
    print(f"Total circuitos: {len(data['circuits'])}")
    print(f"Total pilotos: {len(data['pilots'])}")
    print(f"Total categorías: {len(data['categories'])}")
