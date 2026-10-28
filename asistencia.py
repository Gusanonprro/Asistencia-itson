"""
Registro automático de asistencia en ivirtual.itson.edu.mx (Moodle, módulo "attendance").

Inicia sesión, abre la lista de asistencia del curso, marca "Presente",
guarda y verifica la confirmación. Guarda capturas con fecha y hora en evidencias/.

Uso:
  pip install -r requirements.txt
  python -m playwright install chromium
  python asistencia.py
"""
import os
import sys
import time
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# .env y evidencias/ siempre en la carpeta del script, se ejecute desde donde se ejecute
CARPETA = Path(__file__).resolve().parent
load_dotenv(CARPETA / ".env")

BASE = "https://ivirtual.itson.edu.mx"
ATTENDANCE_ID = os.getenv("ATTENDANCE_ID", "1662559")  # Ingeniería de Requisitos
USER = os.getenv("ITSON_USER")
PASS = os.getenv("ITSON_PASS")
if not USER or not PASS:
    sys.exit(f"Falta ITSON_USER o ITSON_PASS en {CARPETA / '.env'}")
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
INTENTOS = int(os.getenv("INTENTOS", "5"))        # reintentos si aún no aparece el enlace
ESPERA_SEG = int(os.getenv("ESPERA_SEG", "120"))  # segundos entre reintentos
TIMEOUT_MS = 30000

EVIDENCIAS = CARPETA / "evidencias"
EVIDENCIAS.mkdir(exist_ok=True)


def log(msg: str) -> None:
    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {msg}", flush=True)


def evidencia(page, nombre: str) -> None:
    ahora = datetime.now()
    ruta = EVIDENCIAS / f"{ahora:%Y%m%d_%H%M%S}_{nombre}.png"
    try:
        # Franja con fecha y hora arriba de la página, para que quede en la captura
        page.evaluate(
            """texto => {
                const d = document.createElement('div');
                d.textContent = texto;
                d.style.cssText = 'background:#1a7f37;color:#fff;font:bold 20px Arial,sans-serif;'
                    + 'padding:12px 16px;text-align:center;';
                document.body.prepend(d);
            }""",
            f"Captura: {ahora:%d/%m/%Y %H:%M:%S} — {nombre.replace('_', ' ')}",
        )
        page.screenshot(path=str(ruta), full_page=True)
        log(f"Captura guardada: {ruta}")
    except Exception as e:
        log(f"No se pudo guardar la captura: {e}")


def login(page) -> None:
    log("Iniciando sesión...")
    page.goto(f"{BASE}/login/index.php")
    page.fill("#username", USER)
    page.fill("#password", PASS)
    with page.expect_navigation():
        page.click("#loginbtn")
    if "login/index.php" in page.url:
        evidencia(page, "login_fallido")
        raise RuntimeError("No se pudo iniciar sesión. Revisa usuario y contraseña en .env")
    log("Sesión iniciada.")


def capturar_asistencia(page) -> bool:
    page.goto(f"{BASE}/mod/attendance/view.php?id={ATTENDANCE_ID}")

    # "Enviar asistencia" solo aparece con la sesión abierta y si aún no has registrado
    enlace = page.locator("a[href*='attendance.php?sessid']")
    if enlace.count() == 0:
        return False

    log("Enlace 'Enviar asistencia' encontrado. Registrando...")
    enlace.first.click()
    page.wait_for_selector("#id_submitbutton", timeout=TIMEOUT_MS)

    # El id del radio cambia en cada sesión, así que se busca por el texto de su label
    page.locator("label:has-text('Presente') input[name='status']").first.check()
    with page.expect_navigation():
        page.click("#id_submitbutton")

    confirmacion = page.locator("#user-notifications .alert", has_text="ha sido registrada")
    try:
        confirmacion.first.wait_for(timeout=TIMEOUT_MS)
    except Exception:
        evidencia(page, "sin_confirmacion")
        raise RuntimeError("Se envió el formulario pero no apareció el mensaje de confirmación")

    evidencia(page, "asistencia_registrada")
    return True


def main() -> int:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        page = browser.new_page()
        try:
            login(page)
            for intento in range(1, INTENTOS + 1):
                if capturar_asistencia(page):
                    log("Asistencia registrada correctamente.")
                    return 0
                log(f"Aún no aparece el enlace (intento {intento}/{INTENTOS}).")
                if intento < INTENTOS:
                    time.sleep(ESPERA_SEG)
            evidencia(page, "sin_enlace")
            log("No apareció el enlace de asistencia. Regístrala manualmente.")
            return 1
        except Exception as e:
            log(f"Error: {e}")
            evidencia(page, "error")
            return 2
        finally:
            browser.close()


if __name__ == "__main__":
    sys.exit(main())
