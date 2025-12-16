#!/usr/bin/env python3
"""
Google Instant Indexing API Script
Sitemap'teki tum URL'leri Google'a aninda bildirir.
Progress tracking ile gunluk limitler yonetilir.
"""

import json
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime

try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("[!] Gerekli kutuphaneler yuklu degil.")
    print("[i] Lutfen su komutu calistirin:")
    print("    pip install google-auth google-api-python-client")
    exit(1)

# ============================================================================
# YAPILANDIRMA
# ============================================================================

# Service Account JSON dosyasinin yolu
CREDENTIALS_FILE = r"C:\Users\Dante\Desktop\Yeniden\WebSite\ruya-sitesi gerekenler\ruya-sitesi-indexing-c75b4771bf27.json"

# Sitemap dosyasinin yolu
SITEMAP_FILE = r"C:\Users\Dante\Desktop\Yeniden\WebSite\ruya-sitesi\hugo-site\public\sitemap.xml"

# Progress dosyasi - hangi URL'lerin gonderildigini takip eder
PROGRESS_FILE = r"C:\Users\Dante\Desktop\Yeniden\WebSite\ruya-sitesi\scripts\indexing_progress.json"

# API Limitleri
DAILY_LIMIT = 200  # Google gunluk 200 URL limiti var
DELAY_BETWEEN_REQUESTS = 1  # Her istek arasinda bekleme (saniye)

# ============================================================================
# FONKSIYONLAR
# ============================================================================

def load_progress():
    """Onceki ilerlemeyi yukler."""
    if Path(PROGRESS_FILE).exists():
        try:
            with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return {
        'indexed_urls': [],
        'last_run': None,
        'total_indexed': 0
    }


def save_progress(progress):
    """Ilerlemeyi kaydeder."""
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)


def get_urls_from_sitemap(sitemap_path):
    """Sitemap XML dosyasindan URL'leri ceker."""
    urls = []

    try:
        tree = ET.parse(sitemap_path)
        root = tree.getroot()

        # XML namespace
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

        # Tum <loc> etiketlerini bul
        for url in root.findall('.//ns:loc', namespace):
            urls.append(url.text)

        # Eger namespace yoksa
        if not urls:
            for url in root.iter():
                if url.tag.endswith('loc'):
                    urls.append(url.text)

    except Exception as e:
        print(f"[X] Sitemap okuma hatasi: {e}")
        return []

    return urls


def create_indexing_service(credentials_file):
    """Google Indexing API servisi olusturur."""
    try:
        credentials = service_account.Credentials.from_service_account_file(
            credentials_file,
            scopes=['https://www.googleapis.com/auth/indexing']
        )
        service = build('indexing', 'v3', credentials=credentials)
        return service
    except Exception as e:
        print(f"[X] API servisi olusturulamadi: {e}")
        return None


def submit_url(service, url, action="URL_UPDATED"):
    """Tek bir URL'i Google'a bildirir."""
    body = {
        'url': url,
        'type': action  # URL_UPDATED veya URL_DELETED
    }

    try:
        response = service.urlNotifications().publish(body=body).execute()
        return True, response, None
    except HttpError as e:
        if e.resp.status == 429:
            return False, None, "QUOTA_EXCEEDED"
        return False, None, str(e)
    except Exception as e:
        return False, None, str(e)


def main():
    print("=" * 60)
    print("  GOOGLE INSTANT INDEXING")
    print("=" * 60)
    print()

    # Credentials dosyasini kontrol et
    if not Path(CREDENTIALS_FILE).exists():
        print(f"[X] Credentials dosyasi bulunamadi:")
        print(f"    {CREDENTIALS_FILE}")
        print()
        print("[i] Dosya yolunu CREDENTIALS_FILE degiskeninde guncelleyin.")
        return

    # Sitemap dosyasini kontrol et
    if not Path(SITEMAP_FILE).exists():
        print(f"[X] Sitemap dosyasi bulunamadi:")
        print(f"    {SITEMAP_FILE}")
        return

    print(f"[i] Credentials: {Path(CREDENTIALS_FILE).name}")
    print(f"[i] Sitemap: {Path(SITEMAP_FILE).name}")
    print()

    # Onceki ilerlemeyi yukle
    progress = load_progress()
    indexed_urls = set(progress['indexed_urls'])

    print(f"[i] Onceden indexlenmis: {len(indexed_urls)} URL")
    print()

    # URL'leri al
    print("[~] Sitemap okunuyor...")
    all_urls = get_urls_from_sitemap(SITEMAP_FILE)

    if not all_urls:
        print("[X] Sitemap'te URL bulunamadi!")
        return

    print(f"[OK] {len(all_urls)} URL bulundu")

    # Henuz indexlenmemis URL'leri filtrele
    pending_urls = [url for url in all_urls if url not in indexed_urls]

    if not pending_urls:
        print()
        print("[OK] Tum URL'ler zaten indexlenmis!")
        return

    print(f"[i] Indexlenecek: {len(pending_urls)} URL")
    print()

    # Gunluk limit kontrolu
    urls_to_send = pending_urls[:DAILY_LIMIT]
    print(f"[i] Bu oturumda gonderilecek: {len(urls_to_send)} URL (gunluk limit: {DAILY_LIMIT})")
    print()

    # API servisini olustur
    print("[~] Google API'ye baglaniliyor...")
    service = create_indexing_service(CREDENTIALS_FILE)

    if not service:
        return

    print("[OK] API baglantisi basarili")
    print()

    # URL'leri gonder
    print(f"[~] URL'ler gonderiliyor...")
    print("-" * 60)

    success_count = 0
    error_count = 0
    quota_exceeded = False
    newly_indexed = []

    for i, url in enumerate(urls_to_send, 1):
        success, response, error = submit_url(service, url)

        if success:
            success_count += 1
            newly_indexed.append(url)
            status = "[OK]"
        else:
            if error == "QUOTA_EXCEEDED":
                quota_exceeded = True
                print(f"[!] [{i}/{len(urls_to_send)}] KOTA ASIMI - Durduruluyor...")
                break
            error_count += 1
            status = "[X]"

        # Kisa URL goster
        short_url = url.replace("https://ruyatabirisozlugu.com", "")
        print(f"{status} [{i}/{len(urls_to_send)}] {short_url[:50]}")

        # Rate limiting
        if i < len(urls_to_send) and not quota_exceeded:
            time.sleep(DELAY_BETWEEN_REQUESTS)

    print("-" * 60)
    print()

    # Ilerlemeyi kaydet
    progress['indexed_urls'] = list(indexed_urls.union(set(newly_indexed)))
    progress['last_run'] = datetime.now().isoformat()
    progress['total_indexed'] = len(progress['indexed_urls'])
    save_progress(progress)

    # Sonuc ozeti
    print("=" * 60)
    print("  SONUC")
    print("=" * 60)
    print(f"  Bu oturumda basarili:  {success_count}")
    print(f"  Bu oturumda hatali:    {error_count}")
    print(f"  Toplam indexlenmis:    {progress['total_indexed']}")
    print(f"  Kalan URL:             {len(all_urls) - progress['total_indexed']}")
    print("=" * 60)

    if quota_exceeded:
        print()
        print("[!] GUNLUK KOTA DOLDU")
        print("[i] Yarin tekrar calistirin: python instant_indexing.py")
    elif len(pending_urls) > DAILY_LIMIT:
        remaining_days = (len(pending_urls) - success_count) // DAILY_LIMIT + 1
        print()
        print(f"[i] Kalan URL'ler icin tahmini sure: {remaining_days} gun")
        print("[i] Yarin tekrar calistirin: python instant_indexing.py")

    print()
    print(f"[i] Ilerleme kaydedildi: {PROGRESS_FILE}")


if __name__ == "__main__":
    main()
