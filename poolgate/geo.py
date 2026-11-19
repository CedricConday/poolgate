"""Towns the pool lives in, and straight-line distance between them.

Coordinates are town centres, rounded. Distances are great-circle (Luftlinie),
which is what a PLZ radius search in an ATS usually computes. Road distance is
longer; the vacancies state that their radius is Luftlinie.
"""

from __future__ import annotations

import math

# town -> (PLZ, lat, lon)
OWL = {
    "Paderborn": ("33098", 51.7189, 8.7575),
    "Bad Lippspringe": ("33175", 51.7810, 8.8170),
    "Delbrück": ("33129", 51.7667, 8.5667),
    "Salzkotten": ("33154", 51.6706, 8.6047),
    "Büren": ("33142", 51.5508, 8.5590),
    "Altenbeken": ("33184", 51.7667, 8.9333),
    "Hövelhof": ("33161", 51.8167, 8.6500),
    "Schloß Holte-Stukenbrock": ("33758", 51.8833, 8.6167),
    "Bielefeld": ("33602", 52.0302, 8.5325),
    "Gütersloh": ("33330", 51.9069, 8.3785),
    "Verl": ("33415", 51.8833, 8.5167),
    "Rheda-Wiedenbrück": ("33378", 51.8417, 8.3000),
    "Harsewinkel": ("33428", 51.9622, 8.2297),
    "Halle (Westf.)": ("33790", 52.0600, 8.3600),
    "Herford": ("32052", 52.1146, 8.6734),
    "Bad Salzuflen": ("32105", 52.0867, 8.7506),
    "Detmold": ("32756", 51.9387, 8.8793),
    "Lemgo": ("32657", 52.0277, 8.9016),
    "Lage": ("32791", 51.9917, 8.7917),
    "Bad Oeynhausen": ("32545", 52.2050, 8.8000),
    "Minden": ("32423", 52.2895, 8.9146),
    "Lübbecke": ("32312", 52.3081, 8.6231),
    "Höxter": ("37671", 51.7742, 9.3822),
    "Brakel": ("33034", 51.7167, 9.1833),
    "Bad Driburg": ("33014", 51.7333, 9.0167),
    "Warburg": ("34414", 51.4881, 9.1400),
    "Lippstadt": ("59555", 51.6739, 8.3447),
    "Geseke": ("59590", 51.6400, 8.5100),
}

# Outside OWL: where a "too far" candidate lives.
FAR = {
    "Kassel": ("34117", 51.3127, 9.4797),
    "Hamm": ("59065", 51.6739, 7.8150),
    "Dortmund": ("44135", 51.5136, 7.4653),
    "Osnabrück": ("49074", 52.2799, 8.0472),
    "Hannover": ("30159", 52.3759, 9.7320),
    "Münster": ("48143", 51.9607, 7.6261),
    "Göttingen": ("37073", 51.5413, 9.9158),
    "Arnsberg": ("59821", 51.3967, 8.0644),
    "Hameln": ("31785", 52.1036, 9.3561),
    "Soest": ("59494", 51.5711, 8.1092),
}

TOWNS = {**OWL, **FAR}


def plz(town: str) -> str:
    return TOWNS[town][0]


def km(a: str, b: str) -> float:
    """Great-circle distance between two towns, in km."""
    _, la1, lo1 = TOWNS[a]
    _, la2, lo2 = TOWNS[b]
    p1, p2 = math.radians(la1), math.radians(la2)
    dp, dl = p2 - p1, math.radians(lo2 - lo1)
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * 6371.0 * math.asin(math.sqrt(h))
