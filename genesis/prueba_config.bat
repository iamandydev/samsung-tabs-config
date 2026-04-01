@echo off
echo ==========================================
echo  Script de configuracion - Tab A9 / General
echo ==========================================

REM ====== Verificar si OnlyOffice esta instalado ======
echo Verificando si OnlyOffice ya esta instalado...
adb shell pm list packages | findstr "com.onlyoffice" >nul
if %errorlevel%==0 (
    echo OnlyOffice ya esta instalado, no se instalara de nuevo.
) else (
    echo OnlyOffice no esta instalado. Procediendo a copiar e instalar...
    adb push "C:\Users\MSI\Desktop\onlyoffice.apk" /sdcard/Download/onlyoffice.apk
    adb install -r /sdcard/Download/onlyoffice.apk
    echo Instalacion de OnlyOffice completada.

    echo Concediendo permisos a OnlyOffice...
    adb shell pm grant com.onlyoffice.permission.STORAGE android.permission.READ_EXTERNAL_STORAGE
    adb shell pm grant com.onlyoffice.permission.STORAGE android.permission.WRITE_EXTERNAL_STORAGE
    adb shell pm grant com.onlyoffice android.permission.READ_MEDIA_IMAGES
    adb shell pm grant com.onlyoffice android.permission.READ_MEDIA_VIDEO
    adb shell pm grant com.onlyoffice android.permission.READ_MEDIA_AUDIO
    adb shell appops set com.onlyoffice MANAGE_EXTERNAL_STORAGE allow

    echo Abriendo OnlyOffice...
    adb shell monkey -p com.onlyoffice 1
)

REM ====== Desinstalar apps innecesarias si existen ======
set apps=\
com.netflix.mediaclient \
com.google.android.apps.youtube.music \
com.samsung.sree \
com.samsung.android.free \
com.samsung.android.game.gamehome \
com.disney.disneyplus \
com.microsoft.office.outlook \
com.microsoft.skydrive \
com.microsoft.office.officehubrow

for %%a in (%apps%) do (
    echo Verificando %%a ...
    adb shell pm list packages | findstr "%%a" >nul
    if %errorlevel%==0 (
        echo Desinstalando %%a ...
        adb shell pm uninstall --user 0 %%a
    ) else (
        echo %%a no esta instalado, se omite.
    )
)

REM ====== Desactivar Samsung Daily Board si existe ======
echo Verificando Samsung Daily Board...
adb shell pm list packages | findstr "com.samsung.android.dailyboard" >nul
if %errorlevel%==0 (
    echo Desactivando Samsung Daily Board...
    adb shell pm disable-user --user 0 com.samsung.android.dailyboard
) else (
    echo Samsung Daily Board no esta presente.
)

REM ====== Desactivar Android Setup si existe ======
echo Verificando Android Setup...
adb shell pm list packages | findstr "com.google.android.setupwizard" >nul
if %errorlevel%==0 (
    echo Desactivando Android Setup...
    adb shell pm disable-user --user 0 com.google.android.setupwizard
) else (
    echo Android Setup no esta presente.
)

echo ==========================================
echo  Proceso terminado.
echo ==========================================
pause
