# Asistencia automática ITSON

Script que registra tu asistencia en **ivirtual.itson.edu.mx** (Moodle) de forma automática.

Inicia sesión, abre la lista de asistencia de tu curso, marca **Presente**, guarda y verifica
el mensaje *"Su asistencia en esta sesión ha sido registrada."*. Cada registro deja una
captura con fecha y hora en la carpeta `evidencias/`.

Con el Programador de tareas de Windows se ejecuta solo a la hora de tu clase. Si el profe
todavía no abre la asistencia, reintenta cada 2 minutos durante ~50 minutos.

## Requisitos

- Windows 10/11
- [Python 3.10 o más reciente](https://www.python.org/downloads/) (o desde la Microsoft Store)

## Instalación

1. Descarga el proyecto (botón **Code → Download ZIP**, o `git clone`) y descomprímelo.
2. Abre una terminal **dentro de la carpeta** e instala lo necesario:

   ```bash
   pip install -r requirements.txt
   python -m playwright install chromium
   ```

3. Copia `.env.example`, renómbralo a `.env` y llena tus datos:

   ```
   ITSON_USER=tu_id_de_alumno
   ITSON_PASS=tu_contraseña
   ATTENDANCE_ID=1662559
   ```

   `ATTENDANCE_ID` es el número al final de la URL de la "Lista de Asistencia" de tu curso
   (`.../mod/attendance/view.php?id=`**`1662559`**). El que viene es el de Ingeniería de
   Requisitos; si tu curso es otro, cámbialo.

## Uso manual

```bash
python asistencia.py
```

Se abre el navegador y verás cómo registra la asistencia. Útil para probar que todo funciona.

## Ejecución automática

1. Abre `programar_tarea.ps1` con el Bloc de notas y cambia los días y la hora de tu clase:

   ```powershell
   $Dias = "Monday", "Wednesday", "Friday"
   $Hora = "10:00"
   ```

2. En una terminal dentro de la carpeta ejecuta:

   ```bash
   powershell -ExecutionPolicy Bypass -File programar_tarea.ps1
   ```

Se crea la tarea **"Asistencia ITSON"** en el Programador de tareas. Ahí la puedes
**Ejecutar** para probarla, **Deshabilitar** en vacaciones o **Eliminar**.

Para que funcione, la PC debe estar **encendida y con tu sesión de Windows iniciada**
(puede estar bloqueada o suspendida). Si estaba apagada, la tarea corre al encenderla.

## Resultados

| Archivo | Qué contiene |
|---|---|
| `log.txt` | Lo que hizo el script en cada ejecución automática |
| `evidencias/*_asistencia_registrada.png` | Captura de la confirmación, con fecha y hora |
| `evidencias/*_sin_enlace.png` | No se abrió la asistencia a tiempo: regístrala a mano |
| `evidencias/*_error.png` / `*_login_fallido.png` | Algo falló; revisa `log.txt` o tu contraseña |

## Problemas comunes

- **`playwright` no se reconoce**: usa `python -m playwright install chromium`.
- **`No such file or directory`**: la terminal no está en la carpeta del proyecto; entra con `cd "ruta\de\la\carpeta"`.
- **`Falta ITSON_USER o ITSON_PASS`**: no existe el `.env` o le falta algún dato.

## Seguridad

Tu contraseña solo vive en tu `.env`, en tu computadora. Ese archivo está en `.gitignore`:
**nunca lo subas ni lo compartas**.

## Aviso

Proyecto personal sin relación oficial con ITSON. Úsalo bajo tu responsabilidad y solo para
registrar tu propia asistencia cuando estés en clase.
