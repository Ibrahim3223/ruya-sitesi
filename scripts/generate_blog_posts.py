#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import time
from groq import Groq
from datetime import datetime, timedelta

# Load API key
with open('api_keys.json', 'r') as f:
    api_keys = json.load(f)
    GROQ_API_KEY = api_keys['groq_api_keys'][0]

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Blog post topics - carefully chosen for SEO and AdSense value
BLOG_TOPICS = [
    {
        "title": "Rüyada Renklerin Anlamı: Psikolojik ve İslami Perspektif",
        "slug": "ruyada-renklerin-anlami",
        "description": "Rüyada renkler ne anlama gelir? Kırmızı, mavi, yeşil, beyaz, siyah rüya yorumları. Psikolojik ve İslami bakış açısıyla renk sembolleri.",
        "category": "Rüya Yorumlama",
        "tags": ["renkler", "rüya sembolleri", "psikoloji", "İslam"],
        "prompt": """Rüyada renklerin anlamı hakkında 2500+ kelimelik, son derece detaylı ve kaliteli bir blog yazısı yaz.

İÇERİK GEREKSİNİMLERİ:
1. GİRİŞ: Renklerin rüyalardaki önemi, bilimsel araştırmalar
2. HER RENK İÇİN DETAYLI BÖLÜM:
   - Kırmızı (tutku, öfke, enerji)
   - Mavi (huzur, sakinlik, maneviyat)
   - Yeşil (umut, bereket, doğa)
   - Sarı (mutluluk, enerji, dikkat)
   - Beyaz (saflık, temizlik, masumiyet)
   - Siyah (korku, bilinmeyen, güç)
   - Mor (maneviyat, soylu luk)
   - Turuncu, pembe, gri vb.
3. İSLAMİ YORUMLAR: İbni Sirin ve İmam-ı Nablusi'ye göre
4. PSİKOLOJİK YORUMLAR: Freud, Jung, modern psikoloji
5. PRATİK ÖRNEKLER: Gerçek rüya senaryoları
6. KÜLTÜREL FARKLILIKLAR: Renklerin farklı kültürlerdeki anlamları
7. SONUÇ: Özet ve pratik öneriler

STİL VE TON:
- Samimi, sohbet tarzı ama profesyonel
- Örneklerle zenginleştir
- Başlıklar, alt başlıklar, liste kullan
- Okuyucuya doğrudan hitap et ("siz", "sizin")
- Bilimsel kaynaklara atıf yap
- Emoji kullanma, sadece markdown formatı

MARKDOWN FORMATI:
- # ana başlık
- ## alt başlıklar
- ### detay başlıklar
- **kalın** vurgular
- Liste ve numaralama
- > alıntılar

ÇOK ÖNEMLİ: İnsan yazmış gibi yaz. Çeşitli cümle yapıları, kişisel örnekler, sohbet tonu. 2500+ kelime olmalı."""
    },
    {
        "title": "Rüyada Ölüm Görmek: Korkulacak Bir Şey mi?",
        "slug": "ruyada-olum-gormek",
        "description": "Rüyada ölüm, ölü insan, cenazes görme neanlamagelir? İslami yorumlar, psikolojik analiz, yaygın ölüm rüyaları ve gerçek anlamları.",
        "category": "Rüya Yorumlama",
        "tags": ["ölüm", "ölü görmek", "cenaze", "İslami yorum"],
        "prompt": """Rüyada ölüm görmek hakkında 2500+ kelimelik, detaylı, empatik ve bilgilendirici bir blog yazısı yaz.

İÇERİK:
1. GİRİŞ: Ölüm rüyalarının yaygınlığı, ilk tepkiler, gerçek anlamlar
2. ÖLÜM RÜYALARININ TÜRLER İ:
   - Kendi ölümünüzü görmek
   - Sevilen birinin ölümü
   - Yabancı birinin ölümü
   - Cenaze töreni
   - Mezarlık görmek
   - Ölü insanlarla konuşmak
3. İSLAMİ YORUMLAR:
   - Hz. Muhammed'in hadisleri
   - İbni Sirin'in yorumları
   - İmam-ı Nablusi'nin açıklamaları
   - Ölü ile konuşma rüyalarının önemi
4. PSİKOLOJİK YORUMLAR:
   - Freud'un ölüm dürtüsü teorisi
   - Jung'un dönüşüm yorumu
   - Modern psikolojide ölüm rüyaları
   - Kaygı ve değişim sembolleri
5. YAYGN ÖLÜM RÜYASI SENARYOLARI:
   - Annenin/babanın ölümü → Bağımsızlık
   - Eşin ölümü → İlişki kaygısı
   - Kendi ölümünüz → Yeni başlangıç
6. NE ZAMAN ENDİŞELENMELİ:
   - Normal vs travmatik ölüm rüyaları
   - PTSD ve tekrar eden kabuslar
   - Ne zaman terapist desteği alınmalı
7. RAHATLATICI GERÇEKLER:
   - Ölüm rüyaları genellikle gerçek ölümü öngörmez
   - Dönüşüm ve yeni başlangıç sembolüdür
   - Çoğu kültürde olumlu yorumları da vardır
8. PRATİK ÖNERİLER:
   - Ölüm rüyası gördüğünüzde ne yapmalı
   - Duygusal işleme teknikleri
   - İslami dualar ve öneriler

STİL: Empatik, rahatlatıcı, bilgilendirici. Korku yerine anlayış yaratın. 2500+ kelime."""
    },
    {
        "title": "En Çok Görülen 20 Rüya ve Anlamları (2025 İstatistikleri)",
        "slug": "en-cok-gorulen-ruyalar",
        "description": "Dünyanın her yerinde en sık görülen rüyalar hangileri? Düşme, kovalanma, diş dökülmesi, uçma, sınav rüyaları ve bilimsel açıklamaları.",
        "category": "Rüya İstatistikleri",
        "tags": ["yaygın rüyalar", "rüya istatistikleri", "evrensel rüyalar"],
        "prompt": """En çok görülen rüyalar hakkında 2500+ kelimelik, araştırma temelli, ilgi çekici bir blog yazısı yaz.

İÇERİK:
1. GİRİŞ: Evrensel rüya fenomeni, araştırmalar, istatistikler
2. TOP 20 RÜYA (Her biri için detaylı bölüm):
   1. Düşmek (%60-70 sıklık)
   2. Kovalanmak/Kaçmak (%50-60)
   3. Uçmak (%40-50)
   4. Dişlerin Dökülmesi (%30-40)
   5. Sınava Girmek/Hazırsız Olmak
   6. Geç Kalmak
   7. Çıplak Kalmak/Utanç
   8. Sevilen Birinin Kaybı
   9. Arabayı Kontrol Edememe
   10. Eski Ev/Okul
   11. Hamile Olmak (hem kadın hem erkek)
   12. Su (okyanus, sel, göl)
   13. Yılan
   14. Yaralanma/Kan
   15. Kaybolma
   16. Paraliz (hareket edememe)
   17. Cinsel Rüyalar
   18. Ünlü Birini Görme
   19. Doğal Afetler
   20. Ölüm

HER RÜYA İÇİN:
- Yaygınlık istatistiği
- Psikolojik açıklama
- İslami yorum
- Neden bu kadar yaygın?
- Gerçek örnekler

3. BİLİMSEL ARAŞTIRMALAR:
   - Calvin Hall'un rüya araştırmaları
   - DreamBank verileri
   - Kültürler arası karşılaştırmalar
4. NEDEN EVRENSEL?:
   - Evrimsel psikoloji açıklamaları
   - Ortak insan deneyimleri
   - Kollektif bilinçdışı (Jung)
5. SONUÇ: Rüyalarınızın normalliği, ne zaman endişelenmeli

STİL: İstatistiklerle zenginleştir, bilimsel ama anlaşılır. 2500+ kelime."""
    },
    {
        "title": "Lucid Dreaming (Bilinçli Rüya Görme): Teknikler ve Tehlikeler",
        "slug": "lucid-dreaming-bilinçli-ruya",
        "description": "Lucid dream (bilinçli rüya) nedir, nasıl yapılır? WILD, MILD, DILD teknikleri. Faydaları, riskleri, İslami bakış açısı.",
        "category": "Rüya Psikolojisi",
        "tags": ["lucid dream", "bilinçli rüya", "rüya kontrolü"],
        "prompt": """Lucid dreaming (bilinçli rüya görme) hakkında 2500+ kelimelik, kapsamlı, dengeli bir rehber yaz.

İÇERİK:
1. GİRİŞ: Lucid dream nedir, bilimsel tanım, tarihçe
2. BİLİMSEL TEMELLER:
   - REM uykusu ve beyin aktivitesi
   - Stephen LaBerge'ın araştırmaları
   - Bilimsel çalışmalar ve kanıtlar
3. LUCID DREAM TEKNİKLERİ (Her biri detaylı):
   - **Reality Testing**: Gerçeklik kontrolleri
   - **MILD (Mnemonic Induction)**: Hafıza tekniği
   - **WILD (Wake Initiated)**: Uyanık başlatma
   - **DILD (Dream Initiated)**: Rüyada farkındalık
   - **WBTB (Wake Back to Bed)**: Geri uyuma
   - Rüya günlüğü tutma önemi
   - Meditasyon ve farkındalık
4. ADIM ADIM BAŞLANGIÇ REHBERİ:
   - 1. Hafta: Rüya günlüğü
   - 2. Hafta: Reality testing
   - 3. Hafta: MILD tekniği
   - 4. Hafta: İlk lucid dream denemeleri
5. LUCID DREAM'İN FAYDALARI:
   - Kabus kontrolü
   - Yaratıcılık artışı
   - Problem çözme
   - Kişisel gelişim
   - Eğlence ve keşif
6. RİSKLER VE DİKKAT EDİLMESİ GEREKENLER:
   - Uyku paralizi riski
   - Gerçekle rüyanın karışması
   - Bağımlılık potansiyeli
   - Uyku kalitesi sorunları
   - Psikolojik yan etkiler
7. İSLAMİ BAKIŞ AÇISI:
   - Alimlerin görüşleri
   - Helal mi haram mı?
   - Nefsi kontrol vs ilahi rehberlik tartışması
8. KİMLER YAPMAMALIC?:
   - Uyku bozuklukları olanlar
   - Psikoz riski olanlar
   - Şizofreni hastaları
9. PRATİK İPUÇLARI:
   - En iyi saatler
   - Beslenme önerileri
   - Çevresel faktörler

STİL: Dengeli, hem fırsat hem riskleri vurgula. Bilimsel ama uygulanabilir. 2500+ kelime."""
    },
    {
        "title": "Çocuk Rüyaları ve Kabuslar: Ebeveyn Rehberi",
        "slug": "cocuk-ruyalari-ve-kabuslar",
        "description": "Çocukların rüyaları ve kabusları nasıl yorumlanır? Yaşa göre rüya gelişimi, yaygın çocuk kabus ları, ebeveyn nasıl yardımcı olabilir.",
        "category": "Çocuk Psikolojisi",
        "tags": ["çocuk rüyaları", "çocuk kabusları", "ebeveynlik"],
        "prompt": """Çocuk rüyaları ve kabusları hakkında 2500+ kelimelik, ebeveynlere yönelik, pratik ve empatik bir rehber yaz.

İÇERİK:
1. GİRİŞ: Çocuk rüyaları neden farklıdır?
2. YAŞA GÖRE RÜYA GELİŞİMİ:
   - 0-2 yaş: Rüya görüyorlar mı?
   - 2-5 yaş: İlk rüyalar, animizm
   - 5-8 yaş: Gerçek vs hayal ayrımı
   - 8-12 yaş: Daha karmaşık rüyalar
   - Ergenlik: Yetişkin benzeri rüyalar
3. EN YAYGN ÇOCUK KABUSLARI:
   - Canavar/yaratık rüyaları
   - Anne-babayı kaybetme
   - Karanlık, boğulma
   - Okulda utanç
   - Yaralanma, kan
4. KABUSLARIN NEDENLERİ:
   - Gelişimsel kaygılar
   - Gündüz stresi
   - Medya etkisi (korku filmleri, haberler)
   - Aile içi sorunlar
   - Travma ve istismar işaretleri (DİKKATLİ!)
5. GECE KORKUSU vs KABUS:
   - Night Terror nedir?
   - Kabustan farkları
   - Nasıl müdahale edilir?
6. EBEVEYN NASIL YARDIMCI OLABİLİR:
   - Dinleme ve onaylama
   - Rüya günlüğü tutturma (yaşa uygun)
   - Rüyayı "yeniden yazma" tekniği
   - Kabus önleme ritüelleri
   - Yatak odası düzenlemeleri
7. NE ZAMAN PROFESYONEL YARDIM ALINMALI:
   - Sık ve yoğun kabuslar
   - Uyku bozuklukları
   - Travma belirtileri
   - İstismar şüphesi
8. PRATİK STRATEJİLER:
   - Uyku hijyeni
   - Yatmadan önce rutinler
   - Hikaye terapisi
   - Oyun terapisi
9. KÜLTÜREL VE DİNİ YAKLAŞIMLAR:
   - İslami dualar (Ayetel Kürsi, vb.)
   - Çocuğa uygun dini açıklamalar
10. KAYNAKLAR: Ebeveynler için kitaplar, websiteler

STİL: Empatik, pratik, bilimsel. Ebeveynlere güven ver. 2500+ kelime."""
    },
    {
        "title": "Hamilelik Döneminde Rüyalar: Ne Anlama Gelir?",
        "slug": "hamilelik-donemi-ruyalari",
        "description": "Hamile kadınların gördüğü rüyalar. Bebeğin cinsiyeti, doğum, korku rüyaları. Hormonal değişiklikler ve rüyalar. Bilimsel açıklamalar.",
        "category": "Hamilelik ve Rüyalar",
        "tags": ["hamilelik", "hamile rüyaları", "bebek rüyası"],
        "prompt": """Hamilelik döneminde görülen rüyalar hakkında 2500+ kelimelik, bilimsel ve destekleyici bir rehber yaz.

İÇERİK:
1. GİRİŞ: Hamilelikte rüyalar neden daha canlı?
2. BİLİMSEL AÇIKLAMALAR:
   - Hormonal değişiklikler (progesteron, östrojen)
   - Uyku bozuklukları ve REM artışı
   - Duygusal yoğunluk
   - Kaygı ve beklentiler
3. TRİMESTERLARA GÖRE RÜYALAR:
   - **1. Trimester**: Verimlilik, tohum, küçük hayvanlar
   - **2. Trimester**: Bebek bağı, hayvan yavruları
   - **3. Trimester**: Doğum, su, yolculuk
4. EN YAYGN HAMİLELİK RÜYALARI:
   - Bebeğin cinsiyeti (doğru çıkıyor mu?)
   - Doğum ve sancı rüyaları
   - Bebeği unutma/kaybetme kabusları
   - Hamile olduğunu unutma
   - Mükemmel olmayan bebek (endişe yansıması)
   - Eski sevgili/eşle rüyalar (bağlanma kaygısı)
   - Tuhaf yiyecek kombinasyonları
5. YAYGN KABUS TEMALARI:
   - Bebeği düşürme
   - Kötü bebek
   - Doğumda komplikasyon
   - Eş vefasızlığı (güvensizlik)
6. BU RÜYALAR NORMAL Mİ?:
   - Evet! %80 hamile kadın yoğun rüyalar görür
   - Kaygı işleme mekanizması
   - Anneliğe hazırlık
7. PARTNER RÜYALARI:
   - Babalar da etkilenir (couvade sendromu)
   - Partner destek stratejileri
8. RÜYALARDAN FAYDALANMA:
   - Kaygıları konuşma fırsatı
   - Bağlanma sürecinin parçası
   - Rüya günlüğü hatıra olarak
9. NE ZAMAN ENDİŞELENMELİ:
   - Travmatik kabuslar
   - Uyku yoksunluğu
   - Depresyon belirtileri
10. PRATİK ÖNERİLER:
    - Uyku hijyeni
    - Rahatlatma teknikleri
    - Partner iletişimi
    - Meditasyon

STİL: Destekleyici, normalleştirici, bilgilendirici. Kaygıları azalt. 2500+ kelime."""
    },
        {
        "title": "Rüyalarda Cinsellik: Psikolojik ve İslami Bakış Açısı",
        "slug": "ruyalarda-cinsellik",
        "description": "Cinsel rüyalar normal mi? Freud'un yorumları, İslami perspektif, ihtilam, bastırılmış arzular. Utanmadan anlatılan bilimsel gerçekler.",
        "category": "Rüya Psikolojisi",
        "tags": ["cinsel rüyalar", "ihtilam", "Freud", "İslami yorum"],
        "prompt": """Rüyalarda cinsellik konusunu 2500+ kelime ile, profesyonel, bilimsel ve hassas bir şekilde ele al.

İÇERİK:
1. GİRİŞ: Cinsel rüyaların normalliği, utanç vs bilim
2. BİLİMSEL GERÇEKLER:
   - %70-80 insanın cinsel rüya gördüğü araştırmalar
   - REM uykusunda genital uyarılma (fizyolojik)
   - Cinsiyet farklılıkları (erkek vs kadın rüyaları)
3. FREUD'UN YAKLAŞIMI:
   - Bastırılmış arzular teorisi
   - Cinsel sembollizm (tren, merdiven, vb.)
   - Libido ve rüyalar
4. JUNG'UN YAKLAŞIMI:
   - Anima/Animus entegrasyonu
   - Cinselliğin ruhsal anlamı
   - Sembollerin manevi yorumu
5. MODERN PSİKOLOJİ:
   - Cinsel rüyalar stresi azaltır
   - Duygusal işleme
   - İlişki kalitesine etkisi
   - Keşif ve hayal kurma
6. İSLAMİ BAKIŞ AÇISI:
   - İhtilam (gusül gerektiren rüya)
   - Hangi rüyalar günah sayılmaz?
   - Hangi rüyalar endişe vericidir?
   - Alimlerin görüşleri
   - Temizlik ve namaz kuralları
7. YAYGN CİNSEL RÜYA TİPLERİ:
   - Eşle birlikte olma
   - Eski sevgiliyle
   - Yabancı biriyle
   - Ünlü biriyle
   - Aynı cinsiyetten biriyle (ne anlama gelir?)
   - Yasak/tabu durumlar
8. BU RÜYALAR NE ANLAMA GELİR?:
   - Mutlaka o kişiyi istediğiniz anlamına gelmez
   - Sembolik anlamlar
   - Duygusal ihtiyaçlar
9. İLİŞKİDEKİ ETKİSİ:
   - Partnerinize anlatmalı mı?
   - Kıskançlık vs anlayış
   - İletişim stratejileri
10. NE ZAMAN ENDİŞE EDİLMELİ:
    - Obsesif cinsel rüyalar
    - Travma sonrası cinsel kabuslar
    - Sapkınlık içerikli tekrar eden rüyalar

STİL: Profesyonel, utanç yaratmayan, bilimsel. Hassas konu dikkatli yaklaş. 2500+ kelime."""
    },
    {
        "title": "Tekrar Eden Rüyalar: Neden Aynı Rüyayı Tekrar Tekrar Görürüz?",
        "slug": "tekrar-eden-ruyalar",
        "description": "Recurring dreams (tekrar eden rüyalar) neden görülür? Çözülmemiş sorunlar, travma, bilinçaltı mesajları. Tekrar eden rüyadan kurtulma yöntemleri.",
        "category": "Rüya Psikolojisi",
        "tags": ["tekrar eden rüyalar", "recurring dreams", "kabus"],
        "prompt": """Tekrar eden rüyalar hakkında 2500+ kelimelik, psikolojik derinlikte bir analiz yaz.

İÇERİK:
1. GİRİŞ: Tekrar eden rüya fenomeni, yaygınlık
2. BİLİMSEL AÇIKLAMALAR:
   - Nörobiyoloji: Hafıza konsolidasyonu
   - Çözülmemiş duygusal sorunlar
   - Beynin "çözüm arama" mekanizması
3. PSİKOLOJİK TEORİLER:
   - Freud: Bastırılmış travmalar
   - Jung: Dikkat bekleyen arketipler
   - Gestalt: Tamamlanmamış duygusal işler
   - PTSD ve travma ilişkisi
4. EN YAYGN TEKRAR EDEN RÜYA TEMALARI:
   - Kovalanma (kaçış, kontrol kaybı)
   - Düşme (güvensizlik)
   - Hazırsız sınav (performans kaygısı)
   - Dişlerin dökülmesi (kayıp korkusu)
   - Eski ev/okul (geçmişle hesaplaşma)
   - Sevilen birinin kaybı (ayrılık kaygısı)
5. RÜYA ne ANLATMAYA ÇALIŞIYOR?:
   - Her rüya için detaylı analiz
   - Sembolik mesajlar
   - Gerçek hayat bağlantıları
6. TEKRAR EDEN RÜYADAN KURTULMA YÖNTEMLERİ:
   - **İmaj Prova Terapisi (IRT)**: Rüyayı değiştirme
   - **Lucid Dreaming**: Rüyada kontrol
   - **Aktif Hayal (Jung)**: Rüyayı uyanıkken devam ettirme
   - **Rüya Günlüğü**: Kalıpları fark etme
   - **Terapi**: Kök nedeni çözme
7. ÖRNEK VAKAsılar:
   - Vaka 1: 10 yıldır aynı kabusu gören kişi
   - Vaka 2: Çocukluktan kalma tekrar eden rüya
   - Çözüm süreçleri ve sonuçlar
8. ÇOCUKLARDA TEKRAR EDEN RÜYALAR:
   - Gelişimsel kaygılar
   - Ebeveyn müdahalesi
9. TRAVMA VE PTSD:
   - Travmatik rüyalar vs normal tekrar eden rüyalar
   - Ne zaman profesyonel yardım alınmalı
   - EMDR terapisi
10. PRATİK EGZERSİZLER:
    - Rüyayı yeniden yazma
    - Günlük tutma şablonu
    - Rahatlama teknikleri

STİL: Umut verici, çözüm odaklı, derin analiz. 2500+ kelime."""
    },
    {
        "title": "Rüya Günlüğü Tutmanın 10 İnanılmaz Faydası (Bilimsel Kanıtlarla)",
        "slug": "ruya-gunlugu-faydalari",
        "description": "Rüya günlüğü tutmak neden önemli? Hafıza güçlendirme, yaratıcılık artışı, duygusal farkındalık. Nasıl tutulur, şablonlar, ipuçları.",
        "category": "Rüya Yorumlama",
        "tags": ["rüya günlüğü", "dream journal", "kişisel gelişim"],
        "prompt": """Rüya günlüğü tutmanın faydaları hakkında 2500+ kelimelik, bilimsel araştırmalarla desteklenmiş, pratik bir rehber yaz.

İÇERİK:
1. GİRİŞ: Rüya günlüğü nedir, tarihçe
2. 10 BİLİMSEL KANITI FAYDA (Her biri için araştırmalar):
   1. **Rüya Hatırlama Artar** (%300'e kadar)
   2. **Duygusal Zeka Gelişir**
   3. **Yaratıcılık Patlama Yapar** (ünlü örnekler)
   4. **Problem Çözme Becerisi**
   5. **Öz-Farkındalık ve Bilinç**
   6. **Stres ve Kaygı Azalır**
   7. **Lucid Dream Olasılığı Artar**
   8. **Travma İyileştirme Yardımcısı**
   9. **Kişisel Gelişim İçgörüleri**
   10. **Hafıza ve Bilişsel Gelişim**
3. BİLİMSEL ARAŞTIRMALAR:
   - Harvard Medical School çalışmaları
   - Calvin Hall'un 50,000 rüya analizi
   - DreamBank veritabanı bulguları
4. RÜYA GÜNLÜĞÜ NASIL TUTULUR:
   - Geleneksel defter vs dijital
   - Sabah rutini
   - Ne kadar detaylı yazılmalı?
   - Format ve şablon örnekleri
5. ÖRNEK ŞABLON:
   ```
   Tarih:
   Uyku Saati:
   Uyanma Saati:
   Rüya:
   Duygular:
   Semboller:
   Gerçek Hayat Bağlantıları:
   Yorum:
   ```
6. İLERİ SEVİYE TEKNİKLER:
   - Renkli kalemler (duygulara göre)
   - Çizim ve sketchler
   - Ses kaydı
   - Uygulama önerileri
7. YAYIN ÖRNEKLERİ:
   - Ünlülerin rüya günlükleri (Jung, Lincoln, vb.)
   - Rüya günlüğünden doğan başarı hikayeleri
8. SIK SORULAN SORULAR:
   - Her rüyayı mı yazmalıyım?
   - Sabahları zamanım yok, ne yapmalıyım?
   - Rüyalarımı hatırlamıyorum, nasıl başlayayım?
9. 30 GÜNLÜK CHALLENGE:
   - Haftalık hedefler
   - İlerleme takibi
10. KAYNAKLAR: Uygulamalar, kitaplar, şablonlar

STİL: Motivasyonel, bilimsel, pratik. Okuyucuyu harekete geçir. 2500+ kelime."""
    },
    {
        "title": "Rüyalarda Hayvanlar ve Sembolleri: Kapsamlı Rehber",
        "slug": "ruyalarda-hayvanlar",
        "description": "Rüyada hayvan görmek ne anlama gelir? Yılan, köpek, kedi, kuş, aslan, at yorumları. İslami ve psikolojik perspektifle 50+ hayvan sembolü.",
        "category": "Rüya Sembolleri",
        "tags": ["hayvan rüyaları", "yılan", "köpek", "kedi", "kuş"],
        "prompt": """Rüyalarda hayvan sembolleri hakkında 3000+ kelimelik, kapsamlı bir ansiklopedik rehber yaz.

İÇERİK:
1. GİRİŞ: Hayvanların arketipsel gücü, Jung'un perspektifi
2. HAYVANLAR VE IÇGÜDÜLER:
   - Hayvanlar bilinçaltımızın hangi yanını temsil eder?
   - Primitif benlik, bastırılmış dürtüler
3. EN YAYGN HAYVANLAR (Her biri için 200-300 kelime):

   **YILAN:**
   - İslami Yorum (İbni Sirin, İmam-ı Nablusi)
   - Psikolojik Yorum (Jung: dönüşüm, Freud: fallik sembol)
   - Kültürel Anlamlar (Çin: bilgelik, Hıristiyanlık: şeytan)
   - Farklı Senaryolar (yılanı öldürmek, ısırılmak, vs.)

   **KÖPEK:**
   - Sadakat vs tehdit
   - İslami bakış
   - Köpek türüne göre farklılıklar

   **KEDİ:**
   - Bağımsızlık, dişil enerji
   - Renklere göre anlamlar

   **ASLAN:**
   - Güç, liderlik
   - Kral hayvan arketipi

   **KUŞ:**
   - Özgürlük, ruh, manevi yükseliş
   - Kuş türlerine göre (kartal, güvercin, karga)

   **AT:**
   - Güç, cinsellik, özgürlük
   - Renk ve davranışa göre

   **BALIK:**
   - Bilinçdışı, duygular
   - Su elementi

   **AYI:**
   - Anne arketipi, koruma

   **KELEBEK:**
   - Dönüşüm, metamorfoz

   **ARI:**
   - Çalışkanlık, topluluk

4. DİĞER HAYVANLAR (Kısaca):
   - Fil, maymun, tilki, kurt, fare, kurbağa, timsah, vb. (25+ hayvan)

5. HAYVAN DAVRAINIŞLARI:
   - Saldıran hayvan
   - Sevimli/uysal hayvan
   - Konuşan hayvan
   - Ölü hayvan
   - Yavrular

6. TOTEM HAYVANLAR:
   - Kişisel hayvan sembolleri
   - Tekrar eden hayvan rüyaları

7. KÜLTÜRLER ARASI KARŞILAŞTIRMA:
   - Aynı hayvanın farklı kültürlerde anlamları

8. PRATİK YORUM REHBERİ:
   - Hangi soruları sorun?
   - Kendi hayvan sembol sisteminizi bulun

STİL: Ansiklopedik ama okunabilir, örneklerle zengin. 3000+ kelime."""
    },
    {
        "title": "Rüyalarda Evler ve Mekanlar: İç Dünyanızın Haritası",
        "slug": "ruyalarda-evler-ve-mekanlar",
        "description": "Rüyada ev, okul, hastane, mezarlık, mağaza görmek. Jung'a göre ev = psişe. Oda yorumları, bodrum, çatı katı sembolleri.",
        "category": "Rüya Sembolleri",
        "tags": ["ev rüyası", "mekan sembolleri", "Jung", "psişe"],
        "prompt": """Rüyalarda mekan sembolleri hakkında 2500+ kelimelik, Jung'un derinlikli analizini temel alan bir rehber yaz.

İÇERİK:
1. GİRİŞ: Mekanlar neden önemli? Jung'un ev-psişe benzetmesi
2. EV: PSİŞENİN YAPISI (Jung Analizi):
   - **Ev = Kendiniz**
   - **Bodrum**: Bilinçaltı, bastırılmış anılar
   - **Zemin Kat**: Günlük bilinç
   - **Üst Katlar**: Daha yüksek bilinç, manevi yanlar
   - **Çatı Katı**: Ruhani, derin bilinç
   - **Bahçe**: Büyüme potansiyeli
   - **Garaj**: Hazır araçlar, beceriler
3. EV DURUMLARI:
   - Yeni ev (yeni benlik)
   - Eski/yıkık ev (geçmiş)
   - Tanıdık ev (çocukluk, geçmiş benlik)
   - Büyük malikane (potansiyel)
   - Küçük ev (sınırlanmışlık)
4. ODALAR VE ANLAMLARI:
   - **Mutfak**: Beslenme, dönüşüm
   - **Yatak Odası**: Mahremiyet, ilişkiler, cinsellik
   - **Banyo**: Temizlik, duygusal arınma
   - **Salon**: Sosyal benlik
   - **Tuvalet**: Atıkları bırakma, sahte şeyleri temizleme
5. DİĞER MEKANLAR:
   - **Okul**: Öğrenme, test edilme
   - **Hastane**: İyileşme, bakım ihtiyacı
   - **Mezarlık**: Geçmiş, kayıplar
   - **Kilise/Mescid**: Maneviyat
   - **Mağaza/AVM**: Seçimler, değer
   - **Hapishanea**: Sıkışmışlık
   - **Orman**: Bilinmeyen, keşif
   - **Deniz/Okyanus**: Duygular, bilinçdışı
   - **Dağ**: Zorluk, yükseliş
6. MEKAN VE DUYGU İLİŞKİSİ:
   - Kapalı mekan (sıkışmışlık)
   - Açık mekan (özgürlük vs kaybolma)
7. MEKAN DEĞİŞİMLERİ:
   - Bir mekandan diğerine geçiş (transformasyon)
8. İSLAMİ YORUMLAR:
   - Mescid, Kabe, cennet bahçesi, vb.
9. PRATİK YORUM EGZERSİZİ:
   - Rüyanızdaki mekanı çizin
   - Duygularınızı not edin
   - Gerçek hayat bağlantısı kurun

STİL: Derin analitik, görselleştirilebilir, içgörü uyandırıcı. 2500+ kelime."""
    },
    {
        "title": "Rüyalarda Su: Deniz, Nehir, Yağmur, Sel Yorumları",
        "slug": "ruyalarda-su-sembolleri",
        "description": "Rüyada su görmek ne demek? Temiz su, bulanık su, yüzmek, boğulmak, yağmur, sel yorumları. İslami ve psikolojik analizler.",
        "category": "Rüya Sembolleri",
        "tags": ["su rüyası", "deniz", "yağmur", "sel", "boğulmak"],
        "prompt": """Rüyalarda su sembolleri hakkında 2500+ kelimelik, tüm su çeşitlerini kapsayan detaylı bir rehber yaz.

İÇERİK:
1. GİRİŞ: Su = Duygu, Bilinçdışı, Hayat
2. SUYUN PSİKOLOJİK ANLAMI:
   - Jung: Kollektif bilinçdışı
   - Freud: Anne rahmi, doğum
   - Modern psikoloji: Duygusal durum
3. SU TÜRLER VE ANLAMLARI:

   **TEMİZ/BERRAK SU:**
   - İslami: İlim, hikmet (İbni Sirin)
   - Psikolojik: Duygusal netlik
   - Örnekler: İçme, yıkanma

   **BULANIK/KİRLİ SU:**
   - İslami: Fitne, problem
   - Psikolojik: Duygusal karmaşa

   **DENİZ/OKYANUS:**
   - Sınırsız bilinçdışı
   - Derin duygular
   - Sakin vs fırtınalı deniz

   **NEHİR/AKARSU:**
   - Hayatın akışı
   - Değişim, yolculuk

   **GÖL:**
   - Durgun duygular
   - İç dünya

   **ŞELale:**
   - Duygusal akış, katarsis

   **YAĞMUR:**
   - Bereket, arınma
   - İslami: Rahmet

   **SEL:**
   - Kontrolsüz duygular
   - Bunaltıcı sorunlar

   **ÇEŞME/PINAR:**
   - İslami: Cennet nimetleri
   - Yaşam kaynağı

   **HAVUZ:**
   - Kontrollü duygular
   - Rahatlatıcı

4. SU AKTİVİTELERİ:
   - **Yüzmek**: Duygularla başa çıkma
   - **Boğulmak**: Bunalma, kontrol kaybı
   - **Suya Dalmak**: Bilinçdışına iniş
   - **Su İçmek**: Bilgiyi almak
   - **Yağmurda Islanmak**: Arınma

5. SU VE RENKLERİ:
   - Mavi, yeşil, siyah su anlamları

6. DİN VE KÜLTÜR:
   - İslam'da suyun önemi
   - Tufan hikayeleri
   - Vaftiz sembolizmi

7. SU VE HAYAT EVRELERİ:
   - Doğum (amniotic sıvı)
   - Ölüm (sonsuzluk denizi)
   - Dönüşüm

8. ÖRNEK VAKasında:
   - Tekrar eden su rüyaları
   - Travma sonrası boğulma kabuları

9. PRATİK YORUM:
   - Su durumu → Duygusal durumunuz
   - Aktiviteniz → Duygularla ilişkiniz

STİL: Akıcı (su gibi!), şiirsel ama bilimsel. 2500+ kelime."""
    },
    {
        "title": "Paraliz ve Kabus: Sleep Paralysis (Uyku Felci) Gerçeği",
        "slug": "sleep-paralysis-uyku-felci",
        "description": "Sleep paralysis (uyku felci) nedir? Karabasan, cin basması efsaneleri. Bilimsel açıklama, neden olur, nasıl önlenir, İslami bakış.",
        "category": "Uyku Bozuklukları",
        "tags": ["sleep paralysis", "karabasan", "uyku felci", "paraliz"],
        "prompt": """Sleep paralysis (uyku felci) hakkında 2500+ kelimelik, korkuyu azaltan, bilimsel açıklamalı bir rehber yaz.

İÇERİK:
1. GİRİŞ: Karabasan korkusu, evrensel deneyim
2. SLEEP PARALYSIS NEDİR?:
   - Bilimsel tanım
   - REM uykusu ve atonia
   - %8 insanın deneyimlediği
3. NASIL OLUR? (Adım Adım):
   - REM uykusuna giriş/çıkış
   - Bilinç uyanır, kas felci devam eder
   - Halüsinasyonların nörobiyolojisi
4. TİPİK BELIRTILER:
   - Hareket edememe
   - Göğüs baskısı, nefes darlığı hissi
   - Halüsinasyonlar (görsel, işitsel, dokunsal)
   - Gölge varlıklar, cin, yaratık görme
   - Yoğun korku
5. KÜLTÜRLER ARASI İSİMLER:
   - Türkiye: Karabasan
   - Arap dünyası: Cin basması
   - İngiltere: Old Hag
   - Japonya: Kanashibari
   - İtalya: Pandafeche
6. TARİHİ VE KÜLTÜREL AÇIKLAMALAR:
   - Ortaçağ: Succubus/Incubus
   - Din: Cin, şeytan
   - Sanat: Henry Fuseli'nin "The Nightmare" tablosu
7. BİLİMSEL AÇIKLAMALAR:
   - REM intrusion
   - Hypnagogic vs hypnopompic halüsinasyonlar
   - Beyin taramaları ne gösteriyor?
8. TETİKLEYEN FAKTÖRLER:
   - Sırt üstü uyuma (%60 artış)
   - Uyku yoksunluğu
   - Düzensiz uyku
   - Stres ve kaygı
   - Narkolepsi
   - İlaçlar
9. İSLAMİ BAKIŞ AÇISI:
   - Gerçekten cin mi?
   - Alimlerin görüşleri
   - Ayetel Kürsi, dualar
   - Dindar alimlerin bilimsel yaklaşımı
10. NASIL ÖNLENİR?:
    - Uyku pozisyonu değiştirme
    - Düzenli uyku saatleri
    - Stres yönetimi
    - Kafein/alkol azaltma
11. YAŞANDIĞINDA NE YAPILMALI?:
    - Sakin kalın (biliyorum zor!)
    - Küçük hareketlerle başlayın (parmaklar)
    - Kontrollü nefes alın
    - Panik yapmayın, geçecek (1-2 dakika)
12. NE ZAMAN DOKTORA?:
    - Sık yaşanıyorsa (haftada 1+)
    - Uyku kalitesini bozuyorsa
    - Narkolepsi belirtileri varsa
13. KİŞİSEL HİKAYELER:
    - İlk kez yaşayanların deneyimleri
    - Nasıl başa çıktılar?

STİL: Rahatlatıcı, korkuyu azaltan, bilimsel. "Bu normaldir" mesajı ver. 2500+ kelime."""
    },
    {
        "title": "Rüya ve Gerçeklik: Rüya Mı Görüyorum Yoksa Gerçek Mi?",
        "slug": "ruya-ve-gerceklik",
        "description": "Reality testing nedir? Rüya vs gerçek ayrımı nasıl yapılır? Lucid dream için gerçeklik testleri. Felsefi perspektif: Zhuangzi'nin kelebeği.",
        "category": "Rüya Felsefesi",
        "tags": ["reality testing", "lucid dream", "felsefe", "gerçeklik"],
        "prompt": """Rüya ve gerçeklik ilişkisi hakkında 2500+ kelimelik, felsefi derinlikte ama anlaşılır bir makale yaz.

İÇERİK:
1. GİRİŞ: "Nasıl biliyorsunuz şu an rüya görmediğinizi?"
2. FELSEFİ SORULAR:
   - **Zhuangzi'nin Kelebeği**: Kelebek miyim, kelebek rüyası gören insan mı?
   - **Descartes'in Şüphesi**: "Cogito ergo sum"
   - **Matrix Sorusu**: Gerçeklik simülasyonu mu?
3. RÜYA VS GERÇEK FARKLARI:
   - **Fiziksel İstikrar**: Gerçek tutarlı, rüya değişken
   - **Mantık**: Gerçekte mantık işler, rüyada absürd kabul edilir
   - **Hafıza**: Gerçekte geçmişinizi hatırlarsınız
   - **Metin/Sayılar**: Rüyada okumak zor
4. REALITY TESTING (Gerçeklik Testleri):
   - Lucid dreaming için kullanılan teknikler

   **5 Klasik Test:**
   1. **Parmak Sayma**: Parmaklarınızı sayın (rüyada fazla/eksik çıkar)
   2. **Metin Okuma**: Bir şey okuyun, başka tarafa bakın, tekrar okuyun (değişir)
   3. **Ayna**: Aynaya bakın (rüyada garip görünürsünüz)
   4. **Burun Tutma**: Burnunuzu tutup nefes almaya çalışın (rüyada yine alırsınız!)
   5. **Saat**: Saate bakın, başka tarafa bakın, tekrar bakın (değişir)

5. BİLİMSEL ARAŞTIRMALAR:
   - Lucid dreamers'ların beyin taramaları
   - Gerçek vs rüya beyin aktivitesi farkları
6. KÜLTÜRLERve Gerçeklik:
   - Aborijinler: "Dreamtime" - Rüya gerçektir
   - Tibetliler: "Dream yoga" - Rüyada uyanış
   - Sufiler: Dünya bir rüyadır
7. FALSE AWAKENINGS (Sahte Uyanışlar):
   - Uyanmış sanıyorsunuz ama hala rüyadasınız
   - Christopher Nolan'ın "Inception" filmi
   - Nasıl fark edilir?
8. PSİKOLOJİK BOZUKLUKLARDA GERÇEKLIK:
   - Derealizasyon: "Bu gerçek gibi değil"
   - Depersonalizasyon: "Ben ben değilim"
   - Şizofreni: Halüsinasyonlar vs gerçek
9. PRATİK EGZERSİZLER:
   - Günde 10 kez reality check yapın
   - Farkındalık meditasyonu
10. FELSEFİ SORU: Önemli mi?
    - Belki gerçek olmasa da deneyim gerçek
    - Cogito: "Düşünüyorum, öyleyse varım"

STİL: Düşündürücü, felsefi ama erişilebilir. Okuyucuyu şaşırt. 2500+ kelime."""
    },
    {
        "title": "Rüya ve Kreativite: Sanatçılar Rüyalardan Nasıl İlham Alır?",
        "slug": "ruya-ve-kreativite",
        "description": "Ünlü sanatçıların rüya hikayeleri. Mendeleev, Paul McCartney, Salvador Dali. Rüyalardan yaratıcılık çıkarma teknikleri.",
        "category": "Rüya ve Yaratıcılık",
        "tags": ["yaratıcılık", "sanat", "ünlüler", "icatlar"],
        "prompt": """Rüya ve yaratıcılık ilişkisi hakkında 2500+ kelimelik, ilham verici, hikayelerle dolu bir makale yaz.

İÇERİK:
1. GİRİŞ: "Rüyalar, yaratıcılığın anayoludur"
2. BİLİM: Neden Rüyalar Yaratıcıdır?
   - REM uykusunda prefrontal korteks azalır → mantık engeli kalkar
   - Rastgele bağlantılar, lateral düşünme
   - Araştırmalar: REM uykusundan sonra %30 daha yaratıcı çözümler
3. ÜNLÜ RÜYA HİKAYELERİ (Detaylı anlatımlar):

   **BİLİM:**
   - **Mendeleev**: Periyodik tabloyu rüyasında gördü
   - **Elias Howe**: Dikiş makinesinin iğne tasarımı
   - **August Kekulé**: Benzen halkası (yılan rüyası)
   - **Otto Loewi**: Sinir iletimi deneyi (Nobel Ödülü)

   **MÜZİK:**
   - **Paul McCartney**: "Yesterday" şarkısı tam olarak rüyasında geldi
   - **Keith Richards**: "(I Can't Get No) Satisfaction" riffı
   - **Giuseppe Tartini**: "Devil's Trill Sonata"
   - **Billy Joel**: Birçok melodiyi rüyalarında duydu

   **EDEBIYAT:**
   - **Mary Shelley**: Frankenstein hikayesi
   - **Robert Louis Stevenson**: Dr. Jekyll and Mr. Hyde
   - **Stephen King**: Birçok korku hikayesi
   - **S.T. Coleridge**: "Kubla Khan" şiiri (uyuşturuculu rüya)

   **SANAT:**
   - **Salvador Dali**: "Rüya-gerçek" tekniği
   - **William Blake**: Vizyoner rüya sanatı

   **FİLM:**
   - **James Cameron**: Terminator'ın görsel tasarımı
   - **Christopher Nolan**: Inception fikri

4. DALİ'NİN TEKNİĞİ: "Slumber with a Key"
   - Elinde anahtar tutarak uyumak
   - Uykuya dalınca anahtar düşer, uyanırsınız
   - Hypnagogic (uykuya dalma) halinde yaratıcı görüntüler
5. THOMAS EDISON'UN YÖNTEMİ:
   - Elinde metal bilye
   - Uykuya dalınca düşer, uyanır
   - Çözümü not eder
6. RÜYALARDAN YARATICILIK ÇIKARMA:
   - **Rüya Günlüğü**: Her sabah yazın
   - **Hipnagogic State**: Uykuya dalma anını yakalayin
   - **Lucid Dreaming**: Rüyada kontrol
   - **Rüya İnkübasyonu**: Sorunuzu sorun, uyuyun
7. RÜYA İNKÜBASYONU TEKNİĞİ:
   - Akşam sorununuzu yazın
   - "Bu soruna çözüm rüyamda gelecek" deyin
   - Sabah hemen not alın
   - %30+ başarı oranı (araştırmalarla)
8. PRAKTİK EGZERSİZLER:
   - 7 günlük yaratıcılık challenge'ı
   - Rüya tema seçme
9. SANATÇILAR İÇİN ÖNERİLER:
   - Yatak yanında defter/ses kaydedici
   - Hipnagogic alarm (20 dakika sonra alarm)
   - Rüya sembolleri sketchbook
10. UYARI: Rüya vs Gerçeklik
    - Rüyalar ilham verir ama işlemek gerekir
    - Uygulamaya dökmek önemli

STİL: İlham verici, hikaye odaklı, motivasyonel. 2500+ kelime."""
    }
]

def generate_blog_post(topic_config):
    """Generate a single blog post using Groq API"""
    try:
        print(f"\n{'='*60}")
        print(f"Generating: {topic_config['title']}")
        print(f"{'='*60}")

        # Call Groq API
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": """Sen profesyonel bir blog yazarısın. Türkçe yazıyorsun.
Görevin: Rüya tabirleri, psikoloji ve İslami rüya yorumu konularında son derece kaliteli,
insan yazmış gibi, samimi ve detaylı blog yazıları yazmak.

KRİTİK KURALLAR:
1. ASLA front matter (YAML başlığı) yazma, sadece markdown içerik
2. Çeşitli cümle yapıları kullan
3. Kişisel örnekler ver
4. Okuyucuya doğrudan hitap et
5. Samimi bir ton kullan
6. Başlıklar: # ## ### formatında
7. Listeler, kalın vurgular, alıntılar kullan
8. Emoji kullanma
9. Her paragraf 3-5 cümle olsun
10. Minimum 2500 kelime yaz"""
                },
                {
                    "role": "user",
                    "content": topic_config['prompt']
                }
            ],
            model="llama-3.3-70b-versatile",  # High-quality model
            temperature=0.8,  # Creative but not too random
            max_completion_tokens=8000,  # Long content
            top_p=0.95
        )

        # Extract content
        content = chat_completion.choices[0].message.content

        # Add front matter
        date_obj = datetime.now() - timedelta(days=len(BLOG_TOPICS) - BLOG_TOPICS.index(topic_config))
        front_matter = f"""---
title: "{topic_config['title']}"
description: "{topic_config['description']}"
slug: "{topic_config['slug']}"
date: {date_obj.strftime('%Y-%m-%d')}
lastmod: {datetime.now().strftime('%Y-%m-%d')}
categories: ["{topic_config['category']}"]
tags: {json.dumps(topic_config['tags'], ensure_ascii=False)}
---

"""

        full_content = front_matter + content

        # Save to file
        blog_dir = "../hugo-site/content/blog"
        os.makedirs(blog_dir, exist_ok=True)

        filename = f"{blog_dir}/{topic_config['slug']}.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(full_content)

        print(f"[OK] Generated successfully: {filename}")
        print(f"   Word count: ~{len(content.split())} words")

        return True

    except Exception as e:
        print(f"[ERROR] Error generating {topic_config['title']}: {str(e)}")
        return False

def main():
    """Main function to generate all blog posts"""
    print("\n" + "="*60)
    print("GROQ API BLOG POST GENERATOR")
    print("="*60)
    print(f"Total topics to generate: {len(BLOG_TOPICS)}")
    print(f"Using model: llama-3.3-70b-versatile")
    print("="*60)

    successful = 0
    failed = 0

    for i, topic in enumerate(BLOG_TOPICS, 1):
        print(f"\n[{i}/{len(BLOG_TOPICS)}]", end=" ")

        if generate_blog_post(topic):
            successful += 1
        else:
            failed += 1

        # Rate limiting - wait between requests
        if i < len(BLOG_TOPICS):
            print("[WAIT] Waiting 3 seconds before next generation...")
            time.sleep(3)

    # Summary
    print("\n" + "="*60)
    print("GENERATION COMPLETE")
    print("="*60)
    print(f"[OK] Successful: {successful}/{len(BLOG_TOPICS)}")
    print(f"[ERROR] Failed: {failed}/{len(BLOG_TOPICS)}")
    print("="*60)

if __name__ == "__main__":
    main()
