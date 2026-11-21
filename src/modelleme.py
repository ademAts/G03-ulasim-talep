import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, root_mean_squared_error
from config import PROC

KAT = ["saat", "haftanin_gunu"]
SAY = ["sicaklik", "yagis", "ruzgar", "hafta_sonu", "tatil", "bayram_oncesi", "okul_donemi"]
X_KOL = KAT + SAY

def on_isleme():
    """Kategorik degiskenleri one-hot encodera alir, sayisallari aynen gecirir."""
    oh = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    return ColumnTransformer([("oh", oh, KAT)], remainder="passthrough", sparse_threshold=0)

def modelleri_kur():
    """Kilavuzdaki 3 modeli pipeline icinde olusturur."""
    return {
        "Doğrusal Regresyon": make_pipeline(on_isleme(), LinearRegression()),
        "Random Forest": make_pipeline(on_isleme(), RandomForestRegressor(
            n_estimators=100, min_samples_leaf=3, n_jobs=-1, random_state=42)),
        "HistGradientBoosting": make_pipeline(on_isleme(), HistGradientBoostingRegressor(
            max_iter=200, learning_rate=0.06, random_state=42)),
    }

def veri_hazirla(df_mod, test_gun=21):
    """Veriyi zamana gore egitim ve test kumesine ayirir, naif baseline uretir."""
    d = df_mod.set_index("dt").sort_index()
    d["naif"] = d["yolcu"].shift(168)  # 168 saat = 7 gun onceki ayni saat
    d = d.dropna(subset=X_KOL)
    kesim = d.index.max() - pd.Timedelta(days=test_gun)
    egitim, test = d[d.index <= kesim], d[d.index > kesim]
    return egitim, test.dropna(subset=["naif"])

def degerlendir(df_mod):
    """Modelleri egitir, MAE ve RMSE metriklerini hesaplar."""
    egitim, test = veri_hazirla(df_mod)
    y = test["yolcu"]
    satir = [{
        "model": "Naif Baseline (Gecen Hafta Ayni Saat)",
        "MAE": mean_absolute_error(y, test["naif"]),
        "RMSE": root_mean_squared_error(y, test["naif"])
    }]
    modeller = {}
    for ad, m in modelleri_kur().items():
        m.fit(egitim[X_KOL], egitim["yolcu"])
        t = m.predict(test[X_KOL])
        satir.append({
            "model": ad,
            "MAE": mean_absolute_error(y, t),
            "RMSE": root_mean_squared_error(y, t)
        })
        modeller[ad] = m
    return pd.DataFrame(satir), modeller, egitim, test
