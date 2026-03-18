import subprocess
import json
import os
import time
from datetime import datetime

# === ARCHIVOS DE CONFIG Y LOG ===
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "s_config.json")
LOG_FILE = os.path.join(os.path.dirname(__file__), "tab_config_log.txt")

# === FUNCIONES DE APOYO ===
def ejecutar_adb(comando):
    """Ejecuta un comando ADB y devuelve la salida"""
    try:
        resultado = subprocess.run(["adb"] + comando.split(), capture_output=True, text=True)
        return resultado.stdout.strip(), resultado.stderr.strip()
    except Exception as e:
        return "", str(e)

def loggear(mensaje):
    """Escribe en archivo de logs con fecha"""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - {mensaje}\n")

# === 1. VERIFICAR CONEXIÓN ADB ===
def verificar_conexion():
    out, err = ejecutar_adb("devices")
    if "device" in out.splitlines()[-1]:
        device_id = out.splitlines()[-1].split()[0]
        loggear(f"ADB conectado correctamente - {device_id}")
        return device_id
    else:
        loggear("Error: No hay dispositivos conectados")
        return None

# === 2. DESINSTALAR APPS NO DESEADAS ===
APPS_DESINSTALAR = [
    "com.netflix.mediaclient",
    "com.spotify.music",
    "com.google.android.apps.youtube.music",
    "com.samsung.sree",  # Samsung Free
    "com.samsung.android.samsungpassautofill", # Samsung Global Goals placeholder
    "com.samsung.android.game.gamehome", # Gaming Hub
    "com.disney.disneyplus",
    "com.microsoft.office.outlook",
    "com.microsoft.skydrive", # OneDrive
    "com.microsoft.office.officehubrow" # Microsoft 365
]

def desinstalar_apps():
    for app in APPS_DESINSTALAR:
        out, err = ejecutar_adb(f"shell pm uninstall --user 0 {app}")
        if "Success" in out:
            loggear(f"[UNINSTALL] {app} eliminada")
        else:
            loggear(f"[UNINSTALL] {app} no encontrada o error")

# === 3. DESACTIVAR CONFIGURACIONES ===
def desactivar_apps():
    # Android Setup
    ejecutar_adb("shell pm disable-user --user 0 com.google.android.setupwizard")
    loggear("[DISABLE] Android Setup deshabilitada")

    # Samsung Daily
    ejecutar_adb("shell pm disable-user --user 0 com.samsung.android.app.spage")
    loggear("[DISABLE] Samsung Daily deshabilitado")

# === 4. DESACTIVAR GOOGLE DISCOVER ===
def desactivar_discover():
    ejecutar_adb("shell cmd overlay disable com.google.android.googlequicksearchbox")
    loggear("[DISABLE] Google Discover deshabilitado")

# === 5. INSTALAR Y CONFIGURAR ONLYOFFICE ===
def instalar_onlyoffice():
    paquete = "com.onlyoffice.documents"
    out, _ = ejecutar_adb(f"shell pm list packages {paquete}")
    if paquete not in out:
        # instalar (suponiendo que el APK está en la carpeta del script como onlyoffice.apk)
        apk_path = os.path.join(os.path.dirname(__file__), "apk/onlyoffice.apk")
        if os.path.exists(apk_path):
            out, err = ejecutar_adb(f"install {apk_path}")
            if "Success" in out:
                loggear("[INSTALL] OnlyOffice instalado correctamente")
            else:
                loggear("[INSTALL] Error instalando OnlyOffice")
        else:
            loggear("[INSTALL] No se encontró el APK de OnlyOffice")
    else:
        loggear("[INSTALL] OnlyOffice ya estaba instalado")

    # Permisos básicos
    ejecutar_adb(f"shell pm grant {paquete} android.permission.READ_EXTERNAL_STORAGE")
    ejecutar_adb(f"shell pm grant {paquete} android.permission.WRITE_EXTERNAL_STORAGE")

    # Abrir la app
    ejecutar_adb(f"shell monkey -p {paquete} -c android.intent.category.LAUNCHER 1")
    loggear("[OPEN] OnlyOffice abierto")

# === 6. REASIGNAR NOMBRE DE DISPOSITIVO ===
def reasignar_nombre():
    if not os.path.exists(CONFIG_FILE):
        loggear("Error: No se encontró s4_config.json")
        return None

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    for clave, valor in data.items():
        if not valor:
            # Cambiar nombre de dispositivo
            ejecutar_adb(f"shell settings put global device_name {clave}")
            loggear(f"successful - {clave}")
            data[clave] = True
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            return clave
    loggear("No quedan nombres disponibles en s4_config.json")
    return None

# === PROGRAMA PRINCIPAL ===
def main():
    start_time = time.time()

    device_id = verificar_conexion()
    if not device_id:
        return

    desinstalar_apps()
    desactivar_apps()
    desactivar_discover()
    instalar_onlyoffice()
    nombre_asignado = reasignar_nombre()

    end_time = time.time()
    duration = end_time - start_time

    if nombre_asignado:
        loggear(f"{device_id} → {nombre_asignado} completado en {duration:.2f}s")
    else:
        loggear(f"{device_id} completado en {duration:.2f}s (sin reasignar nombre)")

if __name__ == "__main__":
    main()
