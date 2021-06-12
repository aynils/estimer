from dataclasses import dataclass
from datetime import date
from typing import List


@dataclass
class MedianM2Price:
    year: int
    value: float


@dataclass
class SalesPerStreet:
    nom_voie: int
    nombre_ventes: float


@dataclass
class Address:
    numero: int
    suffixe: str
    nom_voie: str
    code_voie: float
    code_postal: int
    code_commune: int
    code_departement: int
    latitude: int
    longitude: int


@dataclass
class Sale:
    date: date
    price: float
    surface: int
    m2_price: int
    type_local: str
    address: Address
    rooms_count: int


@dataclass
class StreetMedianPrice:
    nom_voie: int
    avg_m2_price: float


@dataclass
class Agent:
    picture: str
    name: str
    agency: str
    description: str
    phone_number: str
    email: str
    website_url: str


@dataclass
class Geometry:
    coordinates: List[int]
    type: str = "Point"


@dataclass
class MapMarker:
    geometry: Geometry
    properties: Sale
    type: str = "Feature"


@dataclass
class CityData:
    median_m2_price_appartement: MedianM2Price
    median_m2_price_maison: MedianM2Price
    median_m2_prices_years: List[MedianM2Price]
    last_sales: List[Sale]
    most_expensive_streets: List[StreetMedianPrice]
    less_expensive_streets: List[StreetMedianPrice]
    number_of_sales: int
    agent: Agent
    bar_heights: dict
    price_evolution_text: str
    map_markers: List[MapMarker]
