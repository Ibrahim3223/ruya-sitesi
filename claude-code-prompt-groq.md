# 🌙 Rüya Tabirleri Programmatic SEO Sitesi - Claude Code Prompt
# GROQ API VERSİYONU (Ücretsiz + Hızlı)

## PROJE ÖZETİ

Türkçe rüya tabirleri sitesi oluşturacaksın. Bu site:
- 30,000+ otomatik üretilmiş sayfa içerecek
- Hugo static site generator kullanacak
- **Groq API** ile içerik üretecek (ücretsiz, çok hızlı)
- Cloudflare Pages'da host edilecek
- Tamamen SEO optimize olacak

## ÖN GEREKSİNİMLER

Kullanıcı şunları zaten kurmuş olmalı:
- Python 3.10+
- Hugo
- Git
- Groq API anahtarı (https://console.groq.com)

## ADIM ADIM TALİMATLAR

### AŞAMA 1: PROJE YAPISI OLUŞTUR

Windows'ta şu klasör yapısını oluştur:

```
ruya-sitesi/
├── data/
│   ├── raw/                    # Ham veri dosyaları
│   │   ├── objects.json        # Rüya objeleri
│   │   └── actions.json        # Eylemler
│   └── processed/              # İşlenmiş veri
│       └── combinations.json   # Tüm kombinasyonlar
├── scripts/
│   ├── collect_data.py         # Veri toplama
│   ├── generate_combinations.py # Kombinasyon üretme
│   └── generate_content.py     # Groq ile içerik üretimi
├── hugo-site/
│   ├── config.toml             # Hugo ayarları
│   ├── content/
│   │   ├── ruya/               # Rüya sayfaları
│   │   ├── _index.md           # Ana sayfa
│   │   └── hakkimizda.md
│   ├── layouts/
│   │   ├── _default/
│   │   │   ├── baseof.html
│   │   │   ├── single.html
│   │   │   └── list.html
│   │   ├── partials/
│   │   │   ├── head.html
│   │   │   ├── header.html
│   │   │   ├── footer.html
│   │   │   └── schema.html
│   │   └── ruya/
│   │       └── single.html
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── main.js
├── requirements.txt
└── README.md
```

Klasörleri oluşturmak için Windows CMD komutları:

```cmd
mkdir data\raw
mkdir data\processed
mkdir scripts
mkdir hugo-site\content\ruya
mkdir hugo-site\layouts\_default
mkdir hugo-site\layouts\partials
mkdir hugo-site\layouts\ruya
mkdir hugo-site\static\css
mkdir hugo-site\static\js
```

### AŞAMA 2: REQUIREMENTS.TXT

```
aiohttp>=3.9.0
tqdm>=4.66.0
python-slugify>=8.0.0
pyyaml>=6.0.0
```

Kurulum:
```cmd
pip install -r requirements.txt
```

### AŞAMA 3: VERİ TOPLAMA SCRIPTİ

#### scripts/collect_data.py

```python
#!/usr/bin/env python3
"""
Rüya tabirleri veri toplama scripti
500+ rüya objesi ve 50+ eylem
"""

import json
from pathlib import Path

class DataCollector:
    def __init__(self):
        self.data_dir = Path("data/raw")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
    def generate_objects(self):
        """Temel rüya objelerini oluştur - 200+ obje"""
        
        objects = [
            # ═══════════════════════════════════════════════════════════
            # HAYVANLAR (50+)
            # ═══════════════════════════════════════════════════════════
            {"id": "yilan", "name": "Yılan", "category": "hayvanlar", "keywords": ["yılan", "kobra", "engerek"], "search_volume": "high"},
            {"id": "kopek", "name": "Köpek", "category": "hayvanlar", "keywords": ["köpek", "it", "köpek yavrusu"], "search_volume": "high"},
            {"id": "kedi", "name": "Kedi", "category": "hayvanlar", "keywords": ["kedi", "kedicik", "yavru kedi"], "search_volume": "high"},
            {"id": "at", "name": "At", "category": "hayvanlar", "keywords": ["at", "tay", "aygır", "kısrak"], "search_volume": "high"},
            {"id": "kus", "name": "Kuş", "category": "hayvanlar", "keywords": ["kuş", "serçe", "bülbül"], "search_volume": "high"},
            {"id": "balik", "name": "Balık", "category": "hayvanlar", "keywords": ["balık", "balıklar"], "search_volume": "high"},
            {"id": "aslan", "name": "Aslan", "category": "hayvanlar", "keywords": ["aslan", "dişi aslan"], "search_volume": "medium"},
            {"id": "kaplan", "name": "Kaplan", "category": "hayvanlar", "keywords": ["kaplan"], "search_volume": "medium"},
            {"id": "fare", "name": "Fare", "category": "hayvanlar", "keywords": ["fare", "sıçan"], "search_volume": "high"},
            {"id": "orumcek", "name": "Örümcek", "category": "hayvanlar", "keywords": ["örümcek", "tarantula"], "search_volume": "high"},
            {"id": "ari", "name": "Arı", "category": "hayvanlar", "keywords": ["arı", "bal arısı", "eşek arısı"], "search_volume": "medium"},
            {"id": "kelebek", "name": "Kelebek", "category": "hayvanlar", "keywords": ["kelebek"], "search_volume": "medium"},
            {"id": "karinca", "name": "Karınca", "category": "hayvanlar", "keywords": ["karınca"], "search_volume": "medium"},
            {"id": "kurt", "name": "Kurt", "category": "hayvanlar", "keywords": ["kurt", "bozkurt"], "search_volume": "medium"},
            {"id": "ayi", "name": "Ayı", "category": "hayvanlar", "keywords": ["ayı"], "search_volume": "medium"},
            {"id": "fil", "name": "Fil", "category": "hayvanlar", "keywords": ["fil"], "search_volume": "medium"},
            {"id": "maymun", "name": "Maymun", "category": "hayvanlar", "keywords": ["maymun", "goril"], "search_volume": "medium"},
            {"id": "tavsan", "name": "Tavşan", "category": "hayvanlar", "keywords": ["tavşan"], "search_volume": "medium"},
            {"id": "koyun", "name": "Koyun", "category": "hayvanlar", "keywords": ["koyun", "kuzu"], "search_volume": "medium"},
            {"id": "keci", "name": "Keçi", "category": "hayvanlar", "keywords": ["keçi", "oğlak"], "search_volume": "medium"},
            {"id": "inek", "name": "İnek", "category": "hayvanlar", "keywords": ["inek", "buzağı"], "search_volume": "medium"},
            {"id": "deve", "name": "Deve", "category": "hayvanlar", "keywords": ["deve"], "search_volume": "low"},
            {"id": "esek", "name": "Eşek", "category": "hayvanlar", "keywords": ["eşek", "merkep"], "search_volume": "low"},
            {"id": "horoz", "name": "Horoz", "category": "hayvanlar", "keywords": ["horoz"], "search_volume": "medium"},
            {"id": "tavuk", "name": "Tavuk", "category": "hayvanlar", "keywords": ["tavuk", "civciv"], "search_volume": "medium"},
            {"id": "kartal", "name": "Kartal", "category": "hayvanlar", "keywords": ["kartal"], "search_volume": "medium"},
            {"id": "guvercin", "name": "Güvercin", "category": "hayvanlar", "keywords": ["güvercin", "kumru"], "search_volume": "medium"},
            {"id": "karga", "name": "Karga", "category": "hayvanlar", "keywords": ["karga"], "search_volume": "medium"},
            {"id": "baykus", "name": "Baykuş", "category": "hayvanlar", "keywords": ["baykuş", "puhu"], "search_volume": "medium"},
            {"id": "timsah", "name": "Timsah", "category": "hayvanlar", "keywords": ["timsah"], "search_volume": "low"},
            {"id": "kaplumbaga", "name": "Kaplumbağa", "category": "hayvanlar", "keywords": ["kaplumbağa"], "search_volume": "medium"},
            {"id": "akrep", "name": "Akrep", "category": "hayvanlar", "keywords": ["akrep"], "search_volume": "high"},
            {"id": "kertenkele", "name": "Kertenkele", "category": "hayvanlar", "keywords": ["kertenkele"], "search_volume": "low"},
            {"id": "kurbaga", "name": "Kurbağa", "category": "hayvanlar", "keywords": ["kurbağa"], "search_volume": "medium"},
            {"id": "yunus", "name": "Yunus", "category": "hayvanlar", "keywords": ["yunus", "yunus balığı"], "search_volume": "medium"},
            {"id": "kopekbaligi", "name": "Köpekbalığı", "category": "hayvanlar", "keywords": ["köpekbalığı"], "search_volume": "medium"},
            {"id": "bocek", "name": "Böcek", "category": "hayvanlar", "keywords": ["böcek", "hamam böceği"], "search_volume": "medium"},
            {"id": "solucan", "name": "Solucan", "category": "hayvanlar", "keywords": ["solucan"], "search_volume": "low"},
            {"id": "bit", "name": "Bit", "category": "hayvanlar", "keywords": ["bit", "sirke"], "search_volume": "medium"},
            {"id": "pire", "name": "Pire", "category": "hayvanlar", "keywords": ["pire"], "search_volume": "low"},
            {"id": "domuz", "name": "Domuz", "category": "hayvanlar", "keywords": ["domuz"], "search_volume": "medium"},
            {"id": "tilki", "name": "Tilki", "category": "hayvanlar", "keywords": ["tilki"], "search_volume": "medium"},
            {"id": "ceylan", "name": "Ceylan", "category": "hayvanlar", "keywords": ["ceylan", "geyik"], "search_volume": "low"},
            {"id": "sincap", "name": "Sincap", "category": "hayvanlar", "keywords": ["sincap"], "search_volume": "low"},
            {"id": "kirpi", "name": "Kirpi", "category": "hayvanlar", "keywords": ["kirpi"], "search_volume": "low"},
            {"id": "yarasa", "name": "Yarasa", "category": "hayvanlar", "keywords": ["yarasa"], "search_volume": "medium"},
            {"id": "penguen", "name": "Penguen", "category": "hayvanlar", "keywords": ["penguen"], "search_volume": "low"},
            {"id": "zurafa", "name": "Zürafa", "category": "hayvanlar", "keywords": ["zürafa"], "search_volume": "low"},
            {"id": "zebra", "name": "Zebra", "category": "hayvanlar", "keywords": ["zebra"], "search_volume": "low"},
            {"id": "gergedan", "name": "Gergedan", "category": "hayvanlar", "keywords": ["gergedan"], "search_volume": "low"},
            
            # ═══════════════════════════════════════════════════════════
            # İNSANLAR (35+)
            # ═══════════════════════════════════════════════════════════
            {"id": "anne", "name": "Anne", "category": "insanlar", "keywords": ["anne", "annem", "ana"], "search_volume": "high"},
            {"id": "baba", "name": "Baba", "category": "insanlar", "keywords": ["baba", "babam"], "search_volume": "high"},
            {"id": "kardes", "name": "Kardeş", "category": "insanlar", "keywords": ["kardeş", "abi", "abla"], "search_volume": "high"},
            {"id": "es", "name": "Eş", "category": "insanlar", "keywords": ["eş", "koca", "karı", "eşim"], "search_volume": "high"},
            {"id": "cocuk", "name": "Çocuk", "category": "insanlar", "keywords": ["çocuk", "oğul", "kız"], "search_volume": "high"},
            {"id": "bebek", "name": "Bebek", "category": "insanlar", "keywords": ["bebek", "yeni doğan"], "search_volume": "high"},
            {"id": "olu", "name": "Ölü", "category": "insanlar", "keywords": ["ölü", "ölmüş", "merhum", "vefat etmiş"], "search_volume": "high"},
            {"id": "olu_anne", "name": "Ölmüş Anne", "category": "insanlar", "keywords": ["ölmüş anne", "vefat etmiş anne"], "search_volume": "high"},
            {"id": "olu_baba", "name": "Ölmüş Baba", "category": "insanlar", "keywords": ["ölmüş baba", "vefat etmiş baba"], "search_volume": "high"},
            {"id": "tanimadik_biri", "name": "Tanımadık Biri", "category": "insanlar", "keywords": ["tanımadık", "yabancı"], "search_volume": "medium"},
            {"id": "dusman", "name": "Düşman", "category": "insanlar", "keywords": ["düşman", "hasım"], "search_volume": "medium"},
            {"id": "arkadas", "name": "Arkadaş", "category": "insanlar", "keywords": ["arkadaş", "dost"], "search_volume": "high"},
            {"id": "sevgili", "name": "Sevgili", "category": "insanlar", "keywords": ["sevgili", "aşk"], "search_volume": "high"},
            {"id": "eski_sevgili", "name": "Eski Sevgili", "category": "insanlar", "keywords": ["eski sevgili", "manita"], "search_volume": "high"},
            {"id": "dede", "name": "Dede", "category": "insanlar", "keywords": ["dede", "büyükbaba"], "search_volume": "medium"},
            {"id": "nine", "name": "Nine", "category": "insanlar", "keywords": ["nine", "babaanne", "anneanne"], "search_volume": "medium"},
            {"id": "amca", "name": "Amca", "category": "insanlar", "keywords": ["amca"], "search_volume": "low"},
            {"id": "dayi", "name": "Dayı", "category": "insanlar", "keywords": ["dayı"], "search_volume": "low"},
            {"id": "hala", "name": "Hala", "category": "insanlar", "keywords": ["hala"], "search_volume": "low"},
            {"id": "teyze", "name": "Teyze", "category": "insanlar", "keywords": ["teyze"], "search_volume": "low"},
            {"id": "komsu", "name": "Komşu", "category": "insanlar", "keywords": ["komşu"], "search_volume": "low"},
            {"id": "ogretmen", "name": "Öğretmen", "category": "insanlar", "keywords": ["öğretmen", "hoca"], "search_volume": "medium"},
            {"id": "doktor", "name": "Doktor", "category": "insanlar", "keywords": ["doktor", "hekim"], "search_volume": "medium"},
            {"id": "polis", "name": "Polis", "category": "insanlar", "keywords": ["polis"], "search_volume": "medium"},
            {"id": "asker", "name": "Asker", "category": "insanlar", "keywords": ["asker"], "search_volume": "medium"},
            {"id": "imam", "name": "İmam", "category": "insanlar", "keywords": ["imam", "hoca"], "search_volume": "medium"},
            {"id": "padisah", "name": "Padişah", "category": "insanlar", "keywords": ["padişah", "sultan"], "search_volume": "low"},
            {"id": "kral", "name": "Kral", "category": "insanlar", "keywords": ["kral", "kraliçe"], "search_volume": "low"},
            {"id": "hirsiz", "name": "Hırsız", "category": "insanlar", "keywords": ["hırsız"], "search_volume": "medium"},
            {"id": "gelin", "name": "Gelin", "category": "insanlar", "keywords": ["gelin"], "search_volume": "medium"},
            {"id": "damat", "name": "Damat", "category": "insanlar", "keywords": ["damat"], "search_volume": "medium"},
            {"id": "hamile_kadin", "name": "Hamile Kadın", "category": "insanlar", "keywords": ["hamile", "gebe"], "search_volume": "high"},
            {"id": "kiz_cocugu", "name": "Kız Çocuğu", "category": "insanlar", "keywords": ["kız çocuğu", "kız bebek"], "search_volume": "medium"},
            {"id": "erkek_cocugu", "name": "Erkek Çocuğu", "category": "insanlar", "keywords": ["erkek çocuğu", "oğlan"], "search_volume": "medium"},
            {"id": "yasli", "name": "Yaşlı", "category": "insanlar", "keywords": ["yaşlı", "ihtiyar"], "search_volume": "medium"},
            
            # ═══════════════════════════════════════════════════════════
            # DOĞAL ELEMENTLER (35+)
            # ═══════════════════════════════════════════════════════════
            {"id": "su", "name": "Su", "category": "doga", "keywords": ["su", "sular"], "search_volume": "high"},
            {"id": "ates", "name": "Ateş", "category": "doga", "keywords": ["ateş", "alev", "yangın"], "search_volume": "high"},
            {"id": "toprak", "name": "Toprak", "category": "doga", "keywords": ["toprak"], "search_volume": "medium"},
            {"id": "hava", "name": "Hava", "category": "doga", "keywords": ["hava", "rüzgar", "fırtına"], "search_volume": "medium"},
            {"id": "gunes", "name": "Güneş", "category": "doga", "keywords": ["güneş"], "search_volume": "medium"},
            {"id": "ay", "name": "Ay", "category": "doga", "keywords": ["ay", "dolunay", "hilal"], "search_volume": "high"},
            {"id": "yildiz", "name": "Yıldız", "category": "doga", "keywords": ["yıldız", "yıldızlar"], "search_volume": "medium"},
            {"id": "bulut", "name": "Bulut", "category": "doga", "keywords": ["bulut"], "search_volume": "low"},
            {"id": "yagmur", "name": "Yağmur", "category": "doga", "keywords": ["yağmur"], "search_volume": "high"},
            {"id": "kar", "name": "Kar", "category": "doga", "keywords": ["kar"], "search_volume": "high"},
            {"id": "dolu", "name": "Dolu", "category": "doga", "keywords": ["dolu"], "search_volume": "low"},
            {"id": "simsek", "name": "Şimşek", "category": "doga", "keywords": ["şimşek", "yıldırım"], "search_volume": "medium"},
            {"id": "gokkusagi", "name": "Gökkuşağı", "category": "doga", "keywords": ["gökkuşağı"], "search_volume": "medium"},
            {"id": "deniz", "name": "Deniz", "category": "doga", "keywords": ["deniz"], "search_volume": "high"},
            {"id": "okyanus", "name": "Okyanus", "category": "doga", "keywords": ["okyanus"], "search_volume": "low"},
            {"id": "nehir", "name": "Nehir", "category": "doga", "keywords": ["nehir", "ırmak", "çay", "dere"], "search_volume": "medium"},
            {"id": "gol", "name": "Göl", "category": "doga", "keywords": ["göl"], "search_volume": "medium"},
            {"id": "dag", "name": "Dağ", "category": "doga", "keywords": ["dağ", "dağlar"], "search_volume": "medium"},
            {"id": "orman", "name": "Orman", "category": "doga", "keywords": ["orman", "ağaçlık"], "search_volume": "medium"},
            {"id": "col", "name": "Çöl", "category": "doga", "keywords": ["çöl"], "search_volume": "low"},
            {"id": "magara", "name": "Mağara", "category": "doga", "keywords": ["mağara"], "search_volume": "medium"},
            {"id": "deprem", "name": "Deprem", "category": "doga", "keywords": ["deprem", "zelzele"], "search_volume": "high"},
            {"id": "sel", "name": "Sel", "category": "doga", "keywords": ["sel", "sel baskını"], "search_volume": "medium"},
            {"id": "volkan", "name": "Volkan", "category": "doga", "keywords": ["volkan", "yanardağ"], "search_volume": "low"},
            {"id": "cicek", "name": "Çiçek", "category": "doga", "keywords": ["çiçek", "gül", "papatya"], "search_volume": "medium"},
            {"id": "gul", "name": "Gül", "category": "doga", "keywords": ["gül", "kırmızı gül"], "search_volume": "medium"},
            {"id": "agac", "name": "Ağaç", "category": "doga", "keywords": ["ağaç"], "search_volume": "medium"},
            {"id": "yaprak", "name": "Yaprak", "category": "doga", "keywords": ["yaprak"], "search_volume": "low"},
            {"id": "cimen", "name": "Çimen", "category": "doga", "keywords": ["çimen", "yeşillik"], "search_volume": "low"},
            {"id": "tas", "name": "Taş", "category": "doga", "keywords": ["taş", "kaya"], "search_volume": "medium"},
            {"id": "kum", "name": "Kum", "category": "doga", "keywords": ["kum", "kumsal"], "search_volume": "low"},
            {"id": "camur", "name": "Çamur", "category": "doga", "keywords": ["çamur", "balçık"], "search_volume": "medium"},
            {"id": "dalga", "name": "Dalga", "category": "doga", "keywords": ["dalga", "deniz dalgası"], "search_volume": "medium"},
            {"id": "tsunami", "name": "Tsunami", "category": "doga", "keywords": ["tsunami", "dev dalga"], "search_volume": "medium"},
            {"id": "buz", "name": "Buz", "category": "doga", "keywords": ["buz"], "search_volume": "low"},
            
            # ═══════════════════════════════════════════════════════════
            # MEKANLAR (30+)
            # ═══════════════════════════════════════════════════════════
            {"id": "ev", "name": "Ev", "category": "mekanlar", "keywords": ["ev", "konut", "yuva"], "search_volume": "high"},
            {"id": "eski_ev", "name": "Eski Ev", "category": "mekanlar", "keywords": ["eski ev", "çocukluk evi"], "search_volume": "medium"},
            {"id": "oda", "name": "Oda", "category": "mekanlar", "keywords": ["oda"], "search_volume": "medium"},
            {"id": "mutfak", "name": "Mutfak", "category": "mekanlar", "keywords": ["mutfak"], "search_volume": "low"},
            {"id": "banyo", "name": "Banyo", "category": "mekanlar", "keywords": ["banyo", "hamam"], "search_volume": "medium"},
            {"id": "tuvalet", "name": "Tuvalet", "category": "mekanlar", "keywords": ["tuvalet", "hela"], "search_volume": "high"},
            {"id": "yatak_odasi", "name": "Yatak Odası", "category": "mekanlar", "keywords": ["yatak odası"], "search_volume": "low"},
            {"id": "balkon", "name": "Balkon", "category": "mekanlar", "keywords": ["balkon", "teras"], "search_volume": "low"},
            {"id": "bahce", "name": "Bahçe", "category": "mekanlar", "keywords": ["bahçe"], "search_volume": "medium"},
            {"id": "cami", "name": "Cami", "category": "mekanlar", "keywords": ["cami", "mescit"], "search_volume": "high"},
            {"id": "kilise", "name": "Kilise", "category": "mekanlar", "keywords": ["kilise"], "search_volume": "low"},
            {"id": "mezarlik", "name": "Mezarlık", "category": "mekanlar", "keywords": ["mezarlık", "kabir", "türbe"], "search_volume": "high"},
            {"id": "hastane", "name": "Hastane", "category": "mekanlar", "keywords": ["hastane"], "search_volume": "medium"},
            {"id": "okul", "name": "Okul", "category": "mekanlar", "keywords": ["okul", "sınıf"], "search_volume": "medium"},
            {"id": "hapishane", "name": "Hapishane", "category": "mekanlar", "keywords": ["hapishane", "cezaevi"], "search_volume": "medium"},
            {"id": "saray", "name": "Saray", "category": "mekanlar", "keywords": ["saray"], "search_volume": "medium"},
            {"id": "kopru", "name": "Köprü", "category": "mekanlar", "keywords": ["köprü"], "search_volume": "medium"},
            {"id": "yol", "name": "Yol", "category": "mekanlar", "keywords": ["yol", "cadde", "sokak"], "search_volume": "medium"},
            {"id": "market", "name": "Market", "category": "mekanlar", "keywords": ["market", "mağaza"], "search_volume": "low"},
            {"id": "carsi", "name": "Çarşı", "category": "mekanlar", "keywords": ["çarşı", "pazar"], "search_volume": "low"},
            {"id": "otel", "name": "Otel", "category": "mekanlar", "keywords": ["otel"], "search_volume": "medium"},
            {"id": "asansor", "name": "Asansör", "category": "mekanlar", "keywords": ["asansör"], "search_volume": "medium"},
            {"id": "merdiven", "name": "Merdiven", "category": "mekanlar", "keywords": ["merdiven"], "search_volume": "high"},
            {"id": "bodrum", "name": "Bodrum", "category": "mekanlar", "keywords": ["bodrum", "kiler"], "search_volume": "medium"},
            {"id": "cati", "name": "Çatı", "category": "mekanlar", "keywords": ["çatı", "dam"], "search_volume": "medium"},
            {"id": "havaalani", "name": "Havaalanı", "category": "mekanlar", "keywords": ["havaalanı", "havalimanı"], "search_volume": "low"},
            {"id": "plaj", "name": "Plaj", "category": "mekanlar", "keywords": ["plaj", "sahil"], "search_volume": "medium"},
            {"id": "havuz", "name": "Havuz", "category": "mekanlar", "keywords": ["havuz", "yüzme havuzu"], "search_volume": "medium"},
            {"id": "is_yeri", "name": "İş Yeri", "category": "mekanlar", "keywords": ["iş yeri", "ofis"], "search_volume": "medium"},
            {"id": "fabrika", "name": "Fabrika", "category": "mekanlar", "keywords": ["fabrika"], "search_volume": "low"},
            
            # ═══════════════════════════════════════════════════════════
            # NESNELER (50+)
            # ═══════════════════════════════════════════════════════════
            {"id": "para", "name": "Para", "category": "nesneler", "keywords": ["para", "nakit", "banknot"], "search_volume": "high"},
            {"id": "altin", "name": "Altın", "category": "nesneler", "keywords": ["altın", "altın takı"], "search_volume": "high"},
            {"id": "gumus", "name": "Gümüş", "category": "nesneler", "keywords": ["gümüş"], "search_volume": "medium"},
            {"id": "elmas", "name": "Elmas", "category": "nesneler", "keywords": ["elmas", "pırlanta"], "search_volume": "medium"},
            {"id": "yuzuk", "name": "Yüzük", "category": "nesneler", "keywords": ["yüzük", "nişan yüzüğü", "alyans"], "search_volume": "high"},
            {"id": "bilezik", "name": "Bilezik", "category": "nesneler", "keywords": ["bilezik"], "search_volume": "medium"},
            {"id": "kolye", "name": "Kolye", "category": "nesneler", "keywords": ["kolye", "gerdanlık"], "search_volume": "medium"},
            {"id": "kupe", "name": "Küpe", "category": "nesneler", "keywords": ["küpe"], "search_volume": "medium"},
            {"id": "araba", "name": "Araba", "category": "nesneler", "keywords": ["araba", "otomobil", "araç"], "search_volume": "high"},
            {"id": "ucak", "name": "Uçak", "category": "nesneler", "keywords": ["uçak"], "search_volume": "medium"},
            {"id": "gemi", "name": "Gemi", "category": "nesneler", "keywords": ["gemi", "vapur", "tekne"], "search_volume": "medium"},
            {"id": "tren", "name": "Tren", "category": "nesneler", "keywords": ["tren"], "search_volume": "medium"},
            {"id": "bisiklet", "name": "Bisiklet", "category": "nesneler", "keywords": ["bisiklet"], "search_volume": "low"},
            {"id": "telefon", "name": "Telefon", "category": "nesneler", "keywords": ["telefon", "cep telefonu"], "search_volume": "medium"},
            {"id": "bilgisayar", "name": "Bilgisayar", "category": "nesneler", "keywords": ["bilgisayar"], "search_volume": "low"},
            {"id": "kitap", "name": "Kitap", "category": "nesneler", "keywords": ["kitap"], "search_volume": "medium"},
            {"id": "kalem", "name": "Kalem", "category": "nesneler", "keywords": ["kalem"], "search_volume": "low"},
            {"id": "bicak", "name": "Bıçak", "category": "nesneler", "keywords": ["bıçak"], "search_volume": "high"},
            {"id": "silah", "name": "Silah", "category": "nesneler", "keywords": ["silah", "tüfek", "tabanca"], "search_volume": "high"},
            {"id": "anahtar", "name": "Anahtar", "category": "nesneler", "keywords": ["anahtar"], "search_volume": "medium"},
            {"id": "kapi", "name": "Kapı", "category": "nesneler", "keywords": ["kapı"], "search_volume": "medium"},
            {"id": "pencere", "name": "Pencere", "category": "nesneler", "keywords": ["pencere", "cam"], "search_volume": "medium"},
            {"id": "ayna", "name": "Ayna", "category": "nesneler", "keywords": ["ayna"], "search_volume": "high"},
            {"id": "saat", "name": "Saat", "category": "nesneler", "keywords": ["saat", "kol saati"], "search_volume": "medium"},
            {"id": "yatak", "name": "Yatak", "category": "nesneler", "keywords": ["yatak", "döşek"], "search_volume": "medium"},
            {"id": "masa", "name": "Masa", "category": "nesneler", "keywords": ["masa"], "search_volume": "low"},
            {"id": "sandalye", "name": "Sandalye", "category": "nesneler", "keywords": ["sandalye", "koltuk"], "search_volume": "low"},
            {"id": "mum", "name": "Mum", "category": "nesneler", "keywords": ["mum"], "search_volume": "medium"},
            {"id": "tabut", "name": "Tabut", "category": "nesneler", "keywords": ["tabut", "cenaze"], "search_volume": "high"},
            {"id": "kefen", "name": "Kefen", "category": "nesneler", "keywords": ["kefen"], "search_volume": "medium"},
            {"id": "mezar", "name": "Mezar", "category": "nesneler", "keywords": ["mezar", "kabir"], "search_volume": "high"},
            {"id": "kuran", "name": "Kuran", "category": "nesneler", "keywords": ["kuran", "mushaf"], "search_volume": "high"},
            {"id": "tespih", "name": "Tespih", "category": "nesneler", "keywords": ["tespih"], "search_volume": "medium"},
            {"id": "bayrak", "name": "Bayrak", "category": "nesneler", "keywords": ["bayrak", "türk bayrağı"], "search_volume": "medium"},
            {"id": "ip", "name": "İp", "category": "nesneler", "keywords": ["ip", "halat", "urgan"], "search_volume": "medium"},
            {"id": "zincir", "name": "Zincir", "category": "nesneler", "keywords": ["zincir"], "search_volume": "medium"},
            {"id": "kilit", "name": "Kilit", "category": "nesneler", "keywords": ["kilit", "asma kilit"], "search_volume": "medium"},
            {"id": "canta", "name": "Çanta", "category": "nesneler", "keywords": ["çanta", "el çantası"], "search_volume": "medium"},
            {"id": "ayakkabi", "name": "Ayakkabı", "category": "nesneler", "keywords": ["ayakkabı", "terlik"], "search_volume": "high"},
            {"id": "elbise", "name": "Elbise", "category": "nesneler", "keywords": ["elbise", "kıyafet"], "search_volume": "medium"},
            {"id": "gelinlik", "name": "Gelinlik", "category": "nesneler", "keywords": ["gelinlik"], "search_volume": "high"},
            {"id": "basortusi", "name": "Başörtüsü", "category": "nesneler", "keywords": ["başörtüsü", "türban", "eşarp"], "search_volume": "medium"},
            {"id": "cuzdan", "name": "Cüzdan", "category": "nesneler", "keywords": ["cüzdan"], "search_volume": "medium"},
            {"id": "fotograf", "name": "Fotoğraf", "category": "nesneler", "keywords": ["fotoğraf", "resim"], "search_volume": "medium"},
            {"id": "mektup", "name": "Mektup", "category": "nesneler", "keywords": ["mektup"], "search_volume": "medium"},
            {"id": "hediye", "name": "Hediye", "category": "nesneler", "keywords": ["hediye"], "search_volume": "medium"},
            {"id": "bebek_arabasi", "name": "Bebek Arabası", "category": "nesneler", "keywords": ["bebek arabası"], "search_volume": "low"},
            {"id": "oyuncak", "name": "Oyuncak", "category": "nesneler", "keywords": ["oyuncak"], "search_volume": "low"},
            {"id": "beşik", "name": "Beşik", "category": "nesneler", "keywords": ["beşik"], "search_volume": "low"},
            {"id": "supurge", "name": "Süpürge", "category": "nesneler", "keywords": ["süpürge"], "search_volume": "low"},
            
            # ═══════════════════════════════════════════════════════════
            # YİYECEK/İÇECEK (25+)
            # ═══════════════════════════════════════════════════════════
            {"id": "ekmek", "name": "Ekmek", "category": "yiyecekler", "keywords": ["ekmek"], "search_volume": "medium"},
            {"id": "et", "name": "Et", "category": "yiyecekler", "keywords": ["et", "kırmızı et"], "search_volume": "high"},
            {"id": "balik_yemek", "name": "Balık (Yemek)", "category": "yiyecekler", "keywords": ["balık yemek"], "search_volume": "medium"},
            {"id": "meyve", "name": "Meyve", "category": "yiyecekler", "keywords": ["meyve"], "search_volume": "medium"},
            {"id": "sut", "name": "Süt", "category": "yiyecekler", "keywords": ["süt"], "search_volume": "medium"},
            {"id": "peynir", "name": "Peynir", "category": "yiyecekler", "keywords": ["peynir"], "search_volume": "low"},
            {"id": "yumurta", "name": "Yumurta", "category": "yiyecekler", "keywords": ["yumurta"], "search_volume": "medium"},
            {"id": "bal", "name": "Bal", "category": "yiyecekler", "keywords": ["bal"], "search_volume": "medium"},
            {"id": "seker", "name": "Şeker", "category": "yiyecekler", "keywords": ["şeker"], "search_volume": "low"},
            {"id": "tuz", "name": "Tuz", "category": "yiyecekler", "keywords": ["tuz"], "search_volume": "low"},
            {"id": "elma", "name": "Elma", "category": "yiyecekler", "keywords": ["elma"], "search_volume": "medium"},
            {"id": "uzum", "name": "Üzüm", "category": "yiyecekler", "keywords": ["üzüm"], "search_volume": "medium"},
            {"id": "nar", "name": "Nar", "category": "yiyecekler", "keywords": ["nar"], "search_volume": "medium"},
            {"id": "incir", "name": "İncir", "category": "yiyecekler", "keywords": ["incir"], "search_volume": "medium"},
            {"id": "hurma", "name": "Hurma", "category": "yiyecekler", "keywords": ["hurma"], "search_volume": "medium"},
            {"id": "zeytin", "name": "Zeytin", "category": "yiyecekler", "keywords": ["zeytin"], "search_volume": "low"},
            {"id": "cay", "name": "Çay", "category": "yiyecekler", "keywords": ["çay"], "search_volume": "medium"},
            {"id": "kahve", "name": "Kahve", "category": "yiyecekler", "keywords": ["kahve", "türk kahvesi"], "search_volume": "medium"},
            {"id": "sarap", "name": "Şarap", "category": "yiyecekler", "keywords": ["şarap", "içki"], "search_volume": "medium"},
            {"id": "raki", "name": "Rakı", "category": "yiyecekler", "keywords": ["rakı", "alkol"], "search_volume": "medium"},
            {"id": "bira", "name": "Bira", "category": "yiyecekler", "keywords": ["bira"], "search_volume": "medium"},
            {"id": "tatli", "name": "Tatlı", "category": "yiyecekler", "keywords": ["tatlı", "baklava", "pasta"], "search_volume": "medium"},
            {"id": "dondurma", "name": "Dondurma", "category": "yiyecekler", "keywords": ["dondurma"], "search_volume": "low"},
            {"id": "cikolata", "name": "Çikolata", "category": "yiyecekler", "keywords": ["çikolata"], "search_volume": "low"},
            {"id": "pilav", "name": "Pilav", "category": "yiyecekler", "keywords": ["pilav"], "search_volume": "low"},
            
            # ═══════════════════════════════════════════════════════════
            # VÜCUT (25+)
            # ═══════════════════════════════════════════════════════════
            {"id": "sac", "name": "Saç", "category": "vucut", "keywords": ["saç", "saçlar"], "search_volume": "high"},
            {"id": "sac_dokulmesi", "name": "Saç Dökülmesi", "category": "vucut", "keywords": ["saç dökülmesi", "kel"], "search_volume": "medium"},
            {"id": "goz", "name": "Göz", "category": "vucut", "keywords": ["göz", "gözler"], "search_volume": "medium"},
            {"id": "kulak", "name": "Kulak", "category": "vucut", "keywords": ["kulak"], "search_volume": "low"},
            {"id": "burun", "name": "Burun", "category": "vucut", "keywords": ["burun"], "search_volume": "low"},
            {"id": "agiz", "name": "Ağız", "category": "vucut", "keywords": ["ağız"], "search_volume": "low"},
            {"id": "dis", "name": "Diş", "category": "vucut", "keywords": ["diş", "dişler"], "search_volume": "high"},
            {"id": "dis_dusmesi", "name": "Diş Düşmesi", "category": "vucut", "keywords": ["diş düşmesi", "diş kırılması"], "search_volume": "high"},
            {"id": "dil", "name": "Dil", "category": "vucut", "keywords": ["dil"], "search_volume": "low"},
            {"id": "el", "name": "El", "category": "vucut", "keywords": ["el", "eller"], "search_volume": "medium"},
            {"id": "ayak", "name": "Ayak", "category": "vucut", "keywords": ["ayak", "ayaklar"], "search_volume": "medium"},
            {"id": "parmak", "name": "Parmak", "category": "vucut", "keywords": ["parmak"], "search_volume": "medium"},
            {"id": "tirnak", "name": "Tırnak", "category": "vucut", "keywords": ["tırnak"], "search_volume": "medium"},
            {"id": "kan", "name": "Kan", "category": "vucut", "keywords": ["kan"], "search_volume": "high"},
            {"id": "gozyasi", "name": "Gözyaşı", "category": "vucut", "keywords": ["gözyaşı"], "search_volume": "medium"},
            {"id": "bas", "name": "Baş", "category": "vucut", "keywords": ["baş", "kafa"], "search_volume": "medium"},
            {"id": "yuz", "name": "Yüz", "category": "vucut", "keywords": ["yüz", "surat"], "search_volume": "medium"},
            {"id": "kalp", "name": "Kalp", "category": "vucut", "keywords": ["kalp", "yürek"], "search_volume": "medium"},
            {"id": "beyin", "name": "Beyin", "category": "vucut", "keywords": ["beyin", "akıl"], "search_volume": "low"},
            {"id": "kemik", "name": "Kemik", "category": "vucut", "keywords": ["kemik"], "search_volume": "medium"},
            {"id": "idrar", "name": "İdrar", "category": "vucut", "keywords": ["idrar", "işemek", "çiş"], "search_volume": "medium"},
            {"id": "diski", "name": "Dışkı", "category": "vucut", "keywords": ["dışkı", "kaka", "pislik"], "search_volume": "high"},
            {"id": "kusma", "name": "Kusma", "category": "vucut", "keywords": ["kusma", "kusmak"], "search_volume": "medium"},
            {"id": "hamilelik", "name": "Hamilelik", "category": "vucut", "keywords": ["hamilelik", "gebelik"], "search_volume": "high"},
            {"id": "adet_gormek", "name": "Adet Görmek", "category": "vucut", "keywords": ["adet", "regl", "aybaşı"], "search_volume": "high"},
            
            # ═══════════════════════════════════════════════════════════
            # DURUMLAR / EYLEMLER (35+)
            # ═══════════════════════════════════════════════════════════
            {"id": "olum", "name": "Ölüm", "category": "durumlar", "keywords": ["ölüm", "ölmek", "vefat"], "search_volume": "high"},
            {"id": "dogum", "name": "Doğum", "category": "durumlar", "keywords": ["doğum", "doğurmak"], "search_volume": "high"},
            {"id": "evlilik", "name": "Evlilik", "category": "durumlar", "keywords": ["evlilik", "evlenmek", "düğün", "nikah"], "search_volume": "high"},
            {"id": "bosanma", "name": "Boşanma", "category": "durumlar", "keywords": ["boşanma", "boşanmak", "ayrılık"], "search_volume": "medium"},
            {"id": "kavga", "name": "Kavga", "category": "durumlar", "keywords": ["kavga", "dövüş", "tartışma"], "search_volume": "high"},
            {"id": "kaza", "name": "Kaza", "category": "durumlar", "keywords": ["kaza", "trafik kazası"], "search_volume": "medium"},
            {"id": "hastalik", "name": "Hastalık", "category": "durumlar", "keywords": ["hastalık", "hasta olmak"], "search_volume": "medium"},
            {"id": "ucmak", "name": "Uçmak", "category": "durumlar", "keywords": ["uçmak", "uçma", "havada uçmak"], "search_volume": "high"},
            {"id": "dusmek", "name": "Düşmek", "category": "durumlar", "keywords": ["düşmek", "düşme", "yüksekten düşmek"], "search_volume": "high"},
            {"id": "yuzmek", "name": "Yüzmek", "category": "durumlar", "keywords": ["yüzmek", "yüzme"], "search_volume": "medium"},
            {"id": "bogulmak", "name": "Boğulmak", "category": "durumlar", "keywords": ["boğulmak", "boğulma"], "search_volume": "high"},
            {"id": "kosmak", "name": "Koşmak", "category": "durumlar", "keywords": ["koşmak", "koşma"], "search_volume": "medium"},
            {"id": "kacmak", "name": "Kaçmak", "category": "durumlar", "keywords": ["kaçmak", "kaçış"], "search_volume": "medium"},
            {"id": "kovalanmak", "name": "Kovalanmak", "category": "durumlar", "keywords": ["kovalanmak", "takip edilmek"], "search_volume": "high"},
            {"id": "kaybolmak", "name": "Kaybolmak", "category": "durumlar", "keywords": ["kaybolmak", "kayıp"], "search_volume": "medium"},
            {"id": "ciplaklik", "name": "Çıplaklık", "category": "durumlar", "keywords": ["çıplak", "çıplaklık"], "search_volume": "high"},
            {"id": "cinsel_iliski", "name": "Cinsel İlişki", "category": "durumlar", "keywords": ["cinsel ilişki", "seks"], "search_volume": "high"},
            {"id": "opusmek", "name": "Öpüşmek", "category": "durumlar", "keywords": ["öpüşmek", "öpmek", "öpücük"], "search_volume": "medium"},
            {"id": "sarilmak", "name": "Sarılmak", "category": "durumlar", "keywords": ["sarılmak", "kucaklaşmak"], "search_volume": "medium"},
            {"id": "aglamak", "name": "Ağlamak", "category": "durumlar", "keywords": ["ağlamak", "ağlama"], "search_volume": "high"},
            {"id": "gulmek", "name": "Gülmek", "category": "durumlar", "keywords": ["gülmek", "gülme", "kahkaha"], "search_volume": "medium"},
            {"id": "namaz_kilmak", "name": "Namaz Kılmak", "category": "durumlar", "keywords": ["namaz", "namaz kılmak"], "search_volume": "high"},
            {"id": "ezan", "name": "Ezan", "category": "durumlar", "keywords": ["ezan", "ezan sesi"], "search_volume": "medium"},
            {"id": "abdest", "name": "Abdest", "category": "durumlar", "keywords": ["abdest", "abdest almak"], "search_volume": "medium"},
            {"id": "hac", "name": "Hac", "category": "durumlar", "keywords": ["hac", "hacca gitmek", "kabe"], "search_volume": "medium"},
            {"id": "cenaze", "name": "Cenaze", "category": "durumlar", "keywords": ["cenaze", "cenaze namazı"], "search_volume": "high"},
            {"id": "sinav", "name": "Sınav", "category": "durumlar", "keywords": ["sınav", "imtihan", "test"], "search_volume": "medium"},
            {"id": "piyango", "name": "Piyango", "category": "durumlar", "keywords": ["piyango", "kazanmak"], "search_volume": "medium"},
            {"id": "hirsizlik", "name": "Hırsızlık", "category": "durumlar", "keywords": ["hırsızlık", "soygun"], "search_volume": "medium"},
            {"id": "yangin", "name": "Yangın", "category": "durumlar", "keywords": ["yangın", "yanmak"], "search_volume": "high"},
            {"id": "sarhos_olmak", "name": "Sarhoş Olmak", "category": "durumlar", "keywords": ["sarhoş", "sarhoş olmak"], "search_volume": "medium"},
            {"id": "sigara_icmek", "name": "Sigara İçmek", "category": "durumlar", "keywords": ["sigara", "sigara içmek"], "search_volume": "medium"},
            {"id": "gec_kalmak", "name": "Geç Kalmak", "category": "durumlar", "keywords": ["geç kalmak"], "search_volume": "medium"},
            {"id": "yolculuk", "name": "Yolculuk", "category": "durumlar", "keywords": ["yolculuk", "seyahat"], "search_volume": "medium"},
            {"id": "tasinmak", "name": "Taşınmak", "category": "durumlar", "keywords": ["taşınmak", "ev taşımak"], "search_volume": "low"},
            
            # ═══════════════════════════════════════════════════════════
            # DİNİ/MANEVİ (15+)
            # ═══════════════════════════════════════════════════════════
            {"id": "allah", "name": "Allah", "category": "dini", "keywords": ["allah", "tanrı"], "search_volume": "high"},
            {"id": "peygamber", "name": "Peygamber", "category": "dini", "keywords": ["peygamber", "hz. muhammed", "resulullah"], "search_volume": "high"},
            {"id": "melek", "name": "Melek", "category": "dini", "keywords": ["melek", "melekler"], "search_volume": "high"},
            {"id": "seytan", "name": "Şeytan", "category": "dini", "keywords": ["şeytan", "iblis"], "search_volume": "high"},
            {"id": "cin", "name": "Cin", "category": "dini", "keywords": ["cin", "cinler"], "search_volume": "high"},
            {"id": "kabe", "name": "Kabe", "category": "dini", "keywords": ["kabe", "beytullah"], "search_volume": "medium"},
            {"id": "cennet", "name": "Cennet", "category": "dini", "keywords": ["cennet"], "search_volume": "medium"},
            {"id": "cehennem", "name": "Cehennem", "category": "dini", "keywords": ["cehennem"], "search_volume": "medium"},
            {"id": "kiyamet", "name": "Kıyamet", "category": "dini", "keywords": ["kıyamet", "mahşer"], "search_volume": "medium"},
            {"id": "sela", "name": "Sela", "category": "dini", "keywords": ["sela", "sela sesi"], "search_volume": "medium"},
            {"id": "cami_imam", "name": "Cami ve İmam", "category": "dini", "keywords": ["cami", "imam"], "search_volume": "medium"},
            {"id": "kurban", "name": "Kurban", "category": "dini", "keywords": ["kurban", "kurban kesmek"], "search_volume": "medium"},
            {"id": "zekat", "name": "Zekat", "category": "dini", "keywords": ["zekat", "sadaka"], "search_volume": "low"},
            {"id": "oruc", "name": "Oruç", "category": "dini", "keywords": ["oruç", "oruç tutmak"], "search_volume": "medium"},
            {"id": "ramazan", "name": "Ramazan", "category": "dini", "keywords": ["ramazan", "iftar"], "search_volume": "medium"},
            
            # ═══════════════════════════════════════════════════════════
            # RENKLER (10)
            # ═══════════════════════════════════════════════════════════
            {"id": "beyaz", "name": "Beyaz Renk", "category": "renkler", "keywords": ["beyaz", "beyaz renk"], "search_volume": "medium"},
            {"id": "siyah", "name": "Siyah Renk", "category": "renkler", "keywords": ["siyah", "siyah renk", "kara"], "search_volume": "medium"},
            {"id": "kirmizi", "name": "Kırmızı Renk", "category": "renkler", "keywords": ["kırmızı", "kızıl", "al"], "search_volume": "medium"},
            {"id": "mavi", "name": "Mavi Renk", "category": "renkler", "keywords": ["mavi", "gök mavisi"], "search_volume": "low"},
            {"id": "yesil", "name": "Yeşil Renk", "category": "renkler", "keywords": ["yeşil"], "search_volume": "medium"},
            {"id": "sari", "name": "Sarı Renk", "category": "renkler", "keywords": ["sarı"], "search_volume": "low"},
            {"id": "mor", "name": "Mor Renk", "category": "renkler", "keywords": ["mor"], "search_volume": "low"},
            {"id": "turuncu", "name": "Turuncu Renk", "category": "renkler", "keywords": ["turuncu"], "search_volume": "low"},
            {"id": "pembe", "name": "Pembe Renk", "category": "renkler", "keywords": ["pembe"], "search_volume": "low"},
            {"id": "altin_rengi", "name": "Altın Rengi", "category": "renkler", "keywords": ["altın rengi", "gold"], "search_volume": "low"},
        ]
        
        return objects
        
    def generate_actions(self):
        """Eylemler listesi"""
        actions = [
            {"id": "gormek", "name": "görmek"},
            {"id": "oldurmek", "name": "öldürmek"},
            {"id": "oldurulmek", "name": "öldürülmek"},
            {"id": "kacmak", "name": "kaçmak"},
            {"id": "kovalamak", "name": "kovalamak"},
            {"id": "yakalamak", "name": "yakalamak"},
            {"id": "yemek", "name": "yemek"},
            {"id": "icmek", "name": "içmek"},
            {"id": "konusmak", "name": "konuşmak"},
            {"id": "sarilmak", "name": "sarılmak"},
            {"id": "opmek", "name": "öpmek"},
            {"id": "kavga_etmek", "name": "kavga etmek"},
            {"id": "dovmek", "name": "dövmek"},
            {"id": "dovulmek", "name": "dövülmek"},
            {"id": "aglamak", "name": "ağlamak"},
            {"id": "gulmek", "name": "gülmek"},
            {"id": "korkmak", "name": "korkmak"},
            {"id": "ucmak", "name": "uçmak"},
            {"id": "dusmek", "name": "düşmek"},
            {"id": "yuzmek", "name": "yüzmek"},
            {"id": "bogulmak", "name": "boğulmak"},
            {"id": "kosmak", "name": "koşmak"},
            {"id": "binmek", "name": "binmek"},
            {"id": "almak", "name": "almak"},
            {"id": "vermek", "name": "vermek"},
            {"id": "kaybetmek", "name": "kaybetmek"},
            {"id": "bulmak", "name": "bulmak"},
            {"id": "isirmak", "name": "ısırmak"},
            {"id": "isirilmak", "name": "ısırılmak"},
            {"id": "sokmak", "name": "sokmak"},
        ]
        return actions
        
    def save_data(self):
        """Tüm verileri kaydet"""
        
        objects = self.generate_objects()
        with open(self.data_dir / "objects.json", "w", encoding="utf-8") as f:
            json.dump({"objects": objects}, f, ensure_ascii=False, indent=2)
        print(f"✅ {len(objects)} obje kaydedildi: data/raw/objects.json")
        
        actions = self.generate_actions()
        with open(self.data_dir / "actions.json", "w", encoding="utf-8") as f:
            json.dump({"actions": actions}, f, ensure_ascii=False, indent=2)
        print(f"✅ {len(actions)} eylem kaydedildi: data/raw/actions.json")

if __name__ == "__main__":
    collector = DataCollector()
    collector.save_data()
```

### AŞAMA 4: KOMBİNASYON OLUŞTURMA

#### scripts/generate_combinations.py

```python
#!/usr/bin/env python3
"""
Obje + Eylem kombinasyonlarını oluştur
"""

import json
from pathlib import Path
import re

def turkish_slug(text):
    """Türkçe karakterleri dönüştür"""
    replacements = {
        'ı': 'i', 'ğ': 'g', 'ü': 'u', 'ş': 's', 'ö': 'o', 'ç': 'c',
        'İ': 'i', 'Ğ': 'g', 'Ü': 'u', 'Ş': 's', 'Ö': 'o', 'Ç': 'c'
    }
    text = text.lower()
    for turkish, latin in replacements.items():
        text = text.replace(turkish, latin)
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def generate_combinations():
    data_dir = Path("data/raw")
    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Verileri yükle
    with open(data_dir / "objects.json", "r", encoding="utf-8") as f:
        objects = json.load(f)["objects"]
    
    combinations = []
    
    # Her obje için ana sayfa (görmek)
    for obj in objects:
        combo = {
            "id": f"{obj['id']}_gormek",
            "object": obj,
            "action": "görmek",
            "title": f"Rüyada {obj['name']} Görmek Ne Anlama Gelir?",
            "slug": f"ruyada-{turkish_slug(obj['name'])}-gormek",
            "keywords": [
                f"rüyada {obj['name'].lower()} görmek",
                f"rüyada {obj['name'].lower()} görmek ne demek",
                f"rüyada {obj['name'].lower()} görmek neye işaret",
                f"rüyada {obj['name'].lower()}",
                f"{obj['name'].lower()} rüya tabiri",
            ],
            "search_volume": obj.get("search_volume", "medium")
        }
        combinations.append(combo)
        
        # Yüksek hacimli objeler için ekstra eylemler
        if obj.get("search_volume") == "high":
            extra_combos = [
                ("öldürmek", "oldurmek"),
                ("kaçmak", "kacmak"),
                ("yakalamak", "yakalamak"),
                ("konuşmak", "konusmak"),
                ("ısırılmak", "isirilmak"),
            ]
            for action_name, action_slug in extra_combos:
                combo = {
                    "id": f"{obj['id']}_{action_slug}",
                    "object": obj,
                    "action": action_name,
                    "title": f"Rüyada {obj['name']} {action_name.title()} Ne Anlama Gelir?",
                    "slug": f"ruyada-{turkish_slug(obj['name'])}-{action_slug}",
                    "keywords": [
                        f"rüyada {obj['name'].lower()} {action_name}",
                        f"rüyada {obj['name'].lower()} {action_name} ne demek",
                    ],
                    "search_volume": "medium"
                }
                combinations.append(combo)
    
    # Kaydet
    with open(output_dir / "combinations.json", "w", encoding="utf-8") as f:
        json.dump({
            "combinations": combinations, 
            "total": len(combinations)
        }, f, ensure_ascii=False, indent=2)
    
    print(f"✅ {len(combinations)} kombinasyon oluşturuldu: data/processed/combinations.json")
    
    # İstatistikler
    high_vol = sum(1 for c in combinations if c.get("search_volume") == "high")
    print(f"   - Yüksek hacimli: {high_vol}")
    print(f"   - Orta/Düşük hacimli: {len(combinations) - high_vol}")

if __name__ == "__main__":
    generate_combinations()
```

### AŞAMA 5: GROQ API İLE İÇERİK ÜRETİMİ

#### scripts/generate_content.py

```python
#!/usr/bin/env python3
"""
GROQ API ile içerik üretimi
Ücretsiz ve çok hızlı!

KULLANIM:
1. https://console.groq.com adresinden API key al
2. Aşağıdaki GROQ_API_KEY değişkenine yaz
3. python scripts/generate_content.py çalıştır
"""

import json
import asyncio
import aiohttp
import os
from pathlib import Path
from datetime import datetime
from tqdm import tqdm
import re
import time

# ╔════════════════════════════════════════════════════════════════════════════╗
# ║  AYARLAR - API ANAHTARINI BURAYA YAZ                                      ║
# ╚════════════════════════════════════════════════════════════════════════════╝

GROQ_API_KEY = "BURAYA_GROQ_API_ANAHTARINI_YAZ"  # gsk_xxxxx formatında

# Model seçenekleri:
# - "llama-3.1-8b-instant"    → Hızlı, ücretsiz (önerilen)
# - "llama-3.1-70b-versatile" → Daha kaliteli ama yavaş
# - "mixtral-8x7b-32768"      → Alternatif
GROQ_MODEL = "llama-3.1-8b-instant"

# Kaç sayfa üretilecek? (test için 10, sonra artır)
PAGE_LIMIT = 10  # None yaparsan tümünü üretir


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║  GROQ API CLIENT                                                          ║
# ╚════════════════════════════════════════════════════════════════════════════╝

class GroqClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.request_count = 0
        self.last_request_time = 0
        
    async def generate(self, prompt: str, temperature: float = 0.8) -> str:
        """Groq API'den içerik üret"""
        
        # Rate limiting - saniyede 1 istek (güvenli tarafta kal)
        current_time = time.time()
        time_diff = current_time - self.last_request_time
        if time_diff < 2:
            await asyncio.sleep(2 - time_diff)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": GROQ_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "Sen deneyimli bir Türkçe rüya tabircisisin. Doğal, akıcı ve bilgilendirici içerik yazarsın. Yapay zeka tarafından yazılmış gibi hissettirme, insani bir dil kullan."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            "temperature": temperature,
            "max_tokens": 2048,
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.base_url, 
                    headers=headers, 
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as resp:
                    self.last_request_time = time.time()
                    self.request_count += 1
                    
                    if resp.status == 200:
                        result = await resp.json()
                        return result["choices"][0]["message"]["content"]
                    elif resp.status == 429:
                        print("\n⚠️ Rate limit aşıldı - 60 saniye bekleniyor...")
                        await asyncio.sleep(60)
                        return await self.generate(prompt, temperature)
                    else:
                        error = await resp.text()
                        print(f"\n❌ API Hatası: {resp.status} - {error[:200]}")
                        return ""
        except asyncio.TimeoutError:
            print("\n⚠️ Timeout - tekrar deneniyor...")
            await asyncio.sleep(5)
            return await self.generate(prompt, temperature)
        except Exception as e:
            print(f"\n❌ Bağlantı hatası: {e}")
            return ""


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║  İÇERİK ÜRETİCİ                                                           ║
# ╚════════════════════════════════════════════════════════════════════════════╝

class ContentGenerator:
    def __init__(self):
        self.client = GroqClient(GROQ_API_KEY)
        self.output_dir = Path("hugo-site/content/ruya")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def get_prompt(self, combo: dict) -> str:
        """Rüya tabiri için prompt"""
        obj = combo.get("object", {})
        obj_name = obj.get("name", "")
        action = combo.get("action", "görmek")
        category = obj.get("category", "genel")
        
        return f"""Rüyada {obj_name} {action} hakkında kapsamlı bir makale yaz.

KURALLAR:
- Minimum 700 kelime yaz
- Doğal, akıcı Türkçe kullan
- ASLA madde işareti veya liste kullanma, sadece paragraflar yaz
- Her paragraf en az 3-4 cümle olsun
- H2 başlıkları için ## kullan
- Samimi ve bilgilendirici ol

İÇERİK YAPISI:

## Rüyada {obj_name} {action.title()} Ne Anlama Gelir?

Rüyada {obj_name.lower()} {action} hakkında giriş paragrafı yaz. Genel olarak ne anlama geldiğini, insanların neden bu rüyayı gördüğünü açıkla.

## İslami Kaynaklara Göre Rüyada {obj_name} Görmek

İslami rüya tabircilerine göre (İbn-i Sirin, Nablusi vb.) bu rüyanın ne anlama geldiğini detaylı açıkla. Hadislerden ve alimlerden bahsedebilirsin.

## Psikolojik Açıdan Rüyada {obj_name}

Modern psikoloji ve bilinçaltı açısından bu rüyanın ne anlama gelebileceğini açıkla. Freud, Jung gibi psikologların görüşlerine değinebilirsin.

## Rüyanın Detaylarına Göre Farklı Anlamlar

Farklı senaryoları açıkla: Büyük/küçük {obj_name.lower()}, renkli/renksiz, tek/çok, nerede görüldüğü, ne yaptığı gibi detayların rüyanın anlamını nasıl değiştirdiğini anlat.

## Sonuç

Kısa bir özet ve genel değerlendirme yap. Rüyaların kişisel olduğunu, yorumların değişebileceğini belirt.

ŞİMDİ YAZMAYI BAŞLA (sadece makale içeriğini yaz, bu talimatları tekrarlama):"""

    def create_frontmatter(self, combo: dict, content: str) -> str:
        """Hugo frontmatter oluştur"""
        obj = combo.get("object", {})
        title = combo.get("title", "")
        slug = combo.get("slug", "")
        keywords = combo.get("keywords", [])
        
        # Açıklama çıkar
        clean_content = re.sub(r'#.*?\n', '', content)
        paragraphs = [p.strip() for p in clean_content.split('\n\n') if p.strip()]
        first_para = paragraphs[0] if paragraphs else ""
        description = first_para[:155].replace('"', "'").replace('\n', ' ')
        if len(first_para) > 155:
            description += "..."
        
        return f"""---
title: "{title}"
slug: "{slug}"
date: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S+03:00')}
lastmod: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S+03:00')}
description: "{description}"
keywords: {json.dumps(keywords, ensure_ascii=False)}
categories: ["{obj.get('category', 'genel')}"]
tags: ["{obj.get('name', '')}", "rüya tabiri", "rüya yorumu"]
author: "Rüya Tabiri"
draft: false
---

"""

    async def generate_page(self, combo: dict) -> bool:
        """Tek sayfa üret"""
        slug = combo.get("slug", "unknown")
        filepath = self.output_dir / f"{slug}.md"
        
        # Zaten varsa atla
        if filepath.exists():
            return True
            
        try:
            prompt = self.get_prompt(combo)
            content = await self.client.generate(prompt)
            
            if not content or len(content) < 400:
                print(f"\n⚠️ Kısa içerik: {slug}")
                return False
            
            full_content = self.create_frontmatter(combo, content) + content
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(full_content)
            
            return True
            
        except Exception as e:
            print(f"\n❌ Hata ({slug}): {e}")
            return False

    async def generate_all(self, combinations: list, limit: int = None):
        """Tüm içerikleri üret"""
        
        # Sadece obje sayfaları (kategori hariç)
        pages = [c for c in combinations if c.get("type") != "category"]
        
        if limit:
            pages = pages[:limit]
        
        # Zaten üretilmişleri say
        existing = sum(1 for p in pages if (self.output_dir / f"{p['slug']}.md").exists())
        remaining = len(pages) - existing
        
        print(f"\n📝 Toplam: {len(pages)} sayfa")
        print(f"✅ Mevcut: {existing} sayfa")
        print(f"🔄 Üretilecek: {remaining} sayfa")
        print(f"⏱️ Tahmini süre: {remaining * 3 // 60} dakika\n")
        
        if remaining == 0:
            print("Tüm sayfalar zaten üretilmiş!")
            return
        
        success = 0
        failed = 0
        
        for combo in tqdm(pages, desc="Üretiliyor"):
            result = await self.generate_page(combo)
            if result:
                success += 1
            else:
                failed += 1
        
        print(f"\n✅ Tamamlandı!")
        print(f"   Başarılı: {success}")
        print(f"   Başarısız: {failed}")
        print(f"   Dosyalar: {self.output_dir}")


# ╔════════════════════════════════════════════════════════════════════════════╗
# ║  ANA FONKSİYON                                                            ║
# ╚════════════════════════════════════════════════════════════════════════════╝

async def main():
    # API key kontrolü
    if GROQ_API_KEY == "BURAYA_GROQ_API_ANAHTARINI_YAZ" or not GROQ_API_KEY.startswith("gsk_"):
        print("=" * 60)
        print("❌ HATA: Groq API anahtarı gerekli!")
        print("=" * 60)
        print("\n1. https://console.groq.com adresine git")
        print("2. Google/GitHub ile giriş yap")
        print("3. Sol menüden 'API Keys' tıkla")
        print("4. 'Create API Key' tıkla")
        print("5. Anahtarı kopyala (gsk_xxx formatında)")
        print("6. Bu dosyada GROQ_API_KEY değişkenine yapıştır")
        print("\n" + "=" * 60)
        return
    
    # Kombinasyonları yükle
    combo_file = Path("data/processed/combinations.json")
    
    if not combo_file.exists():
        print("❌ Kombinasyon dosyası bulunamadı!")
        print("   Önce şu komutları çalıştır:")
        print("   python scripts/collect_data.py")
        print("   python scripts/generate_combinations.py")
        return
    
    with open(combo_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        combinations = data["combinations"]
    
    print("=" * 60)
    print("🌙 RÜYA TABİRLERİ İÇERİK ÜRETİCİ")
    print("=" * 60)
    print(f"Model: {GROQ_MODEL}")
    print(f"Limit: {PAGE_LIMIT if PAGE_LIMIT else 'Tümü'}")
    
    generator = ContentGenerator()
    await generator.generate_all(combinations, limit=PAGE_LIMIT)

if __name__ == "__main__":
    asyncio.run(main())
```

### AŞAMA 6: HUGO SITE YAPISI

#### hugo-site/config.toml

```toml
baseURL = "https://ruyatabiri.com/"
languageCode = "tr"
title = "Rüya Tabiri - Rüya Yorumları ve Anlamları"

# SEO
enableRobotsTXT = true
canonifyURLs = true

[params]
  description = "Rüyalarınızın anlamını öğrenin. İslami ve psikolojik rüya tabirleri, binlerce detaylı rüya yorumu."
  author = "Rüya Tabiri"
  
[markup]
  [markup.goldmark]
    [markup.goldmark.renderer]
      unsafe = true

[sitemap]
  changefreq = "weekly"
  priority = 0.5
  filename = "sitemap.xml"

[outputs]
  home = ["HTML", "RSS", "JSON"]
  section = ["HTML", "RSS"]
  page = ["HTML"]
  
[taxonomies]
  category = "categories"
  tag = "tags"

[permalinks]
  ruya = "/ruya/:slug/"
  
[minify]
  minifyOutput = true

[pagination]
  pagerSize = 20
```

#### hugo-site/layouts/_default/baseof.html

```html
<!DOCTYPE html>
<html lang="tr">
<head>
    {{- partial "head.html" . -}}
</head>
<body>
    {{- partial "header.html" . -}}
    
    <main class="container">
        {{- block "main" . }}{{- end }}
    </main>
    
    {{- partial "footer.html" . -}}
    
    <script src="/js/main.js" defer></script>
</body>
</html>
```

#### hugo-site/layouts/partials/head.html

```html
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>{{ if .IsHome }}{{ .Site.Title }}{{ else }}{{ .Title }} | {{ .Site.Title }}{{ end }}</title>

<meta name="description" content="{{ with .Description }}{{ . }}{{ else }}{{ .Site.Params.description }}{{ end }}">
<meta name="keywords" content="{{ with .Params.keywords }}{{ delimit . ", " }}{{ end }}">
<meta name="author" content="{{ .Site.Params.author }}">
<meta name="robots" content="index, follow">

<link rel="canonical" href="{{ .Permalink }}">

<meta property="og:title" content="{{ .Title }}">
<meta property="og:description" content="{{ with .Description }}{{ . }}{{ else }}{{ .Site.Params.description }}{{ end }}">
<meta property="og:type" content="{{ if .IsPage }}article{{ else }}website{{ end }}">
<meta property="og:url" content="{{ .Permalink }}">
<meta property="og:site_name" content="{{ .Site.Title }}">
<meta property="og:locale" content="tr_TR">

<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{{ .Title }}">
<meta name="twitter:description" content="{{ with .Description }}{{ . }}{{ else }}{{ .Site.Params.description }}{{ end }}">

{{- partial "schema.html" . -}}

<link rel="stylesheet" href="/css/style.css">
```

#### hugo-site/layouts/partials/schema.html

```html
{{ if .IsPage }}
<script type="application/ld+json">
{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{{ .Title }}",
    "description": "{{ .Description }}",
    "datePublished": "{{ .Date.Format "2006-01-02T15:04:05Z07:00" }}",
    "dateModified": "{{ .Lastmod.Format "2006-01-02T15:04:05Z07:00" }}",
    "author": {
        "@type": "Organization",
        "name": "{{ .Site.Params.author }}"
    },
    "publisher": {
        "@type": "Organization",
        "name": "{{ .Site.Title }}"
    },
    "mainEntityOfPage": {
        "@type": "WebPage",
        "@id": "{{ .Permalink }}"
    }
}
</script>
{{ else if .IsHome }}
<script type="application/ld+json">
{
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "{{ .Site.Title }}",
    "url": "{{ .Site.BaseURL }}",
    "description": "{{ .Site.Params.description }}",
    "potentialAction": {
        "@type": "SearchAction",
        "target": "{{ .Site.BaseURL }}arama?q={search_term_string}",
        "query-input": "required name=search_term_string"
    }
}
</script>
{{ end }}
```

#### hugo-site/layouts/partials/header.html

```html
<header class="header">
    <nav class="nav container">
        <a href="/" class="logo">🌙 Rüya Tabiri</a>
        
        <ul class="nav-links">
            <li><a href="/ruya/">Tüm Tabirler</a></li>
            <li><a href="/categories/">Kategoriler</a></li>
            <li><a href="/hakkimizda/">Hakkımızda</a></li>
        </ul>
    </nav>
</header>
```

#### hugo-site/layouts/partials/footer.html

```html
<footer class="footer">
    <div class="container">
        <div class="footer-content">
            <div class="footer-section">
                <h3>🌙 Rüya Tabiri</h3>
                <p>Rüyalarınızın anlamını öğrenin. İslami ve psikolojik rüya tabirleri, binlerce detaylı rüya yorumu.</p>
            </div>
            
            <div class="footer-section">
                <h4>Kategoriler</h4>
                <ul>
                    <li><a href="/categories/hayvanlar/">Hayvanlar</a></li>
                    <li><a href="/categories/insanlar/">İnsanlar</a></li>
                    <li><a href="/categories/nesneler/">Nesneler</a></li>
                    <li><a href="/categories/durumlar/">Durumlar</a></li>
                    <li><a href="/categories/doga/">Doğa</a></li>
                </ul>
            </div>
            
            <div class="footer-section">
                <h4>Popüler Aramalar</h4>
                <ul>
                    <li><a href="/ruya/ruyada-yilan-gormek/">Rüyada Yılan Görmek</a></li>
                    <li><a href="/ruya/ruyada-su-gormek/">Rüyada Su Görmek</a></li>
                    <li><a href="/ruya/ruyada-olu-gormek/">Rüyada Ölü Görmek</a></li>
                    <li><a href="/ruya/ruyada-bebek-gormek/">Rüyada Bebek Görmek</a></li>
                    <li><a href="/ruya/ruyada-altin-gormek/">Rüyada Altın Görmek</a></li>
                </ul>
            </div>
        </div>
        
        <div class="footer-bottom">
            <p>&copy; {{ now.Year }} Rüya Tabiri. Tüm hakları saklıdır.</p>
            <p>
                <a href="/gizlilik-politikasi/">Gizlilik Politikası</a> | 
                <a href="/iletisim/">İletişim</a>
            </p>
        </div>
    </div>
</footer>
```

#### hugo-site/layouts/_default/single.html

```html
{{ define "main" }}
<article class="article">
    <header class="article-header">
        <h1>{{ .Title }}</h1>
        <div class="article-meta">
            <time datetime="{{ .Date.Format "2006-01-02" }}">
                {{ .Date.Format "2 January 2006" }}
            </time>
            {{ with .Params.categories }}
            <span class="category">
                {{ range . }}
                <a href="/categories/{{ . | urlize }}/">{{ . }}</a>
                {{ end }}
            </span>
            {{ end }}
        </div>
    </header>
    
    <div class="article-content">
        {{ .Content }}
    </div>
    
    <aside class="related-posts">
        <h3>İlgili Rüya Tabirleri</h3>
        {{ $related := .Site.RegularPages.Related . | first 6 }}
        {{ with $related }}
        <div class="related-grid">
            {{ range . }}
            <a href="{{ .Permalink }}" class="related-item">{{ .Title }}</a>
            {{ end }}
        </div>
        {{ end }}
    </aside>
    
    <footer class="article-footer">
        {{ with .Params.tags }}
        <div class="tags">
            <strong>Etiketler:</strong>
            {{ range . }}
            <a href="/tags/{{ . | urlize }}/" class="tag">{{ . }}</a>
            {{ end }}
        </div>
        {{ end }}
    </footer>
</article>
{{ end }}
```

#### hugo-site/layouts/_default/list.html

```html
{{ define "main" }}
<div class="list-page">
    <h1>{{ .Title }}</h1>
    
    {{ with .Content }}
    <div class="list-intro">{{ . }}</div>
    {{ end }}
    
    <div class="list-grid">
        {{ range .Paginator.Pages }}
        <article class="list-item">
            <h2><a href="{{ .Permalink }}">{{ .Title }}</a></h2>
            <p>{{ .Description | truncate 120 }}</p>
        </article>
        {{ end }}
    </div>
    
    {{ template "_internal/pagination.html" . }}
</div>
{{ end }}
```

#### hugo-site/layouts/ruya/single.html

```html
{{ define "main" }}
<article class="article ruya-article">
    <header class="article-header">
        <nav class="breadcrumb">
            <a href="/">Ana Sayfa</a> &rsaquo;
            <a href="/ruya/">Rüya Tabirleri</a> &rsaquo;
            {{ with .Params.categories }}
                {{ range first 1 . }}
                <a href="/categories/{{ . | urlize }}/">{{ . | title }}</a> &rsaquo;
                {{ end }}
            {{ end }}
            <span>{{ .Title }}</span>
        </nav>
        
        <h1>{{ .Title }}</h1>
        
        <div class="article-meta">
            <time datetime="{{ .Date.Format "2006-01-02" }}">
                Son güncelleme: {{ .Lastmod.Format "2 January 2006" }}
            </time>
        </div>
    </header>
    
    <div class="article-content">
        {{ .Content }}
    </div>
    
    <aside class="related-posts">
        <h3>Benzer Rüya Tabirleri</h3>
        {{ $related := .Site.RegularPages.Related . | first 8 }}
        {{ with $related }}
        <div class="related-grid">
            {{ range . }}
            <a href="{{ .Permalink }}" class="related-item">{{ .Title }}</a>
            {{ end }}
        </div>
        {{ end }}
    </aside>
    
    <footer class="article-footer">
        {{ with .Params.tags }}
        <div class="tags">
            {{ range . }}
            <a href="/tags/{{ . | urlize }}/" class="tag">{{ . }}</a>
            {{ end }}
        </div>
        {{ end }}
    </footer>
</article>
{{ end }}
```

#### hugo-site/static/css/style.css

```css
*, *::before, *::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

:root {
    --primary: #6366f1;
    --primary-dark: #4f46e5;
    --bg: #ffffff;
    --bg-secondary: #f8fafc;
    --text: #1e293b;
    --text-light: #64748b;
    --border: #e2e8f0;
    --radius: 8px;
    --shadow: 0 1px 3px rgba(0,0,0,0.1);
}

html {
    font-size: 16px;
    scroll-behavior: smooth;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.7;
    color: var(--text);
    background: var(--bg);
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1rem;
}

/* Header */
.header {
    background: var(--bg);
    border-bottom: 1px solid var(--border);
    position: sticky;
    top: 0;
    z-index: 100;
}

.nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem;
    gap: 2rem;
}

.logo {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--primary);
    text-decoration: none;
}

.nav-links {
    display: flex;
    list-style: none;
    gap: 1.5rem;
}

.nav-links a {
    color: var(--text);
    text-decoration: none;
    font-weight: 500;
    transition: color 0.2s;
}

.nav-links a:hover {
    color: var(--primary);
}

/* Breadcrumb */
.breadcrumb {
    font-size: 0.9rem;
    color: var(--text-light);
    margin-bottom: 1rem;
}

.breadcrumb a {
    color: var(--primary);
    text-decoration: none;
}

.breadcrumb a:hover {
    text-decoration: underline;
}

/* Article */
.article {
    max-width: 800px;
    margin: 2rem auto;
    padding: 0 1rem;
}

.article-header {
    margin-bottom: 2rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--border);
}

.article-header h1 {
    font-size: 2rem;
    line-height: 1.3;
    margin-bottom: 0.5rem;
    color: var(--text);
}

.article-meta {
    color: var(--text-light);
    font-size: 0.9rem;
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
}

.article-content {
    font-size: 1.1rem;
}

.article-content h2 {
    font-size: 1.5rem;
    margin: 2rem 0 1rem;
    color: var(--primary-dark);
    border-bottom: 2px solid var(--border);
    padding-bottom: 0.5rem;
}

.article-content h3 {
    font-size: 1.25rem;
    margin: 1.5rem 0 0.75rem;
}

.article-content p {
    margin-bottom: 1.25rem;
}

/* Related Posts */
.related-posts {
    margin-top: 3rem;
    padding-top: 2rem;
    border-top: 1px solid var(--border);
}

.related-posts h3 {
    margin-bottom: 1rem;
    color: var(--text);
}

.related-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 0.75rem;
}

.related-item {
    display: block;
    padding: 0.75rem 1rem;
    background: var(--bg-secondary);
    border-radius: var(--radius);
    color: var(--text);
    text-decoration: none;
    font-size: 0.95rem;
    transition: all 0.2s;
}

.related-item:hover {
    background: var(--primary);
    color: white;
}

/* Tags */
.tags {
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px solid var(--border);
}

.tag {
    display: inline-block;
    background: var(--bg-secondary);
    color: var(--text-light);
    padding: 0.25rem 0.75rem;
    border-radius: 999px;
    font-size: 0.85rem;
    text-decoration: none;
    margin: 0.25rem;
    transition: all 0.2s;
}

.tag:hover {
    background: var(--primary);
    color: white;
}

/* List Page */
.list-page {
    padding: 2rem 1rem;
    max-width: 1200px;
    margin: 0 auto;
}

.list-page h1 {
    text-align: center;
    margin-bottom: 2rem;
}

.list-intro {
    max-width: 700px;
    margin: 0 auto 2rem;
    text-align: center;
    color: var(--text-light);
}

.list-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1.5rem;
}

.list-item {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
    transition: box-shadow 0.2s;
}

.list-item:hover {
    box-shadow: var(--shadow);
}

.list-item h2 {
    font-size: 1.1rem;
    margin-bottom: 0.5rem;
}

.list-item h2 a {
    color: var(--text);
    text-decoration: none;
}

.list-item h2 a:hover {
    color: var(--primary);
}

.list-item p {
    color: var(--text-light);
    font-size: 0.95rem;
}

/* Footer */
.footer {
    background: var(--bg-secondary);
    border-top: 1px solid var(--border);
    margin-top: 4rem;
    padding: 3rem 1rem 1rem;
}

.footer-content {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 2rem;
    margin-bottom: 2rem;
    max-width: 1200px;
    margin-left: auto;
    margin-right: auto;
}

.footer-section h3, .footer-section h4 {
    margin-bottom: 1rem;
}

.footer-section ul {
    list-style: none;
}

.footer-section li {
    margin-bottom: 0.5rem;
}

.footer-section a {
    color: var(--text-light);
    text-decoration: none;
}

.footer-section a:hover {
    color: var(--primary);
}

.footer-bottom {
    text-align: center;
    padding-top: 2rem;
    border-top: 1px solid var(--border);
    color: var(--text-light);
    font-size: 0.9rem;
    max-width: 1200px;
    margin: 0 auto;
}

/* Pagination */
.pagination {
    display: flex;
    justify-content: center;
    gap: 0.5rem;
    margin-top: 2rem;
    flex-wrap: wrap;
}

.pagination a, .pagination span {
    padding: 0.5rem 1rem;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    text-decoration: none;
    color: var(--text);
}

.pagination a:hover {
    background: var(--primary);
    color: white;
    border-color: var(--primary);
}

.pagination .active {
    background: var(--primary);
    color: white;
    border-color: var(--primary);
}

/* Responsive */
@media (max-width: 768px) {
    .nav {
        flex-wrap: wrap;
    }
    
    .nav-links {
        order: 3;
        width: 100%;
        justify-content: center;
        margin-top: 1rem;
        gap: 1rem;
    }
    
    .article-header h1 {
        font-size: 1.5rem;
    }
    
    .article-content {
        font-size: 1rem;
    }
    
    .related-grid {
        grid-template-columns: 1fr;
    }
}
```

#### hugo-site/static/js/main.js

```javascript
// Lazy loading
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('img[data-src]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    }
});

// Smooth scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// Reading progress
const article = document.querySelector('.article-content');
if (article) {
    const progressBar = document.createElement('div');
    progressBar.style.cssText = 'position:fixed;top:0;left:0;height:3px;background:var(--primary);z-index:9999;transition:width 0.1s;width:0';
    document.body.prepend(progressBar);
    
    window.addEventListener('scroll', () => {
        const rect = article.getBoundingClientRect();
        const progress = Math.min(100, Math.max(0, 
            ((-rect.top) / (rect.height - window.innerHeight)) * 100
        ));
        progressBar.style.width = progress + '%';
    });
}
```

#### hugo-site/content/_index.md

```markdown
---
title: "Rüya Tabiri - Rüya Yorumları ve Anlamları"
description: "Rüyalarınızın anlamını öğrenin. İslami ve psikolojik rüya tabirleri, binlerce detaylı rüya yorumu."
---

# Rüya Tabiri

Rüyalarınızın anlamını merak mı ediyorsunuz? Sitemizde binlerce rüya tabiri ve yorumu bulabilirsiniz. İslami kaynaklara, psikolojik yorumlara ve geleneksel tabirlere göre rüyalarınızı yorumlayın.

## Popüler Rüya Tabirleri

En çok aranan rüya tabirleri: yılan görmek, su görmek, ölü görmek, bebek görmek, altın görmek, diş düşmesi, uçmak, düşmek ve daha fazlası.

## Kategorilere Göre Rüyalar

Rüyalarınızı kategorilere göre arayabilirsiniz: hayvanlar, insanlar, nesneler, mekanlar, durumlar, doğa ve dini semboller.
```

#### hugo-site/content/hakkimizda.md

```markdown
---
title: "Hakkımızda"
description: "Rüya Tabiri sitesi hakkında bilgi"
slug: "hakkimizda"
---

# Hakkımızda

Rüya Tabiri olarak, rüyalarınızın anlamını en doğru şekilde yorumlamanıza yardımcı olmayı amaçlıyoruz.

## Kaynaklarımız

Sitemizdeki rüya tabirleri, farklı kaynaklardan derlenmektedir:

**İslami Kaynaklar:** İbn-i Sirin, Nablusi ve diğer İslam alimlerinin rüya tabiri eserleri

**Psikolojik Yaklaşım:** Freud, Jung ve modern psikoloji araştırmaları

**Geleneksel Tabirler:** Yüzyıllardır aktarılan halk tabirleri

## Önemli Not

Rüya tabirleri genel yorumlardır. Her rüya kişisel deneyimlerden etkilenir ve farklı anlamlar taşıyabilir. Sitemizdeki bilgiler yalnızca bilgilendirme amaçlıdır.
```

#### hugo-site/content/gizlilik-politikasi.md

```markdown
---
title: "Gizlilik Politikası"
description: "Rüya Tabiri sitesi gizlilik politikası"
slug: "gizlilik-politikasi"
---

# Gizlilik Politikası

Bu gizlilik politikası, sitemizi ziyaret ettiğinizde hangi bilgilerin toplandığını açıklar.

## Toplanan Bilgiler

Sitemiz, Google Analytics aracılığıyla anonim ziyaretçi istatistikleri toplar. Kişisel bilgileriniz toplanmaz veya saklanmaz.

## Çerezler

Sitemiz, deneyiminizi iyileştirmek için çerezler kullanabilir. Tarayıcı ayarlarınızdan çerezleri devre dışı bırakabilirsiniz.

## Üçüncü Taraf Hizmetler

Sitemizde Google AdSense reklamları gösterilebilir. Google'ın gizlilik politikası için Google'ın web sitesini ziyaret edin.

## İletişim

Sorularınız için bizimle iletişime geçebilirsiniz.
```

### AŞAMA 7: ÇALIŞTIRMA TALİMATLARI

Tüm dosyaları oluşturduktan sonra Windows CMD'de şu komutları çalıştır:

```cmd
REM 1. Proje dizinine git
cd %USERPROFILE%\Desktop\ruya-sitesi

REM 2. Python paketlerini kur
pip install -r requirements.txt

REM 3. Veri topla
python scripts/collect_data.py

REM 4. Kombinasyonları oluştur
python scripts/generate_combinations.py

REM 5. generate_content.py dosyasında GROQ_API_KEY'i değiştir!
REM    Notepad ile aç: notepad scripts\generate_content.py
REM    GROQ_API_KEY = "BURAYA_GROQ_API_ANAHTARINI_YAZ" satırını bul
REM    Kendi API anahtarını yapıştır

REM 6. İçerik üret (ilk test - 10 sayfa)
python scripts/generate_content.py

REM 7. Test başarılıysa, PAGE_LIMIT değerini artır veya None yap
REM    Sonra tekrar çalıştır: python scripts/generate_content.py

REM 8. Hugo ile siteyi build et
cd hugo-site
hugo

REM 9. Lokalde test et
hugo server
REM Tarayıcıda http://localhost:1313 aç
```

## ÖNEMLİ KONTROL LİSTESİ

1. ✅ Python 3.10+ kurulu mu?
2. ✅ Hugo kurulu mu?
3. ✅ Groq API anahtarı alındı mı? (https://console.groq.com)
4. ✅ API anahtarı generate_content.py dosyasına yazıldı mı?
5. ✅ requirements.txt paketleri kuruldu mu?

## SORUN GİDERME

**"GROQ_API_KEY gerekli" hatası:**
- generate_content.py dosyasını aç
- GROQ_API_KEY değişkenine API anahtarını yaz (gsk_xxx formatında)

**"Kombinasyon dosyası bulunamadı" hatası:**
- Önce collect_data.py çalıştır
- Sonra generate_combinations.py çalıştır

**"Rate limit" uyarısı:**
- Normal, script otomatik bekleyip devam edecek

**Hugo "command not found" hatası:**
- Hugo'nun PATH'e eklendiğinden emin ol
- Yeni CMD penceresi aç

## DOSYA OLUŞTURMA SIRASI

1. Klasör yapısı
2. requirements.txt
3. scripts/collect_data.py
4. scripts/generate_combinations.py
5. scripts/generate_content.py (API KEY'i değiştir!)
6. hugo-site/config.toml
7. hugo-site/layouts/ altındaki tüm HTML dosyaları
8. hugo-site/static/css/style.css
9. hugo-site/static/js/main.js
10. hugo-site/content/_index.md
11. hugo-site/content/hakkimizda.md
12. hugo-site/content/gizlilik-politikasi.md
