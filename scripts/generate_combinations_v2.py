#!/usr/bin/env python3
"""
Genisletilmis Kombinasyon Ureticisi
5000+ sayfa icin obje + eylem + niteleyici kombinasyonlari
"""

import json
from pathlib import Path
import re

def turkish_slug(text):
    """Turkce karakterleri donustur"""
    replacements = {
        'ı': 'i', 'ğ': 'g', 'ü': 'u', 'ş': 's', 'ö': 'o', 'ç': 'c',
        'İ': 'i', 'Ğ': 'g', 'Ü': 'u', 'Ş': 's', 'Ö': 'o', 'Ç': 'c',
        ' ': '-'
    }
    text = text.lower()
    for turkish, latin in replacements.items():
        text = text.replace(turkish, latin)
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

# Eylemler ve hangi kategorilere uygulanacagi
ACTIONS = {
    # Eylem: (slug, uygulanacak kategoriler - None = hepsi)
    "görmek": ("gormek", None),
    "öldürmek": ("oldurmek", ["hayvanlar", "insanlar"]),
    "kaçmak": ("kacmak", ["hayvanlar", "insanlar", "durumlar"]),
    "kovalamak": ("kovalamak", ["hayvanlar", "insanlar"]),
    "yakalamak": ("yakalamak", ["hayvanlar", "insanlar", "nesneler"]),
    "konuşmak": ("konusmak", ["hayvanlar", "insanlar", "dini"]),
    "ısırılmak": ("isirilmak", ["hayvanlar"]),
    "yemek": ("yemek", ["yiyecekler", "hayvanlar"]),
    "içmek": ("icmek", ["yiyecekler", "doga"]),
    "almak": ("almak", ["nesneler", "yiyecekler"]),
    "vermek": ("vermek", ["nesneler", "yiyecekler"]),
    "kaybetmek": ("kaybetmek", ["nesneler", "insanlar"]),
    "bulmak": ("bulmak", ["nesneler", "insanlar", "hayvanlar"]),
    "binmek": ("binmek", ["hayvanlar", "nesneler"]),
    "düşmek": ("dusmek", ["mekanlar", "doga"]),
    "yüzmek": ("yuzmek", ["doga"]),
    "satın almak": ("satin-almak", ["nesneler", "hayvanlar"]),
    "hediye etmek": ("hediye-etmek", ["nesneler"]),
    "kırmak": ("kirmak", ["nesneler"]),
    "tamir etmek": ("tamir-etmek", ["nesneler"]),
    "temizlemek": ("temizlemek", ["nesneler", "mekanlar", "vucut"]),
    "boyamak": ("boyamak", ["nesneler", "mekanlar"]),
    "giymek": ("giymek", ["nesneler"]),
    "çıkarmak": ("cikarmak", ["nesneler", "vucut"]),
    "takmak": ("takmak", ["nesneler"]),
    "okumak": ("okumak", ["nesneler", "dini"]),
}

# Niteleyiciler (renkler, boyutlar vs.) - opsiyonel genisleme icin
MODIFIERS = {
    "renkler": [
        ("beyaz", "beyaz"),
        ("siyah", "siyah"),
        ("kırmızı", "kirmizi"),
        ("yeşil", "yesil"),
        ("mavi", "mavi"),
        ("sarı", "sari"),
        ("kahverengi", "kahverengi"),
        ("gri", "gri"),
        ("altın", "altin"),
    ],
    "boyutlar": [
        ("büyük", "buyuk"),
        ("küçük", "kucuk"),
        ("dev", "dev"),
        ("iri", "iri"),
        ("minik", "minik"),
    ],
    "miktar": [
        ("çok", "cok"),
        ("sürü", "suru"),
        ("iki", "iki"),
        ("üç", "uc"),
    ],
    "durumlar": [
        ("ölü", "olu"),
        ("yaralı", "yarali"),
        ("hasta", "hasta"),
        ("uyuyan", "uyuyan"),
        ("koşan", "kosan"),
        ("uçan", "ucan"),
        ("yavru", "yavru"),
    ],
    "mekanlar": [
        ("evde", "evde"),
        ("yolda", "yolda"),
        ("suda", "suda"),
        ("bahçede", "bahcede"),
        ("yatakta", "yatakta"),
    ]
}

def should_apply_action(obj_category, action_categories):
    """Eylemin bu kategoriye uygulanip uygulanmayacagini kontrol et"""
    if action_categories is None:
        return True
    return obj_category in action_categories

def generate_combinations():
    data_dir = Path("data/raw")
    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Verileri yukle
    with open(data_dir / "objects.json", "r", encoding="utf-8") as f:
        objects = json.load(f)["objects"]

    combinations = []
    seen_slugs = set()  # Duplicate onleme

    print(f"[i] {len(objects)} obje yuklendi")
    print(f"[i] {len(ACTIONS)} eylem tanimli")

    # Her obje icin kombinasyonlar olustur
    for obj in objects:
        obj_category = obj.get("category", "genel")
        obj_name = obj["name"]
        obj_id = obj["id"]
        search_volume = obj.get("search_volume", "medium")

        for action_name, (action_slug, action_categories) in ACTIONS.items():
            # Bu eylem bu kategoriye uygulanabilir mi?
            if not should_apply_action(obj_category, action_categories):
                continue

            # Slug olustur
            slug = f"ruyada-{turkish_slug(obj_name)}-{action_slug}"

            # Duplicate kontrolu
            if slug in seen_slugs:
                continue
            seen_slugs.add(slug)

            # Baslik olustur
            if action_name == "görmek":
                title = f"Rüyada {obj_name} Görmek Ne Anlama Gelir?"
            else:
                title = f"Rüyada {obj_name} {action_name.title()} Ne Anlama Gelir?"

            combo = {
                "id": f"{obj_id}_{action_slug}",
                "object": obj,
                "action": action_name,
                "title": title,
                "slug": slug,
                "keywords": [
                    f"rüyada {obj_name.lower()} {action_name}",
                    f"rüyada {obj_name.lower()} {action_name} ne demek",
                    f"rüyada {obj_name.lower()}",
                    f"{obj_name.lower()} rüya tabiri",
                ],
                "search_volume": search_volume if action_name == "görmek" else "medium",
                "type": "page"
            }
            combinations.append(combo)

    # Renk + Obje kombinasyonlari (populer objeler icin)
    popular_objects = [obj for obj in objects if obj.get("search_volume") == "high"]
    medium_objects = [obj for obj in objects if obj.get("search_volume") == "medium"]

    # Yuksek hacimli objeler icin tum renkler
    for obj in popular_objects:
        obj_name = obj["name"]
        obj_id = obj["id"]

        for color_name, color_slug in MODIFIERS["renkler"]:
            slug = f"ruyada-{color_slug}-{turkish_slug(obj_name)}-gormek"

            if slug in seen_slugs:
                continue
            seen_slugs.add(slug)

            combo = {
                "id": f"{color_slug}_{obj_id}_gormek",
                "object": obj,
                "action": "görmek",
                "modifier": color_name,
                "title": f"Rüyada {color_name.title()} {obj_name} Görmek Ne Anlama Gelir?",
                "slug": slug,
                "keywords": [
                    f"rüyada {color_name} {obj_name.lower()} görmek",
                    f"rüyada {color_name} {obj_name.lower()}",
                    f"{color_name} {obj_name.lower()} rüya tabiri",
                ],
                "search_volume": "medium",
                "type": "page"
            }
            combinations.append(combo)

    # Orta hacimli objeler icin bazi renkler
    for obj in medium_objects[:60]:
        obj_name = obj["name"]
        obj_id = obj["id"]

        for color_name, color_slug in MODIFIERS["renkler"][:4]:  # Sadece ilk 4 renk
            slug = f"ruyada-{color_slug}-{turkish_slug(obj_name)}-gormek"

            if slug in seen_slugs:
                continue
            seen_slugs.add(slug)

            combo = {
                "id": f"{color_slug}_{obj_id}_gormek",
                "object": obj,
                "action": "görmek",
                "modifier": color_name,
                "title": f"Rüyada {color_name.title()} {obj_name} Görmek Ne Anlama Gelir?",
                "slug": slug,
                "keywords": [
                    f"rüyada {color_name} {obj_name.lower()} görmek",
                    f"rüyada {color_name} {obj_name.lower()}",
                ],
                "search_volume": "low",
                "type": "page"
            }
            combinations.append(combo)

    # Hayvanlar icin tum boyutlar ve durumlar
    animal_objects = [obj for obj in objects if obj.get("category") == "hayvanlar"]

    for obj in animal_objects:
        obj_name = obj["name"]
        obj_id = obj["id"]

        # Boyutlar
        for size_name, size_slug in MODIFIERS["boyutlar"]:
            slug = f"ruyada-{size_slug}-{turkish_slug(obj_name)}-gormek"

            if slug in seen_slugs:
                continue
            seen_slugs.add(slug)

            combo = {
                "id": f"{size_slug}_{obj_id}_gormek",
                "object": obj,
                "action": "görmek",
                "modifier": size_name,
                "title": f"Rüyada {size_name.title()} {obj_name} Görmek Ne Anlama Gelir?",
                "slug": slug,
                "keywords": [
                    f"rüyada {size_name} {obj_name.lower()} görmek",
                    f"rüyada {size_name} {obj_name.lower()}",
                ],
                "search_volume": "low",
                "type": "page"
            }
            combinations.append(combo)

        # Durumlar (olu, yarali vs.)
        for state_name, state_slug in MODIFIERS["durumlar"]:
            slug = f"ruyada-{state_slug}-{turkish_slug(obj_name)}-gormek"

            if slug in seen_slugs:
                continue
            seen_slugs.add(slug)

            combo = {
                "id": f"{state_slug}_{obj_id}_gormek",
                "object": obj,
                "action": "görmek",
                "modifier": state_name,
                "title": f"Rüyada {state_name.title()} {obj_name} Görmek Ne Anlama Gelir?",
                "slug": slug,
                "keywords": [
                    f"rüyada {state_name} {obj_name.lower()} görmek",
                    f"rüyada {state_name} {obj_name.lower()}",
                ],
                "search_volume": "low",
                "type": "page"
            }
            combinations.append(combo)

        # Miktarlar
        for amount_name, amount_slug in MODIFIERS["miktar"]:
            slug = f"ruyada-{amount_slug}-{turkish_slug(obj_name)}-gormek"

            if slug in seen_slugs:
                continue
            seen_slugs.add(slug)

            combo = {
                "id": f"{amount_slug}_{obj_id}_gormek",
                "object": obj,
                "action": "görmek",
                "modifier": amount_name,
                "title": f"Rüyada {amount_name.title()} {obj_name} Görmek Ne Anlama Gelir?",
                "slug": slug,
                "keywords": [
                    f"rüyada {amount_name} {obj_name.lower()} görmek",
                    f"rüyada {obj_name.lower()}lar görmek",
                ],
                "search_volume": "low",
                "type": "page"
            }
            combinations.append(combo)

    # Insanlar icin durumlar
    people_objects = [obj for obj in objects if obj.get("category") == "insanlar"]

    for obj in people_objects:
        obj_name = obj["name"]
        obj_id = obj["id"]

        # Durumlar (olu haric - zaten var)
        for state_name, state_slug in [("ağlayan", "aglayan"), ("gülen", "gulen"), ("kızgın", "kizgin"), ("mutlu", "mutlu"), ("üzgün", "uzgun")]:
            slug = f"ruyada-{state_slug}-{turkish_slug(obj_name)}-gormek"

            if slug in seen_slugs:
                continue
            seen_slugs.add(slug)

            combo = {
                "id": f"{state_slug}_{obj_id}_gormek",
                "object": obj,
                "action": "görmek",
                "modifier": state_name,
                "title": f"Rüyada {state_name.title()} {obj_name} Görmek Ne Anlama Gelir?",
                "slug": slug,
                "keywords": [
                    f"rüyada {state_name} {obj_name.lower()} görmek",
                ],
                "search_volume": "low",
                "type": "page"
            }
            combinations.append(combo)

    # Mekan bazli kombinasyonlar (populer objeler)
    for obj in popular_objects[:40]:
        obj_name = obj["name"]
        obj_id = obj["id"]
        obj_cat = obj.get("category", "")

        # Sadece hayvanlar ve insanlar icin mekan kombinasyonlari
        if obj_cat not in ["hayvanlar", "insanlar"]:
            continue

        for place_name, place_slug in MODIFIERS["mekanlar"]:
            slug = f"ruyada-{place_slug}-{turkish_slug(obj_name)}-gormek"

            if slug in seen_slugs:
                continue
            seen_slugs.add(slug)

            combo = {
                "id": f"{place_slug}_{obj_id}_gormek",
                "object": obj,
                "action": "görmek",
                "modifier": place_name,
                "title": f"Rüyada {place_name.title()} {obj_name} Görmek Ne Anlama Gelir?",
                "slug": slug,
                "keywords": [
                    f"rüyada {place_name} {obj_name.lower()} görmek",
                ],
                "search_volume": "low",
                "type": "page"
            }
            combinations.append(combo)

    # Kaydet
    with open(output_dir / "combinations.json", "w", encoding="utf-8") as f:
        json.dump({
            "combinations": combinations,
            "total": len(combinations)
        }, f, ensure_ascii=False, indent=2)

    print(f"\n[OK] {len(combinations)} kombinasyon olusturuldu!")
    print(f"     Dosya: data/processed/combinations.json")

    # Istatistikler
    by_type = {}
    for c in combinations:
        vol = c.get("search_volume", "medium")
        by_type[vol] = by_type.get(vol, 0) + 1

    print(f"\n[i] Dagilim:")
    for vol, count in sorted(by_type.items()):
        print(f"    - {vol}: {count}")

if __name__ == "__main__":
    generate_combinations()
