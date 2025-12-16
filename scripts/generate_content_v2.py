#!/usr/bin/env python3
"""
GROQ API ile Gelismis Icerik Uretimi
- Coklu API key destegi (rate limit dolunca otomatik gecis)
- Ilerleme takibi (kaldigi yerden devam)
- Duplicate onleme
- Tum keyler dolunca durdurma

KULLANIM:
1. scripts/api_keys.json dosyasina API keylerini ekle
2. python scripts/generate_content_v2.py calistir
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

# ============================================================================
#  YAPILANDIRMA
# ============================================================================

SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent

# API Keys dosyasi (.gitignore'da olmali!)
API_KEYS_FILE = SCRIPT_DIR / "api_keys.json"

# Progress dosyasi
PROGRESS_FILE = SCRIPT_DIR / "generation_progress.json"

# Model
GROQ_MODEL = "llama-3.1-8b-instant"

# Kac sayfa uretilecek? (None = tumunu uret)
PAGE_LIMIT = None

# ============================================================================
#  API KEY YONETICISI
# ============================================================================

class APIKeyManager:
    """Birden fazla API key'i yoneten sinif"""

    def __init__(self, keys_file: Path):
        self.keys = []
        self.current_index = 0
        self.exhausted_keys = set()
        self.key_request_counts = {}
        self.key_last_used = {}

        self._load_keys(keys_file)

    def _load_keys(self, keys_file: Path):
        """API keylerini dosyadan yukle"""
        if not keys_file.exists():
            raise FileNotFoundError(
                f"API keys dosyasi bulunamadi: {keys_file}\n"
                "Lutfen scripts/api_keys.json olusturun."
            )

        with open(keys_file, 'r') as f:
            data = json.load(f)

        self.keys = data.get("groq_api_keys", [])

        if not self.keys:
            raise ValueError("API keys dosyasinda anahtar bulunamadi!")

        # Her key icin sayac baslat
        for key in self.keys:
            short_key = key[-8:]
            self.key_request_counts[short_key] = 0
            self.key_last_used[short_key] = 0

        print(f"[i] {len(self.keys)} API key yuklendi")

    def get_current_key(self) -> str:
        """Mevcut aktif key'i dondur"""
        if self.all_exhausted():
            return None
        return self.keys[self.current_index]

    def get_current_key_short(self) -> str:
        """Mevcut key'in son 8 karakteri"""
        key = self.get_current_key()
        return key[-8:] if key else "---"

    def mark_exhausted(self):
        """Mevcut key'i tukenmis olarak isaretle ve sonrakine gec"""
        current_key = self.keys[self.current_index]
        self.exhausted_keys.add(current_key)
        short = current_key[-8:]
        print(f"\n[!] API key ...{short} tukendi (gunluk limit)")

        # Sonraki kullanilabilir key'e gec
        self._rotate_to_next()

    def rotate_key(self):
        """Rate limit icin key degistir (tukenmis isaretleme)"""
        old_short = self.get_current_key_short()
        self._rotate_to_next()
        new_short = self.get_current_key_short()
        print(f"\n[~] Key degistirildi: ...{old_short} -> ...{new_short}")

    def _rotate_to_next(self):
        """Bir sonraki kullanilabilir key'e gec"""
        original_index = self.current_index

        for _ in range(len(self.keys)):
            self.current_index = (self.current_index + 1) % len(self.keys)
            if self.keys[self.current_index] not in self.exhausted_keys:
                return

        # Tum keyler tukenmis
        self.current_index = original_index

    def all_exhausted(self) -> bool:
        """Tum keyler tukendi mi?"""
        return len(self.exhausted_keys) >= len(self.keys)

    def record_request(self):
        """Istek sayacini artir"""
        short = self.get_current_key_short()
        self.key_request_counts[short] = self.key_request_counts.get(short, 0) + 1
        self.key_last_used[short] = time.time()

    def get_stats(self) -> dict:
        """Key kullanim istatistikleri"""
        return {
            "total_keys": len(self.keys),
            "exhausted_keys": len(self.exhausted_keys),
            "request_counts": dict(self.key_request_counts)
        }


# ============================================================================
#  ILERLEME TAKIBI
# ============================================================================

class ProgressTracker:
    """Ilerleme takibi - kaldigi yerden devam etme"""

    def __init__(self, progress_file: Path):
        self.progress_file = progress_file
        self.completed_slugs = set()
        self.failed_slugs = set()
        self.stats = {
            "total_generated": 0,
            "last_run": None,
            "sessions": []
        }

        self._load_progress()

    def _load_progress(self):
        """Onceki ilerlemeyi yukle"""
        if self.progress_file.exists():
            try:
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.completed_slugs = set(data.get("completed_slugs", []))
                    self.failed_slugs = set(data.get("failed_slugs", []))
                    self.stats = data.get("stats", self.stats)
            except Exception as e:
                print(f"[!] Progress yuklenemedi: {e}")

    def save_progress(self):
        """Ilerlemeyi kaydet"""
        data = {
            "completed_slugs": list(self.completed_slugs),
            "failed_slugs": list(self.failed_slugs),
            "stats": self.stats
        }
        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def mark_completed(self, slug: str):
        """Sayfa tamamlandi olarak isaretle"""
        self.completed_slugs.add(slug)
        self.failed_slugs.discard(slug)
        self.stats["total_generated"] += 1

    def mark_failed(self, slug: str):
        """Sayfa basarisiz olarak isaretle"""
        self.failed_slugs.add(slug)

    def is_completed(self, slug: str) -> bool:
        """Sayfa daha once uretilmis mi?"""
        return slug in self.completed_slugs

    def get_pending_count(self, total: int) -> int:
        """Kalan sayfa sayisi"""
        return total - len(self.completed_slugs)


# ============================================================================
#  GROQ API CLIENT
# ============================================================================

class GroqClient:
    def __init__(self, key_manager: APIKeyManager):
        self.key_manager = key_manager
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.last_request_time = 0

    async def generate(self, prompt: str, temperature: float = 0.8, retry_count: int = 0) -> str:
        """Groq API'den icerik uret"""

        # Tum keyler tukendiyse None don
        if self.key_manager.all_exhausted():
            return None

        api_key = self.key_manager.get_current_key()

        # Rate limiting - istekler arasi bekleme
        current_time = time.time()
        time_diff = current_time - self.last_request_time
        if time_diff < 1.5:
            await asyncio.sleep(1.5 - time_diff)

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": GROQ_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "Sen deneyimli bir Turkce ruya tabircisisin. Dogal, akici ve bilgilendirici icerik yazarsin. Yapay zeka tarafindan yazilmis gibi hissettirme, insani bir dil kullan."
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
                    self.key_manager.record_request()

                    if resp.status == 200:
                        result = await resp.json()
                        return result["choices"][0]["message"]["content"]

                    elif resp.status == 429:
                        error_text = await resp.text()

                        # Gunluk limit mi yoksa dakikalik rate limit mi?
                        if "daily" in error_text.lower() or "tokens per day" in error_text.lower():
                            # Gunluk limit - bu key'i isaretle ve sonrakine gec
                            self.key_manager.mark_exhausted()

                            if self.key_manager.all_exhausted():
                                print("\n[X] TUM API KEYLER TUKENDI!")
                                return None

                            # Yeni key ile tekrar dene
                            return await self.generate(prompt, temperature, retry_count)

                        else:
                            # Dakikalik rate limit - key degistir ve devam et
                            if retry_count < len(self.key_manager.keys):
                                self.key_manager.rotate_key()
                                await asyncio.sleep(2)
                                return await self.generate(prompt, temperature, retry_count + 1)
                            else:
                                # Tum keyler rate limited, bekle
                                print("\n[!] Tum keyler rate limited - 60 saniye bekleniyor...")
                                await asyncio.sleep(60)
                                return await self.generate(prompt, temperature, 0)

                    else:
                        error = await resp.text()
                        print(f"\n[X] API Hatasi: {resp.status} - {error[:200]}")
                        return ""

        except asyncio.TimeoutError:
            print("\n[!] Timeout - tekrar deneniyor...")
            await asyncio.sleep(5)
            if retry_count < 3:
                return await self.generate(prompt, temperature, retry_count + 1)
            return ""

        except Exception as e:
            print(f"\n[X] Baglanti hatasi: {e}")
            return ""


# ============================================================================
#  ICERIK URETICISI
# ============================================================================

class ContentGenerator:
    def __init__(self, key_manager: APIKeyManager, progress_tracker: ProgressTracker):
        self.client = GroqClient(key_manager)
        self.key_manager = key_manager
        self.progress = progress_tracker
        self.output_dir = PROJECT_DIR / "hugo-site" / "content" / "ruya"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def get_prompt(self, combo: dict) -> str:
        """Ruya tabiri icin prompt"""
        obj = combo.get("object", {})
        obj_name = obj.get("name", "")
        action = combo.get("action", "gormek")
        modifier = combo.get("modifier", "")
        category = obj.get("category", "genel")

        if modifier:
            subject = f"{modifier} {obj_name}"
        else:
            subject = obj_name

        return f"""Ruyada {subject} {action} hakkinda kapsamli bir makale yaz.

KURALLAR:
- Minimum 700 kelime yaz
- Dogal, akici Turkce kullan
- ASLA madde isareti veya liste kullanma, sadece paragraflar yaz
- Her paragraf en az 3-4 cumle olsun
- H2 basliklari icin ## kullan
- Samimi ve bilgilendirici ol

ICERIK YAPISI:

## Ruyada {subject} {action.title()} Ne Anlama Gelir?

Ruyada {subject.lower()} {action} hakkinda giris paragrafi yaz. Genel olarak ne anlama geldigini, insanlarin neden bu ruyayi gordugunu acikla.

## Islami Kaynaklara Gore Ruyada {subject} Gormek

Islami ruya tabircilerine gore (Ibn-i Sirin, Nablusi vb.) bu ruyanin ne anlama geldigini detayli acikla. Hadislerden ve alimlerden bahsedebilirsin.

## Psikolojik Acidan Ruyada {subject}

Modern psikoloji ve bilincalti acisindan bu ruyanin ne anlama gelebilecegini acikla. Freud, Jung gibi psikologların goruslerine deginebilirsin.

## Ruyanin Detaylarina Gore Farkli Anlamlar

Farkli senaryolari acikla: Buyuk/kucuk {subject.lower()}, renkli/renksiz, tek/cok, nerede goruldugu, ne yaptigi gibi detaylarin ruyanin anlamini nasil degistirdigini anlat.

## Sonuc

Kisa bir ozet ve genel degerlendirme yap. Ruyalarin kisisel oldugunu, yorumlarin degisebilecegini belirt.

SIMDI YAZMAYI BASLA (sadece makale icerigini yaz, bu talimatlari tekrarlama):"""

    def create_frontmatter(self, combo: dict, content: str) -> str:
        """Hugo frontmatter olustur"""
        obj = combo.get("object", {})
        title = combo.get("title", "")
        slug = combo.get("slug", "")
        keywords = combo.get("keywords", [])
        modifier = combo.get("modifier", "")

        # Aciklama cikar
        clean_content = re.sub(r'#.*?\n', '', content)
        paragraphs = [p.strip() for p in clean_content.split('\n\n') if p.strip()]
        first_para = paragraphs[0] if paragraphs else ""
        description = first_para[:155].replace('"', "'").replace('\n', ' ')
        if len(first_para) > 155:
            description += "..."

        # Tags
        tags = [obj.get('name', ''), "ruya tabiri", "ruya yorumu"]
        if modifier:
            tags.append(modifier)

        return f"""---
title: "{title}"
slug: "{slug}"
date: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S+03:00')}
lastmod: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S+03:00')}
description: "{description}"
keywords: {json.dumps(keywords, ensure_ascii=False)}
categories: ["{obj.get('category', 'genel')}"]
tags: {json.dumps(tags, ensure_ascii=False)}
author: "Ruya Tabiri"
draft: false
---

"""

    async def generate_page(self, combo: dict) -> bool:
        """Tek sayfa uret"""
        slug = combo.get("slug", "unknown")
        filepath = self.output_dir / f"{slug}.md"

        # Zaten dosya varsa atla
        if filepath.exists():
            self.progress.mark_completed(slug)
            return True

        # Progress'te tamamlanmis mi?
        if self.progress.is_completed(slug):
            return True

        try:
            prompt = self.get_prompt(combo)
            content = await self.client.generate(prompt)

            # Tum keyler tukendiyse
            if content is None:
                return None

            if not content or len(content) < 400:
                self.progress.mark_failed(slug)
                return False

            full_content = self.create_frontmatter(combo, content) + content

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(full_content)

            self.progress.mark_completed(slug)
            return True

        except Exception as e:
            print(f"\n[X] Hata ({slug}): {e}")
            self.progress.mark_failed(slug)
            return False

    async def generate_all(self, combinations: list, limit: int = None):
        """Tum icerikleri uret"""

        # Sadece sayfa tipleri
        pages = [c for c in combinations if c.get("type") != "category"]

        if limit:
            pages = pages[:limit]

        # Mevcut durumu kontrol et
        existing = sum(1 for p in pages if (self.output_dir / f"{p['slug']}.md").exists())
        already_done = sum(1 for p in pages if self.progress.is_completed(p['slug']))
        remaining = len(pages) - max(existing, already_done)

        print(f"\n[i] Toplam: {len(pages)} sayfa")
        print(f"[+] Mevcut dosya: {existing}")
        print(f"[+] Onceden uretilmis: {already_done}")
        print(f"[*] Uretilecek: {remaining} sayfa")
        print(f"[~] Tahmini sure: {remaining * 2 // 60} dakika\n")

        if remaining == 0:
            print("Tum sayfalar zaten uretilmis!")
            return

        success = 0
        failed = 0
        session_start = datetime.now().isoformat()

        try:
            for combo in tqdm(pages, desc="Uretiliyor"):
                # Key durumunu goster
                key_short = self.key_manager.get_current_key_short()
                tqdm.write(f"", end="")  # tqdm satir bozulmamasi icin

                result = await self.generate_page(combo)

                if result is None:
                    # Tum keyler tukendi
                    print("\n\n[!] TUM API KEYLER TUKENDI - Durduruluyor...")
                    break
                elif result:
                    success += 1
                else:
                    failed += 1

                # Her 10 sayfada bir kaydet
                if (success + failed) % 10 == 0:
                    self.progress.save_progress()

        except KeyboardInterrupt:
            print("\n\n[!] Kullanici tarafindan durduruldu")

        finally:
            # Son ilerlemeyi kaydet
            self.progress.stats["last_run"] = datetime.now().isoformat()
            self.progress.stats["sessions"].append({
                "start": session_start,
                "end": datetime.now().isoformat(),
                "success": success,
                "failed": failed
            })
            self.progress.save_progress()

        # Sonuc ozeti
        print(f"\n{'='*60}")
        print(f"  SONUC")
        print(f"{'='*60}")
        print(f"  Bu oturumda basarili: {success}")
        print(f"  Bu oturumda basarisiz: {failed}")
        print(f"  Toplam uretilmis: {len(self.progress.completed_slugs)}")
        print(f"  Kalan: {len(pages) - len(self.progress.completed_slugs)}")
        print(f"{'='*60}")

        # Key istatistikleri
        stats = self.key_manager.get_stats()
        print(f"\n[i] API Key Kullanimi:")
        for key_short, count in stats["request_counts"].items():
            status = "TUKENDI" if any(k.endswith(key_short) for k in self.key_manager.exhausted_keys) else "Aktif"
            print(f"    ...{key_short}: {count} istek [{status}]")


# ============================================================================
#  ANA FONKSIYON
# ============================================================================

async def main():
    print("=" * 60)
    print("  RUYA TABIRLERI ICERIK URETICISI v2")
    print("=" * 60)

    # API Key Manager
    try:
        key_manager = APIKeyManager(API_KEYS_FILE)
    except (FileNotFoundError, ValueError) as e:
        print(f"\n[X] HATA: {e}")
        print("\nLutfen scripts/api_keys.json dosyasi olusturun:")
        print('{')
        print('  "groq_api_keys": [')
        print('    "gsk_xxxxx",')
        print('    "gsk_yyyyy"')
        print('  ]')
        print('}')
        return

    # Progress Tracker
    progress = ProgressTracker(PROGRESS_FILE)
    print(f"[i] Onceden uretilmis: {len(progress.completed_slugs)} sayfa")

    # Kombinasyonlari yukle
    combo_file = PROJECT_DIR / "data" / "processed" / "combinations.json"

    if not combo_file.exists():
        print("\n[X] Kombinasyon dosyasi bulunamadi!")
        print("    Once su komutu calistirin:")
        print("    python scripts/generate_combinations_v2.py")
        return

    with open(combo_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        combinations = data["combinations"]

    print(f"[i] Kombinasyon: {len(combinations)} sayfa")
    print(f"[i] Model: {GROQ_MODEL}")
    print(f"[i] Limit: {PAGE_LIMIT if PAGE_LIMIT else 'Tumunu uret'}")

    generator = ContentGenerator(key_manager, progress)
    await generator.generate_all(combinations, limit=PAGE_LIMIT)

    print("\n[i] Ilerleme kaydedildi:", PROGRESS_FILE)
    print("[i] Yarin tekrar calistirarak devam edebilirsiniz.")


if __name__ == "__main__":
    asyncio.run(main())
