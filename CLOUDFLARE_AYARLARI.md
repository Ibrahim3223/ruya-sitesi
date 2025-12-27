# Cloudflare Pages Ayarlari

Bu dokumantasyon, ruyatabirisozlugu.com icin onerilen Cloudflare ayarlarini icerir.

## Build Ayarlari (Cloudflare Pages)

```
Build command: hugo --minify --gc
Build output directory: public
Root directory: hugo-site
Environment variable: HUGO_VERSION = 0.140.0
```

## Speed > Optimization (MANUEL AYARLANMALI)

Cloudflare Dashboard > Speed > Optimization sayfasindan:

### Auto Minify
- [x] JavaScript - ACIK
- [x] CSS - ACIK
- [x] HTML - ACIK

### Speed Brain
- [x] ACIK (varsa)

### Rocket Loader
- [x] ACIK (JavaScript performansi icin)

### Polish (Pro plan gerekli)
- Lossy - Gorselleri optimize eder

### Mirage (Pro plan gerekli)
- ACIK - Mobil gorsel optimizasyonu

### Brotli
- [x] ACIK (varsayilan olarak acik olmali)

## Caching > Configuration

### Browser Cache TTL
- 1 year (statik icerik icin ideal)

### Cache Level
- Standard

### Always Online
- [x] ACIK

## SSL/TLS

### SSL/TLS Encryption Mode
- Full (strict)

### Always Use HTTPS
- [x] ACIK

### Automatic HTTPS Rewrites
- [x] ACIK

### Minimum TLS Version
- TLS 1.2

## Security

### Security Level
- Medium

### Bot Fight Mode
- [x] ACIK

## Rules > Page Rules (Opsiyonel)

### Cache Everything Rule
```
URL: ruyatabirisozlugu.com/*
Setting: Cache Level = Cache Everything
Edge Cache TTL: 1 month
```

## Network

### HTTP/2
- [x] ACIK (varsayilan)

### HTTP/3 (QUIC)
- [x] ACIK

### 0-RTT Connection Resumption
- [x] ACIK

### WebSockets
- [x] ACIK

## Scrape Shield

### Email Address Obfuscation
- [x] ACIK

### Server-side Excludes
- [x] ACIK

---

## Kontrol Listesi

Asagidaki ayarlari Cloudflare Dashboard'dan kontrol edin:

1. [ ] Speed > Auto Minify (JS, CSS, HTML)
2. [ ] Speed > Brotli
3. [ ] Speed > Rocket Loader
4. [ ] Caching > Browser Cache TTL (1 year)
5. [ ] SSL/TLS > Always Use HTTPS
6. [ ] SSL/TLS > Automatic HTTPS Rewrites
7. [ ] Security > Bot Fight Mode
8. [ ] Network > HTTP/3

## Performans Testi

Ayarlardan sonra asagidaki araclari kullanarak test edin:

- PageSpeed Insights: https://pagespeed.web.dev/?url=https://ruyatabirisozlugu.com
- GTmetrix: https://gtmetrix.com
- WebPageTest: https://webpagetest.org

### Hedef Skorlar
- Mobile: 85+
- Desktop: 90+
- LCP: < 2.5s
- FID: < 100ms
- CLS: < 0.1
