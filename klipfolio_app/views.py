import os
import logging
import requests
import zipfile
from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import img2pdf

# Configurar logging
logger = logging.getLogger(__name__)

# Rutas de Chromium y ChromeDriver en Render
CHROMIUM_BINARY = "/opt/google/chrome/chrome"
CHROMEDRIVER_BINARY = "/usr/local/bin/chromedriver"  

# Función para descargar y configurar Chromium en Render o WHM
def setup_chromium():
    """Verifica que Chromium y ChromeDriver están instalados"""
    if not os.path.exists(CHROMIUM_BINARY):
        raise FileNotFoundError("Chromium no encontrado en el servidor.")
    if not os.path.exists(CHROMEDRIVER_BINARY):
        raise FileNotFoundError("ChromeDriver no encontrado en el servidor.")

# Vista principal
def index(request):
    return render(request, 'klipfolio_app/index.html')

@csrf_exempt
def generar_pdf(request):
    def capture_dashboards():
        try:
            # Asegurar que Chromium está instalado
            setup_chromium()

            # Configuración de Selenium
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--window-size=1920,1080")

            # Usar las rutas de Chromium y ChromeDriver personalizadas
            chrome_options.binary_location = CHROMIUM_BINARY
            service = ChromeService(executable_path=CHROMEDRIVER_BINARY)

            driver = webdriver.Chrome(service=service, options=chrome_options)

            # URLs de los dashboards
            urls = [
                "https://app.klipfolio.com/published/61daedb930b345b49d75f5f6e1fe7ac6/principal-data",
                "https://app.klipfolio.com/published/429a3c2e6f292b4c504d6a7527b3189f/geo",
                "https://app.klipfolio.com/published/d7a139b1e038b1be8befb9233f04a504/tech",
                "https://app.klipfolio.com/published/104859d210f21508786a8cb4bf8b41c3/views",
                "https://app.klipfolio.com/published/083b5e4529574c3bcf3d0faabaffc8d0/analtica"
            ]

            screenshots = []
            for i, url in enumerate(urls):
                logger.info(f"Capturando {url}...")
                driver.get(url)

                try:
                    WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.TAG_NAME, "body"))  # Ajusta el selector si es necesario
                    )
                    logger.info("Dashboard cargado completamente.")
                except Exception as e:
                    logger.error(f"Error al esperar la carga del dashboard: {e}")

                # Obtener el tamaño completo del documento para capturar toda la página
                total_height = driver.execute_script("return document.body.scrollHeight")
                driver.set_window_size(1920, total_height + 100)

                # Guardar captura de pantalla
                screenshot_path = f"screenshot_{i}.png"
                driver.save_screenshot(screenshot_path)
                screenshots.append(screenshot_path)
                logger.info(f"Captura guardada como {screenshot_path}")

            driver.quit()
            logger.info("Capturas de pantalla completadas.")

            # Generar el PDF combinando las capturas
            output_pdf = "dashboards_unificados.pdf"
            logger.info(f"Combinando capturas en {output_pdf}...")
            with open(output_pdf, "wb") as f:
                f.write(img2pdf.convert([open(img, "rb") for img in screenshots]))

            # Eliminar imágenes temporales
            for img in screenshots:
                os.remove(img)

            logger.info(f"PDF generado exitosamente: {output_pdf}")
            return output_pdf

        except Exception as e:
            logger.error(f"Error en capture_dashboards: {e}")
            raise

    try:
        pdf_path = capture_dashboards()
        return FileResponse(open(pdf_path, 'rb'), as_attachment=True, filename='dashboards_unificados.pdf')
    except Exception as e:
        logger.error(f"Error en generar_pdf: {e}")
        return HttpResponse(f"Error: {str(e)}", status=500)
