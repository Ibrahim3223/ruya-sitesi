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
# ║  AYARLAR - API ANAHTARI                                                    ║
# ╚════════════════════════════════════════════════════════════════════════════╝

GROQ_API_KEY = "YOUR_GROQ_API_KEY_HERE"  # https://console.groq.com adresinden alın

# Model seçenekleri:
# - "llama-3.1-8b-instant"    → Hızlı, ücretsiz (önerilen)
# - "llama-3.1-70b-versatile" → Daha kaliteli ama yavaş
# - "mixtral-8x7b-32768"      → Alternatif
GROQ_MODEL = "llama-3.1-8b-instant"

# Kaç sayfa üretilecek? (test için 10, sonra artır)
PAGE_LIMIT = None  # None yaparsan tümünü üretir


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
                        print("\n[!] Rate limit asildi - 60 saniye bekleniyor...")
                        await asyncio.sleep(60)
                        return await self.generate(prompt, temperature)
                    else:
                        error = await resp.text()
                        print(f"\n[X] API Hatasi: {resp.status} - {error[:200]}")
                        return ""
        except asyncio.TimeoutError:
            print("\n[!] Timeout - tekrar deneniyor...")
            await asyncio.sleep(5)
            return await self.generate(prompt, temperature)
        except Exception as e:
            print(f"\n[X] Baglanti hatasi: {e}")
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
                print(f"\n[!] Kisa icerik: {slug}")
                return False

            full_content = self.create_frontmatter(combo, content) + content

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(full_content)

            return True

        except Exception as e:
            print(f"\n[X] Hata ({slug}): {e}")
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

        print(f"\n[i] Toplam: {len(pages)} sayfa")
        print(f"[+] Mevcut: {existing} sayfa")
        print(f"[*] Uretilecek: {remaining} sayfa")
        print(f"[~] Tahmini sure: {remaining * 3 // 60} dakika\n")

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

        print(f"\n[OK] Tamamlandi!")
        print(f"   Basarili: {success}")
        print(f"   Basarisiz: {failed}")
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
