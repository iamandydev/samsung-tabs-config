@echo off
title SG_Tab_A9 - Limpieza y Configuración Inicial
echo ==========================================
echo   Script para limpiar apps y copiar OnlyOffice
echo ==========================================
echo.

REM 1. Verificar conexión con el dispositivo
adb devices
echo.
pause

REM Lista de paquetes a eliminar si existen
set packages=com.netflix.mediaclient com.spotify.music com.google.android.apps.youtube.music com.samsung.sree com.samsung.android.app.spage com.samsung.android.game.gamehome com.disney.disneyplus com.microsoft.office.outlook com.microsoft.skydrive com.microsoft.office.officehubrow

echo --- Desinstalando aplicaciones innecesarias ---
for %%p in (%packages%) do (
    echo Verificando %%p ...
    adb shell pm list packages | findstr "%%p" >nul
    if %errorlevel%==0 (
        echo Desinstalando %%p ...
        adb shell pm uninstall --user 0 %%p
    ) else (
        echo %%p no está instalado, se omite.
    )
)
echo.
echo --- Proceso de desinstalación finalizado ---
echo.

REM 2. Copiar archivo onlyoffice.apk al almacenamiento interno
echo --- Copiando OnlyOffice.apk ---
adb push "C:\Users\MSI\Desktop\onlyoffice.apk" "/sdcard/Download/onlyoffice.apk"
echo Copia completada.
echo.

REM 3. Verificar que el archivo se haya copiado correctamente
echo --- Verificando archivo ---
adb shell ls -l "/sdcard/Download/onlyoffice.apk"
echo.

echo Script finalizado.
pause
