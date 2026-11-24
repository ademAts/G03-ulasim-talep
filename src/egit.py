import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor
import shap

# 03_Model ve 02_Kod klasörlerini kesin oluştur
Path("03_Model").mkdir(parents=True, exist_ok=True)
Path("02_Kod").mkdir(parents=True, exist_ok=True)

print("1/5: Veri okunuyor...")
df = pd.read_csv("01_Veri/ulasim_toplanmis_ozet.csv")
df["tarih_saat"] = pd.to_datetime(df["tarih"]) + pd.to_timedelta(df["saat"], unit="h")
df = df.sort_values("tarih_saat").reset_index(drop=True)

# Özellikler ve Hedef
feats = ["saat", "haftanin_gunu", "hafta_sonu", "tatil", "okul_donemi", "sicaklik", "yagis", "ruzgar"]
hedef = "yolcu"

# 2/5: Zamana göre Train-Test ayrımı (Son 14 gün test kümesi)
cutoff = df["tarih_saat"].max() - pd.Timedelta(days=14)
train = df[df["tarih_saat"] < cutoff].copy()
test = df[df["tarih_saat"] >= cutoff].copy()

print(f"Egitim seti: {len(train):,} satir (Tarih: {train['tarih'].min()} -> {train['tarih'].max()})")
print(f"Test seti: {len(test):,} satir (Tarih: {test['tarih'].min()} -> {test['tarih'].max()})")

# 3/5: Naif Baseline Model (Gecen hafta ayni gun ve saatteki ortalama)
baseline_map = train.groupby(["saat", "haftanin_gunu"])[hedef].mean()
test["baseline_pred"] = test.set_index(["saat", "haftanin_gunu"]).index.map(baseline_map).fillna(train[hedef].mean())

sonuclar = []
sonuclar.append({
    "Model": "Naif Baseline",
    "MAE": mean_absolute_error(test[hedef], test["baseline_pred"]),
    "RMSE": np.sqrt(mean_squared_error(test[hedef], test["baseline_pred"]))
})

# 4/5: 3 Regresyon Modeli Egitimi
modeller = {
    "Dogrusal Regresyon": LinearRegression(),
    "Random Forest": RandomForestRegressor(n_estimators=100, max_depth=12, random_state=42, n_jobs=-1),
    "HistGradientBoosting": HistGradientBoostingRegressor(max_iter=150, random_state=42)
}

egitilmis = {}
for ad, model in modeller.items():
    print(f"   -> {ad} egitiliyor...")
    model.fit(train[feats], train[hedef])
    preds = model.predict(test[feats])
    sonuclar.append({
        "Model": ad,
        "MAE": mean_absolute_error(test[hedef], preds),
        "RMSE": np.sqrt(mean_squared_error(test[hedef], preds))
    })
    egitilmis[ad] = model

df_sonuc = pd.DataFrame(sonuclar)
print("\n========== MODEL KIYASLAMA TABLOSU ==========")
print(df_sonuc.to_string(index=False))

# Sonuç tablosunu CSV olarak kaydet
df_sonuc.to_csv("03_Model/model_kiyaslama_tablosu.csv", index=False)

# En iyi modeli seç ve kaydet (HistGradientBoosting veya Random Forest karmaşık ilişkiler için Streamlit simülatöründe en kararlısıdır)
en_iyi_model = egitilmis["HistGradientBoosting"]
joblib.dump(en_iyi_model, "03_Model/model.joblib")
print(f"\nModel basariyla 03_Model/model.joblib olarak kaydedildi!")

# 5/5: +3 Puan SHAP Analizi
print("\nSHAP analizi calisiyor (hava ve saat etkileri cikariliyor)...")
test_ornek = test[feats].sample(n=min(1000, len(test)), random_state=42)
explainer = shap.Explainer(en_iyi_model, train[feats].sample(n=500, random_state=42))
shap_values = explainer(test_ornek)

plt.figure(figsize=(10, 6))
shap.plots.beeswarm(shap_values, show=False)
plt.title("SHAP Oznitelik Onem Grafigi (Ulasim Talebi Uzerindeki Etkiler)", fontsize=12)
plt.tight_layout()
plt.savefig("03_Model/shap_ozet.png", dpi=200)
plt.close()
print("SHAP grafigi 03_Model/shap_ozet.png olarak kaydedildi!")
print("\nTUM MODELLER VE ANALIZLER BASARIYLA TAMAMLANDI!")
