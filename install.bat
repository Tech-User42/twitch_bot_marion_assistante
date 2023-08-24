@echo off
echo Installation des dépendances python...
pip3 install -U --no-cache-dir --force-reinstall -r requirements.txt
cls
color a
echo Installation terminée !
timeout 10
exit