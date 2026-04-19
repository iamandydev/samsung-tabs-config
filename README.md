# Script de Configuración Automática para Tablets Samsung
Este script automatiza la configuración inicial de **tablets Samsung Galaxy Tab S4** mediante **ADB (Android Debug Bridge)**.  
Su propósito es desinstalar aplicaciones innecesarias, deshabilitar configuraciones, instalar y configurar **OnlyOffice**, y reasignar nombres de dispositivo de manera automática, dejando un registro detallado en un archivo de log.

---

## ⚙️ Funcionalidades

1. **Verificación de conexión ADB**  
   - Detecta si la tablet está correctamente conectada y reconocida por `adb`.

2. **Desinstalación de apps no deseadas**  
   - Elimina aplicaciones preinstaladas como Netflix, Spotify, Disney+, Outlook, OneDrive, Gaming Hub, entre otras.

3. **Desactivación de configuraciones**  
   - Deshabilita servicios y apps como el *Setup Wizard* y *Samsung Daily*.

4. **Desactivación de Google Discover**  
   - Inhabilita el feed de noticias de Google en la pantalla principal.

5. **Instalación y configuración de OnlyOffice**  
   - Revisa si está instalado.  
   - En caso contrario, instala el APK localizado en la misma carpeta (`onlyoffice.apk`).  
   - Concede permisos de almacenamiento.  
   - Abre la app automáticamente.

6. **Reasignación de nombre de dispositivo**  
   - Lee un archivo `s4_config.json` con nombres predefinidos.  
   - Asigna el primero disponible y lo marca como usado.  
   - Ejemplo de `s4_config.json`:
     ```json
     {
         "S4-01": false,
         "S4-02": false,
         "S4-03": true
     }
     ```

7. **Registro detallado (logging)**  
   - Todas las acciones quedan registradas en `tab_config_log.txt` con fecha y hora.  
   - Incluye tiempo total de ejecución.  
   - Ejemplo:
     ```
     16/08/2025 19:01:43 - ADB conectado correctamente - R58M12XYZ
     16/08/2025 19:01:47 - [UNINSTALL] com.netflix.mediaclient eliminada
     16/08/2025 19:02:10 - R58M12XYZ → S4-06 completado en 45.87s
     ```

---

## 📂 Archivos del proyecto

- `main.py` → Script principal.  
- `s4_config.json` → Lista de nombres disponibles para asignar.  
- `onlyoffice.apk` → Instalador de OnlyOffice (debe estar en la misma carpeta).  
- `tab_config_log.txt` → Log generado automáticamente.  

---

## ▶️ Requisitos

- **Python 3.7+**  
- **ADB** instalado y agregado al `PATH`.  
- Tablet Samsung Tab S4 conectada por USB y con **depuración USB** activada.

---

## 🚀 Uso

1. Conecta la tablet por USB y habilita la depuración.  
2. Coloca `onlyoffice.apk` en la misma carpeta que `main.py`.  
3. Prepara `s4_config.json` con los nombres disponibles.  
4. Ejecuta:

   ```bash
   python main.py
