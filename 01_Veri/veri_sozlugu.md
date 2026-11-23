# G03 - Istanbul Toplu Ulasim Talep Tahmini: Veri Sozlugu (Data Dictionary)

Bu veri seti, Istanbul Buyuksehir Belediyesi (IBB) Acik Veri Portali BELBIM saatlik gecis verileri, Open-Meteo Tarihsel Hava Durumu API'si ve Turkiye resmi tatil takviminin birlestirilmesiyle olusturulmustur.

## Kapsam
- Tarih Araligi: 01 Temmuz 2024 - 30 Eylul 2024 (3 Ay)
- Kayit Sayisi: 70,235 satir
- Granulerlik: Saatlik bazda ilce ve ulasim modu agregasyonu

---

## Degisken Aciklamalari

| Kolon Adi | Veri Tipi | Kaynak | Aciklama |
| :--- | :--- | :--- | :--- |
| tarih | Date (YYYY-MM-DD) | BELBIM | Ulasim gecisinin gerceklestigi gun. |
| saat | Integer (0-23) | BELBİM | Gunun saati (0: 00:00-00:59 arasi). |
| mod | String / Kategori | BELBİM | Ulasim turu (Otobus, Rayli, Deniz, vb.). |
| ilce | String | BELBİM | Gecisin gerceklestigi Istanbul ilcesi. |
| yolcu | Integer | BELBİM | Ilgili saat ve ilcedeki tekil yolcu kart basim sayisi. |
| yolculuk | Integer | BELBİM | Aktarmalar dahil toplam gecis sayisi. |
| sicaklik | Float (C) | Open-Meteo | Istanbul geneli saatlik yuzey sicakligi (2m). |
| yagis | Float (mm) | Open-Meteo | Saatlik toplam yagis miktari. |
| ruzgar | Float (km/h) | Open-Meteo | Saatlik ortalama ruzgar hizi (10m). |
| ruzgar_hamle | Float (km/h) | Open-Meteo | Saatlik maksimum ruzgar hamle hizi. |
| haftanin_gunu | Integer (0-6) | Turetilmis | 0: Pazartesi, ..., 6: Pazar. |
| hafta_sonu | Binary (0 / 1) | Turetilmis | 1: Cumartesi/Pazar, 0: Hafta ici. |
| tatil | Binary (0 / 1) | holidays | 1: Resmi/dini tatil, 0: Normal gun. |
| bayram_oncesi | Binary (0 / 1) | Turetilmis | Dini bayram oncesi son is gunu mu? |
| okul_donemi | Binary (0 / 1) | Turetilmis | Okullarin acik oldugu donem mi? |
