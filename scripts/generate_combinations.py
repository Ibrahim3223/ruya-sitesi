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
