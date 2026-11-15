from pathlib import Path

KOK = Path(__file__).resolve().parent
RAW = KOK / "data" / "raw"
PROC = KOK / "data" / "processed"
MODEL = KOK / "model"

for p in (RAW, PROC, MODEL):
    p.mkdir(parents=True, exist_ok=True)

KOLON = {
    "transition_date": "tarih",
    "transition_hour": "saat",
    "transport_type_id": "mod",
    "town": "ilce",
    "line": "hat",
    "number_of_passenger": "yolcu",
    "number_of_passage": "yolculuk",
}

MOD_ADI = {1: "Karayolu", 2: "Raylı", 3: "Deniz"}
