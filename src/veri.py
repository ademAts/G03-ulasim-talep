import pandas as pd
import requests
from config import KOLON, MOD_ADI

def kaynaklari_listele():
    """Portaldaki kaynakların adını, biçimini ve indirme adresini yazdırır."""
    r = requests.get("https://data.ibb.gov.tr/api/3/action/package_show",
                     params={"id": "hourly-public-transport-data-set"}, timeout=60)
    r.raise_for_status()
    for k in r.json()["result"]["resources"]:
        print(k["name"], "|", k["format"], "|", k["url"])

def indir(url, hedef):
    """Büyük CSV dosyasını internetten parça parça indirir."""
    with requests.get(url, stream=True, timeout=120) as r:
        r.raise_for_status()
        with open(hedef, "wb") as f:
            for blok in r.iter_content(1024 * 1024):
                f.write(blok)

def toplula(csv_yolu, chunksize=500_000):
    """Dev CSV'yi parça parça okur; saat x mod x ilçe (ve saat x mod x hat) toplar."""
    ilce_p, hat_p = [], []
    for ch in pd.read_csv(csv_yolu, chunksize=chunksize, usecols=list(KOLON)):
        ch = ch.rename(columns=KOLON)
        ch["tarih"] = pd.to_datetime(ch["tarih"]).dt.date
        ch["saat"] = ch["saat"].astype(int)
        ch["mod"] = ch["mod"].map(MOD_ADI)
        k1 = ["tarih", "saat", "mod", "ilce"]
        k2 = ["tarih", "saat", "mod", "hat"]
        ilce_p.append(ch.groupby(k1, as_index=False, dropna=False)[["yolcu", "yolculuk"]].sum())
        hat_p.append(ch.groupby(k2, as_index=False, dropna=False)[["yolcu"]].sum())
    ilce = pd.concat(ilce_p).groupby(k1, as_index=False, dropna=False).sum()
    hat = pd.concat(hat_p).groupby(k2, as_index=False, dropna=False).sum()
    return ilce, hat

# --- 2. KISIM: HAVA DURUMU VE ZAMAN OZELLIKLERI ---
import holidays

OKUL_TATIL = [
    ("2024-11-11", "2024-11-15"),
]

def hava_cek(bas, bit):
    """Open-Meteo gecmis hava verisi (Istanbul, saatlik). bas/bit: 'YYYY-AA-GG'."""
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": 41.01, "longitude": 28.98,
        "start_date": bas, "end_date": bit,
        "hourly": "temperature_2m,precipitation,wind_speed_10m,wind_gusts_10m",
        "timezone": "Europe/Istanbul"
    }
    r = requests.get(url, params=params, timeout=60)
    r.raise_for_status()
    h = pd.DataFrame(r.json()["hourly"])
    h["time"] = pd.to_datetime(h["time"])
    return h.rename(columns={
        "time": "dt",
        "temperature_2m": "sicaklik",
        "precipitation": "yagis",
        "wind_speed_10m": "ruzgar",
        "wind_gusts_10m": "ruzgar_hamle"
    })

def ozellik_uret(df):
    """Zaman damgasindan tatil, hafta sonu, saat gibi ML ozelliklerini uretir."""
    yillar = sorted(df["dt"].dt.year.unique())
    tr = holidays.country_holidays("TR", years=yillar)
    gun = df["dt"].dt.normalize()
    df["saat"] = df["dt"].dt.hour
    df["haftanin_gunu"] = df["dt"].dt.dayofweek
    df["hafta_sonu"] = (df["haftanin_gunu"] >= 5).astype(int)
    df["tatil"] = gun.dt.date.map(lambda d: int(d in tr)).astype(int)
    yarin = (gun + pd.Timedelta(days=1)).dt.date.map(lambda d: int(d in tr))
    df["bayram_oncesi"] = (yarin & (df["tatil"] == 0)).astype(int)
    
    tatilde = pd.Series(False, index=df.index)
    for b_bas, b_bit in OKUL_TATIL:
        tatilde |= (gun >= pd.Timestamp(b_bas)) & (gun <= pd.Timestamp(b_bit))
    df["okul_donemi"] = (~tatilde).astype(int)
    return df
