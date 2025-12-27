@echo off
cd /d "c:\Users\Dante\Desktop\Yeniden\WebSite\ruya-sitesi"
python scripts/instant_indexing.py >> scripts/indexing_log.txt 2>&1
echo [%date% %time%] Indexing tamamlandi >> scripts/indexing_log.txt
