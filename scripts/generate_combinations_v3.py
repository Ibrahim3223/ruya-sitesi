#!/usr/bin/env python3
"""
Gelismis Kombinasyon Ureticisi v3
8000+ sayfa icin genisletilmis kombinasyonlar
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

# Eylemler - genisletilmis
ACTIONS = {
    # Temel eylemler
    "görmek": ("gormek", None),
    "öldürmek": ("oldurmek", ["hayvanlar", "insanlar"]),
    "kaçmak": ("kacmak", ["hayvanlar", "insanlar", "durumlar"]),
    "kovalamak": ("kovalamak", ["hayvanlar", "insanlar"]),
    "yakalamak": ("yakalamak", ["hayvanlar", "insanlar", "nesneler"]),
    "konuşmak": ("konusmak", ["hayvanlar", "insanlar", "dini"]),
    "ısırılmak": ("isirilmak", ["hayvanlar"]),

    # Yiyecek-icecek
    "yemek": ("yemek", ["yiyecekler", "hayvanlar"]),
    "içmek": ("icmek", ["yiyecekler", "doga"]),
    "pişirmek": ("pisirmek", ["yiyecekler"]),

    # Nesne eylemleri
    "almak": ("almak", ["nesneler", "yiyecekler"]),
    "vermek": ("vermek", ["nesneler", "yiyecekler"]),
    "kaybetmek": ("kaybetmek", ["nesneler", "insanlar"]),
    "bulmak": ("bulmak", ["nesneler", "insanlar", "hayvanlar"]),
    "satın almak": ("satin-almak", ["nesneler", "hayvanlar"]),
    "hediye etmek": ("hediye-etmek", ["nesneler"]),
    "çalmak": ("calmak", ["nesneler"]),

    # Nesne bakimi
    "kırmak": ("kirmak", ["nesneler"]),
    "tamir etmek": ("tamir-etmek", ["nesneler"]),
    "temizlemek": ("temizlemek", ["nesneler", "mekanlar", "vucut"]),
    "boyamak": ("boyamak", ["nesneler", "mekanlar"]),
    "yıkamak": ("yikamak", ["nesneler", "vucut"]),

    # Giyim
    "giymek": ("giymek", ["nesneler"]),
    "çıkarmak": ("cikarmak", ["nesneler", "vucut"]),
    "takmak": ("takmak", ["nesneler"]),
    "dikmek": ("dikmek", ["nesneler"]),

    # Hareket
    "binmek": ("binmek", ["hayvanlar", "nesneler"]),
    "düşmek": ("dusmek", ["mekanlar", "doga"]),
    "yüzmek": ("yuzmek", ["doga"]),
    "uçmak": ("ucmak", ["hayvanlar", "doga"]),
    "koşmak": ("kosmak", ["hayvanlar", "insanlar", "mekanlar"]),
    "yürümek": ("yurumek", ["mekanlar", "doga"]),

    # Diger
    "okumak": ("okumak", ["nesneler", "dini"]),
    "yazmak": ("yazmak", ["nesneler"]),
    "açmak": ("acmak", ["nesneler", "mekanlar"]),
    "kapatmak": ("kapatmak", ["nesneler", "mekanlar"]),
    "kilitlemek": ("kilitlemek", ["nesneler", "mekanlar"]),
}

# Niteleyiciler - genisletilmis
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
        ("pembe", "pembe"),
        ("mor", "mor"),
        ("turuncu", "turuncu"),
    ],
    "boyutlar": [
        ("büyük", "buyuk"),
        ("küçük", "kucuk"),
        ("dev", "dev"),
        ("iri", "iri"),
        ("minik", "minik"),
        ("kocaman", "kocaman"),
        ("ufak", "ufak"),
    ],
    "miktar": [
        ("çok", "cok"),
        ("sürü", "suru"),
        ("iki", "iki"),
        ("üç", "uc"),
        ("dört", "dort"),
        ("beş", "bes"),
        ("bir sürü", "bir-suru"),
    ],
    "durumlar": [
        ("ölü", "olu"),
        ("yaralı", "yarali"),
        ("hasta", "hasta"),
        ("uyuyan", "uyuyan"),
        ("koşan", "kosan"),
        ("uçan", "ucan"),
        ("yavru", "yavru"),
        ("taze", "taze"),
        ("çürük", "curuk"),
        ("kırık", "kirik"),
    ],
    "duygular": [
        ("ağlayan", "aglayan"),
        ("gülen", "gulen"),
        ("kızgın", "kizgin"),
        ("mutlu", "mutlu"),
        ("üzgün", "uzgun"),
        ("korkmuş", "korkmus"),
        ("şaşkın", "saskin"),
    ],
    "mekanlar": [
        ("evde", "evde"),
        ("yolda", "yolda"),
        ("suda", "suda"),
        ("bahçede", "bahcede"),
        ("yatakta", "yatakta"),
        ("dağda", "dagda"),
        ("ormanda", "ormanda"),
        ("gökte", "gokte"),
    ],
    "zamanlar": [
        ("gece", "gece"),
        ("gündüz", "gunduz"),
        ("sabah", "sabah"),
        ("akşam", "aksam"),
    ],
    "malzemeler": [
        ("ahşap", "ahsap"),
        ("demir", "demir"),
        ("cam", "cam"),
        ("plastik", "plastik"),
        ("taş", "tas"),
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
    seen_slugs = set()

    print(f"[i] {len(objects)} obje yuklendi")
    print(f"[i] {len(ACTIONS)} eylem tanimli")
    print(f"[i] {sum(len(v) for v in MODIFIERS.values())} niteleyici tanimli")

    # 1. TEMEL KOMBINASYONLAR: Obje + Eylem
    for obj in objects:
        obj_category = obj.get("category", "genel")
        obj_name = obj["name"]
        obj_id = obj["id"]
        search_volume = obj.get("search_volume", "medium")

        for action_name, (action_slug, action_categories) in ACTIONS.items():
            if not should_apply_action(obj_category, action_categories):
                continue

            slug = f"ruyada-{turkish_slug(obj_name)}-{action_slug}"

            if slug in seen_slugs:
                continue
            seen_slugs.add(slug)

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
                ],
                "search_volume": search_volume if action_name == "görmek" else "medium",
                "type": "page"
            }
            combinations.append(combo)

    print(f"[+] Temel kombinasyonlar: {len(combinations)}")

    # 2. RENKLER: Tum populer ve medium objeler icin
    popular_objects = [obj for obj in objects if obj.get("search_volume") in ["high", "medium"]]

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
                ],
                "search_volume": "low",
                "type": "page"
            }
            combinations.append(combo)

    print(f"[+] Renk kombinasyonlari eklendi: {len(combinations)}")

    # 3. HAYVANLAR: Boyutlar, durumlar, miktarlar, duygular
    animal_objects = [obj for obj in objects if obj.get("category") == "hayvanlar"]

    for obj in animal_objects:
        obj_name = obj["name"]
        obj_id = obj["id"]

        # Boyutlar
        for size_name, size_slug in MODIFIERS["boyutlar"]:
            slug = f"ruyada-{size_slug}-{turkish_slug(obj_name)}-gormek"
            if slug not in seen_slugs:
                seen_slugs.add(slug)
                combinations.append({
                    "id": f"{size_slug}_{obj_id}_gormek",
                    "object": obj,
                    "action": "görmek",
                    "modifier": size_name,
                    "title": f"Rüyada {size_name.title()} {obj_name} Görmek Ne Anlama Gelir?",
                    "slug": slug,
                    "keywords": [f"rüyada {size_name} {obj_name.lower()} görmek"],
                    "search_volume": "low",
                    "type": "page"
                })

        # Durumlar
        for state_name, state_slug in MODIFIERS["durumlar"]:
            slug = f"ruyada-{state_slug}-{turkish_slug(obj_name)}-gormek"
            if slug not in seen_slugs:
                seen_slugs.add(slug)
                combinations.append({
                    "id": f"{state_slug}_{obj_id}_gormek",
                    "object": obj,
                    "action": "görmek",
                    "modifier": state_name,
                    "title": f"Rüyada {state_name.title()} {obj_name} Görmek Ne Anlama Gelir?",
                    "slug": slug,
                    "keywords": [f"rüyada {state_name} {obj_name.lower()} görmek"],
                    "search_volume": "low",
                    "type": "page"
                })

        # Miktarlar
        for amount_name, amount_slug in MODIFIERS["miktar"]:
            slug = f"ruyada-{amount_slug}-{turkish_slug(obj_name)}-gormek"
            if slug not in seen_slugs:
                seen_slugs.add(slug)
                combinations.append({
                    "id": f"{amount_slug}_{obj_id}_gormek",
                    "object": obj,
                    "action": "görmek",
                    "modifier": amount_name,
                    "title": f"Rüyada {amount_name.title()} {obj_name} Görmek Ne Anlama Gelir?",
                    "slug": slug,
                    "keywords": [f"rüyada {amount_name} {obj_name.lower()} görmek"],
                    "search_volume": "low",
                    "type": "page"
                })

    print(f"[+] Hayvan kombinasyonlari eklendi: {len(combinations)}")

    # 4. INSANLAR: Duygular
    people_objects = [obj for obj in objects if obj.get("category") == "insanlar"]

    for obj in people_objects:
        obj_name = obj["name"]
        obj_id = obj["id"]

        for emotion_name, emotion_slug in MODIFIERS["duygular"]:
            slug = f"ruyada-{emotion_slug}-{turkish_slug(obj_name)}-gormek"
            if slug not in seen_slugs:
                seen_slugs.add(slug)
                combinations.append({
                    "id": f"{emotion_slug}_{obj_id}_gormek",
                    "object": obj,
                    "action": "görmek",
                    "modifier": emotion_name,
                    "title": f"Rüyada {emotion_name.title()} {obj_name} Görmek Ne Anlama Gelir?",
                    "slug": slug,
                    "keywords": [f"rüyada {emotion_name} {obj_name.lower()} görmek"],
                    "search_volume": "low",
                    "type": "page"
                })

    print(f"[+] Insan duygu kombinasyonlari eklendi: {len(combinations)}")

    # 5. MEKANLAR: Populer objeler icin
    for obj in popular_objects[:50]:
        obj_name = obj["name"]
        obj_id = obj["id"]
        obj_cat = obj.get("category", "")

        if obj_cat not in ["hayvanlar", "insanlar", "nesneler"]:
            continue

        for place_name, place_slug in MODIFIERS["mekanlar"]:
            slug = f"ruyada-{place_slug}-{turkish_slug(obj_name)}-gormek"
            if slug not in seen_slugs:
                seen_slugs.add(slug)
                combinations.append({
                    "id": f"{place_slug}_{obj_id}_gormek",
                    "object": obj,
                    "action": "görmek",
                    "modifier": place_name,
                    "title": f"Rüyada {place_name.title()} {obj_name} Görmek Ne Anlama Gelir?",
                    "slug": slug,
                    "keywords": [f"rüyada {place_name} {obj_name.lower()} görmek"],
                    "search_volume": "low",
                    "type": "page"
                })

    print(f"[+] Mekan kombinasyonlari eklendi: {len(combinations)}")

    # 6. ZAMANLAR: En populer 30 obje icin
    top_objects = [obj for obj in objects if obj.get("search_volume") == "high"][:30]

    for obj in top_objects:
        obj_name = obj["name"]
        obj_id = obj["id"]

        for time_name, time_slug in MODIFIERS["zamanlar"]:
            slug = f"ruyada-{time_slug}-{turkish_slug(obj_name)}-gormek"
            if slug not in seen_slugs:
                seen_slugs.add(slug)
                combinations.append({
                    "id": f"{time_slug}_{obj_id}_gormek",
                    "object": obj,
                    "action": "görmek",
                    "modifier": time_name,
                    "title": f"Rüyada {time_name.title()} {obj_name} Görmek Ne Anlama Gelir?",
                    "slug": slug,
                    "keywords": [f"rüyada {time_name} {obj_name.lower()} görmek"],
                    "search_volume": "low",
                    "type": "page"
                })

    print(f"[+] Zaman kombinasyonlari eklendi: {len(combinations)}")

    # 7. MALZEMELER: Nesneler icin
    object_objects = [obj for obj in objects if obj.get("category") == "nesneler"][:40]

    for obj in object_objects:
        obj_name = obj["name"]
        obj_id = obj["id"]

        for material_name, material_slug in MODIFIERS["malzemeler"]:
            slug = f"ruyada-{material_slug}-{turkish_slug(obj_name)}-gormek"
            if slug not in seen_slugs:
                seen_slugs.add(slug)
                combinations.append({
                    "id": f"{material_slug}_{obj_id}_gormek",
                    "object": obj,
                    "action": "görmek",
                    "modifier": material_name,
                    "title": f"Rüyada {material_name.title()} {obj_name} Görmek Ne Anlama Gelir?",
                    "slug": slug,
                    "keywords": [f"rüyada {material_name} {obj_name.lower()} görmek"],
                    "search_volume": "low",
                    "type": "page"
                })

    print(f"[+] Malzeme kombinasyonlari eklendi: {len(combinations)}")

    # 8. IKI NITELEYICI: En populer 20 obje icin (renk + boyut)
    super_popular = [obj for obj in objects if obj.get("search_volume") == "high"][:20]

    for obj in super_popular:
        obj_name = obj["name"]
        obj_id = obj["id"]

        # Renk + Boyut kombinasyonlari
        for color_name, color_slug in MODIFIERS["renkler"][:6]:  # İlk 6 renk
            for size_name, size_slug in MODIFIERS["boyutlar"][:3]:  # İlk 3 boyut
                slug = f"ruyada-{color_slug}-{size_slug}-{turkish_slug(obj_name)}-gormek"
                if slug not in seen_slugs:
                    seen_slugs.add(slug)
                    combinations.append({
                        "id": f"{color_slug}_{size_slug}_{obj_id}_gormek",
                        "object": obj,
                        "action": "görmek",
                        "modifier": f"{color_name} {size_name}",
                        "title": f"Rüyada {color_name.title()} {size_name.title()} {obj_name} Görmek Ne Anlama Gelir?",
                        "slug": slug,
                        "keywords": [f"rüyada {color_name} {size_name} {obj_name.lower()} görmek"],
                        "search_volume": "low",
                        "type": "page"
                    })

    print(f"[+] Cift niteleyici kombinasyonlari eklendi: {len(combinations)}")

    # Kaydet
    with open(output_dir / "combinations.json", "w", encoding="utf-8") as f:
        json.dump({
            "combinations": combinations,
            "total": len(combinations)
        }, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}")
    print(f"[OK] {len(combinations)} kombinasyon olusturuldu!")
    print(f"     Dosya: data/processed/combinations.json")
    print(f"{'='*60}")

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
